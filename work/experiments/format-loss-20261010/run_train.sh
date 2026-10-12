#!/usr/bin/env bash
set -euo pipefail
ROOT=${PROJECT_ROOT}
cd "$ROOT"
C="$ROOT/work/experiments/format-loss-20261010"
D="$ROOT/work/experiments/instruct-token-warmup-20261010"
case "${1:-}" in smoke|production) ;; *) exit 2 ;; esac
export TMPDIR="$ROOT/t/warm4bfmt"
mkdir -p "$TMPDIR"
export OMP_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export PYTHONPATH="$C:$D"
PY="${PARALLEL_R1_PYTHON:-$ROOT/.venv/bin/python}"
exec "$PY" -B -m torch.distributed.run --standalone --nproc_per_node=8 "$C/train.py" --stage "$1"
