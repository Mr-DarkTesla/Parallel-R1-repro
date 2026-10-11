#!/usr/bin/env bash
# Wait for the matched Sol6.1 SFT pair, then evaluate both step-24 exports on fixed40.
set -euo pipefail

data=/work/exp21/teacher_sft
runroot=/tmp/exp21-selective-runs
for _ in $(seq 1 600); do
    test -s "$data/TRAIN_PAIR_DONE" && break
    sleep 5
done
test -s "$data/TRAIN_PAIR_DONE"
for arm in tagged plain; do
    run="$runroot/exp21-teacher-sol61-${arm}-p24"
    test -s "$run/DONE"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="/tmp/exp21-teacher-sol61-${arm}-eval" EXP21_STEPS=24 \
        bash /work/parallel-r1/scripts/exp21/eval_checkpoint_steps_pod.sh
done
date -Is > "$data/STEP24_PILOT_DONE"
