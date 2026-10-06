#!/usr/bin/env bash
set -euo pipefail
checkpoint=$(realpath "${1:?Usage: $0 CHECKPOINT [Hydra overrides...]}")
shift
repo=$(cd "$(dirname "$0")/../.." && pwd)
cd "$repo/verl"
name=${PARALLEL_R1_EVAL_NAME:-$(basename "$(dirname "$checkpoint")")-$(basename "$checkpoint")}
exec "${PARALLEL_R1_PYTHON:-python}" "$repo/scripts/qwen3.py" eval \
  --model "$checkpoint" --name "$name" --gpus "${NPROC_PER_NODE:-8}" \
  --run-dir "${PARALLEL_R1_OUTPUT_ROOT:-checkpoints}/eval/$name" -- "$@"
