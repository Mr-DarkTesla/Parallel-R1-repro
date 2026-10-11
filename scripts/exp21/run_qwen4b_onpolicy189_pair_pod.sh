#!/usr/bin/env bash
# One-GPU paired continuation from matched 4B mixed401 step-128 checkpoints.
set -euo pipefail

data=${QWEN4B_PAIR_DATA_ROOT:-/work/exp21/qwen4b_onpolicy189}
onpolicy_root=${QWEN4B_ONPOLICY_ROOT:-/checkpoints/exp21-qwen4b-onpolicy189}
prereq_done=${QWEN4B_PAIR_PREREQ_DONE:-$onpolicy_root/ATTEMPT_DONE}
require_generator=${QWEN4B_PAIR_REQUIRE_GENERATOR:-1}
run_prefix=${QWEN4B_PAIR_RUN_PREFIX:-exp21-4b-onpolicy189}
marker=$data/ATTEMPT_DONE
runroot=/tmp/exp21-selective-runs
[[ "$require_generator" = 0 || "$require_generator" = 1 ]] || { echo 'invalid generator guard' >&2; exit 2; }
[[ "$run_prefix" =~ ^exp21-4b-[a-z0-9-]+$ ]] || { echo 'invalid run prefix' >&2; exit 2; }
mkdir -p "$data"
exec 9>"$data/runner.lock"
flock -n 9 || { echo 'onpolicy189 paired runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$marker"' EXIT

# The previous owner of GPU 0 must finish before either paired continuation.
for _ in $(seq 1 7200); do
    test -s "$prereq_done" && break
    sleep 5
done
test -s "$prereq_done" || { echo "prerequisite unfinished: $prereq_done" >&2; exit 1; }
if [ "$require_generator" = 1 ]; then
    test -s "$onpolicy_root/GENERATION_DONE"
    grep -q ' status=0$' "$onpolicy_root/ATTEMPT_DONE" \
        || { echo "on-policy generator failed: $onpolicy_root/ATTEMPT_DONE" >&2; exit 1; }
fi
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|generate_onpolicy_masked.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU job is active on the owned pod' >&2
    exit 1
fi

test -s "$data/build_report.json"
for arm in tagged plain; do
    test -s "$data/${arm}_train.parquet"
    test -s "$data/${arm}_val.parquet"
done
/work/venv/bin/python - "$data/build_report.json" <<'PY'
import json, sys

report = json.load(open(sys.argv[1]))
assert report['status'] == 'ready_for_paired_onpolicy_sft'
assert report['accepted']['semantic_path_independence'] == 'reviewed'
assert report['accepted']['count'] >= 30
assert report['rows_per_arm']['val'] == 50
train = report['train']
assert report['rows_per_arm']['train'] == (
    train['positive_rows'] + train['replay_thinking'] + train['replay_no_thinking'])
assert train['positive_rows'] == report['accepted']['count'] * train['positive_copies']
checks = report['checks']
assert checks['same_order']
assert checks['plain_equals_tagged_after_removing_only_tags']
assert checks['candidate_eval_leakcheck'] == 'passed'
assert checks['train_validation_question_overlap'] == 0
assert checks['train_fixed40_question_overlap'] == 0
assert all(size <= 4096 for arm in checks['max_total_tokens'].values() for size in arm.values())
PY

cd /work/parallel-r1
for arm in tagged plain; do
    parent="$runroot/exp21-4b-mixed401-${arm}-p128/step_models/step_128/model"
    test -s "$parent/config.json"
done
# Explicit validated roots only; cache advice releases pages, never model files.
python3 scripts/exp21/evict_own_file_cache_pod.py \
    "$runroot/exp21-4b-mixed401-tagged-p128" \
    "$runroot/exp21-4b-mixed401-plain-p128" \
    "$runroot/exp21-4b-focus34-tagged-p32" \
    "$runroot/exp21-4b-focus34-plain-p32"

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
for arm in tagged plain; do
    parent="$runroot/exp21-4b-mixed401-${arm}-p128/step_models/step_128/model"
    RUN_ROOT="$runroot" RUN_NAME="${run_prefix}-${arm}-p32" \
    MODEL="$parent" DATA_PATH="$data/${arm}_train.parquet" \
    VAL_PATH="$data/${arm}_val.parquet" \
    NGPUS=1 STEPS=32 SAVE_STEPS=8,16,32 LR=5e-7 BATCH=16 MICRO_BATCH=1 \
    MAX_LENGTH=4096 MIN_FREE_GB=30 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
date -Is > "$data/TRAIN_PAIR_DONE"

for arm in tagged plain; do
    run="$runroot/${run_prefix}-${arm}-p32"
    test -s "$run/DONE"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="/tmp/${run_prefix}-${arm}-p32-eval" \
        EXP21_STEPS=8,16,32 bash scripts/exp21/eval_checkpoint_steps_pod.sh
done
date -Is > "$data/EVAL_DONE"
