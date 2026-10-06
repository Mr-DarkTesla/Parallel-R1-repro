#!/usr/bin/env bash
set -euo pipefail
checkpoint=$(realpath "${1:?Usage: $0 CHECKPOINT [Hydra overrides...]}")
shift
cd "$(dirname "$0")/.."

export PARALLEL_R1_EVAL_MODEL="$checkpoint"
export PARALLEL_R1_EVAL_NAME=${PARALLEL_R1_EVAL_NAME:-$(basename "$(dirname "$checkpoint")")-$(basename "$checkpoint")}
export HF_HOME=${HF_HOME:-${PARALLEL_R1_SCRATCH_ROOT:-$PWD/checkpoints}/huggingface}
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
export VLLM_USE_V1=1
result_dir=${PARALLEL_R1_OUTPUT_ROOT:-checkpoints}/eval/$PARALLEL_R1_EVAL_NAME
mkdir -p "$result_dir"

python -m verl.trainer.main_ppo --config-name=eval_qwen3_06b \
  trainer.n_gpus_per_node="${NPROC_PER_NODE:-8}" "$@" 2>&1 | tee "$result_dir/eval.log"
