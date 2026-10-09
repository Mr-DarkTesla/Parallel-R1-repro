"""Select plain dev rows matching a saved Multiverse pilot, in pilot order.

Usage: python select_plain_pilot.py FULL_PLAIN_PARQUET MV_SCORE_ROWS_JSONL OUT_PARQUET
"""
import json
import sys

import pandas as pd

from make_mv_prompts import mv_prompt


if __name__ == "__main__":
    full = pd.read_parquet(sys.argv[1])
    pilot = [json.loads(line) for line in open(sys.argv[2])]
    first = {}
    for _, row in full.iterrows():
        first.setdefault(row["extra_info"]["id"], row)
    assert len(pilot) == len({r["problem_id"] for r in pilot})
    selected = []
    for record in pilot:
        row = first[record["problem_id"]]
        assert mv_prompt(row["prompt"][0]["content"]) == record["problem"]
        selected.append(row)
    pd.DataFrame(selected).reset_index(drop=True).to_parquet(sys.argv[3])
    print(f"matched plain pilot: {len(selected)} unique tasks")
