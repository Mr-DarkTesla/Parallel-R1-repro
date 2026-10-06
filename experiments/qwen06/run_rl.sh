#!/usr/bin/env bash
# Legacy environment/arguments mapped into the shared launcher.
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
root=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
mode=${1:?Usage: run_rl.sh s1|s2 MODEL [Hydra overrides...]}
model=${2:?Supply the validated SFT HF model directory}
shift 2
py=${PARALLEL_R1_PYTHON:-$root/.venv/bin/python}
if [[ ! -x "$py" ]]; then py=${PARALLEL_R1_PYTHON:-python}; fi
name=${RUN_NAME:-qwen06-$mode-seed1}
options=()
overrides=("data.train_batch_size=${BATCH:-32}" "actor_rollout_ref.actor.ppo_mini_batch_size=${MINI:-32}"
  "actor_rollout_ref.rollout.n=${ROLLOUT_N:-8}" "trainer.total_training_steps=${STEPS:-300}"
  "data.max_response_length=${RESPONSE:-3000}" "data.max_prompt_length=${PROMPT:-2000}"
  "actor_rollout_ref.rollout.agent.num_workers=${WORKERS:-4}")
if [[ ${SMOKE:-0} == 1 ]]; then
  options+=(--smoke)
  overrides=()
fi
for arg in "$@"; do
  case "$arg" in
    trainer.resume_mode=auto) options+=(--resume) ;;
    trainer.resume_mode=disable) ;;
    *) overrides+=("$arg") ;;
  esac
done
export PARALLEL_R1_DATA_DIR="$root/data"
export PARALLEL_R1_SCRATCH_ROOT=${PARALLEL_R1_SCRATCH_ROOT:-$root}
exec "$py" "$repo/scripts/qwen3.py" rl "$mode" --model "$model" --name "$name" \
  --gpus "${NPROC_PER_NODE:-1}" --run-dir "$root/runs/$name" --data-dir "$root/data" \
  "${options[@]}" -- "${overrides[@]}"
