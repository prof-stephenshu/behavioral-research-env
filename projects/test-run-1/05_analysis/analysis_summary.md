# Analysis Summary: test-run-1 (blinded)

N=20 synthetic subjects (10/condition), subagent mode, batch size 10, agent_type general-purpose.

## Balance check

No imbalance at conventional p<.05 across age, gender, income_bracket, education, or subjective_numeracy. `financial_literacy` is borderline (condition_1 mean 2.4 vs condition_2 mean 1.7, F-test p=.055) -- worth re-checking at a larger N, but not flagged as a hard imbalance here.

## Primary outcome: choice (sign-up decision)

- condition_1: 80% signed up (SE .133)
- condition_2: 40% signed up (SE .163)
- Logit: condition_2 coefficient = -1.79 (p=.079, marginal at N=20)

## Secondary outcomes

- affordability_rating (1-7): condition_1 mean 5.4 vs condition_2 mean 4.1 (OLS coef -1.30, p=.077)
- clarity_rating (1-7): condition_1 mean 5.8 vs condition_2 mean 5.2 (OLS coef -0.60, p=.077)

## Charts

`charts/choice_by_condition.png`, `charts/affordability_by_condition.png`, `charts/clarity_by_condition.png`

## Note

All three outcomes point the same direction (condition_1 > condition_2) and land in the same marginal p~.08 range at this small N -- consistent, but underpowered to call decisively. No treatment/control interpretation is offered here per the blinding request; unblind when ready and I can reframe these results in those terms.
