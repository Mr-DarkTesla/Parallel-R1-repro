"""Exp 23 thinking check: the first sample of the first N problems of each exp-23 dev parquet (thinking at 16k is slow on the full set).
Usage: python scripts/exp23/make_subset.py <exp23 data dir> <output dir> <N>
"""
import os
import sys

import pandas as pd

source, output, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
for bench in ("gsm8k_dev", "math_dev"):
    frame = pd.read_parquet(f"{source}/dev/plain/{bench}.parquet")
    ids = frame["extra_info"].map(lambda info: info["id"])
    first = frame[~ids.duplicated()].iloc[:n].reset_index(drop=True)  # score.py aligns by position
    os.makedirs(f"{output}/dev/plain", exist_ok=True)
    first.to_parquet(f"{output}/dev/plain/{bench}.parquet")
    print(bench, len(first), "rows")
