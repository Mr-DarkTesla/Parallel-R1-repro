"""Try other correct Qwen samples only where M1 passed and the first M2 plan did not.

Usage: python prepare_m2_alternates.py <m1.jsonl> <m2_answers.jsonl> <m2.jsonl>
       <graded_nt.jsonl> <out.jsonl> [max_alternates_per_problem]
This uses training answers only; no development or frozen score enters selection.
"""
import collections
import json
import re
import sys

from m2_convert import split_units


def read(path):
    return [json.loads(line) for line in open(path)]


m1, primary, m2, graded, out = sys.argv[1:6]
limit = int(sys.argv[6]) if len(sys.argv) > 6 else 2
eligible = {r["id"] for r in read(m1) if r.get("response") and (r.get("check") or {}).get("ok")}
already = {r["id"] for r in read(m2) if r.get("status") == "ok"}
used = {(r["id"], r["sample"]) for r in read(primary)}
choices = collections.defaultdict(list)
for r in read(graded):
    key = r["id"]
    if key not in eligible or key in already or (key, r["sample"]) in used or not r["correct"]:
        continue
    text = r["output"]
    units = len(split_units(text)[0])
    if units < 4 or len(text) < 250 or r["tokens"] > 2048:
        continue
    cue = bool(re.search(r"\b(?:separately|independently|first case|second case|part 1|part 2)\b", text, re.I))
    choices[key].append((not cue, abs(units - 8), r["tokens"], r["sample"], r))
selected = []
for key in sorted(choices):
    selected.extend(x[-1] for x in sorted(choices[key])[:limit])
with open(out, "w") as f:
    for r in selected:
        f.write(json.dumps({k: r[k] for k in ("id", "sample", "question", "gold", "source", "answer_type", "output")}
                           | {"answer": r["gold"]}, ensure_ascii=False) + "\n")
print(json.dumps({"m1_ok": len(eligible), "m2_already_ok": len(already), "eligible_alternate_problems": len(choices),
                  "selected_alternate_answers": len(selected)}, indent=2))
