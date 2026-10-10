#!/usr/bin/env bash
set -euo pipefail

root=/work/exp21/qwen_rewrite180
while [ ! -e "$root/EVAL_DONE" ]; do
    sleep 20
done
bash /work/parallel-r1/scripts/exp21/run_qwen_rewrite180_masked_pilot_pod.sh
date -Is > "$root/AFTER_EVAL_DONE"
