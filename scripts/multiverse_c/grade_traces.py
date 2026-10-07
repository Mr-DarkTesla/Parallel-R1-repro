"""Variant C, step 2b: grade generated traces against the pool answers; keep correct, untruncated, well-formed thinking traces.

Answer = text after </think>; checked like accuracy_robust of scripts/bench/score.py: options by the last answer letter,
math by the last \\boxed{} or the line after the last "Final Answer:", with math_verify, else the math_dapo string check.
Usage (verl/ on PYTHONPATH): python grade_traces.py <pool.jsonl> <traces.jsonl> <graded.jsonl> <summary.json>
"""
import collections
import json
import re
import sys

from math_verify import parse, verify
from verl.utils.reward_score.math_dapo import compute_score, last_boxed_only_string, remove_boxed


def is_letter(row):
    return row["answer_source"] == "solution_answer_letter"


def candidate(answer):
    boxed = last_boxed_only_string(answer)
    if boxed:
        cand = remove_boxed(boxed)
    else:
        parts = re.split(r"(?i)final answer\s*:", answer)
        lines = [ln for ln in parts[-1].splitlines() if ln.strip()] if len(parts) > 1 else []
        cand = lines[0] if lines else ""
    return cand.strip().strip("$").strip().rstrip(".").strip("*").strip()


def correct(row, answer):
    truth = row["answer"]
    if is_letter(row):
        choices = re.findall(r"(?i)(?:final answer|correct answer|answer is|answer)\s*:?\s*\**\(?([A-J])\b", answer)
        return bool(choices) and choices[-1].upper() == truth
    cand = candidate(answer)
    if not cand:
        return False
    options = dict(re.findall(r"\\textbf\{\(([A-E])\)\s*\}\s*([^\\$]+?)\s*(?=\\qquad|\$|\\textbf|$)", row["question"]))
    letter = re.fullmatch(r"\(?\\?(?:textbf\{)?\(?([A-E])\)?\}?\)?", cand)
    if options and letter and letter.group(1) in options:  # AMC-style inline options, gold is the value
        cand = options[letter.group(1)].strip()
    try:
        if verify(parse(f"${truth}$"), parse(f"${cand}$")):
            return True
    except Exception:
        pass
    if bool(compute_score(f"Final Answer: {cand}", truth)["acc"]):
        return True
    return close_numbers(truth, cand)


def close_numbers(truth, cand, rel=1e-2):
    """Science answers with a decimal gold (TheoremQA float, JEE numeric): equal within 1% (absolute 1e-6 for zero)."""
    num = re.compile(r"^[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$")
    t, c = truth.replace(",", "").strip(), re.sub(r"\\(?:text|mathrm)\{[^}]*\}", "", cand).replace(",", "").strip()
    if not (num.match(t) and num.match(c)) or not re.search(r"[.eE]", t):  # integer gold: exact match only (handled above)
        return False
    t, c = float(t), float(c)
    return abs(c - t) <= max(rel * abs(t), 1e-6)


def main(pool_path, traces_path, out_path, summary_path):
    pool = {r["mv_index"]: r for r in map(json.loads, open(pool_path))}
    rows = [json.loads(line) for line in open(traces_path)]
    stats = collections.Counter()
    per_problem = collections.defaultdict(list)
    with open(out_path, "w") as f:
        for t in rows:
            p = pool[t["mv_index"]]
            out = t["output"].replace("<|im_end|>", "").replace("<|endoftext|>", "")
            well_formed = out.count("<think>") <= 1 and out.count("</think>") == 1
            answer = out.split("</think>")[-1]
            ok = (not t["truncated"]) and well_formed and correct(p, answer)
            keep = ok
            t.update({"answer_text": answer.strip()[-300:], "candidate": candidate(answer), "gold": p["answer"],
                      "correct": ok, "well_formed": well_formed, "keep": keep})
            stats["rows"] += 1
            stats["truncated"] += t["truncated"]
            stats["malformed_think"] += not well_formed
            stats["correct"] += ok
            per_problem[t["mv_index"]].append(ok)
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    toks = sorted(t["tokens"] for t in rows)
    kept_toks = sorted(t["tokens"] for t in rows if t["keep"])
    q = lambda xs, p: xs[int(p * (len(xs) - 1))] if xs else None  # noqa: E731
    summary = {
        **stats,
        "problems": len(per_problem),
        "accuracy_mean@samples": round(stats["correct"] / max(stats["rows"], 1), 4),
        "problems_with_>=1_correct": sum(any(v) for v in per_problem.values()),
        "problems_all_correct": sum(all(v) for v in per_problem.values()),
        "tokens_p50_p90_max": [q(toks, .5), q(toks, .9), toks[-1] if toks else None],
        "kept_tokens_p50_p90_max": [q(kept_toks, .5), q(kept_toks, .9), kept_toks[-1] if kept_toks else None],
        "output_tokens_total": sum(toks),
        "by_answer_source": {s: [sum(per_problem[i].count(True) for i in per_problem if pool[i]["answer_source"] == s),
                                 sum(len(per_problem[i]) for i in per_problem if pool[i]["answer_source"] == s)]
                             for s in sorted({pool[i]["answer_source"] for i in per_problem})},
    }
    json.dump(summary, open(summary_path, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:5])
