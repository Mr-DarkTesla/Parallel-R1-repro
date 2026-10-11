"""Build a balanced pilot from independently screened question-only plans."""

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
DATA = ROOT / "data"
QUOTAS = {("math", "integer"): 6, ("math", "expression"): 6,
          ("math", "fraction"): 4, ("gsm8k", "integer"): 16}
REJECTED_IN_REVIEW = {"math-train/3110"}


def read_rows(path):
    rows = [json.loads(line) for line in path.open() if line.strip()]
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate IDs in {path}")
    return rows


def main():
    candidates = read_rows(DATA / "onpolicy46_candidates.jsonl")
    proposals = (read_rows(DATA / "onpolicy46_decomp_math_proposals.jsonl") +
                 read_rows(DATA / "onpolicy46_decomp_gsm_proposals.jsonl"))
    plans = {row["id"]: row for row in proposals}
    if len(plans) != len(proposals):
        raise ValueError("duplicate ID across plan files")
    selected, counts = [], defaultdict(int)
    for row in candidates:
        key = row["source"], row["answer_type"]
        if row["id"] in plans and row["id"] not in REJECTED_IN_REVIEW and counts[key] < QUOTAS.get(key, 0):
            selected.append(row)
            counts[key] += 1
    if dict(counts) != QUOTAS:
        raise ValueError(f"pilot quotas unmet: {dict(counts)}")
    candidate_out = DATA / "onpolicy46_decomp_pilot_candidates.jsonl"
    plan_out = DATA / "onpolicy46_decomp_pilot_plans.jsonl"
    for path, rows in ((candidate_out, selected),
                       (plan_out, [{field: plans[row["id"]][field]
                                    for field in ("id", "subgoal1", "subgoal2", "combine")}
                                   for row in selected])):
        with path.open("x") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"selected": len(selected), "counts": {str(k): v for k, v in counts.items()},
                      "ids": [row["id"] for row in selected]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
