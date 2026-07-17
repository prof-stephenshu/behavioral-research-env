# Regression Results: clarity_rating

DV type: continuous (OLS)
Treatment indicator: treatment (1 = not 'condition_2')

## Without controls

Formula: `clarity_rating ~ treatment`

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:         clarity_rating   R-squared:                       0.000
Model:                            OLS   Adj. R-squared:                 -0.002
Method:                 Least Squares   F-statistic:                    0.1370
Date:                Fri, 17 Jul 2026   Prob (F-statistic):              0.712
Time:                        13:19:31   Log-Likelihood:                -544.25
No. Observations:                 400   AIC:                             1093.
Df Residuals:                     398   BIC:                             1100.
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      5.3100      0.067     79.404      0.000       5.179       5.441
treatment      0.0350      0.095      0.370      0.712      -0.151       0.221
==============================================================================
Omnibus:                       25.831   Durbin-Watson:                   2.112
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               29.208
Skew:                          -0.656   Prob(JB):                     4.54e-07
Kurtosis:                       3.171   Cond. No.                         2.62
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

## With controls

Formula: `clarity_rating ~ treatment + gender`

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:         clarity_rating   R-squared:                       0.000
Model:                            OLS   Adj. R-squared:                 -0.005
Method:                 Least Squares   F-statistic:                   0.07790
Date:                Fri, 17 Jul 2026   Prob (F-statistic):              0.925
Time:                        13:19:31   Log-Likelihood:                -544.24
No. Observations:                 400   AIC:                             1094.
Df Residuals:                     397   BIC:                             1106.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
==================================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------
Intercept          5.3022      0.088     60.589      0.000       5.130       5.474
gender[T.male]     0.0132      0.096      0.138      0.890      -0.175       0.201
treatment          0.0365      0.095      0.383      0.702      -0.151       0.224
==============================================================================
Omnibus:                       25.686   Durbin-Watson:                   2.111
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               29.028
Skew:                          -0.655   Prob(JB):                     4.97e-07
Kurtosis:                       3.166   Cond. No.                         3.44
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
