#!/usr/bin/env bash
# Authors' verl/training_scripts/sft_exp.sh on 1 GPU with Qwen3-0.6B-Base.
# Differences: 1 GPU, micro batch 4 instead of 1, no gradient checkpointing.
# Usage: bash scripts/sft_qwen3_0.6b.sh <model_with_special_tokens> <output_dir> [hydra overrides...]
set -euo pipefail

model=$1
output_dir=$2
shift 2

data=./data_preprocess_scripts/data/gsm8k/adaptive_parallel_thinking_final_with_prompt_v3

cd "$(dirname "$0")/../verl"
torchrun --standalone --nnodes=1 --nproc_per_node=1 \
    -m verl.trainer.fsdp_parallel_sft_trainer \
    data.train_files=$data/sft_all_accuracy_times_parallel_reward/train.parquet \
    data.val_files=$data/rl_all_accuracy_times_parallel_reward/test.parquet \
    data.prompt_key=extra_info \
    data.response_key=extra_info \
    data.max_length=4096 \
    +data.prompt_dict_keys=['question'] \
    +data.response_dict_keys=['answer'] \
    data.micro_batch_size_per_gpu=4 \
    data.train_batch_size=128 \
    model.partial_pretrain="$model" \
    model.enable_gradient_checkpointing=False \
    trainer.default_local_dir="$output_dir" \
    trainer.project_name=Parallel-R1 \
    trainer.experiment_name=Parallel-SFT-Unseen-Qwen3-0.6B \
    trainer.total_epochs=5 \
    trainer.logger=['console'] \
    trainer.default_hdfs_dir=null "$@"
