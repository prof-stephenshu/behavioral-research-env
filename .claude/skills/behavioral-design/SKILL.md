---
name: behavioral-design
description: Stage 3 of the behavioral research workflow. Use when the user wants to set up a control-vs-treatment behavioral test — they give you a control condition stimulus, a treatment condition stimulus, a description of the population to sample, and an outcome variable, and want these turned into a structured design package that feeds the synthetic A/B testing stage.
---

# Behavioral Design (Stage 3)

This is a deliberately simplified Stage 3: the researcher supplies the design directly rather than the skill generating ideas. Your job is to collect four inputs, fill genuine gaps, and emit a structured output package that Stage 4 (`synthetic-ab-test`) and Stage 5 (`data-analysis`) can consume without further clarification.

## Required inputs

Ask for all four in one pass if the user hasn't already provided them conversationally:

1. **Control condition stimulus** — the baseline experience (copy, screen, email, page, message, etc.)
2. **Treatment condition stimulus** — the modified experience being tested
3. **Population to sample** — demographics and/or individual behavioral differences (e.g. financial literacy, numeracy, loss aversion, present bias, personality), given as free text, descriptive stats (means/SDs/fractions), or an uploaded CSV/Excel file
4. **Outcome variable** — the dependent variable to measure, and whether it's binary (e.g. buy/decline) or continuous (e.g. rating, amount)

Do not ask about idea generation, alternative conditions, or design strategy — there is exactly one control and one treatment condition in this version.

## Completeness check

Only ask follow-up questions for genuine gaps that would block Stage 4/5, for example:
- The outcome variable's type (binary vs. continuous) can't be inferred → ask directly.
- The population description is too vague to sample from (e.g. "adults" with no age/income/other detail) → ask for at least rough descriptive stats.
- A stimulus is referenced but not actually provided (e.g. "same as control but friendlier") → ask for the actual copy/content.

Do not ask about anything else — no goals/outcomes audit, no exploratory-vs-narrow design discussion, no stretch reframing ideas. This is an intake step, not an ideation step.

## Output package

Ask for (or infer from context) a short project slug in kebab-case if one hasn't been established, then create:

```
projects/<slug>/03_design/
  research_design.md
  stimuli/control.md
  stimuli/treatment.md
  population_spec.md
  variables_spec.md
```

**`research_design.md`** — two-condition summary:
- Condition names (Control, Treatment)
- One-line note on the behavioral principle behind the treatment (your read of *why* it should move the outcome, e.g. "adds a default option to reduce choice friction")
- The outcome variable and its type

**`stimuli/control.md`, `stimuli/treatment.md`** — the actual stimulus content as given by the user. If the stimulus is a visual artifact (landing page, popup, email, ad, physical mailer), also render it as a self-contained HTML mockup and publish it via the Artifact tool (favicon: use a single relevant emoji, e.g. 🧪) so the user can visually confirm it before moving on. Keep the HTML mockup faithful to what the user described — don't invent copy or layout details they didn't give you.

**`population_spec.md`** — structured version of the population description:
- Any demographic variables mentioned (population, age, gender, income, education, etc.) with whatever specification level was given (text description, or mean/SD, or fraction)
- Any individual behavioral differences mentioned (financial literacy, numeracy, loss aversion, present bias, personality, etc.) similarly specified
- Note explicitly which variables were *not* specified, so Stage 4 knows what it can still ask to refine (e.g. cross-correlations between variables) versus what's already locked in

**`variables_spec.md`** — regression-ready variable spec:
- Independent variable: a single binary treatment indicator (0 = control, 1 = treatment)
- Dependent variable: name, type (binary → logit, continuous → OLS), and how it's measured/scaled
- Note if the user mentioned any candidate controls or covariates (age, income, etc. as controls rather than just sampling strata) — if none mentioned, leave the controls list empty rather than inventing some

## Human gate

After producing the package, summarize it back to the user in a few lines (conditions, principle, population summary, outcome variable) and explicitly ask them to confirm before proceeding to Stage 4. Do not invoke or suggest running `/synthetic-ab-test` until they confirm. If they want changes, edit the relevant file(s) and re-summarize.
