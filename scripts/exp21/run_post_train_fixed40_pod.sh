#!/usr/bin/env bash
# Evaluate the queued M1-367 and 4B-Sol61 pairs after all training leaves the GPU.
set -euo pipefail

pid=$(cat /work/exp21/m1_rewrapped_sft/train_pair.pid)
for _ in $(seq 1 7200); do
    state=$(ps -p "$pid" -o stat= 2>/dev/null | tr -d ' ' || true)
    case "$state" in ""|Z*) break ;; esac
    sleep 5
done
state=$(ps -p "$pid" -o stat= 2>/dev/null | tr -d ' ' || true)
case "$state" in ""|Z*) ;; *) echo "M1 SFT queue still running" >&2; exit 1 ;; esac

for spec in \
    'm1-rewrapped tagged 70' \
    'm1-rewrapped plain 70' \
    '4b-sol61 tagged 16' \
    '4b-sol61 plain 16'; do
    read -r family arm step <<< "$spec"
    run="/tmp/exp21-selective-runs/exp21-${family}-${arm}-p${step}"
    if ! test -s "$run/DONE"; then
        echo "skip unfinished run: $run"
        continue
    fi
    out="/tmp/exp21-${family}-${arm}-eval"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="$out" EXP21_STEPS="$step" \
        bash /work/parallel-r1/scripts/exp21/eval_checkpoint_steps_pod.sh
done
date -Is > /work/exp21/m1_rewrapped_sft/POST_TRAIN_EVAL_DONE
