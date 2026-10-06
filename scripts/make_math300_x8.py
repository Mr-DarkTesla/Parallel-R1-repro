"""MATH300 from the authors' test set repeated 8 times: a lower-noise accuracy check (mean@8) next to the authors' MATH300 mean@1.

Usage (from verl/): python ../scripts/make_math300_x8.py <output.parquet>
"""
import sys

import pandas as pd

test = pd.read_parquet("data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet")
math300 = test[test["data_source"] == "APO_MATH300"]
math300.loc[math300.index.repeat(8)].reset_index(drop=True).to_parquet(sys.argv[1])
