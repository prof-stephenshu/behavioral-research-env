---
name: research-writeup
description: Stage 7 of the behavioral research workflow (results-and-method scope, no mediation/moderation). Use when the user has completed Stage 5 analysis for a project and wants a Word-ready writeup drafted -- method, balance table, and per-outcome results, optionally compared against a reference study's published statistics.
---

# Research Writeup (Stage 7, results-and-method scope)

Produces `projects/<slug>/07_writeup/writeup.md` and a converted `writeup.docx`. Covers Method, Summary Statistics/Balance, and Results only -- no intro/theory framing, no mediation or moderation analysis (out of scope; Stage 5 doesn't compute these).

## Preconditions

Confirm `projects/<slug>/03_design/`, `04_synthetic_test/`, and `05_analysis/` all exist and are populated (balance report, regression results, charts). If Stage 5 hasn't been run, point the user to `/data-analysis` rather than improvising numbers.

Confirm `pandoc` is on PATH (`pandoc --version`); if missing, install via `winget install --id JohnMacFarlane.Pandoc --source winget --scope user` before proceeding.

## 1. Method section

Draft from `03_design/research_design.md`, `03_design/variables_spec.md`, and `04_synthetic_test/test_config.json` and `population_config.json`:
- Sample: N, allocation, and collection mode (subagent batches vs. direct API) -- phrase this accurately as an LLM-simulated sample, not a human recruitment platform. State the underlying population basis (e.g., "profiles sampled to match published crowdworker population statistics: age M=..., SD=...").
- Design: between-subject, conditions and what each one presented (quote stimuli verbatim, condensed if long).
- Outcome variables: primary and secondary, with exact question wording and response scale, drawn from `variables_spec.md`.

## 2. Summary statistics and balance

Convert `05_analysis/balance_report.md` into a Table-1-style table: one row per condition plus overall, columns for each demographic/individual-difference variable, with the balance test statistics (F/chi-sq/Bartlett's, p-values) reported in prose beneath the table -- mirror the style of "An F-test does not reject the null hypothesis that means are the same between conditions" rather than just dumping the raw report.

## 3. Results

One subsection per outcome variable (primary first, then each secondary), pulling from the corresponding `05_analysis/regression_results_*.md`:
- Report the coefficient, direction, and significance in the paper's in-text style: `B=0.817, p<.001` (logit) or `β=0.639, p<.001` (OLS), for both the no-controls and with-controls models where available.
- Embed the corresponding chart from `05_analysis/charts/`.
- Keep interpretation factual and hedged to what the data show -- don't overclaim mechanism (that's what mediation analysis would test, and it's out of scope here).

## 4. Comparison to reference study (optional)

Only include this section if the researcher supplies reference statistics for one or more of the same outcome variables (citation + effect size + p-value, with or without controls). Do not fabricate or estimate reference values yourself.

For each outcome with a supplied reference value, build a table:

| Outcome | Reference study | This run | Assessment |
|---|---|---|---|

Classify **Assessment** with a simple, stated rule (write the rule into the writeup so the classification isn't a black box):
- **Replicates** -- same sign, both p<.05
- **Partially replicates** -- same sign, significant in only one of the two
- **Does not replicate** -- opposite sign, or the reference was significant and this run's estimate is near zero

Add one sentence of honest interpretation per row -- don't smooth over a non-replication.

## 5. Assemble and convert

Write the full markdown to `projects/<slug>/07_writeup/writeup.md`, then convert:
```
pandoc "projects/<slug>/07_writeup/writeup.md" -o "projects/<slug>/07_writeup/writeup.docx"
```
Confirm the docx was created (check file exists and has nonzero size) before telling the user it's done.

## Handoff

Summarize what's in the writeup (word count ballpark, which sections included, whether a comparison section was added) and point to the file paths. Ask if they want any section expanded/trimmed before considering Stage 7 complete -- don't assume the first draft is final.
