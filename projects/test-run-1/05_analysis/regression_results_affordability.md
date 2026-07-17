# Regression Results: affordability_rating

DV type: continuous (OLS)
Treatment indicator: condition_2_indicator (1 = not 'condition_1')

## Without controls

Formula: `affordability_rating ~ condition_2_indicator`

```
                             OLS Regression Results                             
================================================================================
Dep. Variable:     affordability_rating   R-squared:                       0.163
Model:                              OLS   Adj. R-squared:                  0.117
Method:                   Least Squares   F-statistic:                     3.513
Date:                  Fri, 17 Jul 2026   Prob (F-statistic):             0.0772
Time:                          12:22:43   Log-Likelihood:                -36.103
No. Observations:                    20   AIC:                             76.21
Df Residuals:                        18   BIC:                             78.20
Df Model:                             1                                         
Covariance Type:              nonrobust                                         
=========================================================================================
                            coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------------
Intercept                 5.4000      0.490     11.010      0.000       4.370       6.430
condition_2_indicator    -1.3000      0.694     -1.874      0.077      -2.757       0.157
==============================================================================
Omnibus:                        3.216   Durbin-Watson:                   2.039
Prob(Omnibus):                  0.200   Jarque-Bera (JB):                1.402
Skew:                          -0.235   Prob(JB):                        0.496
Kurtosis:                       1.791   Cond. No.                         2.62
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
