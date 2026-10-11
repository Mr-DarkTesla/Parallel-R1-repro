#!/usr/bin/env bash
# One-GPU causal ablation after the higher-priority 4B mixed401 pair.
set -euo pipefail

data=/work/exp21/teacher_sft
for _ in $(seq 1 7200); do
    test -s /work/exp21/qwen4b_mixed401/ATTEMPT_DONE && break
    sleep 5
done
test -s /work/exp21/qwen4b_mixed401/ATTEMPT_DONE
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer' >/dev/null; then
    echo 'prior SFT trainer remains active' >&2
    exit 1
fi
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
python3 scripts/exp21/evict_own_file_cache_pod.py \
    /tmp/exp21-selective-runs/exp21-m1-rewrapped-tagged-p70 \
    /tmp/exp21-selective-runs/exp21-m1-rewrapped-plain-p70 \
    /tmp/exp21-selective-runs/exp21-teacher-sol61-tagged-lr1-p24
RUN_ROOT=/tmp/exp21-selective-runs RUN_NAME=exp21-teacher-sol61-tagged-lr1-p24 \
MODEL=/checkpoints/exp21-v4-recovery8/step_8/model \
DATA_PATH="$data/sft_teacher_tagged_train.parquet" \
VAL_PATH="$data/sft_teacher_val.parquet" \
NGPUS=1 STEPS=24 SAVE_STEPS=4,8,24 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
MAX_LENGTH=4096 MIN_FREE_GB=10 \
bash scripts/instruct4b/sft.sh +data.structure=multiverse \
    +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=1
date -Is > "$data/LR1_TRAIN_DONE"
EXP21_RUN=/tmp/exp21-selective-runs/exp21-teacher-sol61-tagged-lr1-p24 \
EXP21_EVAL_ROOT=/tmp/exp21-teacher-sol61-tagged-lr1-eval EXP21_STEPS=4,8,24 \
bash scripts/exp21/eval_checkpoint_steps_pod.sh
date -Is > "$data/LR1_EVAL_DONE"
