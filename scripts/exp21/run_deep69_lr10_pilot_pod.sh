#!/usr/bin/env bash
# Fixed 40 masked greedy prompts for conditional LR10 tagged/plain pair.
set -euo pipefail

for arm in tagged plain; do
  run=/tmp/exp21-selective-runs/exp21-deep69-lr10-${arm}-p8
  test -s "$run/step_models/step_8/model/config.json"
  EXP21_RUN="$run" \
  EXP21_EVAL_ROOT="/tmp/exp21-deep69-lr10-${arm}-p8-eval" \
  EXP21_STEPS=8 \
    bash /tmp/exp21-eval-v5-checkpoints.sh
done
