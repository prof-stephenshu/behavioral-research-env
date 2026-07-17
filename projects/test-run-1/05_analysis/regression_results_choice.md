# Regression Results: choice

DV type: binary (logit)
Treatment indicator: condition_2_indicator (1 = not 'condition_1')

## Without controls

Formula: `choice ~ condition_2_indicator`

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 choice   No. Observations:                   20
Model:                          Logit   Df Residuals:                       18
Method:                           MLE   Df Model:                            1
Date:                Fri, 17 Jul 2026   Pseudo R-squ.:                  0.1282
Time:                        12:22:31   Log-Likelihood:                -11.734
converged:                       True   LL-Null:                       -13.460
Covariance Type:            nonrobust   LLR p-value:                   0.06317
=========================================================================================
                            coef    std err          z      P>|z|      [0.025      0.975]
-----------------------------------------------------------------------------------------
Intercept                 1.3863      0.791      1.754      0.080      -0.163       2.936
condition_2_indicator    -1.7918      1.021     -1.756      0.079      -3.792       0.209
=========================================================================================
```
