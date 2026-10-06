#!/usr/bin/env bash
# The authors' parallel rollout on any benchmark parquet with a given response budget (tokens), on 1 GPU, without training.
# Same settings as scripts/eval_qwen3_0.6b.sh; validation order is kept so answers line up with the parquet rows.
# Usage: bash scripts/bench/eval_rollout.sh <model> <output_dir> <test_parquet> <response_budget>
set -euo pipefail

model=$1
output_dir=$2
data=./data_preprocess_scripts/data
test=$3
max_length=$4
max_prompt_len=2000

cd "$(dirname "$0")/../../verl"
export VLLM_USE_V1=1
python -m verl.trainer.main_ppo \
    algorithm.adv_estimator=grpo \
    data.train_files="['$data/dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/train.parquet']" \
    data.val_files="['$test']" \
    data.train_batch_size=256 \
    data.return_raw_chat=True \
    data.max_prompt_length=$max_prompt_len \
    data.max_response_length=$max_length \
    data.filter_overlong_prompts=False \
    data.truncation='left' \
    +data.validation_shuffle=False \
    actor_rollout_ref.model.path="$model" \
    actor_rollout_ref.model.use_remove_padding=False \
    actor_rollout_ref.actor.ppo_mini_batch_size=128 \
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=2 \
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=4 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
    actor_rollout_ref.rollout.agent.max_path_response_length=$(( max_length > 4096 ? max_length : 4096 )) \
    actor_rollout_ref.rollout.agent.num_workers=32 \
    actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=4 \
    actor_rollout_ref.rollout.agent.num_paths=2 \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.mode=async \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.6 \
    actor_rollout_ref.rollout.top_p=1.0 \
    actor_rollout_ref.rollout.top_k=-1 \
    actor_rollout_ref.rollout.val_kwargs.temperature=1.0 \
    actor_rollout_ref.rollout.val_kwargs.top_p=1.0 \
    actor_rollout_ref.rollout.val_kwargs.top_k=-1 \
    actor_rollout_ref.rollout.val_kwargs.do_sample=True \
    actor_rollout_ref.rollout.val_kwargs.n=1 \
    trainer.logger=['console'] \
    trainer.project_name=Parallel-R1 \
    trainer.experiment_name=eval \
    trainer.n_gpus_per_node=1 \
    trainer.nnodes=1 \
    trainer.val_before_train=True \
    trainer.val_only=True \
    trainer.validation_data_dir="$output_dir/generations" \
    trainer.default_local_dir="$output_dir"
