#!/usr/bin/env bash
# push_baselines.sh <name>...: copy executor_launch/eval/<name> (shared baselines from A, finished rows/meta) to B own dir
# /work/bench_data/matrix-baselines/<name> (never overwrite), then verify on B: rows and unique problem ids per bench equal the
# executor manifest. No hashes.
set -euo pipefail
O=/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06; S=$O/executor_launch/eval; T=/work/bench_data/matrix-baselines
for n in "$@"; do
  "$O/executor/k.sh" vcharkin-exp-vm-b-0 "test ! -e $T/$n" 2>/dev/null || { echo "$n exists on B, kept"; continue; }
  tar czf - -C "$S" "$n" | "$O/executor/ki.sh" vcharkin-exp-vm-b-0 "mkdir -p $T.tmp && tar xzf - -C $T.tmp && mkdir -p $T && mv $T.tmp/$n $T/$n" 2>/dev/null
done
python3 -c "import json,sys; m=json.load(open('$S/manifest.json')); print(json.dumps({n: {b: [v['rows'], v['unique_problem_ids']] for b, v in m[n]['benchmarks'].items()} for n in sys.argv[1:]}))" "$@" > /tmp/matrix_bl_want.json
"$O/executor/ki.sh" vcharkin-exp-vm-b-0 "cat > /tmp/matrix_bl_want.json" < /tmp/matrix_bl_want.json 2>/dev/null
"$O/executor/k.sh" vcharkin-exp-vm-b-0 "source /work/venv/bin/activate; python - <<'PY'
import json, pandas as pd
want = json.load(open('/tmp/matrix_bl_want.json'))
for n, benches in want.items():
    for b, (rows, ids) in benches.items():
        d = pd.read_json(f'$T/{n}/rows/{b}.jsonl', lines=True)
        print(n, b, len(d), d['problem_id'].nunique(), 'equal_manifest=' + str([len(d), d['problem_id'].nunique()] == [rows, ids]))
PY
rm -f /tmp/matrix_bl_want.json" 2>&1 | grep -v setlocale
