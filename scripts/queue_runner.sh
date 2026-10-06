#!/usr/bin/env bash
# Runs experiment commands for one GPU from /work/queue/gpu<N>.txt, one line at a time, so the GPU never waits for us.
# Usage on the pod: nohup bash scripts/queue_runner.sh <gpu> &
gpu=$1
queue=/work/queue/gpu$gpu.txt
log=/work/queue/gpu$gpu.log
source /work/venv/bin/activate
touch "$queue"
while true; do
    command=$(head -n 1 "$queue")
    if [ -z "$command" ]; then sleep 30; continue; fi
    sed -i 1d "$queue"
    echo "$(date '+%F %T') START $command" >> "$log"
    CUDA_VISIBLE_DEVICES=$gpu bash -c "$command" >> "$log" 2>&1
    echo "$(date '+%F %T') END exit=$? $command" >> "$log"
done
