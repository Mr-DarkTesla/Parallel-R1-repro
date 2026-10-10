#!/usr/bin/env bash
# Tag-free matched control after all already queued tagged runs leave the GPU.
set -euo pipefail

while [ ! -e /work/exp21/qwen_rewrite180/lite16/masked_pilot/MASKED_PILOT_DONE ]; do
    sleep 20
done
root=/work/exp21/expanded_th
bash /work/parallel-r1/scripts/exp21/run_expanded_thinking_control_pod.sh m2
bash /work/parallel-r1/scripts/exp21/run_expanded_thinking_control_eval_pod.sh m2
date -Is > "$root/CONTROL_M2_QUEUE_DONE"
