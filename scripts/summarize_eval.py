"""Metrics table from the validation dump of scripts/eval_qwen3_0.6b.sh, in the format of the authors' main table.

Usage: python scripts/summarize_eval.py <generations.jsonl> <test.parquet>
"""
import json
import sys

import pandas as pd

from tag_validator import validate
from verl.utils.reward_score.math_dapo_acc_parallel_interved import check_parallel_thinking_format

generations_path, test_path = sys.argv[1], sys.argv[2]

generations = pd.read_json(generations_path, lines=True)
test = pd.read_parquet(test_path)
source_by_problem = {row.prompt[0]["content"].split("Problem:")[-1].strip(): row.data_source for row in test.itertuples()}
generations["source"] = generations["input"].map(
    lambda text: next(source for problem, source in source_by_problem.items() if problem in text)
)
generations["parallel"] = generations["output"].str.contains("<Parallel>")
generations["valid_format"] = generations["output"].map(lambda text: not check_parallel_thinking_format(text))
generations[["tags", "correct_tags"]] = generations["output"].map(validate).tolist()
parallel = generations[generations["parallel"]]

per_prompt = generations.groupby(["source", "input"]).agg(mean=("acc", "mean"), passed=("acc", "max"), n=("acc", "size"))
table = per_prompt.groupby("source").agg(mean_acc=("mean", "mean"), pass_at_n=("passed", "mean"), n=("n", "first"), prompts=("n", "size"))
table["parallel_ratio"] = generations.groupby("source")["parallel"].mean()
table["valid_format_of_parallel"] = parallel.groupby("source")["valid_format"].mean()
table["correct_tag_share"] = generations.groupby("source")["correct_tags"].sum() / generations.groupby("source")["tags"].sum()

summary = {
    "avg_mean_acc": table["mean_acc"].mean(),
    "parallel_ratio": generations["parallel"].mean(),
    "valid_format_of_parallel": parallel["valid_format"].mean(),
    "correct_tag_share": generations["correct_tags"].sum() / generations["tags"].sum(),
    "responses": len(generations),
}
print((table * [100, 100, 1, 1, 100, 100, 100]).round(1).to_string())
print(json.dumps({key: round(float(value), 4) for key, value in summary.items()}))
