# Analysis Summary: test-run-1 (unblinded 2026-07-17)

N=20 synthetic subjects (10/condition), subagent mode, batch size 10, agent_type general-purpose.

**Treatment = condition_1** ("$5 a day" framing). **Control = condition_2** ("$150 a month" framing).

## Balance check

No imbalance at conventional p<.05 across age, gender, income_bracket, education, or subjective_numeracy. `financial_literacy` is borderline (treatment mean 2.4 vs control mean 1.7, F-test p=.055) -- worth re-checking at a larger N, but not flagged as a hard imbalance here.

## Primary outcome: choice (sign-up decision)

- Control (condition_2, "$150/month"): 40% signed up (SE .163)
- Treatment (condition_1, "$5/day"): 80% signed up (SE .133)
- Logit: treatment coefficient = +1.79 (p=.079, marginal at N=20)

The temporal reframing manipulation roughly doubled the sign-up rate relative to the equivalent monthly framing, consistent with the classic affordability-framing effect in the behavioral economics literature (smaller, more frequent amounts read as more affordable than the same total presented as a larger periodic sum).

## Secondary outcomes

- affordability_rating (1-7): treatment mean 5.4 vs control mean 4.1 (OLS coef +1.30, p=.077) -- the daily framing was rated more affordable, as expected if affordability perception is the driving mechanism.
- clarity_rating (1-7): treatment mean 5.8 vs control mean 5.2 (OLS coef +0.60, p=.077) -- also rated as somewhat clearer, though this wasn't the primary manipulated dimension.

## Charts

`charts/choice_by_condition.png`, `charts/affordability_by_condition.png`, `charts/clarity_by_condition.png` (titles now labeled treatment/control).

## Caveat

All three outcomes point the same direction and land in the same marginal p~.08 range at this small N (20) -- directionally consistent with a real affordability-framing effect, but underpowered to call decisively. A larger N (e.g. 200/condition, per the earlier token-cost estimate) would be needed for a confident read.
