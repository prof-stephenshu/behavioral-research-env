# Regression Results: affordability_rating

DV type: continuous (OLS)
Treatment indicator: treatment (1 = not 'condition_2')

## Without controls

Formula: `affordability_rating ~ treatment`

```
                             OLS Regression Results                             
================================================================================
Dep. Variable:     affordability_rating   R-squared:                       0.036
Model:                              OLS   Adj. R-squared:                  0.034
Method:                   Least Squares   F-statistic:                     14.97
Date:                  Fri, 17 Jul 2026   Prob (F-statistic):           0.000128
Time:                          13:19:28   Log-Likelihood:                -751.93
No. Observations:                   400   AIC:                             1508.
Df Residuals:                       398   BIC:                             1516.
Df Model:                             1                                         
Covariance Type:              nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      4.0450      0.112     35.991      0.000       3.824       4.266
treatment      0.6150      0.159      3.869      0.000       0.303       0.927
==============================================================================
Omnibus:                      175.553   Durbin-Watson:                   2.073
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               22.905
Skew:                          -0.109   Prob(JB):                     1.06e-05
Kurtosis:                       1.848   Cond. No.                         2.62
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

## With controls

Formula: `affordability_rating ~ treatment + gender`

```
                             OLS Regression Results                             
================================================================================
Dep. Variable:     affordability_rating   R-squared:                       0.041
Model:                              OLS   Adj. R-squared:                  0.036
Method:                   Least Squares   F-statistic:                     8.419
Date:                  Fri, 17 Jul 2026   Prob (F-statistic):           0.000262
Time:                          13:19:28   Log-Likelihood:                -751.00
No. Observations:                   400   AIC:                             1508.
Df Residuals:                       397   BIC:                             1520.
Df Model:                             2                                         
Covariance Type:              nonrobust                                         
==================================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------
Intercept          3.9170      0.147     26.693      0.000       3.628       4.205
gender[T.male]     0.2170      0.160      1.355      0.176      -0.098       0.532
treatment          0.6389      0.160      3.999      0.000       0.325       0.953
==============================================================================
Omnibus:                      169.279   Durbin-Watson:                   2.073
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               22.822
Skew:                          -0.119   Prob(JB):                     1.11e-05
Kurtosis:                       1.854   Cond. No.                         3.44
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
