#!/usr/bin/env bash
# Dev-only probe: preserve backbone with LR 3e-6 while retaining tag-row LR near the 64-step run.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
root=/work/exp21/qwen_rewrite180
scratch=/tmp/exp21-qwen-rewrite-runs
name=exp21-qwen-rewrite180-tagboost64
train=$root/sft_qwen_rewrite180_tagged_train.parquet
val=$root/sft_qwen_rewrite180_tagged_val.parquet
test -e "$train" && test -e "$val"
mkdir -p "$scratch" "$root/tagboost64"
if [ ! -e "$scratch/$name/DONE" ]; then
    if [ -e "$scratch/$name" ]; then
        echo "$scratch/$name exists but is incomplete; inspect before resuming" >&2
        exit 1
    fi
    RUN_ROOT="$scratch" RUN_NAME="$name" DATA_PATH="$train" VAL_PATH="$val" \
      MODEL=/work/assets/models/Qwen3-0.6B-mv NGPUS=1 \
      STEPS=64 LR=3e-6 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
      bash scripts/instruct4b/sft.sh +data.structure=multiverse optim.tag_lr_mult=300
fi
test -e "$scratch/$name/DONE" && test -e "$scratch/$name/model/config.json"
date -Is > "$root/tagboost64/TRAIN_DONE"
EXP21_PILOT_MODEL="$scratch/$name/model" \
EXP21_PILOT_OUT="$root/tagboost64/masked_pilot" \
EXP21_PILOT_READY="$root/tagboost64/TRAIN_DONE" \
  bash scripts/exp21/run_qwen_rewrite180_masked_pilot_pod.sh
date -Is > "$root/tagboost64/PILOT_DONE"
