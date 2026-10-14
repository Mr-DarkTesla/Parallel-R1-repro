#!/usr/bin/env bash
set -euo pipefail
ROOT=${PROJECT_ROOT}
cd "$ROOT"
V="${PROJECT_ROOT}/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3"
export TMPDIR="$ROOT/t/warm4b-lr-1e-3"
mkdir -p "$TMPDIR"
export OMP_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export PYTHONPATH="$V"
PY="${PARALLEL_R1_PYTHON:-$ROOT/.venv/bin/python}"
exec "$PY" -B -m torch.distributed.run --standalone --nproc_per_node=8 "$V/train.py" --stage "$1"
