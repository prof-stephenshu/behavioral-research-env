# Regression Results: clarity_rating

DV type: continuous (OLS)
Treatment indicator: condition_2_indicator (1 = not 'condition_1')

## Without controls

Formula: `clarity_rating ~ condition_2_indicator`

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:         clarity_rating   R-squared:                       0.164
Model:                            OLS   Adj. R-squared:                  0.117
Method:                 Least Squares   F-statistic:                     3.522
Date:                Fri, 17 Jul 2026   Prob (F-statistic):             0.0769
Time:                        12:22:46   Log-Likelihood:                -20.613
No. Observations:                  20   AIC:                             45.23
Df Residuals:                      18   BIC:                             47.22
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
=========================================================================================
                            coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------------
Intercept                 5.8000      0.226     25.655      0.000       5.325       6.275
condition_2_indicator    -0.6000      0.320     -1.877      0.077      -1.272       0.072
==============================================================================
Omnibus:                        2.161   Durbin-Watson:                   1.196
Prob(Omnibus):                  0.339   Jarque-Bera (JB):                1.710
Skew:                          -0.577   Prob(JB):                        0.425
Kurtosis:                       2.151   Cond. No.                         2.62
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
