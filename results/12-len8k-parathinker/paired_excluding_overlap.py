"""scripts/paired_compare.py with eval problems from a JSON list removed identically from both runs
(the 6 problems with confirmed train/eval overlap in exp12 data, results/12-len8k-parathinker/excluded_eval_problems.json).

Usage (on the pod, from verl/): python ../results/12-len8k-parathinker/paired_excluding_overlap.py <excluded.json> /work/runs/<a> /work/runs/<b>
"""
import json
import sys

import numpy as np
import pandas as pd

TESTS = {
    "apo": "data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet",
    "limo": "data_preprocess_scripts/data/limo/test.parquet",
    "math300_x8": "data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/math300_x8.parquet",
}


def per_problem(run):
    """Mean accuracy per problem, indexed by (benchmark, problem text) — same as paired_compare.py."""
    rows = []
    for test, path in TESTS.items():
        generations = pd.read_json(f"{run}/eval_{test}/generations/0.jsonl", lines=True)
        source_by_problem = {row.prompt[0]["content"].split("Problem:")[-1].strip(): row.data_source for row in pd.read_parquet(path).itertuples()}
        problem = generations["input"].map(lambda text: next(p for p in source_by_problem if p in text))
        rows.append(generations.assign(source=problem.map(source_by_problem).str.removeprefix("APO_"), problem=problem))
    return pd.concat(rows).groupby(["source", "problem"])["acc"].mean()


def interval(values, rng):
    boot = rng.choice(values, size=(10000, len(values))).mean(axis=1)
    return {"diff": round(values.mean(), 2), "ci95": [round(np.percentile(boot, 2.5), 2), round(np.percentile(boot, 97.5), 2)], "problems": len(values)}


def norm(text):
    return " ".join(text.split())


excluded = json.load(open(sys.argv[1]))
a, b = per_problem(sys.argv[2]), per_problem(sys.argv[3])
assert a.index.sort_values().equals(b.index.sort_values()), "both runs must be evaluated on the same problems"
drop = []
for item in excluded:
    source = item["source"].removeprefix("APO_")
    hits = [key for key in b.index if key[0] == source and norm(key[1]) == norm(item["question"])]
    assert len(hits) == 1, (item["question"][:80], hits)
    drop += hits
b = b.drop(drop)
difference = (b - a.reindex(b.index)) * 100
rng = np.random.default_rng(0)
result = {source: interval(values.to_numpy(), rng) for source, values in difference.groupby(level="source")}
result["all"] = interval(difference.to_numpy(), rng)
result["excluded"] = [list(key[:1]) + [key[1][:60]] for key in drop]
print(json.dumps(result))
