#!/usr/bin/env bash
set -euo pipefail
root=${PROJECT_ROOT}
output="$root/verl/checkpoints/eval/qwen3-06b-instruct-instant-20261005"
scripts="$root/exps/qwen3-06b-instruct-instant-20261005"
previous="$root/verl/checkpoints/eval/qwen3-4b-public-20261005"
source "$root/.venv/bin/activate"
export HF_HOME=${MODEL_ROOT}/huggingface
export R1_OUTPUT_ROOT="$output" R1_EVAL_NAME=instant NPROC_PER_NODE=8
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
cd "$root/verl"
date -u +%FT%TZ > "$output/queued"
python "$scripts/prepare-instant.py" "$output" > "$output/prepare.log" 2>&1
while [ ! -f "$previous/finished" ]; do sleep 10; done
checkpoint=$(cat "$output/model-path.txt")
date -u +%FT%TZ > "$output/eval-started"
set +e
bash training_scripts/eval_qwen3_06b.sh "$checkpoint" actor_rollout_ref.rollout.mode=sync data.val_batch_size=256 ray_init.num_cpus=32 actor_rollout_ref.rollout.gpu_memory_utilization=0.7 > "$output/instant.driver.log" 2>&1
rc=$?
printf '%s\n' "$rc" > "$output/instant.exit_code"
date -u +%FT%TZ > "$output/finished"
if [ "$rc" = 0 ]; then python "$scripts/derive-summary.py" "$output" instant > "$output/summary.log"; fi
exit "$rc"
