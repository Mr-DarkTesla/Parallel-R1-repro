"""Paired bootstrap for Multiverse blocks inside Qwen3 thinking responses.

Usage: python compare_thinking_blocks.py BASE_ROWS CAND_ROWS OUT_JSON
Rows must have identical tasks, sample numbers and rendered prompts.
"""
import json
import sys

import numpy as np


RATES = ("acc_robust", "think_wellformed", "think_has_parallel", "think_full_block",
         "think_numbered_block", "truncated")
NUMERIC = ("tokens", "forward_passes")


def read(path):
    with open(path) as file:
        return [json.loads(line) for line in file]


def main():
    base, cand = read(sys.argv[1]), read(sys.argv[2])
    assert len(base) == len(cand) and base
    for i, (b, c) in enumerate(zip(base, cand)):
        for key in ("source", "problem_id", "problem", "input", "sample"):
            assert b[key] == c[key], (i, key)
    ids = list(dict.fromkeys(row["problem_id"] for row in base))
    grouped = {key: [] for key in (*RATES, *NUMERIC)}
    for problem_id in ids:
        b = [row for row in base if row["problem_id"] == problem_id]
        c = [row for row in cand if row["problem_id"] == problem_id]
        assert len(b) == len(c) and [r["sample"] for r in b] == [r["sample"] for r in c]
        for key in grouped:
            grouped[key].append((sum(float(row[key]) for row in b) / len(b),
                                 sum(float(row[key]) for row in c) / len(c)))
    rng = np.random.default_rng(0)
    result = {"problems": len(ids), "responses": len(base), "metrics": {}}
    for key, values in grouped.items():
        pair = np.asarray(values)
        delta = pair[:, 1] - pair[:, 0]
        samples = np.concatenate([delta[ix].mean(1) for ix in np.array_split(
            rng.integers(0, len(ids), size=(10000, len(ids))), 20)])
        mult = 100 if key in RATES else 1
        result["metrics"][key] = {
            "base": round(mult * pair[:, 0].mean(), 2),
            "cand": round(mult * pair[:, 1].mean(), 2),
            "delta": round(mult * delta.mean(), 2),
            "ci95": [round(mult * x, 2) for x in np.percentile(samples, [2.5, 97.5])],
        }
    with open(sys.argv[3], "w") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
