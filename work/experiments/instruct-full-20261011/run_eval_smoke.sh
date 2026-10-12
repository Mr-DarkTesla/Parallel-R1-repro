#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/jovyan/shares/SR004.nfs3/larin/tmp/r1
cd "$ROOT"
B="$ROOT/work/experiments/instruct-full-20261011"
"${PARALLEL_R1_PYTHON:-$ROOT/.venv/bin/python}" "$B/check_eval_smoke_admission.py"
exec bash "$B/evaluations/run_eval.sh" --model "$B/runs/epoch1/final" --name epoch1-guard-structured-24 --suite 24 --mode structured --system-file "$B/system.txt"
