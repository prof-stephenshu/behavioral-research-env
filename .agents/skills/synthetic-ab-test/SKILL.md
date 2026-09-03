---
name: synthetic-ab-test
description: Stage 4 of the behavioral research workflow. Use when the user has a completed Stage 3 design package (control/treatment stimuli, population spec, variables spec) and wants to run a synthetic between-subject A/B test using LLM-simulated subjects to collect decision data.
---

<!--
PILOT / UNVALIDATED (Antigravity mirror of .claude/skills/synthetic-ab-test/SKILL.md,
Sept 2026). This is the file most likely to need correction: Claude Code's original
spawns "Agent tool" subagents with specific parameters (run_in_background: false,
batched parallel calls in one turn). The subagent-collection step below is rewritten
in general terms for Antigravity's dynamic subagents, since the exact tool-call
surface Antigravity exposes for this has not been verified against a real run.
See .agents/PILOT-NOTES.md.
-->

# Synthetic Sample A/B Testing (Stage 4)

Reads the Stage 3 design package for a project, fills in sampling details, draws a synthetic subject population, and collects each subject's decision. Produces `subjects_data.csv` for Stage 5.

There are two ways to collect subject responses:

- **`subagent` mode (default)** — you (the orchestrating agent) spawn parallel child subagents, batched, and parse their JSON replies yourself. No API key needed; runs against the researcher's existing Antigravity plan/quota.
- **`api` mode (opt-in)** — a Python script calls the Gemini API directly and concurrently. Faster and cheaper per-subject at large N, but requires a separate API key (e.g. from Google AI Studio) with its own quota/billing, and this pilot has not adapted `run_subjects.py` for a non-Anthropic API — treat `api` mode as **not yet available** on this branch until that script is updated.

Ask the researcher which mode to use only if they haven't said; otherwise default to `subagent` without asking.

## Preconditions

Confirm `projects/<slug>/03_design/` exists with `research_design.md`, `stimuli/control.md`, `stimuli/treatment.md`, `population_spec.md`, and `variables_spec.md`. If any are missing, tell the user to run the behavioral-design skill first rather than trying to reconstruct them yourself.

## 1. Translate the design package into structured configs

Read `population_spec.md`, `variables_spec.md`, and both stimulus files. Ask the user for whatever `population_spec.md` flagged as unspecified, plus:
- Total N and allocation (equal split across control/treatment by default, or explicit counts)
- Any cross-correlation guidance between sampled variables (optional, skip if the user has no view)
- Batch size for subagent mode (default 10 subjects/batch — smaller batches read more reliably but mean more child-agent dispatches; larger batches are cheaper but risk answers drifting toward each other across subjects in the same call)

Write to `projects/<slug>/04_synthetic_test/`:

**`population_config.json`** — matches the schema documented at the top of `scripts/synthetic_sample/sample_population.py`: `conditions`, `n_total`, `allocation`, `variables`, `correlations`.

**`test_config.json`**:
```json
{
  "mode": "subagent",
  "conditions": {"control": "<verbatim text from stimuli/control.md>", "treatment": "<verbatim text from stimuli/treatment.md>"},
  "outcome_variable": {"name": "...", "type": "binary|categorical|continuous", "options": [...], "scale_min": 0, "scale_max": 10, "description": "..."},
  "batch_size": 10,
  "max_tokens": 500
}
```
Take the outcome variable's name/type straight from `variables_spec.md`. If it lists secondary DVs, add them under `outcome_variable.secondary` as a list of the same shape.

Show the user both configs before running anything and get a quick confirmation.

## 2. Sample the population

Run from `scripts/synthetic_sample/`:
```
..\..\.venv\Scripts\python.exe sample_population.py --config ..\..\projects\<slug>\04_synthetic_test\population_config.json --out ..\..\projects\<slug>\04_synthetic_test\subjects_frame.csv --seed <any fixed int>
```
Report the resulting condition counts. If they look off, fix `population_config.json` and re-run before collecting any responses.

## 3. Collect responses (subagent mode)

1. Build the batch prompts:
   ```
   ..\..\.venv\Scripts\python.exe build_batches.py --frame ..\..\projects\<slug>\04_synthetic_test\subjects_frame.csv --population-config ..\..\projects\<slug>\04_synthetic_test\population_config.json --test-config ..\..\projects\<slug>\04_synthetic_test\test_config.json --out ..\..\projects\<slug>\04_synthetic_test\batches.json
   ```
2. Read `batches.json`. For each batch, dispatch one child subagent with that batch's `prompt` as its task, and wait for its result before moving on to merge that batch's output. **Unverified:** whether Antigravity's Mission Control / Agent Manager is the right surface for dispatching these, and how many can usefully run in parallel — start with a small number of concurrent batches and confirm results look sane before scaling up.
3. Each agent's reply should end with a JSON array. Parse it — strip any leading/trailing prose the agent added despite instructions, since subagents don't generally have a forced-output guarantee. If a batch's reply fails to parse, retry that batch once; if it fails again, note the batch's subject_ids as failed and move on rather than blocking the whole run.
4. Concatenate every successfully parsed batch's JSON array into one combined list and write it as `raw_responses.json` in `04_synthetic_test/`.
5. Merge into the final dataset:
   ```
   ..\..\.venv\Scripts\python.exe merge_responses.py --frame ..\..\projects\<slug>\04_synthetic_test\subjects_frame.csv --responses ..\..\projects\<slug>\04_synthetic_test\raw_responses.json --out ..\..\projects\<slug>\04_synthetic_test\subjects_data.csv
   ```

Note for the researcher up front: this mode runs against the free tier's weekly quota (Google does not publish an exact number), so a first pilot run should stay small — N=20-50, not N=400 — until you know how far the quota goes.

## 4. Handoff

Summarize: total subjects collected, condition counts, any failures/missing responses, and a couple of example rows. There's no formal human gate specified for this stage, but confirm with the user that the data looks sane before pointing them to the data-analysis skill — don't invoke that skill yourself.
