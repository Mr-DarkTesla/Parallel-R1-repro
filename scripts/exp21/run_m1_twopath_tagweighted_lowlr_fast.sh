#!/usr/bin/env bash
# Dev search: preserve base text weights with lower main LR; tag effective LR stays near 9e-4.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}" PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "${EXP21_REPO:-/work/parallel-r1-eval}"
data=/work/exp21/expanded_th
scratch=/tmp/exp21-expanded-th-runs
name=exp21-expanded-th-m1-twopath-tagweighted-lr3e6-tag300
train=$data/sft_expanded_th_m1_twopath_replay3_tagged_train.parquet
val=$data/sft_expanded_th_m1_twopath_replay3_tagged_val.parquet
test -e "$train" && test -e "$val"
mkdir -p "$scratch"
if [ -e "$scratch/$name/DONE" ]; then exit 0; fi
if [ -e "$scratch/$name" ]; then
    echo "$scratch/$name exists but is incomplete" >&2
    exit 1
fi

RUN_ROOT="$scratch" RUN_NAME="$name" DATA_PATH="$train" VAL_PATH="$val" \
MODEL=/work/assets/models/Qwen3-0.6B-mv NGPUS=1 \
STEPS=64 LR=3e-6 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
bash scripts/instruct4b/sft.sh +data.structure=multiverse \
    +data.parallel_text_loss_weight=0.1 optim.tag_lr_mult=300
test -e "$scratch/$name/DONE" && test -e "$scratch/$name/model/config.json"
date -Is > "$data/M1_TWOPATH_LOWLR_DONE"
