"""Metrics table from the validation dump of scripts/eval_qwen3_0.6b.sh, in the format of the authors' main table.

parallel_ratio: responses with <Parallel>. valid_responses: tagged responses whose tags all sit in correct blocks
(scripts/tag_validator.py, closed <Summary> included). correct_tag_share: correct tags / all tags.
no_final_answer: responses without "Final Answer:" (truncated or unparsable, scored as wrong).

Usage: python scripts/summarize_eval.py <generations.jsonl> <test.parquet>
"""
import json
import sys

import pandas as pd

from tag_validator import validate

generations_path, test_path = sys.argv[1], sys.argv[2]

generations = pd.read_json(generations_path, lines=True)
test = pd.read_parquet(test_path)
source_by_problem = {row.prompt[0]["content"].split("Problem:")[-1].strip(): row.data_source for row in test.itertuples()}
generations["source"] = generations["input"].map(
    lambda text: next(source for problem, source in source_by_problem.items() if problem in text)
)
generations["parallel"] = generations["output"].str.contains("<Parallel>")
generations[["tags", "correct_tags"]] = generations["output"].map(validate).tolist()
generations["valid"] = (generations["tags"] > 0) & (generations["tags"] == generations["correct_tags"])
generations["no_final_answer"] = ~generations["output"].str.contains("Final Answer:")
tagged = generations[generations["tags"] > 0]

per_prompt = generations.groupby(["source", "input"]).agg(mean=("acc", "mean"), passed=("acc", "max"), n=("acc", "size"))
assert per_prompt.groupby("source")["n"].nunique().eq(1).all(), "every prompt must have the same number of samples"
table = per_prompt.groupby("source").agg(mean_acc=("mean", "mean"), pass_at_n=("passed", "mean"), n=("n", "first"), prompts=("n", "size"))
by_source = generations.groupby("source")
table["parallel_ratio"] = by_source["parallel"].mean()
table["valid_responses"] = tagged.groupby("source")["valid"].mean()
table["correct_tag_share"] = by_source["correct_tags"].sum() / by_source["tags"].sum()
table["no_final_answer"] = by_source["no_final_answer"].mean()

summary = {
    "avg_mean_acc": table["mean_acc"].mean(),
    "parallel_ratio": generations["parallel"].mean(),
    "valid_responses": tagged["valid"].mean(),
    "correct_tag_share": generations["correct_tags"].sum() / generations["tags"].sum(),
    "no_final_answer": generations["no_final_answer"].mean(),
    "responses": len(generations),
}
print((table * [100, 100, 1, 1, 100, 100, 100, 100]).round(1).to_string())
print(json.dumps({key: round(float(value), 4) for key, value in summary.items()}))
