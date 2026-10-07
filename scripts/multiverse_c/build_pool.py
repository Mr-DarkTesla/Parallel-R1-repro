"""Variant C, step 1: problem pool from Multiverse-1K / s1K-1.1 with a checkable answer and no eval overlap.

Usage: python build_pool.py <multiverse1k.json> <s1K-1.1-meta.json> <evalsets_dir> <math_test.parquet> <out_dir>
Writes pool.jsonl (kept problems), dropped.jsonl (reason per problem), pool_summary.json.
"""
import collections
import glob
import json
import os
import re
import sys

import pandas as pd

N = 13
BOILERPLATE_DF = 5  # a gram shared by >= 5 distinct eval problems is template text ("m and n are relatively prime ...")
PROOF = re.compile(r"\b(prove|proof|show that|show how|demonstrate that|justify)\b", re.I)


def words(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).split()


def ngrams(text):
    w = words(text)
    if len(w) < N:  # short question: whole normalized text acts as one gram
        return {" ".join(w)} if w else set()
    return {" ".join(w[i:i + N]) for i in range(len(w) - N + 1)}


def last_boxed(text):
    """Content of the last \\boxed{...} (balanced braces), or None."""
    start = text.rfind("\\boxed")
    if start < 0:
        return None
    i = text.find("{", start)
    if i < 0:
        return None
    depth = 0
    for j in range(i, len(text)):
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        if depth == 0:
            return text[i + 1:j].strip()
    return None


def gold_answer(sol, attempt, grade):
    """(answer, source) from the reference solution; graded attempt only as fallback."""
    sol = (sol or "").strip()
    box = last_boxed(sol)
    if box:
        return box, "solution_boxed"
    m = re.search(r"(?:^|\n)\s*(?:final\s+)?answer\s*[:：]\s*\(?([A-J])\)?\s*$", sol, re.I)
    if m:
        return m.group(1).upper(), "solution_answer_letter"
    if sol and len(sol) <= 40 and "\n" not in sol:
        return sol, "solution_short"
    if grade == "Yes":
        box = last_boxed(attempt or "")
        if box:
            return box, "graded_attempt_boxed"
    return None, None


def eval_problems(evaldir, math_test):
    """{set_name: [problem texts]} for every dev and frozen eval set."""
    sets = {}
    for f in sorted(glob.glob(os.path.join(evaldir, "instruct4b/eval/dev/plain/*.parquet"))):
        sets[os.path.basename(f)[:-8]] = pd.read_parquet(f)
    for f in sorted(glob.glob(os.path.join(evaldir, "plain/*.parquet"))):
        d = pd.read_parquet(f)
        name = os.path.basename(f)[:-8]
        if name == "apo":  # split AIME24/25, AMC23, MATH300
            for src, g in d.groupby("data_source"):
                sets[src.replace("APO_", "").lower()] = g
        else:
            sets[name] = d
    out = {}
    for name, d in sets.items():
        texts = []
        for p in d["prompt"]:
            c = p[0]["content"]
            texts.append(c.split("Problem:", 1)[1] if "Problem:" in c else c)
        out[name] = sorted(set(texts))  # rollout copies collapse to unique problems
    info = {"math_test_full(info)": sorted(set(pd.read_parquet(math_test)["prompt"].map(lambda p: p[0]["content"])))}
    return out, info


def main(mv_path, s1k_path, evaldir, math_test, out_dir):
    mv = json.load(open(mv_path))
    meta = {r["question"].strip(): r for r in json.load(open(s1k_path))}
    evals, info = eval_problems(evaldir, math_test)
    index = collections.defaultdict(set)  # gram -> eval set names
    df = collections.Counter()  # gram -> number of distinct eval problems containing it
    for name, texts in list(evals.items()) + list(info.items()):
        for t in texts:
            for g in ngrams(t):
                index[g].add(name)
                df[g] += 1
    boilerplate = {g for g, c in df.items() if c >= BOILERPLATE_DF}

    kept, dropped = [], []
    overlap_counts = collections.Counter()
    for i, r in enumerate(mv):
        q = r["question"].strip()
        m = meta[q]
        rec = {"mv_index": i, "source_type": m["source_type"], "cot_type": m["cot_type"]}
        hits = set()
        shared = 0
        for g in ngrams(q):
            if g in index and g not in boilerplate:
                hits |= index[g]
                shared += 1
        rec["shared_grams"] = shared
        for h in hits:
            overlap_counts[h] += 1
        eval_hits = sorted(h for h in hits if "(info)" not in h)
        rec["eval_overlap"] = eval_hits
        rec["math_test_overlap"] = "math_test_full(info)" in hits
        ans, src = gold_answer(r["solution"], r["deepseek_attempt"], r["deepseek_grade"])
        if eval_hits:
            reason = "eval_overlap"
        elif m["cot_type"] == "crossword":
            reason = "crossword"
        elif PROOF.search(q):
            reason = "proof"
        elif ans is None:
            reason = "no_checkable_answer"
        else:
            reason = None
        if reason:
            dropped.append({**rec, "reason": reason})
            continue
        kept.append({**rec, "question": q, "answer": ans, "answer_source": src,
                     "r1_grade": r["deepseek_grade"], "metadata": m["metadata"]})

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "pool.jsonl"), "w") as f:
        for k in kept:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    with open(os.path.join(out_dir, "dropped.jsonl"), "w") as f:
        for k in dropped:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    summary = {
        "multiverse1k": len(mv),
        "kept": len(kept),
        "dropped_by_reason (first matching rule)": dict(collections.Counter(d["reason"] for d in dropped)),
        "questions_overlapping_each_set (13-gram, any rule)": dict(overlap_counts),
        "eval_sets_unique_problems": {k: len(v) for k, v in evals.items()},
        "kept_by_answer_source": dict(collections.Counter(k["answer_source"] for k in kept)),
        "kept_by_cot_type": dict(collections.Counter(k["cot_type"] for k in kept)),
        "kept_by_source_type": dict(collections.Counter(k["source_type"] for k in kept).most_common()),
        "kept_r1_grade": dict(collections.Counter(k["r1_grade"] for k in kept)),
        "kept_overlapping_full_MATH_test_not_in_our_evals": sum(k["math_test_overlap"] for k in kept),
        "boilerplate_grams_ignored": len(boilerplate),
        "rules": f"13-gram (grams in >= {BOILERPLATE_DF} eval problems ignored as template) on lowercased alnum words (short texts: whole text); eval problems = text after 'Problem:'; "
                 "AIME IDs: s1K AIME years 1983-2022 only, no 2024/2025; proof regex on question; crossword dropped",
    }
    json.dump(summary, open(os.path.join(out_dir, "pool_summary.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:6])
