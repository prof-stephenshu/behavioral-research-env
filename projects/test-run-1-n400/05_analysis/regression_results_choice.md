# Regression Results: choice

DV type: binary (logit)
Treatment indicator: treatment (1 = not 'condition_2')

## Without controls

Formula: `choice ~ treatment`

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 choice   No. Observations:                  400
Model:                          Logit   Df Residuals:                      398
Method:                           MLE   Df Model:                            1
Date:                Fri, 17 Jul 2026   Pseudo R-squ.:                 0.02667
Time:                        13:19:12   Log-Likelihood:                -267.92
converged:                       True   LL-Null:                       -275.26
Covariance Type:            nonrobust   LLR p-value:                 0.0001274
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept     -0.1805      0.142     -1.271      0.204      -0.459       0.098
treatment      0.7776      0.205      3.794      0.000       0.376       1.179
==============================================================================
```

## With controls

Formula: `choice ~ treatment + gender`

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 choice   No. Observations:                  400
Model:                          Logit   Df Residuals:                      397
Method:                           MLE   Df Model:                            2
Date:                Fri, 17 Jul 2026   Pseudo R-squ.:                 0.03091
Time:                        13:19:12   Log-Likelihood:                -266.75
converged:                       True   LL-Null:                       -275.26
Covariance Type:            nonrobust   LLR p-value:                 0.0002017
==================================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
----------------------------------------------------------------------------------
Intercept         -0.3687      0.189     -1.950      0.051      -0.739       0.002
gender[T.male]     0.3169      0.208      1.525      0.127      -0.090       0.724
treatment          0.8174      0.208      3.937      0.000       0.410       1.224
==================================================================================
```
