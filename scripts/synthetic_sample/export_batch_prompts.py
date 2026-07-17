"""
Utility: explode batches.json into one plain-text file per batch (real
newlines, not JSON-escaped), so each batch's prompt can be read directly
and handed to the Agent tool without manual re-typing.

Usage:
    python export_batch_prompts.py --batches batches.json --out-dir batch_prompts/
"""
import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batches", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    with open(args.batches, "r", encoding="utf-8") as f:
        batches = json.load(f)

    os.makedirs(args.out_dir, exist_ok=True)
    for batch in batches:
        path = os.path.join(args.out_dir, f"{batch['batch_id']}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(batch["prompt"])

    print(f"Wrote {len(batches)} prompt files -> {args.out_dir}")


if __name__ == "__main__":
    sys.exit(main())
