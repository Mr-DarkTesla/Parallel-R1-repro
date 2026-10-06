"""Markdown tables from benchmark results: one table per benchmark, one row per run.

Usage: python scripts/bench/table.py <results_root>   (results_root/<run>/<bench>.json from scripts/bench/score.py)
"""
import json
import os
import sys

root = sys.argv[1]
runs = sorted(os.listdir(root))
results = {run: {} for run in runs}
for run in runs:
    for name in os.listdir(f"{root}/{run}"):
        results[run].update(json.load(open(f"{root}/{run}/{name}")))

COLUMNS = ["accuracy", "accuracy_robust", "pass@16", "pass@4", "prompt_level_loose_acc", "inst_level_strict_acc", "with_parallel", "valid_tagged_responses",
           "no_final_answer", "truncated", "mean_chars"]
for source in ["AIME24", "AIME25", "AMC23", "MATH300", "LIMO", "ARC", "MMLUPRO", "IFEVAL"]:
    rows = {run: result[source] for run, result in results.items() if source in result}
    if not rows:
        continue
    columns = [c for c in COLUMNS if any(c in row for row in rows.values())]
    print(f"\n### {source}\n")
    print("| run | " + " | ".join(columns) + " |")
    print("|---" * (len(columns) + 1) + "|")
    for run, row in rows.items():
        print(f"| {run} | " + " | ".join("—" if row.get(c) is None else str(row[c]) for c in columns) + " |")
