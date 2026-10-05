#!/usr/bin/env bash
# Runs 10 SFT steps with the authors' code (upstream commit) and with our speedups,
# same data order and init, and prints the losses of both runs side by side.
# Usage: bash scripts/check_sft_parity.sh <model_with_special_tokens> <work_dir>
set -euo pipefail

model=$1
work_dir=$2
repo=$(cd "$(dirname "$0")/.." && pwd)
upstream=$work_dir/upstream

git -C "$repo" worktree add --force "$upstream" f1c6389
mkdir -p "$upstream/scripts"
cp "$repo/scripts/sft_qwen3_0.6b.sh" "$upstream/scripts/"

short_run="data.train_batch_size=16 trainer.total_training_steps=10"

bash "$upstream/scripts/sft_qwen3_0.6b.sh" "$model" "$work_dir/ckpt_upstream" $short_run \
    data.micro_batch_size_per_gpu=1 model.enable_gradient_checkpointing=True > "$work_dir/upstream.log" 2>&1
bash "$repo/scripts/sft_qwen3_0.6b.sh" "$model" "$work_dir/ckpt_ours" $short_run > "$work_dir/ours.log" 2>&1

echo "upstream | ours"
paste <(grep -o "step:[0-9]* - [a-z/]*loss:[0-9.]*" "$work_dir/upstream.log") \
      <(grep -o "[a-z/]*loss:[0-9.]*" "$work_dir/ours.log")
