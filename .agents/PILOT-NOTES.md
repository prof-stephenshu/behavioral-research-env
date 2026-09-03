# Antigravity Pilot -- Status

**This branch (`antigravity-pilot`), started September 2026, is unvalidated.** The files under `.agents/skills/` mirror this project's real, tested `.claude/skills/` files (Stages 3, 4, 5, 7), adapted for Google Antigravity's skill convention -- but nobody has run them through Antigravity end-to-end yet. Treat everything here the way workbook Section 7.6 treats the whole Google-stack idea: a conceptual mapping based on Google's published documentation, not a verified case study.

## What's here

- `.agents/skills/behavioral-design/SKILL.md` -- Stage 3 mirror
- `.agents/skills/synthetic-ab-test/SKILL.md` -- Stage 4 mirror
- `.agents/skills/data-analysis/SKILL.md` -- Stage 5 mirror
- `.agents/skills/research-writeup/SKILL.md` -- Stage 7 mirror

Each keeps the same domain logic as its Claude Code counterpart (required inputs, output file structure, human gates) since that's tool-agnostic. What changed is the execution-mechanics language: references to Claude Code's Agent tool and subagent-spawning parameters were replaced with Antigravity's dynamic-subagent concept, described in general terms -- **the exact tool-call names/parameters Antigravity actually exposes for this haven't been verified**, so don't treat those passages as precise API instructions the way the Claude Code originals are.

## Known unknowns

- ~~What does dispatching ~10-subject batches in parallel actually look like~~ -- **confirmed working at N=10/batch size 5** (2 real batches, see Pilot log below). Still open: behavior at N=100+, many parallel batches, or under quota pressure.
- ~~Do the Python scripts under `scripts/` need changes to run correctly when invoked from Antigravity~~ -- **`sample_population.py` confirmed working**: `population_config.json` matched its documented schema exactly. `regression.py`/`charts.py` (Stage 5) not yet tested -- see the script-naming discrepancy noted below, which is exactly why these still need a dedicated check.
- Free-tier quota behavior in practice: is "a meaningful quota, refreshed weekly" (Google's own phrasing) enough to complete even a moderate pilot run (N=100+)? Not yet tested -- N=10 is too small to tell.

## Pilot log

**2026-09-03 -- Skill discovery (Antigravity VS Code extension, first session):**
- ✅ Confirmed: asked "what skills do you have available for this project?" and it correctly listed all four skills by name, path, and stage number, and unprompted noticed this PILOT-NOTES.md file. The `.agents/skills/<name>/SKILL.md` discovery convention works as documented.
- ⚠️ Finding: when summarizing the data-analysis skill, it named the scripts as `regression_analysis.py` and `plot_results.py` -- neither exists. The real files (and the ones actually named in `data-analysis/SKILL.md`) are `regression.py` and `charts.py`. It paraphrased plausible-sounding filenames instead of quoting the ones actually in the file it had just read. Doesn't necessarily mean it'll invoke the wrong script when it comes time to actually *run* Stage 5 (it may re-read the file at that point), but it's a reason to verify actual tool calls/file operations at each stage rather than trust its prose summaries. Watch for this specifically when Stage 4/5 actually execute.

**2026-09-03 -- Stage 3 (behavioral-design), throwaway project `pilot-test-1`:**
- ✅ Ran the standard design-intake prompt (control/treatment stimulus, rough population, outcome). Verified on disk (not just from its chat summary) that all five files landed exactly where the skill specifies: `research_design.md`, `population_spec.md`, `variables_spec.md`, `stimuli/control.md`, `stimuli/treatment.md`.
- ✅ Content quality matched the skill's instructions well: two-condition summary with a named behavioral principle, population spec that explicitly flagged what's unspecified (SD, gender, correlations) rather than inventing values, binary treatment/outcome coding, and it even pre-emptively noted the `--positive-label "Sign Up"` flag Stage 5 will need.
- Net: Stage 3 works as designed on this run. First real evidence the skill-mirroring approach is sound, at least for a stage with no script-execution step.

**2026-09-03 -- Stage 4 (synthetic-ab-test), `pilot-test-1`, N=10, batch size 5:**
- ✅ Verified on disk, not from chat summary: `subjects_frame.csv` (10 rows, 5 control/5 treatment) and `subjects_data.csv` (10 rows, no `_error` values) both exist and are internally consistent with each other.
- ✅ `batches.json` shows exactly 2 batches of 5 subject IDs each, matching the requested batch size -- **real evidence the dynamic-subagent batching mechanism actually ran as 2 separate dispatches**, not a single call or a fabricated-after-the-fact split. This was the single biggest unknown going into the pilot.
- ✅ Every specific number in its chat summary (5/5 allocation, control 1/5 = 20% Sign Up, treatment 3/5 = 60% Sign Up) matches the raw CSV exactly when independently counted.
- Caveat: N=10 is a toy run on the free tier's first request. Doesn't tell us how batching behaves at N=100+, across many parallel batches, or once weekly quota pressure kicks in -- those are still open.
- Net: **the biggest risk in the whole pilot (subagent batching) held up on this run.** Promoting this from "known unknown" to "confirmed at small N, unconfirmed at scale."

**2026-09-03 -- Stage 5 (data-analysis), `pilot-test-1`:**
- ✅ Strongest verification of the pilot: independently re-ran the *actual* `balance_check.py` and `regression.py` on the same `subjects_data.csv` myself. Output was **byte-for-byte identical** to what Antigravity produced (same coefficients, same statsmodels table formatting, only the run timestamp differed).
- ✅ Independently re-ran `charts.py` too -- the resulting PNG's **MD5 hash matched exactly** (`0fa127d8...`) against the chart Antigravity generated. Not just similar -- the identical file.
- This resolves the earlier script-naming concern from the discovery step: despite mis-naming `regression.py`/`charts.py` in a casual summary, when it came time to actually *execute* Stage 5, it correctly invoked the real scripts with the right arguments. Lesson: its prose can be sloppy even when its actions are exact -- verify the artifacts, not the chat.
- Net: **Stage 5 is fully confirmed working**, with the highest-confidence evidence possible (independent reproduction) rather than just plausible-looking output.

**2026-09-03 -- Stage 7 (research-writeup), `pilot-test-1`:**
- ✅ `writeup.md` and `writeup.docx` both exist; the docx is a genuine, valid Microsoft Word file (confirmed via file-type check, not just extension/size).
- ✅ Every statistic in the writeup matches the independently-verified Stage 5 numbers exactly (B=1.792, SE=1.443, p=0.214, OR=6.00) -- no drift or rounding surprises introduced during writeup drafting.
- ✅ Correctly reported the treatment effect as *not* reaching significance rather than overclaiming -- matches the skill's explicit instruction not to overclaim.
- ✅ Correctly omitted the reference-study comparison section, since none was supplied -- matches the skill's "only include if given reference stats" instruction.
- ✅ The one qualitative quote it pulled into the discussion ("seeing 'for your family's future' really caught my attention with two kids at home") is **word-for-word** from subject S00001's actual `reasoning` field in `subjects_data.csv` -- not paraphrased or invented.
- Net: **Stage 7 confirmed working**, with the same standard of evidence as Stage 5 (checked against source data, not just "looks plausible").

## Overall pilot status (as of the log above)

**All four stages (3, 4, 5, 7) have now been run once, end-to-end, on a toy N=10 project (`pilot-test-1`), and every output was independently verified** -- against the filesystem, a from-scratch re-run of the real scripts (byte-identical results for Stage 5), or the source data itself (Stage 7's quote). This is a full, clean pass through the entire pipeline this repo supports.

**Remaining open questions**, none of which an N=10 single run can answer:
- Behavior at real scale (N=100+) and with many batches dispatched in parallel
- Free-tier quota limits under sustained use (Google's own phrasing is only "a meaningful quota, refreshed weekly")
- Whether `api` mode can be made to work (currently marked not-yet-available in `synthetic-ab-test/SKILL.md` pending a Gemini-compatible rewrite of `run_subjects.py`)

**Recommendation:** this is strong enough evidence to keep developing on this branch and consider a larger-N run (e.g. N=50-100) as the next validation step, but not yet strong enough (single toy run) to promote to `master` as a second supported path -- that should wait for at least one moderate-scale run and some signal on quota behavior.

## How this relates to the rest of the repo

- `master` (tagged `v1-claude-code` at the point this branch split off) is untouched by anything here -- nothing in `.claude/`, `scripts/`, or `presentations/` was modified.
- Workbook Section 7.6 (`presentations/2026-workshop/workbook.md`) has the full conceptual mapping and stability caveats this pilot is built on.
- If a real Antigravity run validates (or corrects) what's here, that's the point to consider merging this branch into `master` -- with the corrections folded in and this notes file updated to reflect what was actually confirmed.
