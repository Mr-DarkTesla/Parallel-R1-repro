"""Markdown report per benchmark: accuracy (robust), decode steps and answer length (mean / median / p95), total decode steps.

Usage: python scripts/bench/report.py <results_root>   (results_root/<run>/<bench>.json and results_root/<run>/lengths/<bench>.json)
"""
import json
import os
import sys

root = sys.argv[1]
runs = sorted(name for name in os.listdir(root) if os.path.isdir(f"{root}/{name}"))


def merged(path):
    out = {}
    for name in (f for f in os.listdir(path) if f.endswith(".json")) if os.path.isdir(path) else []:
        out.update(json.load(open(f"{path}/{name}")))
    return out


scores = {run: merged(f"{root}/{run}") for run in runs}
lengths = {run: merged(f"{root}/{run}/lengths") for run in runs}
for source in ["AIME24", "AIME25", "AMC23", "MATH300", "LIMO", "ARC", "MMLUPRO", "IFEVAL"]:
    rows = [run for run in runs if source in lengths[run]]
    if not rows:
        continue
    print(f"\n### {source}\n")
    print("| run | accuracy | decode steps mean / median / p95 | length mean / median / p95 | decode steps total |")
    print("|---|---|---|---|---|")
    for run in rows:
        score = scores[run].get(source, {})
        accuracy = score.get("accuracy_robust", score.get("accuracy"))
        steps, length = lengths[run][source]["decode_steps"], lengths[run][source]["length_tokens"]
        print(f"| {run} | {accuracy} | {steps['mean']:.0f} / {steps['median']:.0f} / {steps['p95']:.0f} | "
              f"{length['mean']:.0f} / {length['median']:.0f} / {length['p95']:.0f} | {lengths[run][source]['decode_steps_total']} |")
