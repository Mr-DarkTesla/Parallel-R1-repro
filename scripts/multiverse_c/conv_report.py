"""Variant C: summary of a conversion directory (refusals, plan errors, checks, structure, cost, answer-first blocks).

Usage: python conv_report.py <conv_dir> [graded.jsonl] [mask_check.json] -> prints JSON, writes <conv_dir>/report.json
answer_first: the graded final candidate (e.g. "628") already occurs in the thinking text before the first <Parallel>
(approximate string match, numbers/short answers only), i.e. the block only re-checks a found answer.
"""
import collections
import glob
import json
import os
import re
import statistics
import sys


def main(conv_dir, graded=None, mask=None):
    cand = {}
    if graded:
        for r in map(json.loads, open(graded)):
            cand[f"{r['mv_index']}_{r['sample']}"] = (r.get("candidate") or "").strip()
    masks = json.load(open(mask))["samples"] if mask else {}
    recs = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(conv_dir, "*_*.json")))]
    c = collections.Counter()
    paths, depth, saved, cost, tin, tout, toks, af = [], [], [], [], [], [], [], []
    for r in recs:
        c["attempted"] += 1
        att = r.get("attempts", [])
        c["refused_first_model"] += bool(att and att[0]["refused"])
        c["refused_after_fallback"] += bool(att and att[-1]["refused"])
        c["api_error_other"] += bool(r["is_error"] and not (att and att[-1]["refused"]))
        c["plan_error"] += bool(r.get("plan_error"))
        if r.get("cost_usd"):
            cost.append(r["cost_usd"])
        u = r.get("usage") or {}
        if u:
            tin.append(u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0))
            tout.append(u.get("output_tokens", 0))
        if r["is_error"] or r.get("plan_error"):
            continue
        if not r["blocks"]:
            c["no_blocks"] += 1
            continue
        ch = r.get("checks", {})
        m = masks.get(r["key"], {})
        ok = ch.get("ok") and (m.get("ok", True) and m.get("fits", True))
        c["converted_ok"] += bool(ok)
        c["independence_flagged"] += any(i.startswith("independence_flags") for i in ch.get("issues", []))
        if not ok:
            c["failed_checks"] += 1
            continue
        st = ch["stats"]
        paths += st["paths_per_block"]
        depth.append(st["max_depth"])
        saved.append(st["share_chars_saved_by_parallel(approx)"])
        if m:
            toks.append(m["prompt_tokens"] + m["response_tokens"])
        a = cand.get(r["key"], "")
        if a and len(a) <= 20:
            think = r["response"].split("</think>")[0]
            first = think.find("<Parallel>")
            hit = re.search(r"(?<![\d.])" + re.escape(a) + r"(?![\d])", think[:first])
            af.append(bool(hit))
    q = lambda xs: [min(xs), statistics.median(xs), max(xs)] if xs else None  # noqa: E731
    rep = {**c, "success_rate_of_attempts": round(c["converted_ok"] / max(c["attempted"], 1), 3),
           "paths_per_block_counts": dict(collections.Counter(paths)),
           "nested_samples": sum(d >= 2 for d in depth), "saved_chars_min_med_max": q(saved),
           "tokens_min_med_max": q(toks), "answer_first_share": round(sum(af) / len(af), 3) if af else None,
           "answer_first_n": len(af), "cost_usd_total": round(sum(cost), 3), "cost_usd_mean": round(statistics.mean(cost), 4) if cost else None,
           "input_tokens_mean": round(statistics.mean(tin)) if tin else None, "output_tokens_mean": round(statistics.mean(tout)) if tout else None}
    json.dump(rep, open(os.path.join(conv_dir, "report.json"), "w"), indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
