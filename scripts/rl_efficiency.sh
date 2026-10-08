#!/usr/bin/env bash
# Run one reward variant. Invoke twice sequentially with the same SFT checkpoint.
set -euo pipefail
if [[ $# -lt 5 ]]; then
  echo 'Usage: bash scripts/rl_efficiency.sh gated_depth|parallel_gain SFT_CHECKPOINT TRAIN.parquet VALIDATION.parquet OUTPUT_DIR [Hydra overrides...]' >&2
  exit 2
fi
mode=$1
case "$mode" in gated_depth|parallel_gain) ;; *) echo 'Unknown efficiency reward mode' >&2; exit 2 ;; esac
repo=$(cd "$(dirname "$0")/.." && pwd)
checkpoint=$(realpath "$2")
train=$(realpath "$3")
validation=$(realpath "$4")
output=$5
shift 5
[[ -d "$checkpoint" && -f "$train" && -f "$validation" ]] || { echo 'Checkpoint and both parquet files must exist' >&2; exit 2; }
[[ "$train" != "$validation" ]] || { echo 'Training and validation files must be separate' >&2; exit 2; }
mkdir -p "$output"
export PARALLEL_R1_RL_DIR=$(cd "$output" && pwd)
export PARALLEL_R1_RL_NAME=${PARALLEL_R1_RL_NAME:-qwen06-$mode-seed20261008}
export PARALLEL_R1_EFFICIENCY_MODE=$mode
export PARALLEL_R1_RL_CONFIG=rl_qwen3_06b_efficiency
export PARALLEL_R1_EFFICIENCY_REWARD_PATH="$repo/verl/verl/utils/reward_score/parallel_efficiency.py"
export NPROC_PER_NODE=${NPROC_PER_NODE:-8}
exec bash "$repo/scripts/qwen3.sh" rl s2 "$checkpoint" \
  "data.train_files=\"$train\"" "data.val_files=\"$validation\"" "$@"
