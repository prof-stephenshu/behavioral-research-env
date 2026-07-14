"""
Stage 4 synthetic sampler.

Reads a population_config.json (produced by the /synthetic-ab-test skill from
Stage 3's population_spec.md plus any refinements the researcher gave) and draws
N synthetic subject profiles, randomly assigned between-subject to conditions.

Continuous variables are drawn jointly via a Gaussian copula so that any
specified pairwise correlations (e.g. income <-> financial_literacy) are
respected; categorical variables are drawn independently per their given
category probabilities. This script only handles sampling of subject
profiles + condition assignment -- it does not call any LLM and does not
know about stimuli or outcome variables (that's run_subjects.py).

Usage:
    python sample_population.py --config population_config.json --out subjects_frame.csv [--seed 42]

Config schema (population_config.json):
{
  "conditions": ["control", "treatment"],
  "n_total": 300,
  "allocation": "equal" | {"control": 150, "treatment": 150},
  "variables": [
    {"name": "age", "kind": "continuous", "role": "demographic",
     "mean": 42, "sd": 12, "min": 18, "max": 85},
    {"name": "gender", "kind": "categorical", "role": "demographic",
     "categories": ["female", "male", "nonbinary"], "probabilities": [0.51, 0.47, 0.02]},
    {"name": "financial_literacy", "kind": "continuous", "role": "individual_difference",
     "mean": 0, "sd": 1}
  ],
  "correlations": [
    {"var1": "income", "var2": "financial_literacy", "rho": 0.3}
  ]
}
"""
import argparse
import json
import sys

import numpy as np
import pandas as pd


def _build_correlation_matrix(continuous_names, correlations):
    n = len(continuous_names)
    idx = {name: i for i, name in enumerate(continuous_names)}
    corr = np.eye(n)
    for pair in correlations or []:
        v1, v2, rho = pair["var1"], pair["var2"], pair["rho"]
        if v1 not in idx or v2 not in idx:
            # correlation referencing a categorical or unknown variable is skipped;
            # copula correlation here only applies to continuous variables
            continue
        i, j = idx[v1], idx[v2]
        corr[i, j] = rho
        corr[j, i] = rho
    # guard against a non-positive-semidefinite matrix from inconsistent pairwise rhos
    eigvals = np.linalg.eigvalsh(corr)
    if eigvals.min() < -1e-8:
        raise ValueError(
            "Specified correlations are not jointly consistent (correlation matrix "
            "is not positive semidefinite). Reduce the number/strength of correlated pairs."
        )
    return corr


def _sample_continuous_block(n_total, variables, correlations, rng):
    names = [v["name"] for v in variables]
    if not names:
        return pd.DataFrame(index=range(n_total))
    corr = _build_correlation_matrix(names, correlations)
    z = rng.multivariate_normal(mean=np.zeros(len(names)), cov=corr, size=n_total)
    out = {}
    for i, v in enumerate(variables):
        mean = v.get("mean", 0.0)
        sd = v.get("sd", 1.0)
        col = mean + sd * z[:, i]
        if "min" in v:
            col = np.maximum(col, v["min"])
        if "max" in v:
            col = np.minimum(col, v["max"])
        out[v["name"]] = col
    return pd.DataFrame(out)


def _sample_categorical_block(n_total, variables, rng):
    out = {}
    for v in variables:
        cats = v["categories"]
        probs = v.get("probabilities")
        if probs is not None:
            probs = np.array(probs, dtype=float)
            probs = probs / probs.sum()
        out[v["name"]] = rng.choice(cats, size=n_total, p=probs)
    return pd.DataFrame(out)


def _assign_conditions(n_total, conditions, allocation, rng):
    if allocation == "equal":
        base = n_total // len(conditions)
        remainder = n_total - base * len(conditions)
        counts = {c: base for c in conditions}
        # distribute any remainder to the first few conditions
        for c in conditions[:remainder]:
            counts[c] += 1
    else:
        counts = dict(allocation)
        if sum(counts.values()) != n_total:
            raise ValueError(
                f"allocation counts {counts} sum to {sum(counts.values())}, "
                f"expected n_total={n_total}"
            )
    labels = np.concatenate([[c] * counts[c] for c in conditions])
    rng.shuffle(labels)
    return labels


def sample_population(config, seed=None):
    rng = np.random.default_rng(seed)

    n_total = config["n_total"]
    conditions = config["conditions"]
    allocation = config.get("allocation", "equal")
    variables = config.get("variables", [])
    correlations = config.get("correlations", [])

    continuous_vars = [v for v in variables if v["kind"] == "continuous"]
    categorical_vars = [v for v in variables if v["kind"] == "categorical"]

    cont_df = _sample_continuous_block(n_total, continuous_vars, correlations, rng)
    cat_df = _sample_categorical_block(n_total, categorical_vars, rng)

    frame = pd.concat([cont_df, cat_df], axis=1)
    frame.insert(0, "subject_id", [f"S{str(i+1).zfill(5)}" for i in range(n_total)])
    frame["condition"] = _assign_conditions(n_total, conditions, allocation, rng)

    return frame


def main():
    parser = argparse.ArgumentParser(description="Sample synthetic subject population for Stage 4.")
    parser.add_argument("--config", required=True, help="Path to population_config.json")
    parser.add_argument("--out", required=True, help="Path to write subjects_frame.csv")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    frame = sample_population(config, seed=args.seed)
    frame.to_csv(args.out, index=False)

    counts = frame["condition"].value_counts().to_dict()
    print(f"Sampled {len(frame)} subjects -> {args.out}")
    print(f"Condition counts: {counts}")


if __name__ == "__main__":
    sys.exit(main())
