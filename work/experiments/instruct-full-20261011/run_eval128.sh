#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/jovyan/shares/SR004.nfs3/larin/tmp/r1
cd "$ROOT"
B="$ROOT/work/experiments/instruct-full-20261011"
PY="${PARALLEL_R1_PYTHON:-$ROOT/.venv/bin/python}"
"$PY" "$B/check_eval128_admission.py"
bash "$B/evaluations/run_eval.sh" --model "$B/runs/epoch1/final" --name epoch1-guard-structured-128 --suite 128 --mode structured --system-file "$B/system.txt"
exec bash "$B/evaluations/run_eval.sh" --model "$ROOT/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final" --name warmup-lr1e3-guard-structured-128 --suite 128 --mode structured --system-file "$B/system.txt"
