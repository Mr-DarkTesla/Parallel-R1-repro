#!/usr/bin/env bash
# Queue masked pilot immediately after the already-running paired evaluation.
set -euo pipefail
while [ ! -e /work/exp21/expanded_th/EVAL_PAIR_DONE ]; do sleep 15; done
bash /work/parallel-r1/scripts/exp21/run_expanded_thinking_masked_pilot_pod.sh
