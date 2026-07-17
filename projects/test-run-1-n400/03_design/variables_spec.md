# Variables Specification: test-run-1

## Independent variable

Single condition indicator: `condition_1` vs. `condition_2` (blinded -- not yet mapped to control/treatment). For regression coding purposes only, `condition_1` will be used as the reference/base category until the researcher reveals which arm is the true control; this is an arbitrary encoding choice, not a claim about which arm is the baseline.

## Primary outcome variable (Question 1)

- **Name:** `choice`
- **Type:** binary
- **Options:** `["Not now", "Yes, start saving"]`
- **Coding requirement (researcher-specified):** "Yes, start saving" = 1, "Not now" = 0. When running Stage 5 regression/charts, pass `--positive-label "Yes, start saving"` explicitly -- do not rely on the alphabetical default.
- **Description:** Whether the subject chooses to start saving after seeing the app's prompt.

## Secondary outcome variables (Question 2)

- **`affordability_rating`** -- continuous, scale 1 (strongly disagree) to 7 (strongly agree). "I found the option to be affordable."
- **`clarity_rating`** -- continuous, scale 1 (strongly disagree) to 7 (strongly agree). "I found the description of the option to be clear and understandable."

## Reasoning (Question 3)

Captured via the standard `reasoning` field, with a custom prompt matching the instrument's exact wording rather than the generic default:
> "List three things you were thinking about when given this savings option, in your own words, as this subject."

## Controls / covariates

None specified by the researcher yet. Candidates available from `population_spec.md` if wanted later: age, gender, income_bracket, education, financial_literacy, subjective_numeracy.
