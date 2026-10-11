#!/usr/bin/env bash
# One-GPU matched 4B pilot on the reviewed Sol6.1 inside-think data.
set -euo pipefail

repo=/work/parallel-r1
data=/work/exp21/teacher_sft
model=/tmp/exp21-qwen3-4b-mv10
runroot=/tmp/exp21-selective-runs

exec 9>/tmp/exp21-4b-teacher-sft.lock
flock -n 9 || { echo "4B teacher SFT already running" >&2; exit 1; }
test -s "$model/config.json"
test -s "$data/TRAIN_PAIR_DONE"
test -s "$data/sft_teacher_build.json"
test -s "$data/sft_teacher_tagged_train.parquet"
test -s "$data/sft_teacher_equaltext_plain_train.parquet"
test -s "$data/sft_teacher_equaltext_plain_audit.json"
test -s "$data/sft_teacher_val.parquet"

/work/venv/bin/python - "$data/sft_teacher_build.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
assert r['positive']['rows'] == 196
assert r['train']['rows_per_arm'] == 383
assert r['validation']['rows'] == 63
assert r['checks']['same_train_row_order_and_prompts']
assert r['checks']['nonpositive_rows_identical']
assert r['checks']['train_val_normalized_question_overlap'] == 0
PY

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo"
for arm in tagged plain; do
    if [ "$arm" = plain ]; then train_data="$data/sft_teacher_equaltext_plain_train.parquet"
    else train_data="$data/sft_teacher_tagged_train.parquet"; fi
    RUN_ROOT="$runroot" RUN_NAME="exp21-4b-sol61-${arm}-p16" \
    MODEL="$model" DATA_PATH="$train_data" \
    VAL_PATH="$data/sft_teacher_val.parquet" \
    NGPUS=1 STEPS=16 SAVE_STEPS=4,8,16 LR=3e-6 BATCH=16 MICRO_BATCH=1 \
    MAX_LENGTH=4096 MIN_FREE_GB=30 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
date -Is > "$data/FOUR_B_PAIR_DONE"
