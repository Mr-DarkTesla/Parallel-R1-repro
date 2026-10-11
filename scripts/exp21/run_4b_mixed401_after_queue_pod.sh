#!/usr/bin/env bash
# One owned H100. Paired continuation from the matching 4B Sol196 step-16 models.
set -euo pipefail

data=/work/exp21/qwen4b_mixed401
marker=$data/ATTEMPT_DONE
mkdir -p "$data"
exec 9>"$data/runner.lock"
flock -n 9 || { echo 'mixed401 runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$marker"' EXIT
for _ in $(seq 1 7200); do
    test -s /work/exp21/m1_rewrapped_sft/M1_RETRY_ATTEMPT_DONE && break
    sleep 5
done
test -s /work/exp21/m1_rewrapped_sft/M1_RETRY_ATTEMPT_DONE
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py' >/dev/null; then
    echo 'another GPU task is active' >&2
    exit 1
fi
test -s "$data/build_report.json"
test -s "$data/tagged_train.parquet"
test -s "$data/plain_train.parquet"
test -s "$data/tagged_val.parquet"
test -s "$data/plain_val.parquet"
/work/venv/bin/python - "$data/build_report.json" <<'PY'
import json, sys
r=json.load(open(sys.argv[1]))
assert r['status']=='ready_for_paired_sft' and r['distinct_positive']==401
assert r['rows_per_arm']=={'train':2383,'val':50}
assert r['plain_only_removes_tags'] and r['val_overlap']==0
assert r['fixed40_question_overlap']==0
PY

cd /work/parallel-r1
python3 scripts/exp21/evict_own_file_cache_pod.py \
    /tmp/exp21-selective-runs/exp21-4b-sol61-tagged-p16 \
    /tmp/exp21-selective-runs/exp21-4b-sol61-plain-p16 \
    /tmp/exp21-selective-runs/exp21-m1-rewrapped-tagged-p70 \
    /tmp/exp21-selective-runs/exp21-m1-rewrapped-plain-p70 \
    /tmp/exp21-selective-runs/exp21-teacher-sol61-tagged-lr1-p24
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
for arm in tagged plain; do
    parent=/tmp/exp21-selective-runs/exp21-4b-sol61-${arm}-p16/step_models/step_16/model
    test -s "$parent/config.json"
    RUN_ROOT=/tmp/exp21-selective-runs RUN_NAME=exp21-4b-mixed401-${arm}-p128 \
    MODEL="$parent" DATA_PATH="$data/${arm}_train.parquet" \
    VAL_PATH="$data/${arm}_val.parquet" \
    NGPUS=1 STEPS=128 SAVE_STEPS=32,64,96,128 LR=3e-6 BATCH=16 MICRO_BATCH=1 \
    MAX_LENGTH=4096 MIN_FREE_GB=30 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
date -Is > "$data/TRAIN_PAIR_DONE"
for arm in tagged plain; do
    run=/tmp/exp21-selective-runs/exp21-4b-mixed401-${arm}-p128
    test -s "$run/DONE"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="/tmp/exp21-4b-mixed401-${arm}-p128-eval" \
        EXP21_STEPS=128 bash scripts/exp21/eval_checkpoint_steps_pod.sh
done
date -Is > "$data/EVAL_DONE"
