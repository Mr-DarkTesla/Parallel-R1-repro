#!/usr/bin/env bash
# Serial retry after the M1 fixed40 queue, with BF16 FSDP checkpoint export.
set -euo pipefail

data=/work/exp21/teacher_sft
marker=$data/FOUR_B_RETRY_ATTEMPT_DONE
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$marker"' EXIT

for _ in $(seq 1 7200); do
    test -s /work/exp21/m1_rewrapped_sft/POST_TRAIN_EVAL_DONE && break
    sleep 5
done
test -s /work/exp21/m1_rewrapped_sft/POST_TRAIN_EVAL_DONE
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py' >/dev/null; then
    echo 'another GPU task is active' >&2
    exit 1
fi
grep -q 'Convert each CPU tensor before serialization' \
    /work/parallel-r1/verl/verl/trainer/fsdp_parallel_sft_trainer.py
cd /work/parallel-r1
bash scripts/exp21/run_4b_teacher_pair_pod.sh

for arm in tagged plain; do
    run=/tmp/exp21-selective-runs/exp21-4b-sol61-${arm}-p16
    test -s "$run/DONE"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="/tmp/exp21-4b-sol61-${arm}-eval" \
        EXP21_STEPS=4,8,16 bash scripts/exp21/eval_checkpoint_steps_pod.sh
done
date -Is > "$data/FOUR_B_RETRY_EVAL_DONE"
