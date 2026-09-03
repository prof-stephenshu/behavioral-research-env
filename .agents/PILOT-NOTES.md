# Antigravity Pilot -- Status

**This branch (`antigravity-pilot`), started September 2026, is unvalidated.** The files under `.agents/skills/` mirror this project's real, tested `.claude/skills/` files (Stages 3, 4, 5, 7), adapted for Google Antigravity's skill convention -- but nobody has run them through Antigravity end-to-end yet. Treat everything here the way workbook Section 7.6 treats the whole Google-stack idea: a conceptual mapping based on Google's published documentation, not a verified case study.

## What's here

- `.agents/skills/behavioral-design/SKILL.md` -- Stage 3 mirror
- `.agents/skills/synthetic-ab-test/SKILL.md` -- Stage 4 mirror
- `.agents/skills/data-analysis/SKILL.md` -- Stage 5 mirror
- `.agents/skills/research-writeup/SKILL.md` -- Stage 7 mirror

Each keeps the same domain logic as its Claude Code counterpart (required inputs, output file structure, human gates) since that's tool-agnostic. What changed is the execution-mechanics language: references to Claude Code's Agent tool and subagent-spawning parameters were replaced with Antigravity's dynamic-subagent concept, described in general terms -- **the exact tool-call names/parameters Antigravity actually exposes for this haven't been verified**, so don't treat those passages as precise API instructions the way the Claude Code originals are.

## Known unknowns (please help resolve these if you pilot this)

- Does Antigravity's Skills auto-invocation (matching on `description`) behave the same way as Claude Code's in practice, for these specific descriptions?
- What does dispatching ~10-subject batches in parallel actually look like in Antigravity's Mission Control / Agent Manager -- is it as workable as spawning subagents inline in Claude Code?
- Do the Python scripts under `scripts/` (population sampling, batching, merging, analysis) need any changes to run correctly when invoked from Antigravity rather than Claude Code? (Expectation: no, since they're plain Python -- but unverified.)
- Free-tier quota behavior in practice: is "a meaningful quota, refreshed weekly" (Google's own phrasing) enough to complete even a small pilot run (N=20)?

## How this relates to the rest of the repo

- `master` (tagged `v1-claude-code` at the point this branch split off) is untouched by anything here -- nothing in `.claude/`, `scripts/`, or `presentations/` was modified.
- Workbook Section 7.6 (`presentations/2026-workshop/workbook.md`) has the full conceptual mapping and stability caveats this pilot is built on.
- If a real Antigravity run validates (or corrects) what's here, that's the point to consider merging this branch into `master` -- with the corrections folded in and this notes file updated to reflect what was actually confirmed.
