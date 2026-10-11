#!/usr/bin/env bash
# Matched 70-step one-GPU SFT on 367 reviewed M1 solutions rewrapped inside think.
set -euo pipefail

repo=/work/parallel-r1
data=/work/exp21/m1_rewrapped_sft
model=/checkpoints/exp21-v4-recovery8/step_8/model
runroot=/tmp/exp21-selective-runs

exec 9>/tmp/exp21-m1-rewrapped-sft.lock
flock -n 9 || { echo "M1 rewrapped SFT already running" >&2; exit 1; }
test -s "$model/config.json"
test -s /checkpoints/exp21-global-top5/GLOBAL_TOP5.json
for file in "$data/sft_m1_rewrapped_tagged_train.parquet" \
            "$data/sft_m1_rewrapped_plain_train.parquet" \
            "$data/sft_m1_rewrapped_tagged_val.parquet" \
            "$data/sft_m1_rewrapped_plain_val.parquet" \
            "$data/m1_rewrapped_report.json"; do
    test -s "$file"
done

/work/venv/bin/python - "$data/m1_rewrapped_report.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
assert r['status'] == 'validated_cpu_only'
assert r['positive_distinct'] == 367
assert r['rows_each_arm'] == {'total': 2301, 'train': 2251, 'val': 50}
assert r['transform']['grammar_and_placement'].startswith('367/367')
assert r['transform']['math_verify'] == '367/367'
assert r['pairing']['same_ids_order_prompts_thinking_mode']
assert r['pairing']['replay_identical']
assert r['validation']['train_val_id_overlap'] == 0
PY

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo"
for arm in tagged plain; do
    RUN_ROOT="$runroot" RUN_NAME="exp21-m1-rewrapped-${arm}-p70" \
    MODEL="$model" DATA_PATH="$data/sft_m1_rewrapped_${arm}_train.parquet" \
    VAL_PATH="$data/sft_m1_rewrapped_${arm}_val.parquet" \
    NGPUS=1 STEPS=70 SAVE_STEPS=16,35,70 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
    MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
date -Is > "$data/TRAIN_PAIR_DONE"
