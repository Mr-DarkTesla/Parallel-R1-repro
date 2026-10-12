"""Compare completed masked full benchmarks with archived ordinary thinking.

Usage: python summarize_full_parallel_pair.py RUN_ROOT OUT_JSON
Each new question has one greedy masked answer. Archived ordinary answers
can have repeats; their per-question mean is the paired reference.
"""

import json
import sys
import tarfile
from collections import defaultdict
from pathlib import Path

import numpy as np


BASE = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
DEV = ("gsm8k_dev", "math_dev", "arc_dev", "mmlu_pro_dev")
FROZEN = ("apo", "arc", "mmlu_pro", "limo", "ifeval")
FIELDS = ("acc", "acc_robust", "tokens", "forward_passes", "truncated")
RATES = {"acc", "acc_robust", "truncated"}


def rows(path):
    with open(path) as file:
        return [json.loads(line) for line in file]


def archived(model, stage, bench):
    if stage == "dev" or bench == "ifeval":
        suffix = "dev" if stage == "dev" else "frozen"
        name = f"qwen4b-{model}-{suffix}-thinking"
        path = BASE / "full_dev" / f"{name}.tgz"
        with tarfile.open(path) as archive:
            text = archive.extractfile(f"{name}/rows/{bench}.jsonl").read().decode()
            return [json.loads(line) for line in text.splitlines()]
    if model != "selected":
        return None
    path = BASE / "eval_archives/qwen4b_clean46_frozen/thinking" / bench / "rows" / f"{bench}.jsonl"
    return rows(path)


def key(row):
    return row["source"], row["problem_id"]


def grouped_reference(reference):
    groups = defaultdict(list)
    for row in reference:
        groups[key(row)].append(row)
    return groups


def interval(deltas, rate):
    vector = np.asarray(deltas, dtype=float)
    rng = np.random.default_rng(21)
    draws = []
    for _ in range(40):
        index = rng.integers(0, len(vector), size=(250, len(vector)))
        draws.extend(vector[index].mean(axis=1))
    scale = 100 if rate else 1
    return [round(float(x * scale), 2) for x in np.quantile(draws, [0.025, 0.975])]


def summarize(new, reference):
    assert new and len({key(row) for row in new}) == len(new)
    old = grouped_reference(reference)
    assert set(old) == {key(row) for row in new}, (len(old), len(new), set(old) ^ {key(row) for row in new})
    result = {"questions": len(new), "archived_responses": len(reference), "masked": {}, "ordinary": {}, "paired_delta": {}}
    for field in FIELDS:
        fresh = [float(row[field]) for row in new]
        previous = [sum(float(x[field]) for x in old[key(row)]) / len(old[key(row)]) for row in new]
        scale = 100 if field in RATES else 1
        result["masked"][field] = round(scale * sum(fresh) / len(fresh), 2)
        result["ordinary"][field] = round(scale * sum(previous) / len(previous), 2)
        deltas = [a - b for a, b in zip(fresh, previous)]
        result["paired_delta"][field] = {
            "estimate": round(scale * sum(deltas) / len(deltas), 2),
            "ci95": interval(deltas, field in RATES),
        }
    for field in ("think_full_block", "think_numbered_block", "think_has_parallel", "think_wellformed"):
        result["masked"][field] = round(100 * sum(bool(row[field]) for row in new) / len(new), 2)
    result["masked"]["full_blocks"] = sum(bool(row["think_full_block"]) for row in new)
    result["masked"]["numbered_blocks"] = sum(bool(row["think_numbered_block"]) for row in new)
    return result


def main():
    root, output = map(Path, sys.argv[1:3])
    report = {
        "protocol": "One greedy masked answer versus archived ordinary sampled answer means on identical question IDs; prompts and decoder differ, so deltas are descriptive",
        "confidence_interval": "10,000 paired bootstrap replicates by question, seed 21",
        "benchmarks": {},
    }
    for stage, benches in (("dev", DEV), ("frozen", FROZEN)):
        for bench in benches:
            folder = root / "output" / stage / "parallel" / bench
            if not (folder / "DONE").exists():
                continue
            fresh = rows(folder / "block_rows.jsonl")
            strict = rows(folder / "score_rows.jsonl")
            assert len(fresh) == len(strict)
            for block, score in zip(fresh, strict):
                assert key(block) == key(score)
                block["acc"] = bool(score["acc"])
            report["benchmarks"][f"{stage}/{bench}"] = {}
            sources = sorted({row["source"] for row in fresh})
            for source in sources:
                subset = [row for row in fresh if row["source"] == source]
                for model in ("selected", "base"):
                    old = archived(model, stage, bench)
                    if old is None:
                        continue
                    reference = [row for row in old if row["source"] == source]
                    report["benchmarks"][f"{stage}/{bench}"].setdefault(source, {})[model] = summarize(subset, reference)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(output)
    for bench, sources in report["benchmarks"].items():
        for source, models in sources.items():
            selected = models["selected"]
            print(bench, source, selected["questions"], selected["masked"]["acc_robust"],
                  selected["masked"]["think_full_block"], selected["masked"]["tokens"],
                  selected["masked"]["forward_passes"])


if __name__ == "__main__":
    main()
