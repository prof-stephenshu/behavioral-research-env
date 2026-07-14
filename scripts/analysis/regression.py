"""
Stage 5 primary regression analysis.

Fits OLS (continuous DV) or logit (binary DV) models of the outcome variable
on the treatment indicator, with and without controls, and optionally with
interactions (e.g. treatment x individual behavioral difference).

Usage:
    python regression.py --data subjects_data.csv --dv purchase_decision --dv-type binary \
        --condition-col condition --control-label control \
        --controls age income --interactions financial_literacy \
        --out regression_results.md
"""
import argparse
import sys

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def _clean_name(name):
    # patsy chokes on some raw column names; keep it simple by requiring
    # caller-supplied names to already be valid Python identifiers.
    return name


def build_formula(dv, treatment_var, controls, interactions):
    rhs_terms = [treatment_var]
    rhs_terms.extend(controls)
    for var in interactions:
        rhs_terms.append(f"{treatment_var}:{var}")
        if var not in controls:
            rhs_terms.append(var)
    rhs = " + ".join(dict.fromkeys(rhs_terms))  # de-dup, preserve order
    return f"{dv} ~ {rhs}"


def fit_model(df, formula, dv_type):
    if dv_type == "binary":
        model = smf.logit(formula, data=df).fit(disp=0)
    else:
        model = smf.ols(formula, data=df).fit()
    return model


def run_regression(df, dv, dv_type, treatment_var, controls, interactions):
    sections = []

    formula_no_controls = build_formula(dv, treatment_var, [], interactions)
    model_no_controls = fit_model(df, formula_no_controls, dv_type)
    sections.append(f"## Without controls\n\nFormula: `{formula_no_controls}`\n")
    sections.append("```\n" + model_no_controls.summary().as_text() + "\n```\n")

    if controls:
        formula_with_controls = build_formula(dv, treatment_var, controls, interactions)
        model_with_controls = fit_model(df, formula_with_controls, dv_type)
        sections.append(f"## With controls\n\nFormula: `{formula_with_controls}`\n")
        sections.append("```\n" + model_with_controls.summary().as_text() + "\n```\n")

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Primary regression analysis for Stage 5.")
    parser.add_argument("--data", required=True)
    parser.add_argument("--dv", required=True)
    parser.add_argument("--dv-type", choices=["binary", "continuous"], required=True)
    parser.add_argument("--condition-col", default="condition")
    parser.add_argument("--control-label", default="control", help="Value of condition-col treated as the reference/base case")
    parser.add_argument("--controls", nargs="*", default=[], help="Covariate column names to include as controls")
    parser.add_argument("--interactions", nargs="*", default=[], help="Column names to interact with the treatment indicator")
    parser.add_argument("--treatment-var", default="treatment", help="Name to give the generated 0/1 treatment indicator column")
    parser.add_argument("--positive-label", default=None, help="Which DV category to code as 1 (default: alphabetically last, reported to stdout)")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.data)

    if args.dv_type == "binary":
        # map the DV's string options to 0/1 if it isn't already numeric
        # (pandas may store text as legacy 'object' dtype or the newer 'str' dtype)
        if not pd.api.types.is_numeric_dtype(df[args.dv]):
            options = sorted(df[args.dv].dropna().unique())
            if len(options) != 2:
                raise ValueError(f"Binary DV '{args.dv}' has {len(options)} distinct values: {options}")
            positive = args.positive_label if args.positive_label is not None else options[-1]
            if positive not in options:
                raise ValueError(f"--positive-label '{positive}' not among observed values {options}")
            df[args.dv] = (df[args.dv] == positive).astype(int)
            other = options[0] if positive == options[-1] else options[-1]
            print(f"Coded {args.dv}: {positive} = 1, {other} = 0")

    df[args.treatment_var] = (df[args.condition_col] != args.control_label).astype(int)

    report = run_regression(df, args.dv, args.dv_type, args.treatment_var, args.controls, args.interactions)
    header = (
        f"# Regression Results: {args.dv}\n\n"
        f"DV type: {args.dv_type} ({'logit' if args.dv_type == 'binary' else 'OLS'})\n"
        f"Treatment indicator: {args.treatment_var} (1 = not '{args.control_label}')\n"
    )
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(header + "\n" + report)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    sys.exit(main())
