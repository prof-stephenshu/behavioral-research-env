# Population Specification: test-run-1

Source population: crowdsourcing platform sample (e.g. Amazon TurkPrime), circa 2019, pre-dating widespread consumer-facing AI platforms.

## Demographics

| Variable | Spec | Notes |
|---|---|---|
| age | mean 34.29, SD 7.24 | modeled as continuous, clipped to [18, 85] |
| gender | 52.3% male | modeled as binary female/male (47.7% female) per researcher confirmation -- no third category |
| income_bracket | mean 5.29, SD 3.2, ordinal 1-16 | 1 = <$10k/yr ... 16 = $150k+/yr in $10k bands (see bracket table below); modeled as continuous, clipped to [1,16], rounded to nearest integer bracket |
| education | high_school 26.29%, college_degree 59.40%, advanced_degree 14.31% | categorical, 3 levels |

**Income bracket table** (1-16):
1: <$9,999 · 2: $10,000-19,999 · 3: $20,000-29,999 · 4: $30,000-39,999 · 5: $40,000-49,999 · 6: $50,000-59,999 · 7: $60,000-69,999 · 8: $70,000-79,999 · 9: $80,000-89,999 · 10: $90,000-99,999 · 11: $100,000-109,999 · 12: $110,000-119,999 · 13: $120,000-129,999 · 14: $130,000-139,999 · 15: $140,000-149,999 · 16: $150,000+

**Known simplification:** 0.33% of the real population did not disclose income. Not modeled separately given its negligible expected count at typical test-run sample sizes -- flagged here rather than silently dropped.

## Individual behavioral differences

| Variable | Spec | Notes |
|---|---|---|
| financial_literacy | mean 2.36, SD 0.91, range 0-3 | 3-item Lusardi & Mitchell scale (interest compounding, inflation, diversification/idiosyncratic risk); count of correct answers, 0 = lowest, 3 = highest. Modeled as continuous, clipped [0,3], rounded to integer. |
| subjective_numeracy | mean 13.96, SD 3.12, range 3-18 | 3-item SNS-3 (McNaughton et al., 2015; self-assessed comfort with fractions/percentages and perceived usefulness of numeric info). Sum-score across three items. Modeled as continuous, clipped [3,18], rounded to integer. |

## Not yet specified

- Cross-correlations between any of the above variables (e.g. income vs. financial literacy) -- defaulting to independent sampling unless the researcher specifies otherwise.
- Total N and allocation across conditions -- pending.
