"""
Stage 5 chart generation (v1 scope: outcome-by-condition bar chart only).

Usage:
    python charts.py --data subjects_data.csv --dv purchase_decision --dv-type binary \
        --condition-col condition --out charts/purchase_decision_by_condition.png
"""
import argparse
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BAR_COLOR = "#4C72B0"
ERROR_COLOR = "#333333"


def bar_chart_by_condition(df, dv, condition_col, dv_type, title=None, positive_label=None):
    if dv_type == "binary" and not pd.api.types.is_numeric_dtype(df[dv]):
        options = sorted(df[dv].dropna().unique())
        positive = positive_label if positive_label is not None else options[-1]
        df = df.copy()
        df[dv] = (df[dv] == positive).astype(int)

    grouped = df.groupby(condition_col)[dv].agg(["mean", "sem", "count"])
    grouped = grouped.sort_index()

    fig, ax = plt.subplots(figsize=(6, 4.5))
    x = range(len(grouped))
    ax.bar(x, grouped["mean"], yerr=grouped["sem"], capsize=6, color=BAR_COLOR,
           ecolor=ERROR_COLOR, error_kw={"elinewidth": 1.5})
    ax.set_xticks(list(x))
    ax.set_xticklabels(grouped.index, fontsize=11)
    ax.set_ylabel(dv.replace("_", " "), fontsize=11)
    ax.set_title(title or f"{dv.replace('_', ' ')} by condition", fontsize=13)
    for i, (mean, n) in enumerate(zip(grouped["mean"], grouped["count"])):
        ax.annotate(f"n={n}", (i, 0), textcoords="offset points", xytext=(0, -22),
                    ha="center", fontsize=9, color="#666666")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig, grouped


def main():
    parser = argparse.ArgumentParser(description="Outcome-by-condition bar chart for Stage 5.")
    parser.add_argument("--data", required=True)
    parser.add_argument("--dv", required=True)
    parser.add_argument("--dv-type", choices=["binary", "continuous"], required=True)
    parser.add_argument("--condition-col", default="condition")
    parser.add_argument("--title", default=None)
    parser.add_argument("--positive-label", default=None, help="Which DV category to treat as 1/success for a binary DV (default: alphabetically last)")
    parser.add_argument("--out", required=True, help="Path to write the PNG chart")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    fig, grouped = bar_chart_by_condition(
        df, args.dv, args.condition_col, args.dv_type, title=args.title, positive_label=args.positive_label
    )
    fig.savefig(args.out, dpi=150)
    print(f"Wrote {args.out}")
    print(grouped.to_string())


if __name__ == "__main__":
    sys.exit(main())
