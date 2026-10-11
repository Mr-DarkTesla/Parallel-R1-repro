#!/usr/bin/env bash
# Matched one-GPU eight-step SFT on the independently accepted 78 authored blocks.
set -euo pipefail

repo=/work/parallel-r1
data=/work/exp21/agent_authored_sft
model=/checkpoints/exp21-v4-recovery8/step_8/model
runroot=/tmp/exp21-selective-runs

exec 9>/tmp/exp21-agent-authored-sft.lock
flock -n 9 || { echo "agent-authored SFT already running" >&2; exit 1; }
test -s "$model/config.json"
test -s /checkpoints/exp21-global-top5/GLOBAL_TOP5.json
for file in "$data/sft_agent_authored_tagged_train.parquet" \
            "$data/sft_agent_authored_plain_train.parquet" \
            "$data/sft_agent_authored_val.parquet" \
            "$data/sft_agent_authored_build.json"; do
    test -s "$file"
done

/work/venv/bin/python - "$data/sft_agent_authored_build.json" <<'PY'
import json, sys
report = json.load(open(sys.argv[1]))
assert report["status"] == "prepared"
assert report["positive"]["rows"] == 78
assert report["positive"]["by_source"] == {"gsm8k": 36, "math": 42}
assert report["positive"]["math_by_answer_type"] == {"integer": 17, "expression": 13, "fraction": 12}
assert report["train"]["rows_per_arm"] == 265
assert report["validation"]["rows"] == 63
assert report["checks"]["train_val_normalized_question_overlap"] == 0
PY

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo"
for arm in tagged plain; do
    RUN_ROOT="$runroot" RUN_NAME="exp21-agent-authored-${arm}-p8" \
    MODEL="$model" DATA_PATH="$data/sft_agent_authored_${arm}_train.parquet" \
    VAL_PATH="$data/sft_agent_authored_val.parquet" \
    NGPUS=1 STEPS=8 SAVE_STEPS=1,2,3,4,5,6,7,8 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
    MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
date -Is > "$data/TRAIN_PAIR_DONE"
