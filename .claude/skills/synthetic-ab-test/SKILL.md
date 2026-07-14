---
name: synthetic-ab-test
description: Stage 4 of the behavioral research workflow. Use when the user has a completed Stage 3 design package (control/treatment stimuli, population spec, variables spec) and wants to run a synthetic between-subject A/B test using LLM-simulated subjects to collect decision data.
---

# Synthetic Sample A/B Testing (Stage 4)

Reads the Stage 3 design package for a project, fills in sampling details, draws a synthetic subject population, and collects each subject's decision. Produces `subjects_data.csv` for Stage 5.

There are two ways to collect subject responses:

- **`subagent` mode (default)** — you (the orchestrating assistant) spawn Claude Code subagents via the Agent tool, batched, and parse their JSON replies yourself. No API key needed; runs against the researcher's existing Claude Code session/plan.
- **`api` mode (opt-in)** — a Python script calls the Anthropic API directly and concurrently. Faster and cheaper per-subject at large N, but requires a separate `ANTHROPIC_API_KEY` with its own billing.

Ask the researcher which mode to use only if they haven't said; otherwise default to `subagent` without asking.

## Preconditions

Confirm `projects/<slug>/03_design/` exists with `research_design.md`, `stimuli/control.md`, `stimuli/treatment.md`, `population_spec.md`, and `variables_spec.md`. If any are missing, tell the user to run `/behavioral-design` first rather than trying to reconstruct them yourself.

If `api` mode is chosen, confirm `ANTHROPIC_API_KEY` is available (environment or a `.env` file at the project root) before proceeding; if missing, tell the user to set it or switch to `subagent` mode.

## 1. Translate the design package into structured configs

Read `population_spec.md`, `variables_spec.md`, and both stimulus files. Ask the user for whatever `population_spec.md` flagged as unspecified, plus:
- Total N and allocation (equal split across control/treatment by default, or explicit counts)
- Any cross-correlation guidance between sampled variables (optional, skip if the user has no view)
- Mode-specific settings (ask only what's relevant to the chosen mode):
  - `subagent` mode: batch size (default 10 subjects/batch — smaller batches read more reliably but mean more Agent calls; larger batches are cheaper but risk the subagent's answers drifting toward each other across subjects in the same call) and which agent type to use (default `general-purpose`)
  - `api` mode: model (default `claude-sonnet-5`), concurrency cap (default 20)

Write to `projects/<slug>/04_synthetic_test/`:

**`population_config.json`** — matches the schema documented at the top of `scripts/synthetic_sample/sample_population.py`: `conditions`, `n_total`, `allocation`, `variables`, `correlations`.

**`test_config.json`**:
```json
{
  "mode": "subagent",
  "conditions": {"control": "<verbatim text from stimuli/control.md>", "treatment": "<verbatim text from stimuli/treatment.md>"},
  "outcome_variable": {"name": "...", "type": "binary|categorical|continuous", "options": [...], "scale_min": 0, "scale_max": 10, "description": "..."},
  "batch_size": 10,
  "agent_type": "general-purpose",
  "model": "claude-sonnet-5",
  "max_concurrency": 20,
  "max_tokens": 500
}
```
Take the outcome variable's name/type straight from `variables_spec.md`. If it lists secondary DVs, add them under `outcome_variable.secondary` as a list of the same shape. Keep both the `subagent`-relevant and `api`-relevant fields present regardless of mode — cheap to have, and it means switching modes later doesn't require rebuilding the config.

Show the user both configs before running anything and get a quick confirmation.

## 2. Sample the population

Run from `scripts/synthetic_sample/`:
```
..\..\.venv\Scripts\python.exe sample_population.py --config ..\..\projects\<slug>\04_synthetic_test\population_config.json --out ..\..\projects\<slug>\04_synthetic_test\subjects_frame.csv --seed <any fixed int>
```
Report the resulting condition counts. If they look off, fix `population_config.json` and re-run before collecting any responses.

## 3. Collect responses

### subagent mode (default)

1. Build the batch prompts:
   ```
   ..\..\.venv\Scripts\python.exe build_batches.py --frame ..\..\projects\<slug>\04_synthetic_test\subjects_frame.csv --population-config ..\..\projects\<slug>\04_synthetic_test\population_config.json --test-config ..\..\projects\<slug>\04_synthetic_test\test_config.json --out ..\..\projects\<slug>\04_synthetic_test\batches.json
   ```
2. Read `batches.json`. For each batch, spawn one Agent (`subagent_type` from `test_config.json`'s `agent_type`, default `general-purpose`) with that batch's `prompt` as the task, `run_in_background: false` so you get the result before continuing, isolation omitted (no worktree needed — these agents aren't touching the repo). Launch several batches per message in parallel (multiple Agent tool calls in one turn) rather than one at a time, to keep this tractable at moderate-to-large N.
3. Each agent's reply should end with a JSON array. Parse it — strip any leading/trailing prose the agent added despite instructions, since subagents don't have a forced-output guarantee the way the API's tool-calling does. If a batch's reply fails to parse, retry that batch once (re-spawn with the same prompt); if it fails again, note the batch's subject_ids as failed and move on rather than blocking the whole run.
4. Concatenate every successfully parsed batch's JSON array into one combined list and write it as `raw_responses.json` in `04_synthetic_test/`.
5. Merge into the final dataset:
   ```
   ..\..\.venv\Scripts\python.exe merge_responses.py --frame ..\..\projects\<slug>\04_synthetic_test\subjects_frame.csv --responses ..\..\projects\<slug>\04_synthetic_test\raw_responses.json --out ..\..\projects\<slug>\04_synthetic_test\subjects_data.csv
   ```

Note for the researcher up front: this mode runs synchronously inside the conversation — collecting N=250 subjects at batch size 10 means roughly 25 Agent calls (fewer wall-clock rounds if launched in parallel batches), which takes real session time and counts against their Claude Code plan usage, not separate API credits.

### api mode (opt-in)

Run:
```
..\..\.venv\Scripts\python.exe run_subjects.py --frame ..\..\projects\<slug>\04_synthetic_test\subjects_frame.csv --population-config ..\..\projects\<slug>\04_synthetic_test\population_config.json --test-config ..\..\projects\<slug>\04_synthetic_test\test_config.json --out ..\..\projects\<slug>\04_synthetic_test\subjects_data.csv
```
This can take a while for large N — let it run and relay progress.

## 4. Handoff

Summarize: total subjects collected, condition counts, any failures/missing responses, and a couple of example rows. There's no formal human gate specified for this stage, but confirm with the user that the data looks sane before pointing them to `/data-analysis` — don't invoke that skill yourself.
