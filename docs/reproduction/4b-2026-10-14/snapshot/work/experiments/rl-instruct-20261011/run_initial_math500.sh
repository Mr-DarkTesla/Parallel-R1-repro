#!/usr/bin/env bash
set -euo pipefail
cd ${PROJECT_ROOT}
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1
export TMPDIR=${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/tmp
mkdir -p "$TMPDIR"
exec "$PARALLEL_R1_PYTHON" -B ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/evaluate_math500.py --model ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final --system-file ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt --mode structured --suite 500 --name initial-lr1e-3-structured500
