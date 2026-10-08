"""Choose one correct Qwen3-0.6B non-thinking answer per M1 problem for plan-only conversion.

Prefer an answer with several short line/paragraph units so Claude can identify independent parts. This choice uses only training
answers, never dev/frozen scores. Usage: python prepare_m2_inputs.py <m1_problems.jsonl> <graded_nt.jsonl> <out.jsonl>.
"""
import collections
import json
import sys

from m2_convert import split_units

problems = {r["id"]: r for r in map(json.loads, open(sys.argv[1]))}
choices = collections.defaultdict(list)
counts = collections.Counter()
for r in map(json.loads, open(sys.argv[2])):
    if r["id"] not in problems or not r["correct"]:
        continue
    units = len(split_units(r["output"])[0])
    if units < 4 or len(r["output"]) < 250 or r["tokens"] > 2048:
        counts["too_short_or_long"] += 1
        continue
    choices[r["id"]].append((abs(units - 8), r["tokens"], r["sample"], r))
with open(sys.argv[3], "w") as f:
    for key in sorted(choices):
        r = min(choices[key])[-1]
        p = problems[key]
        f.write(json.dumps({"id": key, "sample": r["sample"], "question": p["question"], "answer": p["answer"],
                            "source": p["source"], "answer_type": p["answer_type"], "output": r["output"]},
                           ensure_ascii=False) + "\n")
print(json.dumps({"problems": len(choices), "by_source_type": dict(collections.Counter(
    f"{problems[k]['source']}/{problems[k]['answer_type']}" for k in choices)), **dict(counts)}, indent=2))
