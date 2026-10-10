#!/usr/bin/env bash
# Same recipe as deep75, with each new teacher solution used once.
# Sequential one-GPU training; models remain in the pod's scratch until dev selection.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
grep -q 'RUN_ROOT' scripts/instruct4b/sft.sh
scratch=/tmp/exp21-balanced-runs
data=/work/exp21/deep_balanced
mkdir -p "$scratch"
for arm in tagged control; do
    test -e "$data/sft_sol_deep75_balanced_${arm}_train.parquet"
    test -e "$data/sft_sol_deep75_balanced_${arm}_val.parquet"
done

train_one() {
    local name=$1 arm=$2
    if [ -e "$scratch/$name/DONE" ]; then
        echo "$name already finished"
        return
    fi
    if [ -e "$scratch/$name" ]; then
        echo "$scratch/$name exists but is incomplete; inspect before proceeding" >&2
        exit 1
    fi
    RUN_ROOT="$scratch" RUN_NAME="$name" \
      DATA_PATH="$data/sft_sol_deep75_balanced_${arm}_train.parquet" \
      VAL_PATH="$data/sft_sol_deep75_balanced_${arm}_val.parquet" \
      MODEL=/work/assets/models/Qwen3-0.6B-mv \
      NGPUS=1 STEPS=64 LR=1e-5 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
      bash scripts/instruct4b/sft.sh +data.structure=multiverse optim.tag_lr_mult=100
    test -e "$scratch/$name/DONE"
    test -e "$scratch/$name/model/config.json"
}

train_one exp21-sol-deep75-balanced tagged
train_one exp21-sol-deep75-balanced-control control
date -Is > "$data/TRAIN_PAIR_DONE"
