#!/usr/bin/env bash
# Keep one GPU busy without overlapping the expanded M1/M2 masked pilot.
set -euo pipefail

root=/work/exp21/qwen_rewrite180
pilot=/work/exp21/expanded_th/masked_pilot/MASKED_PILOT_DONE
mkdir -p "$root"
while [ ! -e "$pilot" ]; do
    sleep 20
done
date -Is > "$root/STARTED_AFTER_PILOT"
bash /work/parallel-r1/scripts/exp21/run_qwen_rewrite180_sft_pod.sh
bash /work/parallel-r1/scripts/exp21/run_qwen_rewrite180_eval_pod.sh
date -Is > "$root/QUEUE_DONE"
