#!/usr/bin/env bash
# Paired 4B continuation after the single-GPU M2 queue, using reviewed native traces.
set -euo pipefail

data=/work/exp21/qwen4b_focus34
marker=$data/ATTEMPT_DONE
mkdir -p "$data"
exec 9>"$data/runner.lock"
flock -n 9 || { echo 'focus34 runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$marker"' EXIT

for _ in $(seq 1 7200); do
    test -s /work/exp21/expanded_th/M2_SPANFOCUS_ATTEMPT_DONE && break
    sleep 5
done
test -s /work/exp21/expanded_th/M2_SPANFOCUS_EVAL_DONE
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py' >/dev/null; then
    echo 'another GPU task is active' >&2
    exit 1
fi
test -s "$data/build_report.json"
for arm in tagged plain; do
    test -s "$data/${arm}_train.parquet"
    test -s "$data/${arm}_val.parquet"
done
/work/venv/bin/python - "$data/build_report.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
assert r['status'] == 'ready_for_paired_continuation'
assert r['rows_per_arm'] == {'train': 231, 'val': 50}
assert r['checks']['fixed40_normalized_question_overlap'] == 0
assert r['checks']['validation_normalized_question_overlap'] == 0
assert r['checks']['plain_equals_tagged_after_removing_only_10_tag_types']
PY

cd /work/parallel-r1
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
python3 scripts/exp21/evict_own_file_cache_pod.py \
    /tmp/exp21-selective-runs/exp21-4b-mixed401-tagged-p128 \
    /tmp/exp21-selective-runs/exp21-4b-mixed401-plain-p128 \
    /tmp/exp21-selective-runs/exp21-m2-spanfocus-tagged-p64

for arm in tagged plain; do
    parent=/tmp/exp21-selective-runs/exp21-4b-mixed401-${arm}-p128/step_models/step_128/model
    test -s "$parent/config.json"
    RUN_ROOT=/tmp/exp21-selective-runs RUN_NAME=exp21-4b-focus34-${arm}-p32 \
    MODEL="$parent" DATA_PATH="$data/${arm}_train.parquet" \
    VAL_PATH="$data/${arm}_val.parquet" \
    NGPUS=1 STEPS=32 SAVE_STEPS=8,16,32 LR=1e-6 BATCH=16 MICRO_BATCH=1 \
    MAX_LENGTH=4096 MIN_FREE_GB=30 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
date -Is > "$data/TRAIN_PAIR_DONE"

for arm in tagged plain; do
    run=/tmp/exp21-selective-runs/exp21-4b-focus34-${arm}-p32
    test -s "$run/DONE"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="/tmp/exp21-4b-focus34-${arm}-p32-eval" \
        EXP21_STEPS=32 bash scripts/exp21/eval_checkpoint_steps_pod.sh
done
date -Is > "$data/EVAL_DONE"
