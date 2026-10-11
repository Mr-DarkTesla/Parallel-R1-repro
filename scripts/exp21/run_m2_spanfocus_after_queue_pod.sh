#!/usr/bin/env bash
# One owned H100, after mixed401 and the already queued tag-lr=1 ablation.
# Isolates focused CE against the existing all-CE M2 tagged/plain controls.
set -euo pipefail

data=/work/exp21/expanded_th
run=/tmp/exp21-selective-runs/exp21-m2-spanfocus-tagged-p64
marker=$data/M2_SPANFOCUS_ATTEMPT_DONE
exec 9>/tmp/exp21-m2-spanfocus.lock
flock -n 9 || { echo 'M2 spanfocus runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$marker"' EXIT

for _ in $(seq 1 7200); do
    test -s /work/exp21/teacher_sft/LR1_EVAL_DONE && break
    sleep 5
done
test -s /work/exp21/teacher_sft/LR1_EVAL_DONE
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py' >/dev/null; then
    echo 'another GPU task is active' >&2
    exit 1
fi
test -s /work/assets/models/Qwen3-0.6B-mv/config.json
test -s "$data/sft_expanded_th_m2_tagged_train.parquet"
test -s "$data/sft_expanded_th_m2_tagged_val.parquet"
test -s /work/parallel-r1/scripts/exp21/check_span_focused_mask.py
grep -q 'parallel_text_loss_scope' /work/parallel-r1/verl/verl/utils/dataset/parallel_thinking_sft_dataset.py

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
PYTHONPATH=verl python scripts/exp21/check_span_focused_mask.py
python3 scripts/exp21/evict_own_file_cache_pod.py \
    /tmp/exp21-selective-runs/exp21-m1-rewrapped-tagged-p70 \
    /tmp/exp21-selective-runs/exp21-m1-rewrapped-plain-p70 \
    /tmp/exp21-selective-runs/exp21-4b-mixed401-tagged-p128 \
    /tmp/exp21-selective-runs/exp21-4b-mixed401-plain-p128

if [ ! -s "$run/DONE" ]; then
    test ! -e "$run" || { echo "incomplete run exists: $run" >&2; exit 1; }
    RUN_ROOT=/tmp/exp21-selective-runs RUN_NAME=exp21-m2-spanfocus-tagged-p64 \
    MODEL=/work/assets/models/Qwen3-0.6B-mv \
    DATA_PATH="$data/sft_expanded_th_m2_tagged_train.parquet" \
    VAL_PATH="$data/sft_expanded_th_m2_tagged_val.parquet" \
    NGPUS=1 STEPS=64 SAVE_STEPS=16,32,64 LR=1e-5 BATCH=32 MICRO_BATCH=4 \
    MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_scope=parallel_block \
        +data.parallel_text_loss_weight=0.1 optim.tag_lr_mult=100
fi
test -s "$run/DONE"
EXP21_RUN="$run" EXP21_EVAL_ROOT=/tmp/exp21-m2-spanfocus-tagged-eval \
    EXP21_STEPS=16,32,64 bash scripts/exp21/eval_checkpoint_steps_pod.sh
date -Is > "$data/M2_SPANFOCUS_EVAL_DONE"
