#!/usr/bin/env bash
set -euo pipefail

root=/work/exp21/qwen_rewrite180
while [ ! -e "$root/masked_pilot/MASKED_PILOT_DONE" ]; do
    sleep 20
done
bash /work/parallel-r1/scripts/exp21/run_qwen_rewrite180_lite16_pod.sh
date -Is > "$root/lite16/QUEUE_DONE"
