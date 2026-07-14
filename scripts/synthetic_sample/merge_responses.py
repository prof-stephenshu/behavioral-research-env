"""
Stage 4 subagent-mode response merger.

Takes the sampled subject frame and a combined JSON file of subject responses
(the orchestrating skill concatenates the JSON array each subagent batch
returned into one list, one object per subject_id, each with the DV field(s)
and "reasoning") and merges them into the final subjects_data.csv, flagging
any subject_id from the frame that has no matching response.

Usage:
    python merge_responses.py --frame subjects_frame.csv --responses raw_responses.json --out subjects_data.csv
"""
import argparse
import json
import sys

import pandas as pd


def merge_responses(frame, responses):
    responses_df = pd.DataFrame(responses)
    if "subject_id" not in responses_df.columns:
        raise ValueError("Each response object must include a 'subject_id' field")

    dupes = responses_df["subject_id"][responses_df["subject_id"].duplicated()].unique()
    if len(dupes):
        raise ValueError(f"Duplicate subject_id(s) in responses: {list(dupes)}")

    merged = frame.merge(responses_df, on="subject_id", how="left", indicator=True)
    merged["_error"] = merged["_merge"].apply(lambda m: "" if m == "both" else "no response collected")
    merged = merged.drop(columns=["_merge"])
    return merged


def main():
    parser = argparse.ArgumentParser(description="Merge subagent batch responses into subjects_data.csv for Stage 5.")
    parser.add_argument("--frame", required=True, help="Path to subjects_frame.csv from sample_population.py")
    parser.add_argument("--responses", required=True, help="Path to a JSON list of {subject_id, <dv fields>, reasoning}")
    parser.add_argument("--out", required=True, help="Path to write subjects_data.csv")
    args = parser.parse_args()

    frame = pd.read_csv(args.frame)
    with open(args.responses, "r", encoding="utf-8") as f:
        responses = json.load(f)

    merged = merge_responses(frame, responses)
    merged.to_csv(args.out, index=False)

    n_missing = (merged["_error"] != "").sum()
    print(f"Wrote {len(merged)} rows -> {args.out}")
    if n_missing:
        print(f"WARNING: {n_missing} subjects have no matching response (see _error column).")
        missing_ids = merged.loc[merged["_error"] != "", "subject_id"].tolist()
        print(f"Missing subject_ids: {missing_ids}")


if __name__ == "__main__":
    sys.exit(main())
