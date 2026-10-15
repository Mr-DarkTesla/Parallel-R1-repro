"""Exp 23: paired comparison of two run_eval.sh runs on the same dev rows (any prompts / modes), with the reasons of a drop.

Rows are matched by problem_id and sample (score.py rows/<bench>.jsonl). Per problem the mean over its samples, then the mean
difference over problems; 95% interval from 10,000 bootstrap resamples of problems (seed 0), as in instruct4b_eval/paired_compare.py.
Metrics (%): acc_robust; no_final_answer; truncated (plain generation only); acc_robust among rows with a final answer (not paired);
parallel (<Parallel> in the answer); loops = rows with more than 20 <Parallel> in the text (dump needed, see --dump).
Usage: python scripts/exp23/compare.py <base run> <cand run> [bench ...]
"""
import json
import os
import sys

import numpy as np
import pandas as pd


def load(run, bench):
    rows = pd.read_json(f"{run}/rows/{bench}.jsonl", lines=True).set_index(["problem_id", "sample"]).sort_index()
    for dump in (f"{run}/{bench}.jsonl", f"{run}/{bench}/generations/0.jsonl"):
        if os.path.exists(dump):
            text = pd.read_json(dump, lines=True)["output"]
            order = pd.read_json(f"{run}/rows/{bench}.jsonl", lines=True).set_index(["problem_id", "sample"]).index
            rows["loops"] = pd.Series((text.str.count("<Parallel>") > 20).to_numpy(), index=order)
    return rows


def paired(base, cand, column, rng):
    diff = (cand[column].astype(float) - base[column].astype(float)).groupby(level=0).mean().to_numpy()
    boot = diff[rng.integers(0, len(diff), (10_000, len(diff)))].mean(1)
    return round(100 * diff.mean(), 2), [round(100 * q, 2) for q in np.quantile(boot, [0.025, 0.975])]


base_run, cand_run, *benches = sys.argv[1:]
for bench in benches or ("gsm8k_dev", "math_dev"):
    if not all(os.path.exists(f"{r}/rows/{bench}.jsonl") for r in (base_run, cand_run)):
        continue
    base, cand = load(base_run, bench), load(cand_run, bench)
    assert base.index.equals(cand.index), "different rows"
    out = {"base": os.path.basename(base_run), "cand": os.path.basename(cand_run), "bench": bench, "rows": len(base),
           "problems": base.index.get_level_values(0).nunique()}
    for column in ("acc_robust", "no_final_answer", "truncated", "parallel", "loops"):
        if column in base and column in cand and base[column].notna().all() and cand[column].notna().all():
            out[column] = {"base": round(100 * base[column].mean(), 2), "cand": round(100 * cand[column].mean(), 2),
                           "delta_ci95": paired(base, cand, column, np.random.default_rng(0))}
    answered = lambda r: round(100 * r.loc[~r["no_final_answer"].astype(bool), "acc_robust"].mean(), 2)  # noqa: E731
    out["acc_robust_if_answered"] = {"base": answered(base), "cand": answered(cand)}
    print(json.dumps(out))
