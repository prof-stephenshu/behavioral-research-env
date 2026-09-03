# Analysis Summary: pilot-test-1

## 1. Randomization Balance Check
Assignment between conditions was well-balanced across the sampled demographic covariate:
- **Age:**
  - Control ($n=5$): $M = 33.20$ ($SD = 11.39$)
  - Treatment ($n=5$): $M = 30.60$ ($SD = 6.54$)
  - Difference in means: $F(1, 8) = 0.196, p = 0.670$
  - Difference in variances: Bartlett's $\chi^2(1) = 1.041, p = 0.308$

No demographic imbalance was detected ($p > .05$).

## 2. Primary Regression Analysis
A binary logistic regression was fit modeling `click_sign_up` (1 = "Sign Up", 0 = "Not now") on the binary treatment indicator:
$$\text{logit}(P(\text{click\_sign\_up} = 1)) = -1.386 + 1.792 \times \text{treatment}$$

- **Treatment Effect:** $B = 1.7918$ ($SE = 1.443$, $z = 1.241$, $p = 0.214$)
- **Odds Ratio:** $\text{OR} = e^{1.7918} \approx 6.00$
- **Interpretation:** The treatment condition ("Save $5 today — for your family's future") showed a strong positive directional increase in sign-up uptake (60% vs. 20%). In this pilot sample ($N = 10$), the effect did not reach conventional statistical significance ($p = 0.214$).

## 3. Visualization
- **Chart:** [`charts/click_sign_up_by_condition.png`](file:///C:/Users/sds77/behavioral-research-env/projects/pilot-test-1/05_analysis/charts/click_sign_up_by_condition.png)
  - **Control:** 20% conversion rate ($SE = 20.0\%$, $n = 5$)
  - **Treatment:** 60% conversion rate ($SE = 24.5\%$, $n = 5$)

