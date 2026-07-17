# Regression Results: choice

DV type: binary (logit)
Treatment indicator: treatment (1 = not 'condition_2')

## Without controls

Formula: `choice ~ treatment`

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 choice   No. Observations:                   20
Model:                          Logit   Df Residuals:                       18
Method:                           MLE   Df Model:                            1
Date:                Fri, 17 Jul 2026   Pseudo R-squ.:                  0.1282
Time:                        12:52:08   Log-Likelihood:                -11.734
converged:                       True   LL-Null:                       -13.460
Covariance Type:            nonrobust   LLR p-value:                   0.06317
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept     -0.4055      0.645     -0.628      0.530      -1.671       0.860
treatment      1.7918      1.021      1.756      0.079      -0.209       3.792
==============================================================================
```
