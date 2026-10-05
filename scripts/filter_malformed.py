"""exp06: drop SFT examples whose tags are not all in correct blocks (scripts/tag_validator.py); keep examples without tags.

Usage: python scripts/filter_malformed.py <train.parquet> <output.parquet>
"""
import sys

import pandas as pd

from tag_validator import validate

data = pd.read_parquet(sys.argv[1])
counts = [validate(info["answer"]) for info in data["extra_info"]]
keep = [tags == correct for tags, correct in counts]
print(f"kept {sum(keep)} of {len(data)}")
data[keep].to_parquet(sys.argv[2])
