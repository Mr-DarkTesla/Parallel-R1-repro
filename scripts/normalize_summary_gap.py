"""exp05: write "</Parallel>\n<Summary>" exactly as the authors' rollout inserts it, instead of the 4 different gaps in the SFT data.

Usage: python scripts/normalize_summary_gap.py <train.parquet> <output.parquet>
"""
import re
import sys

import pandas as pd

data = pd.read_parquet(sys.argv[1])
data["extra_info"] = [
    {**info, "answer": re.sub(r"</Parallel>\s*<Summary>", "</Parallel>\n<Summary>", info["answer"])} for info in data["extra_info"]
]
data.to_parquet(sys.argv[2])
