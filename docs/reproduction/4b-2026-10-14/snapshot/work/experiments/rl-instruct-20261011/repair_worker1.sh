#!/usr/bin/env bash
set -euo pipefail
cd ${PROJECT_ROOT}
export CUDA_VISIBLE_DEVICES=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS=1
"$PARALLEL_R1_PYTHON" -B ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/evaluate_math500.py --worker 1 --model ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final --system-file ${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/system.txt --mode structured --suite 500 --name initial-lr1e-3-structured500 > ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/evaluations/initial-lr1e-3-structured500/worker-1-repair.log 2>&1
"$PARALLEL_R1_PYTHON" -B ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/resummarize.py
