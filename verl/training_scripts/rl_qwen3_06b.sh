#!/usr/bin/env bash
set -euo pipefail
stage=${1:?Usage: $0 s1|s2 CHECKPOINT [Hydra overrides...]}
case "$stage" in s1|s2) ;; *) echo 'Expected s1 or s2' >&2; exit 2 ;; esac
checkpoint=$(realpath "${2:?Supply an SFT HF checkpoint directory}")
shift 2
[[ ! -f "$checkpoint/SMOKE_ONLY" ]] || { echo 'Disposable smoke weights cannot initialize RL' >&2; exit 2; }
cd "$(dirname "$0")/.."

export PARALLEL_R1_MODEL_PATH="$checkpoint"
export PARALLEL_R1_RL_REWARD=accuracy_reward
if [[ "$stage" == s2 ]]; then export PARALLEL_R1_RL_REWARD=accuracy_parallel_interv_reward; fi
export PARALLEL_R1_RL_NAME=${PARALLEL_R1_RL_NAME:-qwen06-$stage-seed1}
export PARALLEL_R1_RL_DIR=${PARALLEL_R1_RL_DIR:-${PARALLEL_R1_OUTPUT_ROOT:-$PWD/checkpoints}/rl/$PARALLEL_R1_RL_NAME}
export HF_HOME=${HF_HOME:-${PARALLEL_R1_SCRATCH_ROOT:-$PWD/checkpoints}/huggingface}
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
export VLLM_USE_V1=1
export PYTHONUNBUFFERED=1
mkdir -p "$PARALLEL_R1_RL_DIR"
export PARALLEL_R1_RL_DIR=$(cd "$PARALLEL_R1_RL_DIR" && pwd)
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-4}
export WANDB_MODE=${WANDB_MODE:-offline}
export WANDB_DIR="$PARALLEL_R1_RL_DIR"
export PARALLEL_R1_TRACE_DIR=${PARALLEL_R1_TRACE_DIR:-$PARALLEL_R1_RL_DIR/telemetry}
python -m verl.trainer.main_ppo --config-name="${PARALLEL_R1_RL_CONFIG:-rl_qwen3_06b}" \
  trainer.n_gpus_per_node="${NPROC_PER_NODE:-1}" "$@" 2>&1 | tee -a "$PARALLEL_R1_RL_DIR/train.log"
