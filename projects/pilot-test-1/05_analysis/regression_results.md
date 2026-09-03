# Regression Results: click_sign_up

DV type: binary (logit)
Treatment indicator: treatment (1 = not 'control')

## Without controls

Formula: `click_sign_up ~ treatment`

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:          click_sign_up   No. Observations:                   10
Model:                          Logit   Df Residuals:                        8
Method:                           MLE   Df Model:                            1
Date:                Thu, 03 Sep 2026   Pseudo R-squ.:                  0.1282
Time:                        16:10:31   Log-Likelihood:                -5.8671
converged:                       True   LL-Null:                       -6.7301
Covariance Type:            nonrobust   LLR p-value:                    0.1889
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept     -1.3863      1.118     -1.240      0.215      -3.578       0.805
treatment      1.7918      1.443      1.241      0.214      -1.037       4.621
==============================================================================
```
