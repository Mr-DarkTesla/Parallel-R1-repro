#!/usr/bin/env bash
# SFT on 180 corrected Qwen thinking traces after an independent 30-row gate.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
data=/work/exp21/qwen_rewrite180
scratch=/tmp/exp21-qwen-rewrite-runs
name=exp21-qwen-rewrite180
test -e "$data/sft_qwen_rewrite180_tagged_train.parquet"
test -e "$data/sft_qwen_rewrite180_tagged_val.parquet"
mkdir -p "$scratch"
if [ ! -e "$scratch/$name/DONE" ]; then
    if [ -e "$scratch/$name" ]; then
        echo "$scratch/$name exists but is incomplete; inspect before resuming" >&2
        exit 1
    fi
    RUN_ROOT="$scratch" RUN_NAME="$name" \
      DATA_PATH="$data/sft_qwen_rewrite180_tagged_train.parquet" \
      VAL_PATH="$data/sft_qwen_rewrite180_tagged_val.parquet" \
      MODEL=/work/assets/models/Qwen3-0.6B-mv \
      NGPUS=1 STEPS=64 LR=1e-5 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
      bash scripts/instruct4b/sft.sh +data.structure=multiverse optim.tag_lr_mult=100
fi
test -e "$scratch/$name/DONE" && test -e "$scratch/$name/model/config.json"
date -Is > "$data/TRAIN_DONE"
