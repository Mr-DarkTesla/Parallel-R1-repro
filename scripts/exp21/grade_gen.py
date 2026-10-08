"""Grade Qwen3-0.6B pool answers (generate_pool.py output) against the pool references; keep clean correct answers.

Correct = not truncated, a "Final Answer:" line (or \\boxed{}) in the answer part, verified by checks.correct (math_verify, letters for
ARC). Thinking rows also need exactly one <think> ... </think> with a non-empty answer after it; non-thinking rows must not contain
think tags. Also flags answers with CJK text or repeated lines (loops), which are not used for SFT.
Usage: python grade_gen.py <pool.jsonl> <gen.jsonl> <graded.jsonl>   (prints a summary by source and answer type)
"""
import collections
import json
import re
import sys

from checks import candidate, correct

pool = {r["id"]: r for r in map(json.loads, open(sys.argv[1]))}
stats = collections.defaultdict(collections.Counter)
with open(sys.argv[3], "w") as f:
    for line in open(sys.argv[2]):
        g = json.loads(line)
        p = pool[g["id"]]
        out = g["output"].replace("<|im_end|>", "").replace("<|endoftext|>", "").strip()
        if g["mode"] == "thinking":
            well_formed = out.startswith("<think>") and out.count("<think>") == 1 and out.count("</think>") == 1
            answer = out.split("</think>")[-1]
        else:
            well_formed = "<think>" not in out and "</think>" not in out
            answer = out
        lines = [ln.strip() for ln in answer.splitlines() if len(ln.strip()) > 20]
        clean = well_formed and answer.strip() != "" and not re.search(r"[぀-ヿ一-鿿]", out) and \
            len(lines) == len(set(lines))
        cand = candidate(answer)
        ok = (not g["truncated"]) and clean and correct(p["answer"], cand, p["source"])
        g.update(output=out, candidate=cand, gold=p["answer"], source=p["source"], answer_type=p["answer_type"],
                 question=p["question"], clean=clean, correct=ok)
        key = f"{g['mode']}/{p['source']}/{p['answer_type']}"
        stats[key]["rows"] += 1
        stats[key]["truncated"] += g["truncated"]
        stats[key]["correct"] += ok
        f.write(json.dumps(g, ensure_ascii=False) + "\n")
for k, c in sorted(stats.items()):
    print(k, dict(c), f"acc {c['correct'] / c['rows']:.3f}")
