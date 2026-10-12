#!/usr/bin/env bash
set -euo pipefail
root=${PROJECT_ROOT}
output="$root/verl/checkpoints/eval/qwen3-06b-instruct-20261005"
previous="$root/verl/checkpoints/eval/qwen3-4b-base-20261005"
source "$root/.venv/bin/activate"
export HF_HOME=${MODEL_ROOT}/huggingface
export R1_OUTPUT_ROOT="$output" R1_EVAL_NAME=instruct NPROC_PER_NODE=8
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
cd "$root/verl"
date -u +%FT%TZ > "$output/queued"
python "$output/download-model.py" > "$output/download.log" 2>&1
while [ ! -f "$previous/finished" ]; do sleep 10; done
checkpoint=$(cat "$output/model-path.txt")
sha256sum "$checkpoint"/model*.safetensors data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet > "$output/model-data-sha256.txt"
date -u +%FT%TZ > "$output/eval-started"
set +e
bash training_scripts/eval_qwen3_06b.sh "$checkpoint" actor_rollout_ref.rollout.mode=sync data.val_batch_size=256 ray_init.num_cpus=32 actor_rollout_ref.rollout.gpu_memory_utilization=0.7 > "$output/instruct.driver.log" 2>&1
rc=$?
printf '%s\n' "$rc" > "$output/instruct.exit_code"
date -u +%FT%TZ > "$output/finished"
exit "$rc"
