"""
Stage 5 randomization balance check.

For each independent variable sampled in Stage 4 (demographics + individual
behavioral differences), reports descriptive stats by condition and tests
whether assignment to condition looks balanced:
  - categorical variables: chi-squared test of independence vs. condition
  - continuous variables (means): one-way F-test (ANOVA) across conditions
  - continuous variables (variance): Bartlett's test across conditions

Usage:
    python balance_check.py --data subjects_data.csv --population-config population_config.json \
        --condition-col condition --control-label control --out balance_report.md
"""
import argparse
import json
import sys

import pandas as pd
from scipy import stats


def _categorical_balance(df, var, condition_col):
    table = pd.crosstab(df[condition_col], df[var])
    chi2, p, dof, _ = stats.chi2_contingency(table)
    pct_by_condition = (
        df.groupby(condition_col)[var]
        .value_counts(normalize=True)
        .unstack(fill_value=0)
        .round(3)
    )
    return chi2, p, pct_by_condition


def _continuous_balance(df, var, condition_col):
    groups = [g[var].dropna().values for _, g in df.groupby(condition_col)]
    f_stat, f_p = stats.f_oneway(*groups)
    bart_stat, bart_p = stats.bartlett(*groups)
    desc = df.groupby(condition_col)[var].agg(["mean", "std", "count"]).round(3)
    return f_stat, f_p, bart_stat, bart_p, desc


def run_balance_check(df, variables, condition_col):
    lines = []
    n_total = len(df)
    counts = df[condition_col].value_counts()
    lines.append("# Randomization Balance Report\n")
    lines.append(f"Total observations: {n_total}\n")
    lines.append("Condition counts:\n")
    for cond, n in counts.items():
        lines.append(f"- {cond}: {n}")
    lines.append("")

    for var in variables:
        name = var["name"]
        if name not in df.columns:
            continue
        lines.append(f"## {name} ({var['kind']})\n")
        if var["kind"] == "categorical":
            chi2, p, pct = _categorical_balance(df, name, condition_col)
            lines.append("Proportion by condition:\n")
            lines.append(pct.to_markdown())
            lines.append(f"\nChi-squared = {chi2:.3f}, p = {p:.4f}")
            if p < 0.05:
                lines.append("**Imbalance flagged (p < .05).**")
        else:
            f_stat, f_p, bart_stat, bart_p, desc = _continuous_balance(df, name, condition_col)
            lines.append("Descriptive stats by condition:\n")
            lines.append(desc.to_markdown())
            lines.append(f"\nF-statistic (means) = {f_stat:.3f}, p = {f_p:.4f}")
            lines.append(f"Bartlett's statistic (variances) = {bart_stat:.3f}, p = {bart_p:.4f}")
            if f_p < 0.05 or bart_p < 0.05:
                lines.append("**Imbalance flagged (p < .05 on mean and/or variance).**")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Randomization balance check for Stage 5.")
    parser.add_argument("--data", required=True, help="Path to subjects_data.csv")
    parser.add_argument("--population-config", required=True, help="Path to population_config.json")
    parser.add_argument("--condition-col", default="condition")
    parser.add_argument("--out", required=True, help="Path to write balance_report.md")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    with open(args.population_config, "r", encoding="utf-8") as f:
        config = json.load(f)
    variables = config.get("variables", [])

    report = run_balance_check(df, variables, args.condition_col)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    sys.exit(main())
