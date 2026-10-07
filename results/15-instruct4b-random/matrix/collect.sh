#!/usr/bin/env bash
# collect.sh <run name>...: copy finished matrix eval artifacts (meta.json, results/, rows/, *.log; no dumps) from B
# /work/bench/instruct4b/<name> to matrix_continue/eval/<name>, then manifest.json (paths, rows, ids; no hashes).
set -euo pipefail
O=/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06; L=$O/matrix_continue/eval
for n in "$@"; do
  mkdir -p "$L/$n"
  "$O/executor/k.sh" vcharkin-exp-vm-b-0 "cd /work/bench/instruct4b/$n && tar czf - meta.json results rows \$(ls *.log 2>/dev/null)" 2>/dev/null | tar xzf - -C "$L/$n"
done
python3 - "$L" <<'PY'
import json, os, sys
L = sys.argv[1]; man = {}
for n in sorted(os.listdir(L)):
    d = os.path.join(L, n)
    if not os.path.isdir(os.path.join(d, "rows")): continue
    ent = {"remote": f"B:/work/bench/instruct4b/{n}", "meta": json.load(open(os.path.join(d, "meta.json"))), "benchmarks": {}}
    for f in sorted(os.listdir(os.path.join(d, "rows"))):
        if not f.endswith(".jsonl"): continue
        rows = [json.loads(l) for l in open(os.path.join(d, "rows", f))]
        ids = [r.get("problem_id") for r in rows]
        ent["benchmarks"][f[:-6]] = {"rows": len(rows), "unique_problem_ids": len(set(ids)), "first_ids": ids[:3],
                                     "sources": sorted({str(r.get("source")) for r in rows})}
    man[n] = ent
json.dump(man, open(os.path.join(L, "manifest.json"), "w"), indent=1)
for n, e in man.items(): print(n, {b: (v["rows"], v["unique_problem_ids"]) for b, v in e["benchmarks"].items()})
PY
