"""Rank unused correct Qwen answers for plan-only M2 conversion.

Reads only leak-checked train questions and saved Qwen generations. One sample
per task keeps the first planning pass diverse; no eval result is consulted.
Usage: python prepare_more_m2_new_inputs.py POOL GRADED PRIOR_PLANS OLD_M1 OLD_M2
       M1_MORE M2_MORE OUT
"""
import collections
import json
import re
import sys
from pathlib import Path

from m2_convert import split_units


CUE = re.compile(r"\b(?:separately|independently|first case|second case|part 1|part 2|for each)\b", re.I)
GROUPS = ("gsm8k/integer", "math/integer", "math/fraction", "math/expression")
WEIGHTS = (29, 17, 34, 20)  # approximate the new M1 source/answer-type mix


def read(path):
    return (json.loads(line) for line in open(path))


def main():
    pool_path, graded_path, prior_path, m1_path, m2_path, more_m1_path, more_m2_path, output = sys.argv[1:9]
    pool = {r["id"]: r for r in read(pool_path)}
    old = {r["id"] for path in (m1_path, m2_path, more_m2_path) for r in read(path)}
    new_m1 = {r["id"] for r in read(more_m1_path)}
    attempted = {(r["id"], r["sample"]) for r in read(prior_path)}
    attempted_ids = {key for key, _ in attempted}
    choices = collections.defaultdict(list)
    counts = collections.Counter()
    for row in read(graded_path):
        key = row["id"]
        if key not in pool or key in old or not row["correct"] or (key, row["sample"]) in attempted:
            continue
        problem = pool[key]
        group = f"{problem['source']}/{problem['answer_type']}"
        if group not in GROUPS or row["tokens"] > 2048:
            continue
        text = row["output"]
        units = len(split_units(text)[0])
        if units < 4 or len(text) < 250:
            continue
        # Rank by readily separable prose, moderate length, prior task status.
        score = (key not in new_m1, key in attempted_ids, not bool(CUE.search(text)),
                 abs(units - 9), abs(row["tokens"] - 350), row["sample"])
        choices[key].append((score, row))
        counts["eligible_samples"] += 1
    grouped = {name: [] for name in GROUPS}
    for key, candidates in choices.items():
        score, row = min(candidates, key=lambda x: x[0])
        problem = pool[key]
        group = f"{problem['source']}/{problem['answer_type']}"
        grouped[group].append((score, {"id": key, "sample": row["sample"],
                               "question": problem["question"], "answer": problem["answer"],
                               "source": problem["source"], "answer_type": problem["answer_type"],
                               "output": row["output"]}))
    for name in GROUPS:
        grouped[name].sort(key=lambda x: (x[0], x[1]["id"]))
    # Smooth weighted round robin; always use available groups.
    selected = []
    next_index = {name: 0 for name in GROUPS}
    while any(next_index[g] < len(grouped[g]) for g in GROUPS):
        n = len(selected) + 1
        available = [g for g in GROUPS if next_index[g] < len(grouped[g])]
        group = max(available, key=lambda g: WEIGHTS[GROUPS.index(g)] * n / 100 - next_index[g])
        selected.append(grouped[group][next_index[group]][1])
        next_index[group] += 1
    assert len(selected) == len({r["id"] for r in selected})
    out = Path(output)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in selected))
    stats = {"eligible_samples": counts["eligible_samples"], "unique_tasks": len(selected),
             "by_group": {g: len(grouped[g]) for g in GROUPS},
             "first_100": dict(collections.Counter(f"{r['source']}/{r['answer_type']}" for r in selected[:100])),
             "first_100_overlap_new_m1": sum(r["id"] in new_m1 for r in selected[:100])}
    out.with_name(out.stem + "_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()
