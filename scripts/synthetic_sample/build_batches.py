"""
Stage 4 subagent-mode batch builder.

Splits the sampled subject frame into batches and renders one self-contained
prompt per batch (via persona_prompt.build_batch_prompt), ready for the
orchestrating skill to hand to the Agent tool -- one Agent call per batch,
no API key required.

Usage:
    python build_batches.py --frame subjects_frame.csv --population-config population_config.json \
        --test-config test_config.json --out batches.json [--batch-size 10]
"""
import argparse
import json
import sys

import pandas as pd

import persona_prompt


def build_batches(frame, variable_meta, conditions, outcome_variable, batch_size):
    rows = frame.to_dict(orient="records")
    batches = []
    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i + batch_size]
        batch_id = f"B{str(len(batches) + 1).zfill(4)}"
        prompt = persona_prompt.build_batch_prompt(chunk, variable_meta, conditions, outcome_variable)
        batches.append({
            "batch_id": batch_id,
            "subject_ids": [r["subject_id"] for r in chunk],
            "prompt": prompt,
        })
    return batches


def main():
    parser = argparse.ArgumentParser(description="Build subagent-mode batch prompts for Stage 4.")
    parser.add_argument("--frame", required=True, help="Path to subjects_frame.csv from sample_population.py")
    parser.add_argument("--population-config", required=True)
    parser.add_argument("--test-config", required=True)
    parser.add_argument("--batch-size", type=int, default=None, help="Override batch_size from test_config.json")
    parser.add_argument("--out", required=True, help="Path to write batches.json")
    args = parser.parse_args()

    frame = pd.read_csv(args.frame)

    with open(args.population_config, "r", encoding="utf-8") as f:
        population_config = json.load(f)
    variable_meta = population_config.get("variables", [])

    with open(args.test_config, "r", encoding="utf-8") as f:
        test_config = json.load(f)

    conditions = test_config["conditions"]
    outcome_variable = test_config["outcome_variable"]
    batch_size = args.batch_size or test_config.get("batch_size", 10)

    batches = build_batches(frame, variable_meta, conditions, outcome_variable, batch_size)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(batches, f, indent=2)

    print(f"Wrote {len(batches)} batches ({batch_size} subjects/batch, {len(frame)} total) -> {args.out}")


if __name__ == "__main__":
    sys.exit(main())
