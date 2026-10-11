#!/usr/bin/env bash
# Same fixed 40 masked greedy prompts for tagged/plain Deep69 checkpoints.
set -euo pipefail

for step in 8 4; do
  for arm in tagged plain; do
    run=/tmp/exp21-selective-runs/exp21-deep69-${arm}-p8
    test -s "$run/step_models/step_$step/model/config.json"
    EXP21_RUN="$run" \
    EXP21_EVAL_ROOT="/tmp/exp21-deep69-${arm}-p8-eval" \
    EXP21_STEPS="$step" \
      bash /tmp/exp21-eval-v5-checkpoints.sh
  done
done
