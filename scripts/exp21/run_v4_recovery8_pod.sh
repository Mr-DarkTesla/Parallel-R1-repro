#!/usr/bin/env bash
# Short replay recovery from the reviewed v4 step-56 checkpoint.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
work=${EXP21_WORK:-/work}
venv=${EXP21_VENV:-/work/venv}
train=$work/exp21/expanded_th/sft_v4_recovery8_train.parquet
val=$work/exp21/expanded_th/sft_v4_recovery8_val.parquet
model=/checkpoints/exp21-m1-selective-v4/step_56/model
runroot=/tmp/exp21-selective-runs

test -s /tmp/exp21-v5-step-eval/DONE || {
    echo "Finish the ongoing v5 GPU evaluation before recovery training" >&2
    exit 1
}
test -s "$train" && test -s "$val" && test -s "$model/config.json"
test -s "$work/exp21/expanded_th/sft_v4_recovery8_audit.json" || {
    echo "Recovery dataset audit missing on pod" >&2
    exit 1
}

source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
PYTHONPATH="$repo/verl" python "$repo/scripts/exp21/check_weighted_sft_mask.py" \
    "$model" "$train" "$train" > /tmp/exp21-v4-recovery8-loss-mask.json
test -s /tmp/exp21-v4-recovery8-loss-mask.json
cd "$repo"
RUN_ROOT="$runroot" RUN_NAME=exp21-v4-recovery8 \
MODEL="$model" DATA_PATH="$train" VAL_PATH="$val" \
NGPUS=1 STEPS=8 SAVE_STEPS=4,8 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
MAX_LENGTH=4096 MIN_FREE_GB=10 \
bash scripts/instruct4b/sft.sh +data.structure=multiverse \
    +data.parallel_text_loss_weight=0.1 optim.tag_lr_mult=1
