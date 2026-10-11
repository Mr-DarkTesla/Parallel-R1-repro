#!/usr/bin/env bash
# Matched one-GPU eight-step SFT for screened Sol 6.1 teacher trajectories.
# Expects CPU-built data; it never builds data and is not a queue launcher.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
work=${EXP21_WORK:-/work}
venv=${EXP21_VENV:-/work/venv}
data=${EXP21_TEACHER_DATA:-$work/exp21/teacher_sft}
model=${EXP21_PARENT_MODEL:-/checkpoints/exp21-v4-recovery8/step_8/model}
runroot=${EXP21_RUN_ROOT:-/tmp/exp21-selective-runs}
min_accepted=${EXP21_MIN_ACCEPTED:-150}

[[ "$min_accepted" =~ ^[1-9][0-9]*$ ]] || { echo "EXP21_MIN_ACCEPTED must be a positive integer" >&2; exit 1; }
exec 9>/tmp/exp21-teacher-sft.lock
flock -n 9 || { echo "teacher SFT already running" >&2; exit 1; }
test -s "$model/config.json"
test -s /checkpoints/exp21-global-top5/GLOBAL_TOP5.json
for file in "$data/sft_teacher_tagged_train.parquet" \
            "$data/sft_teacher_plain_train.parquet" \
            "$data/sft_teacher_val.parquet" \
            "$data/sft_teacher_build.json"; do
    test -s "$file"
done

"$venv/bin/python" - "$data/sft_teacher_build.json" "$min_accepted" <<'PY'
import json
import sys

report = json.load(open(sys.argv[1]))
minimum = int(sys.argv[2])
assert report["status"] == "prepared"
assert report["positive"]["rows"] >= minimum
assert report["minimum_accepted"] >= minimum
assert report["checks"]["accepted_count_meets_minimum"]
assert report["checks"]["same_train_row_order_and_prompts"]
assert report["checks"]["nonpositive_rows_identical"]
assert report["checks"]["train_val_normalized_question_overlap"] == 0
assert report["validation"]["rows"] == 63
assert report["replay"]["controls"] == 45
assert report["replay"]["by_kind_and_source"] == {
    "replay_th": {"math": 36, "gsm8k": 22, "arc": 13},
    "replay_nt": {"math": 36, "gsm8k": 22, "arc": 13},
}
PY

source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo"
for arm in tagged plain; do
    RUN_ROOT="$runroot" RUN_NAME="exp21-teacher-sol61-${arm}-p8" \
    MODEL="$model" DATA_PATH="$data/sft_teacher_${arm}_train.parquet" \
    VAL_PATH="$data/sft_teacher_val.parquet" \
    NGPUS=1 STEPS=8 SAVE_STEPS=1,2,3,4,5,6,7,8 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
    MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
date -Is > "$data/TRAIN_PAIR_DONE"
