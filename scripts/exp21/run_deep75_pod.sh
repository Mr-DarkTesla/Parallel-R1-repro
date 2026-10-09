#!/usr/bin/env bash
# Sequential one-GPU SFT and durable copy from this pod's ephemeral scratch.
# Run inside vcharkin-exp-vm-0 before the approved GPU window closes.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
scratch=/tmp/exp21-runs
persistent=/work/runs
data=/work/exp21/deep_round2
mkdir -p "$scratch" "$persistent"

train_one() {
    local name=$1 arm=$2 dest="$persistent/$1"
    if [ -e "$dest/DONE" ]; then
        echo "$name already persisted"
        return
    fi
    if [ -e "$dest" ]; then
        echo "$dest exists but is incomplete; inspect before proceeding" >&2
        exit 1
    fi
    RUN_ROOT="$scratch" RUN_NAME="$name" \
      DATA_PATH="$data/sft_sol_deep75_${arm}_train.parquet" \
      VAL_PATH="$data/sft_sol_deep75_${arm}_val.parquet" \
      MODEL=/work/assets/models/Qwen3-0.6B-mv \
      NGPUS=1 STEPS=64 LR=1e-5 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
      bash scripts/instruct4b/sft.sh +data.structure=multiverse optim.tag_lr_mult=100
    test -e "$scratch/$name/DONE"
    test -e "$scratch/$name/model/config.json"
    local stage="$dest.staging.$$"
    mkdir -p "$stage"
    cp -a "$scratch/$name/." "$stage/"
    test -e "$stage/DONE"
    test -e "$stage/model/config.json"
    mv "$stage" "$dest"
    echo "$name persisted to $dest"
}

train_one exp21-sol-deep75 tagged
train_one exp21-sol-deep75-control control
date -Is > "$data/TRAIN_PAIR_DONE"
