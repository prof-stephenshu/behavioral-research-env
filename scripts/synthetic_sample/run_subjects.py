"""
Stage 4 synthetic subject runner.

Takes the subject frame produced by sample_population.py and, for each
subject, calls the Anthropic API in-persona against that subject's assigned
condition stimulus, forcing a structured tool-call response so the decision
(and any secondary DVs) can be parsed reliably. Writes the combined
IV+DV dataset subjects_data.csv.

Usage:
    python run_subjects.py --frame subjects_frame.csv --population-config population_config.json \
        --test-config test_config.json --out subjects_data.csv [--concurrency 20]

Requires ANTHROPIC_API_KEY in the environment (or a .env file in the working
directory / project root, loaded via python-dotenv).
"""
import argparse
import asyncio
import json
import sys
import time

import pandas as pd
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

import persona_prompt

MAX_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 2.0


async def _call_one(client, semaphore, row, variable_meta, conditions, outcome_variable, model, max_tokens):
    stimulus_text = conditions[row["condition"]]
    system, messages, tool_schema = persona_prompt.build_call(
        row, variable_meta, stimulus_text, outcome_variable
    )

    async with semaphore:
        last_error = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                response = await client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    system=system,
                    messages=messages,
                    tools=[tool_schema],
                    tool_choice={"type": "tool", "name": tool_schema["name"]},
                )
                for block in response.content:
                    if block.type == "tool_use" and block.name == "record_response":
                        return {**row, **block.input, "_error": ""}
                last_error = "no tool_use block in response"
            except Exception as exc:  # noqa: BLE001 - want to retry on any transient API error
                last_error = str(exc)
            await asyncio.sleep(RETRY_BACKOFF_SECONDS * attempt)

        return {**row, "_error": last_error}


async def run_all(frame, variable_meta, conditions, outcome_variable, model, max_tokens, concurrency):
    client = AsyncAnthropic()
    semaphore = asyncio.Semaphore(concurrency)
    rows = frame.to_dict(orient="records")

    tasks = [
        _call_one(client, semaphore, row, variable_meta, conditions, outcome_variable, model, max_tokens)
        for row in rows
    ]

    results = []
    total = len(tasks)
    completed = 0
    start = time.time()
    for coro in asyncio.as_completed(tasks):
        result = await coro
        results.append(result)
        completed += 1
        if completed % max(1, total // 20) == 0 or completed == total:
            elapsed = time.time() - start
            print(f"  {completed}/{total} subjects done ({elapsed:.0f}s elapsed)")

    return results


def main():
    parser = argparse.ArgumentParser(description="Run synthetic subjects through the Anthropic API for Stage 4.")
    parser.add_argument("--frame", required=True, help="Path to subjects_frame.csv from sample_population.py")
    parser.add_argument("--population-config", required=True, help="Path to population_config.json (for variable metadata)")
    parser.add_argument("--test-config", required=True, help="Path to test_config.json (conditions, outcome variable, model)")
    parser.add_argument("--out", required=True, help="Path to write subjects_data.csv")
    parser.add_argument("--concurrency", type=int, default=None, help="Override max_concurrency from test_config.json")
    args = parser.parse_args()

    load_dotenv()

    frame = pd.read_csv(args.frame)

    with open(args.population_config, "r", encoding="utf-8") as f:
        population_config = json.load(f)
    variable_meta = population_config.get("variables", [])

    with open(args.test_config, "r", encoding="utf-8") as f:
        test_config = json.load(f)

    conditions = test_config["conditions"]
    outcome_variable = test_config["outcome_variable"]
    model = test_config.get("model", "claude-sonnet-5")
    max_tokens = test_config.get("max_tokens", 500)
    concurrency = args.concurrency or test_config.get("max_concurrency", 20)

    print(f"Running {len(frame)} subjects through model={model}, concurrency={concurrency} ...")
    results = asyncio.run(
        run_all(frame, variable_meta, conditions, outcome_variable, model, max_tokens, concurrency)
    )

    out_frame = pd.DataFrame(results)
    out_frame.to_csv(args.out, index=False)

    n_failed = (out_frame["_error"] != "").sum()
    print(f"Wrote {len(out_frame)} rows -> {args.out}")
    if n_failed:
        print(f"WARNING: {n_failed} subjects failed after {MAX_ATTEMPTS} attempts each (see _error column).")


if __name__ == "__main__":
    sys.exit(main())
