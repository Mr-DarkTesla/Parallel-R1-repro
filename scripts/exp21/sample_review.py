"""Draw the same stratified, reproducible manual-review sample from paired M1/M2 rows.

Usage: python sample_review.py M1.jsonl M2.jsonl OUT_PREFIX [N=30] [SEED=21]
The output JSONL files carry the question, gold answer and one method's response.
"""
import collections
import json
import random
import sys


def read(path):
    return {r["id"]: r for line in open(path) if (r := json.loads(line))}


first, second, prefix = sys.argv[1:4]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 30
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 21
methods = {"m1": read(first), "m2": read(second)}
assert set(methods["m1"]) == set(methods["m2"])
groups = collections.defaultdict(list)
for key, r in methods["m1"].items():
    kind = "gsm8k" if r["source"] == "gsm8k" else r["answer_type"]
    groups[kind].append(key)
rng = random.Random(seed)
for ids in groups.values():
    rng.shuffle(ids)
targets = {"gsm8k": 8, "integer": 8, "fraction": 8, "expression": 6} if n == 30 else {}
chosen = []
for kind in ("gsm8k", "integer", "fraction", "expression"):
    take = min(targets.get(kind, n // max(len(groups), 1)), len(groups[kind]), n - len(chosen))
    chosen.extend(groups[kind][:take])
remaining = sorted(set(methods["m1"]) - set(chosen))
rng.shuffle(remaining)
chosen.extend(remaining[:n - len(chosen)])
assert len(chosen) == n, (n, len(chosen))
for method, data in methods.items():
    with open(f"{prefix}_{method}.jsonl", "w") as out:
        for key in chosen:
            out.write(json.dumps(data[key], ensure_ascii=False) + "\n")
print(json.dumps({"sample": n, "seed": seed,
                  "groups": dict(collections.Counter("gsm8k" if methods["m1"][k]["source"] == "gsm8k"
                                                     else methods["m1"][k]["answer_type"] for k in chosen))}, indent=2))
