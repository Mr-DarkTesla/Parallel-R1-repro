"""Paired comparison of evaluation runs on the same problems (exp 13): candidate(s) minus base, per benchmark and slice.

Inputs are run directories of scripts/instruct4b_eval/run_eval.sh (meta.json, rows/<bench>.jsonl from score.py).
Checks before any number: same protocol (suite, mode, budget, sampling, generator, prompt parquets, IFEval scorer seed; a run
without the seed, i.e. unseeded scoring, only matches another unseeded run), the same benchmarks (at least one), and per benchmark
the same rows in the same order: source, problem id, problem text, rendered chat prompt and sample index; equal samples per problem
within a source. Candidate run names must differ. Runs marked unversioned_test_only (run_eval.sh CPU tests) only with
EVAL_ALLOW_UNVERSIONED=1. Anything else is an error.
Statistics: per problem the mean over its samples, then the difference of means over problems; 95% interval from 10,000 bootstrap
resamples of unique problems (seed 0), all samples of a problem stay together. Ratio metrics (IFEval instruction level) resample
numerator and denominator per problem together.
Several --cand runs = training seeds: each seed is compared separately; "seeds_pooled" averages the seeds per problem first and is
conditional on these seeds (between-seed variance is not in its interval; the per-seed deltas show the spread).
Benchmarks with several sources (AIME24/25, AMC23, MATH300 in one parquet) are also compared per source, every metric, and printed
per source: a per-benchmark tolerance applies to each source; the problem-weighted blend (MATH300 316 of 416 APO problems) is descriptive.
Printed label against the proposed 2 pp tolerance (a working proposal, not confirmed by the user): CI lower bound >= -2 "within",
CI upper bound < -2 "below", otherwise "inconclusive" (expected for AIME/AMC with 30-40 problems).
Slices (report, not gates), primary metric: --meta-dir with meta/<suite>/<bench>.jsonl from make_eval_data.py gives MMLU-Pro category
and MATH type/level (a compared benchmark without its file is an error); IFEval instruction groups (instruction-level strict) come
from the rows.

--cross-prompt compares a no-thinking run (plain prompts) with a parallel or Multiverse run (the corresponding prompt directory),
on the benchmarks both runs have: same source, problem id and sample per row; the inserted paragraph is checked exactly and the
problem text after the first "Problem:" must be equal.
Budget and sampling are equal only nominally (the rollout has its own length limits and no seed).

Usage: python scripts/instruct4b_eval/paired_compare.py --base <run> --cand <run> [--cand <run2>] [--meta-dir <dir>] [--cross-prompt] --out <out.json>
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from exp21.make_mv_prompts import FIRST_LINE, MV_PARAGRAPH  # noqa: E402

PROTOCOL = ("suite", "mode", "budget", "temperature", "top_p", "generator", "prompts", "ifeval_scorer_seed")
SLICES = ("category", "type", "level")
CROSS_PROMPTS = {"no-thinking": "plain", "parallel": "parallel", "multiverse": "multiverse",
                 "multiverse-branch": "multiverse"}
MARGIN = 2.0  # proposed tolerance in pp (not confirmed by the user), only a printed label
BOOTSTRAP, SEED = 10_000, 0


def load(run):
    meta = json.load(open(f"{run}/meta.json"))
    rows = {f[:-6]: pd.read_json(f"{run}/rows/{f}", lines=True) for f in sorted(os.listdir(f"{run}/rows")) if f.endswith(".jsonl")}
    return meta, rows


def header_and_problems(rows, where):
    """'<header>Problem: <problem>' split at the first 'Problem:' -> the run's one header, the problems."""
    parts = rows["problem"].str.split("Problem:", n=1, expand=True)
    if parts.shape[1] != 2 or parts[1].isna().any() or parts[0].nunique() != 1:
        raise ValueError(f"{where}: problems are not '<one header>Problem: <problem>'")
    return parts[0].iloc[0], parts[1].to_numpy()


def check_cross_prompt(base, cand, where, base_mode):
    (base_header, base_problems), (cand_header, cand_problems) = header_and_problems(base, where), header_and_problems(cand, where)
    plain, special = (base_header, cand_header) if base_mode == "no-thinking" else (cand_header, base_header)
    if "Within each parallel block:" in special:
        matches = plain.startswith(FIRST_LINE) and special == FIRST_LINE + MV_PARAGRAPH + plain[len(FIRST_LINE):]
    else:
        start, end = special.find("During the reasoning process"), special.find("End your response")
        matches = 0 < start < end and special[:start] + special[end:] == plain
    if not matches:
        raise ValueError(f"{where}: headers are not matching plain and structured versions")
    bad = np.flatnonzero(base_problems != cand_problems)
    if len(bad):
        raise ValueError(f"{where}: problem text differs in {len(bad)} rows, first row {bad[0]}")


def check_aligned(base, cand, where, cross_mode=None):
    """cross_mode: base mode of a --cross-prompt comparison (the problem text is compared without the header)."""
    if len(base) != len(cand):
        raise ValueError(f"{where}: {len(base)} rows vs {len(cand)}")
    if cross_mode:
        check_cross_prompt(base, cand, where, cross_mode)
    for column in ("source", "problem_id", "sample") + (() if cross_mode else ("problem", "input")):
        bad = np.flatnonzero(base[column].to_numpy() != cand[column].to_numpy())
        if len(bad):
            raise ValueError(f"{where}: {column} differs in {len(bad)} rows, first row {bad[0]}")
    counts = base.groupby(["source", "problem_id"]).size()
    uneven = counts.groupby(level="source").nunique() > 1  # the protocol repeats every problem of a source the same number of times
    if uneven.any():
        raise ValueError(f"{where}: unequal samples per problem in {list(uneven.index[uneven])}: {counts.value_counts().to_dict()}")


def per_problem(rows, metric, group=None):
    """(numerator, denominator) per problem, means over the problem's samples, indexed by problem id."""
    if metric.startswith("inst_level"):
        pairs = [(sum(ok for ok, i in zip(oks, ids) if group in (None, i.split(":")[0])),
                  sum(group in (None, i.split(":")[0]) for i in ids)) for oks, ids in zip(rows[metric], rows["instruction_id_list"])]
        frame = pd.DataFrame(pairs, columns=["num", "den"], index=rows.index)
    else:
        frame = pd.DataFrame({"num": rows[metric].astype(float), "den": 1.0})
    frame = frame.groupby(rows["problem_id"]).mean()
    return frame[frame["den"] > 0]


def bootstrap(base, cand):
    """base, cand: per-problem (num, den) on the same problems. Point delta, 95% interval, discordant problems."""
    assert base.index.equals(cand.index)
    b, c = base.to_numpy(), cand.to_numpy()
    idx = np.random.default_rng(SEED).integers(0, len(b), size=(BOOTSTRAP, len(b)))
    rate = lambda x, i: x[i, 0].sum(-1) / x[i, 1].sum(-1)  # noqa: E731
    deltas = np.concatenate([rate(c, chunk) - rate(b, chunk) for chunk in np.array_split(idx, 20)])
    point = c[:, 0].sum() / c[:, 1].sum() - b[:, 0].sum() / b[:, 1].sum()
    return {"base": round(100 * b[:, 0].sum() / b[:, 1].sum(), 2), "cand": round(100 * c[:, 0].sum() / c[:, 1].sum(), 2),
            "delta": round(100 * point, 2), "ci95": [round(100 * q, 2) for q in np.percentile(deltas, [2.5, 97.5])],
            "problems": len(b), "discordant_problems": round(100 * np.mean(b[:, 0] / b[:, 1] != c[:, 0] / c[:, 1]), 1)}


def bootstrap_mean(base, cand):
    """Paired interval in native units for response length and sequential forward passes."""
    assert base.index.equals(cand.index)
    b, c = base["num"].to_numpy(), cand["num"].to_numpy()
    delta = c - b
    rng = np.random.default_rng(SEED)
    means = np.concatenate([delta[ids].mean(axis=1) for ids in np.array_split(
        rng.integers(0, len(delta), size=(BOOTSTRAP, len(delta))), 20)])
    return {"base": round(float(b.mean()), 2), "cand": round(float(c.mean()), 2),
            "delta": round(float(delta.mean()), 2), "ci95": [round(float(q), 2) for q in np.percentile(means, [2.5, 97.5])],
            "problems": len(delta)}


def compare(base, named, meta):
    """base rows, {run name: candidate rows} (one per training seed), optional meta rows -> results for every metric and slice."""
    cands = list(named.values())
    metrics = [m for m in ("acc_robust", "acc", "prompt_level_loose_acc", "inst_level_strict_acc", "truncated", "parallel",
                           "valid_tags", "mv_valid", "mv_numbered", "no_final_answer")
               if m in base and base[m].notna().all() and all(c[m].notna().all() for c in cands)]
    numeric = [m for m in ("chars", "tokens", "forward_passes")
               if m in base and base[m].notna().all() and all(m in c and c[m].notna().all() for c in cands)]
    pooled = cands[0].copy()
    for m in metrics:
        if not m.startswith("inst_level"):
            pooled[m] = np.mean([c[m].astype(float) for c in cands], axis=0)  # per row mean over seeds, rows are aligned
    if "inst_level_strict_acc" in metrics:
        pooled["inst_level_strict_acc"] = [list(np.mean(v, axis=0)) for v in zip(*[c["inst_level_strict_acc"] for c in cands])]
    runs = named | ({"seeds_pooled": pooled} if len(cands) > 1 else {})
    counts = base.groupby(["source", "problem_id"]).size().groupby(level="source").first()
    out = {"samples_per_problem": {s: int(n) for s, n in counts.items()}, "metrics": {}, "by_source": {}, "slices": {}}
    for name, cand in runs.items():
        out["metrics"][name] = {m: bootstrap(per_problem(base, m), per_problem(cand, m)) for m in metrics}
    out["numeric_metrics"] = {name: {m: bootstrap_mean(per_problem(base, m), per_problem(cand, m)) for m in numeric}
                              for name, cand in runs.items()}
    if len(counts) > 1:  # e.g. the authors' math set: AIME24, AIME25, AMC23, MATH300 are separate benchmarks
        for source in counts.index:
            b = base[base["source"] == source]
            out["by_source"][source] = {name: {m: bootstrap(per_problem(b, m), per_problem(c[base["source"] == source], m)) for m in metrics}
                                        for name, c in runs.items()}
    if "tokens" in base and base["tokens"].notna().all():
        out["mean_tokens"] = {"base": round(base["tokens"].mean(), 1), **{n: round(c["tokens"].mean(), 1) for n, c in runs.items()}}
    primary = "acc_robust" if "acc_robust" in metrics else "acc"
    if meta is not None:
        by_problem = meta.groupby("problem_id").first()
        for key in [k for k in SLICES if k in meta]:
            for value in sorted(set(by_problem[key]) - {""}):
                ids = by_problem.index[by_problem[key] == value]
                out["slices"][f"{key}={value}"] = {n: bootstrap(per_problem(base, primary).loc[ids], per_problem(c, primary).loc[ids])
                                                   for n, c in runs.items()}
    if "instruction_id_list" in base:
        for group in sorted({i.split(":")[0] for ids in base["instruction_id_list"] for i in ids}):
            out["slices"][f"ifeval_group={group}"] = {n: bootstrap(per_problem(base, "inst_level_strict_acc", group),
                                                                   per_problem(c, "inst_level_strict_acc", group)) for n, c in runs.items()}
    out["primary"] = "acc_robust" if primary == "acc_robust" else "acc (IFEval: prompt-level strict)"
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--cand", required=True, action="append")
    parser.add_argument("--meta-dir")
    parser.add_argument("--cross-prompt", action="store_true", help="no-thinking (plain prompts) vs parallel (parallel prompts) only")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    base_meta, base_rows = load(args.base)
    cands = [load(run) for run in args.cand]
    names = [os.path.basename(run.rstrip("/")) for run in args.cand]
    if len(set(names)) != len(names) or "seeds_pooled" in names:
        raise ValueError(f"candidate run names must differ (one result per name): {names}")
    for run, meta in [(args.base, base_meta), *zip(args.cand, [m for m, _ in cands])]:
        if meta.get("unversioned_test_only") and os.environ.get("EVAL_ALLOW_UNVERSIONED") != "1":
            raise ValueError(f"{run}: unversioned test-only run (meta.json commit null)")
    for run, (meta, rows) in zip(args.cand, cands):
        if args.cross_prompt:
            pair = {base_meta.get("mode"): str(base_meta.get("prompts")), meta.get("mode"): str(meta.get("prompts"))}
            if (set(pair) not in ({"no-thinking", "parallel"}, {"no-thinking", "multiverse"},
                                  {"no-thinking", "multiverse-branch"})
                    or any(os.path.basename(p) != CROSS_PROMPTS[m] for m, p in pair.items())
                    or len({os.path.dirname(p) for p in pair.values()}) != 1):
                raise ValueError(f"{run}: --cross-prompt needs one no-thinking run on <data>/plain and one structured run: "
                                 f"{base_meta.get('mode'), base_meta.get('prompts')} vs {meta.get('mode'), meta.get('prompts')}")
        keys = [k for k in PROTOCOL if not (args.cross_prompt and k in ("mode", "prompts", "generator"))]
        differs = {k: (base_meta.get(k), meta.get(k)) for k in keys if base_meta.get(k) != meta.get(k)}
        if differs:
            raise ValueError(f"{run}: protocol differs {differs}")
        if set(rows) != set(base_rows) and not args.cross_prompt:  # parallel runs have the math benchmarks only
            raise ValueError(f"{run}: benchmarks {sorted(rows)} vs base {sorted(base_rows)}")
    report = {"base": args.base, "cands": args.cand, "protocol": {k: base_meta.get(k) for k in PROTOCOL}, "cross_prompt": args.cross_prompt,
              "proposed_margin_pp": MARGIN, "margin_note": "working proposal, not confirmed by the user; applies per benchmark/source",
              "benchmarks": {}}
    common = sorted(set(base_rows).intersection(*[set(rows) for _, rows in cands]))
    if not common:
        raise ValueError(f"no common benchmarks: base {sorted(base_rows)}, cands {[sorted(rows) for _, rows in cands]}")
    report["not_compared"] = sorted(set(base_rows).union(*[set(rows) for _, rows in cands]) - set(common))
    for bench in common:
        base = base_rows[bench]
        for run, (_, rows) in zip(args.cand, cands):
            check_aligned(base, rows[bench], f"{run} {bench}", base_meta.get("mode") if args.cross_prompt else None)
        meta = None
        if args.meta_dir:  # an explicit meta dir must have every compared benchmark
            if not os.path.exists(f"{args.meta_dir}/{bench}.jsonl"):
                raise ValueError(f"{args.meta_dir}/{bench}.jsonl not found (other suite's meta dir?)")
            meta = pd.read_json(f"{args.meta_dir}/{bench}.jsonl", lines=True, dtype=False)
            if meta["problem_id"].astype(str).tolist() != base["problem_id"].astype(str).tolist():
                raise ValueError(f"{bench}: meta rows do not match the scored rows")
            meta["problem_id"] = base["problem_id"]
            meta[[k for k in SLICES if k in meta]] = meta[[k for k in SLICES if k in meta]].astype(str)
        report["benchmarks"][bench] = compare(base, {name: rows[bench] for name, (_, rows) in zip(names, cands)}, meta)
    json.dump(report, open(args.out, "w"), indent=1)
    for bench, result in report["benchmarks"].items():  # the blend, then every source (the tolerance is per source)
        samples = result["samples_per_problem"]
        for where, runs in [(bench, result["metrics"]), *[(f"{bench}/{s}", r) for s, r in result["by_source"].items()]]:
            for name, metrics in runs.items():
                m = metrics["acc_robust" if "acc_robust" in metrics else "acc"]
                label = ("within" if m["ci95"][0] >= -MARGIN else "below" if m["ci95"][1] < -MARGIN else "inconclusive")
                label = "" if args.cross_prompt else " blend, descriptive: see sources" if where == bench and result["by_source"] \
                    else f" vs -{MARGIN:g} pp (proposed): {label}"
                print(f"{where:22s} {name:24s} base {m['base']:6.2f} cand {m['cand']:6.2f} delta {m['delta']:+6.2f} "
                      f"[{m['ci95'][0]:+.2f}, {m['ci95'][1]:+.2f}] problems {m['problems']} "
                      f"samples {samples.get(where.split('/')[-1], samples)}{label}")


if __name__ == "__main__":
    main()
