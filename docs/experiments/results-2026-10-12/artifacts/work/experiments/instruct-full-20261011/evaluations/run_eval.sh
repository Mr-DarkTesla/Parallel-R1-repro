#!/usr/bin/env bash
set -euo pipefail
ROOT=${PROJECT_ROOT}
cd "$ROOT"
E="$ROOT/work/experiments/instruct-full-20261011/evaluations"
export TMPDIR="$ROOT/work/experiments/instruct-full-20261011/eval-tmp"
mkdir -p "$TMPDIR"
export OMP_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
export PYTHONPATH="$E:$E/runtime"
PY="${PARALLEL_R1_PYTHON:-$ROOT/.venv/bin/python}"
exec "$PY" -B "$E/evaluate.py" "$@"
