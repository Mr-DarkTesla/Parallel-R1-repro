#!/usr/bin/env bash
# One own GPU, matched tag/control SFT; scratch checkpoints on the pod overlay.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
grep -q RUN_ROOT scripts/instruct4b/sft.sh
scratch=/tmp/exp21-r3-runs
data=/work/exp21/sol_r3
mkdir -p "$scratch"
for arm in tagged control; do
    test -e "$data/sft_sol_deep75_r3_${arm}_train.parquet"
    test -e "$data/sft_sol_deep75_r3_${arm}_val.parquet"
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
      DATA_PATH="$data/sft_sol_deep75_r3_${arm}_train.parquet" \
      VAL_PATH="$data/sft_sol_deep75_r3_${arm}_val.parquet" \
      MODEL=/work/assets/models/Qwen3-0.6B-mv \
      NGPUS=1 STEPS=64 LR=1e-5 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
      bash scripts/instruct4b/sft.sh +data.structure=multiverse optim.tag_lr_mult=100
    test -e "$scratch/$name/DONE"
    test -e "$scratch/$name/model/config.json"
}

train_one exp21-sol-reserve-r3 tagged
train_one exp21-sol-reserve-r3-control control
date -Is > "$data/TRAIN_PAIR_DONE"
