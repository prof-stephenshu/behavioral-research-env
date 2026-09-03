# Variables Specification: pilot-test-1

## Independent Variable

- **Name:** `condition`
- **Type:** Binary indicator
- **Values:**
  - `0` = Control ("Save $5 today.")
  - `1` = Treatment ("Save $5 today — for your family's future.")

## Primary Outcome Variable

- **Name:** `click_sign_up`
- **Type:** Binary (analyzed via logistic regression in Stage 5)
- **Options:** `["Not now", "Sign Up"]`
- **Coding:**
  - `0` = "Not now" (Did not click)
  - `1` = "Sign Up" (Clicked sign up)
  - Stage 5 positive label: `--positive-label "Sign Up"`
- **Description:** Whether the participant chooses to click the "Sign Up" button versus declining / choosing "Not now".

## Secondary Outcome Variables

*(None specified)*

## Controls / Covariates

*(None specified by researcher at intake. Candidate controls from population sampling, such as `age`, can be incorporated during Stage 5 regression if desired).*

