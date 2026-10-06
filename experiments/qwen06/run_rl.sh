#!/usr/bin/env bash
# Compatibility with the original RL command; one-off VM/analysis tools stay on the RL branch.
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
root=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
stage=${1:?Usage: $0 s1|s2 CHECKPOINT [Hydra overrides...]}
model=${2:?Supply an SFT HF checkpoint directory}
shift 2
[[ ${SMOKE:-0} == 0 ]] || { echo 'Use the original RL branch for its one-off smoke harness' >&2; exit 2; }
if [[ -x "$root/.venv/bin/python" ]]; then export PATH="$root/.venv/bin:$PATH"; fi
export PARALLEL_R1_RL_NAME=${RUN_NAME:-qwen06-$stage-seed1}
export PARALLEL_R1_RL_DIR="$root/runs/$PARALLEL_R1_RL_NAME"
exec bash "$repo/verl/training_scripts/rl_qwen3_06b.sh" "$stage" "$model" \
  data.train_batch_size="${BATCH:-32}" actor_rollout_ref.actor.ppo_mini_batch_size="${MINI:-32}" \
  actor_rollout_ref.rollout.n="${ROLLOUT_N:-8}" trainer.total_training_steps="${STEPS:-300}" \
  data.max_response_length="${RESPONSE:-3000}" data.max_prompt_length="${PROMPT:-2000}" \
  actor_rollout_ref.rollout.agent.num_workers="${WORKERS:-4}" "$@"
