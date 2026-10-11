#!/usr/bin/env python3
"""Summarize completed Qwen4B fixed40 archives with paired intervals."""
import json
import math
import re
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse"
ARCHIVES = ROOT / "eval_archives"
AUDIT = ROOT / "audit"
PATTERN = re.compile(r"qwen4b_sol61_(tagged|plain)_step(4|8|16)$")
METRICS = ("strict", "robust", "block", "truncated", "tokens", "forward_passes")


def read(path):
    return [json.loads(line) for line in path.read_text().split("\n") if line]


def key(row):
    return row["source"], row["problem_id"], row["sample"]


def load(directory):
    if not (directory / "DONE").is_file():
        raise ValueError(f"unfinished archive: {directory}")
    scores = [row for name in ("gsm8k_dev10", "gsm8k_devnext10", "math_dev10", "math_devnext10")
              for row in read(directory / f"{name}-rows.jsonl")]
    blocks = [row for name in ("gsm8k_dev10", "gsm8k_devnext10", "math_dev10", "math_devnext10")
              for row in read(directory / f"{name}-block-rows.jsonl")]
    assert len(scores) == len(blocks) == 40
    by_block = {key(row): row for row in blocks}
    assert len(by_block) == 40
    merged = {}
    for row in scores:
        k = key(row)
        assert k not in merged and k in by_block and row["input"] == by_block[k]["input"]
        block = by_block[k]
        merged[k] = {"input": row["input"], "strict": bool(row["acc"]),
                     "robust": bool(row["acc_robust"]),
                     "block": bool(block["think_numbered_block"]),
                     "truncated": bool(row["truncated"]),
                     "tokens": int(row["tokens"]),
                     "forward_passes": int(row["forward_passes"])}
    return merged


def interval(base, cand, keys, metric):
    values = np.array([cand[k][metric] - base[k][metric] for k in keys], dtype=float)
    samples = values[np.random.default_rng(0).integers(0, len(values), size=(10_000, len(values)))].mean(axis=1)
    scale = 1 if metric in ("tokens", "forward_passes") else 100
    out = {"delta": round(float(scale * values.mean()), 2),
           "ci95": [round(float(scale * q), 2) for q in np.percentile(samples, [2.5, 97.5])]}
    if metric in ("strict", "robust"):
        lost = sum(base[k][metric] and not cand[k][metric] for k in keys)
        gained = sum(cand[k][metric] and not base[k][metric] for k in keys)
        n = lost + gained
        out["discordant"] = {"lost": lost, "gained": gained}
        out["mcnemar_exact_p"] = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(lost, gained) + 1)) / 2**n) if n else 1.0
    return out


def main():
    base = load(ARCHIVES / "qwen4b_init_fixed40")
    runs = {}
    for directory in ARCHIVES.iterdir():
        match = PATTERN.fullmatch(directory.name)
        if match and (directory / "DONE").exists():
            runs[f"{match[1]}_step{match[2]}"] = load(directory)
    assert runs
    keys = sorted(base)
    result = {"baseline": "qwen4b_init_fixed40", "n": 40,
              "protocol": "same fixed40 prompts, thinking, masked greedy, same token budgets",
              "runs": {}, "pairwise": {}}
    for name, rows in sorted(runs.items()):
        assert sorted(rows) == keys and all(rows[k]["input"] == base[k]["input"] for k in keys)
        result["runs"][name] = {
            "metrics": {metric: round(float(np.mean([rows[k][metric] for k in keys]) *
                                            (1 if metric in ("tokens", "forward_passes") else 40)), 2)
                        for metric in METRICS},
            "vs_initial": {metric: interval(base, rows, keys, metric) for metric in METRICS},
        }
    result["baseline_metrics"] = {
        metric: round(float(np.mean([base[k][metric] for k in keys]) *
                            (1 if metric in ("tokens", "forward_passes") else 40)), 2)
        for metric in METRICS}
    for step in (4, 8, 16):
        tagged, plain = (runs.get(f"{arm}_step{step}") for arm in ("tagged", "plain"))
        if tagged and plain:
            result["pairwise"][f"step{step}"] = {
                metric: interval(plain, tagged, keys, metric) for metric in METRICS}
    (AUDIT / "qwen4b_sol61_sweep_auto.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for name, row in result["runs"].items():
        print(name, row["metrics"], row["vs_initial"]["robust"])


if __name__ == "__main__":
    main()
