---
name: data-analysis
description: Stage 5 of the behavioral research workflow (v1 scope). Use when the user has subjects_data.csv from Stage 4 (synthetic A/B test) and wants a randomization balance check, primary regression analysis, and an outcome-by-condition bar chart.
---

# Data Analysis (Stage 5, v1 scope)

v1 covers three things: randomization balance check, primary regression (OLS/logit), and an outcome-by-condition bar chart. Mediation, floodlight/moderation analysis, and SEM diagrams are explicitly out of scope for now — if the user asks for them, note that they're planned but not yet built rather than attempting them ad hoc.

## Preconditions

Confirm `projects/<slug>/04_synthetic_test/subjects_data.csv`, `population_config.json`, and `test_config.json` exist. If missing, point the user to `/synthetic-ab-test` rather than reconstructing them.

Create `projects/<slug>/05_analysis/` and `projects/<slug>/05_analysis/charts/` if they don't exist.

## 1. Balance check

Run from `scripts/analysis/`:
```
..\..\.venv\Scripts\python.exe balance_check.py --data ..\..\projects\<slug>\04_synthetic_test\subjects_data.csv --population-config ..\..\projects\<slug>\04_synthetic_test\population_config.json --out ..\..\projects\<slug>\05_analysis\balance_report.md
```
Read the resulting report back and flag any imbalance (p < .05) to the user before proceeding — an imbalanced randomization is worth knowing about before interpreting the regression, though it doesn't have to block moving forward.

## 2. Regression

Get the DV name/type from `test_config.json`'s `outcome_variable`. Ask the user (don't assume):
- Which columns, if any, to include as controls (candidates: any `variables` in `population_config.json` not already used as the moderator/treatment)
- Any interactions to include (treatment x a specific individual-difference variable)
- The control-condition label (should match Stage 3's condition naming, typically `control`)
- If the DV is binary: which of its two option values should be coded 1 (e.g. "buy" rather than "decline") — pass this via `--positive-label`. Don't let it default silently to alphabetical order; the sign of the treatment effect depends on this.

Run:
```
..\..\.venv\Scripts\python.exe regression.py --data ..\..\projects\<slug>\04_synthetic_test\subjects_data.csv --dv <dv_name> --dv-type <binary|continuous> --condition-col condition --control-label control --positive-label <...> --controls <...> --interactions <...> --out ..\..\projects\<slug>\05_analysis\regression_results.md
```
Summarize the treatment effect (sign, size, significance) back to the user in plain language, both with and without controls if controls were specified.

## 3. Outcome-by-condition bar chart

Run (use the same `--positive-label` choice as the regression step for a binary DV, so the chart and regression agree on direction):
```
..\..\.venv\Scripts\python.exe charts.py --data ..\..\projects\<slug>\04_synthetic_test\subjects_data.csv --dv <dv_name> --dv-type <binary|continuous> --condition-col condition --positive-label <...> --out ..\..\projects\<slug>\05_analysis\charts\<dv_name>_by_condition.png
```
If Stage 3's `variables_spec.md` lists secondary DVs, repeat for each.

## 4. Wrap-up

Write a short `analysis_summary.md` in `05_analysis/` covering: balance check outcome, the treatment effect from the regression, and a pointer to the chart(s). Present this to the user and get explicit confirmation before considering Stage 5 complete — this is the human gate before any future presentation-creation stage (not yet built).
