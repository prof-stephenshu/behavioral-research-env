# Analysis Summary: test-run-1-n400

N=400 synthetic subjects (200/condition), subagent mode, batch size 10 (40 batches). Full-scale replication of the `test-run-1` pilot (N=20). Not blinded -- treatment/control known from the start.

**Treatment = condition_1** ("$5 a day" framing). **Control = condition_2** ("$150 a month" framing).

## Balance check

Age, income_bracket, education, financial_literacy, and subjective_numeracy all balanced (p>.05). **Gender was imbalanced** (condition_1 52% female vs. condition_2 41% female, chi-sq p=.035) -- with 6 variables tested, roughly a 1-in-4 chance of at least one spurious p<.05 result, so this is plausibly chance rather than a sampler bug (the sampler code assigns condition independently of demographics by construction). Confirmed the main results are robust by re-running with gender as a control; conclusions are unchanged.

## Primary outcome: choice (sign-up decision)

- Control (condition_2, "$150/mo"): 45.5% signed up (SE .035)
- Treatment (condition_1, "$5/day"): 64.5% signed up (SE .034)
- Logit: treatment coefficient = +0.78 (p<.001) without controls, +0.82 (p<.001) with gender control

**This replicates the pilot's direction and is now clearly significant at N=400** (the pilot's p=.079 was consistent with a real effect that was simply underpowered to detect at N=20).

## Secondary outcomes

- **affordability_rating (1-7):** treatment 4.66 vs control 4.05 (OLS coef +0.62, p<.001) -- replicates, significant at scale, robust to gender control.
- **clarity_rating (1-7):** treatment 5.35 vs control 5.31 (OLS coef +0.035, p=.71) -- **does not replicate**. The pilot's marginal clarity difference (p=.077 at N=20) washes out entirely at N=400. This is the expected pattern if that pilot result was noise: the stimuli never manipulated comprehensibility, only the framing of the same amount, so a true near-zero effect on clarity is the more plausible read.

## Charts

`charts/choice_by_condition.png`, `charts/affordability_by_condition.png`, `charts/clarity_by_condition.png`

## Takeaway

The temporal reframing effect holds up at scale: reframing $150/month as $5/day meaningfully increases both stated sign-up intent and perceived affordability, with no corresponding change in how clearly the offer was understood -- consistent with affordability perception (not comprehension) being the driving mechanism.
