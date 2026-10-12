#!/usr/bin/env bash
set -uo pipefail
root=${PROJECT_ROOT}
name=Parallel-SFT-Unseen-Qwen3-0.6B-padding-fast-20261005
results="$root/verl/checkpoints/$name"
source "$root/.venv/bin/activate"
cd "$root/verl"
export R1_SCRATCH_ROOT=${MODEL_ROOT} R1_OUTPUT_ROOT="$root/verl/checkpoints"
export R1_MODEL_PATH=${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2
export HF_HOME=${MODEL_ROOT}/huggingface PYTHONPATH="$PWD"
export NPROC_PER_NODE=8 CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
mkdir -p "$results"
date -u +%FT%TZ > "$results/started"
cp "$R1_MODEL_PATH/source.json" "$results/model-source.json"
sha256sum training_scripts/prepare_qwen3_parallel.py verl/utils/dataset/parallel_thinking_sft_dataset.py verl/trainer/fsdp_parallel_sft_trainer.py data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/sft_all_accuracy_times_parallel_reward/train.parquet data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_times_parallel_reward/test.parquet > "$results/code-data-sha256.txt"
python -m verl.trainer.fsdp_parallel_sft_trainer --config-name=sft_qwen3_06b trainer.experiment_name="$name" model.enable_gradient_checkpointing=false --cfg job --resolve > "$results/resolved-config.yaml" 2>&1
bash training_scripts/sft_qwen3_06b.sh unseen trainer.experiment_name="$name" model.enable_gradient_checkpointing=false > "$results/sft.log" 2>&1
rc=$?
printf '%s\n' "$rc" > "$results/sft.exit_code"
date -u +%FT%TZ > "$results/finished"
exit "$rc"
