# Randomization Balance Report

Total observations: 400

Condition counts:

- condition_1: 200
- condition_2: 200

## age (continuous)

Descriptive stats by condition:

| condition   |   mean |   std |   count |
|:------------|-------:|------:|--------:|
| condition_1 | 34.2   | 6.946 |     200 |
| condition_2 | 34.447 | 7.146 |     200 |

F-statistic (means) = 0.123, p = 0.7263
Bartlett's statistic (variances) = 0.160, p = 0.6895

## gender (categorical)

Proportion by condition:

| condition   |   female |   male |
|:------------|---------:|-------:|
| condition_1 |     0.52 |   0.48 |
| condition_2 |     0.41 |   0.59 |

Chi-squared = 4.432, p = 0.0353
**Imbalance flagged (p < .05).**

## income_bracket (continuous)

Descriptive stats by condition:

| condition   |   mean |   std |   count |
|:------------|-------:|------:|--------:|
| condition_1 |   5.1  | 2.879 |     200 |
| condition_2 |   5.61 | 2.948 |     200 |

F-statistic (means) = 3.063, p = 0.0809
Bartlett's statistic (variances) = 0.110, p = 0.7400

## education (categorical)

Proportion by condition:

| condition   |   advanced_degree |   college_degree |   high_school |
|:------------|------------------:|-----------------:|--------------:|
| condition_1 |             0.145 |             0.55 |         0.305 |
| condition_2 |             0.145 |             0.61 |         0.245 |

Chi-squared = 1.930, p = 0.3810

## financial_literacy (continuous)

Descriptive stats by condition:

| condition   |   mean |   std |   count |
|:------------|-------:|------:|--------:|
| condition_1 |  2.245 | 0.76  |     200 |
| condition_2 |  2.275 | 0.802 |     200 |

F-statistic (means) = 0.147, p = 0.7012
Bartlett's statistic (variances) = 0.559, p = 0.4546

## subjective_numeracy (continuous)

Descriptive stats by condition:

| condition   |   mean |   std |   count |
|:------------|-------:|------:|--------:|
| condition_1 | 14.015 | 2.889 |     200 |
| condition_2 | 13.885 | 2.866 |     200 |

F-statistic (means) = 0.204, p = 0.6517
Bartlett's statistic (variances) = 0.013, p = 0.9095
