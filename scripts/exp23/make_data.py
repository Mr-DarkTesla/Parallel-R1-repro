"""Exp 23 dev parquets: the exp-13 dev math rows (gsm8k_dev, math_dev) with the authors' parallel header replaced by header.txt.

Rows, ids, answers and sample order stay as in <eval_data>/dev/parallel, so outcomes pair row by row with earlier dev runs.
The same prompts go to dev/plain (plain generation, scripts/instruct4b_eval/run_eval.sh no-thinking | thinking) and dev/parallel (rollout).
Usage: python scripts/exp23/make_data.py <eval_data> <output_dir>   (eval_data: /work/bench_data/instruct4b/eval)
"""
import os
import sys

import pandas as pd

source, output = sys.argv[1], sys.argv[2]
header = open(os.path.join(os.path.dirname(__file__), "header.txt")).read()
for bench in ("gsm8k_dev", "math_dev"):
    frame = pd.read_parquet(f"{source}/dev/parallel/{bench}.parquet")
    contents = [p[0]["content"] for p in frame["prompt"]]
    assert all(c.startswith("Solve the following problem step by step.") for c in contents)  # header has no "Problem:"
    frame["prompt"] = [[{"role": "user", "content": header + "Problem:" + c.split("Problem:", 1)[1]}] for c in contents]
    for mode in ("plain", "parallel"):
        os.makedirs(f"{output}/dev/{mode}", exist_ok=True)
        frame.to_parquet(f"{output}/dev/{mode}/{bench}.parquet")
    print(bench, len(frame), "rows")
print(frame["prompt"].iloc[0][0]["content"])
