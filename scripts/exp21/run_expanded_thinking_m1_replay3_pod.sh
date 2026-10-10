#!/usr/bin/env bash
# Dev candidate: lower backbone LR, similar effective tag LR, more Qwen replay.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
data=/work/exp21/expanded_th
scratch=/tmp/exp21-expanded-th-runs
name=exp21-expanded-th-m1-replay3-lr3e6-tag300
train=$data/sft_expanded_th_m1_replay3_tagged_train.parquet
val=$data/sft_expanded_th_m1_replay3_tagged_val.parquet
test -e "$train" && test -e "$val"
mkdir -p "$scratch"
if [ -e "$scratch/$name/DONE" ]; then
    echo "$name already finished"
    exit 0
fi
if [ -e "$scratch/$name" ]; then
    echo "$scratch/$name exists but is incomplete; inspect before resuming" >&2
    exit 1
fi
RUN_ROOT="$scratch" RUN_NAME="$name" DATA_PATH="$train" VAL_PATH="$val" \
MODEL=/work/assets/models/Qwen3-0.6B-mv NGPUS=1 \
STEPS=64 LR=3e-6 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
bash scripts/instruct4b/sft.sh +data.structure=multiverse optim.tag_lr_mult=300
test -e "$scratch/$name/DONE" && test -e "$scratch/$name/model/config.json"
date -Is > "$data/M1_REPLAY3_LR3E6_TAG300_DONE"
