"""Compare two aligned masked holdout runs, preserving the 20/20 source mix.

Usage: python scripts/exp21/summarize_masked_holdout40.py RUN_ROOT OUT_JSON
The run root contains clean46/ and mixed401/ with *-block-rows.jsonl.
"""

import argparse
import json
import random
from pathlib import Path


SOURCES = ("gsm8k", "math")
ARMS = ("clean46", "mixed401")
COUNTS = {"gsm8k": 20, "math": 20}
FIELDS = ("problem_id", "problem", "source", "input", "sample")
METRICS = (
    "acc_robust", "think_wellformed", "think_has_parallel",
    "think_full_block", "think_numbered_block", "truncated",
    "tokens", "forward_passes",
)
BINARY = set(METRICS[:6])
REPEATS = 10_000


def read_rows(root, arm, source):
    path = root / arm / f"{source}-block-rows.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if len(rows) != COUNTS[source]:
        raise ValueError(f"{path}: {len(rows)} rows, expected {COUNTS[source]}")
    ids = [row["problem_id"] for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{path}: duplicate problem IDs")
    for row in rows:
        if not all(field in row for field in FIELDS + METRICS):
            raise ValueError(f"{path}: missing field in {row.get('problem_id')}")
        if row["decoder"] != "masked":
            raise ValueError(f"{path}: wrong decoder")
    return rows


def number(value, binary):
    if binary:
        if value not in (True, False, 0, 1):
            raise ValueError(f"expected boolean: {value!r}")
        return float(value)
    return float(value)


def summarize(rows, metric):
    values = [number(row[metric], metric in BINARY) for row in rows]
    mean = sum(values) / len(values)
    return round(mean * (100 if metric in BINARY else 1), 2)


def compare(rows_a, rows_b, metric, seed):
    delta = [number(b[metric], metric in BINARY) - number(a[metric], metric in BINARY)
             for a, b in zip(rows_a, rows_b)]
    rng = random.Random(seed)
    samples = []
    for _ in range(REPEATS):
        picked = [delta[rng.randrange(len(delta))] for _ in delta]
        samples.append(sum(picked) / len(picked))
    samples.sort()
    scale = 100 if metric in BINARY else 1
    return {
        "clean46": summarize(rows_a, metric),
        "mixed401": summarize(rows_b, metric),
        "mixed401_minus_clean46": round(scale * sum(delta) / len(delta), 2),
        "ci95": [round(scale * samples[int(REPEATS * q)], 2) for q in (0.025, 0.975)],
        "n": len(delta),
    }


def compare_stratified(by_source, metric, seed):
    parts = {
        source: [number(b[metric], metric in BINARY) - number(a[metric], metric in BINARY)
                 for a, b in zip(*by_source[source])]
        for source in SOURCES
    }
    rng = random.Random(seed)
    samples = []
    for _ in range(REPEATS):
        total = sum(sum(values[rng.randrange(len(values))] for _ in values)
                    for values in parts.values())
        samples.append(total / sum(len(v) for v in parts.values()))
    samples.sort()
    scale = 100 if metric in BINARY else 1
    a = [row for source in SOURCES for row in by_source[source][0]]
    b = [row for source in SOURCES for row in by_source[source][1]]
    return {
        "clean46": summarize(a, metric),
        "mixed401": summarize(b, metric),
        "mixed401_minus_clean46": round(scale * sum(sum(v) for v in parts.values()) / len(a), 2),
        "ci95": [round(scale * samples[int(REPEATS * q)], 2) for q in (0.025, 0.975)],
        "n": len(a),
        "bootstrap": "10k paired, stratified by source (20 GSM8K + 20 MATH)",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    if not (args.run_root / "EVAL_DONE").is_file():
        raise SystemExit("holdout evaluation is incomplete")
    by_source = {}
    for source in SOURCES:
        a, b = (read_rows(args.run_root, arm, source) for arm in ARMS)
        for left, right in zip(a, b):
            if any(left[field] != right[field] for field in FIELDS):
                raise ValueError(f"{source}: prompts or row order differ: {left['problem_id']}")
        by_source[source] = (a, b)
    result = {
        "protocol": "masked greedy thinking; GSM8K 2048 tokens, MATH 4096 tokens",
        "source_counts": COUNTS,
        "metric_notes": {
            "acc_robust": "correct final value from automatic scorer",
            "think_full_block": "syntactic block within <think>; semantic usefulness requires manual review",
            "forward_passes": "ideal parallel decoder forward passes; model_forward_calls are separate",
        },
        "overall": {metric: compare_stratified(by_source, metric, i) for i, metric in enumerate(METRICS)},
        "by_source": {source: {metric: compare(*by_source[source], metric, i)
                               for i, metric in enumerate(METRICS)} for source in SOURCES},
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result["overall"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
