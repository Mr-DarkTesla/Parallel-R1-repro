#!/usr/bin/env bash
# Runs one persistent GPU queue. An interrupted command stays at the head for a restart.
# Usage on the pod: nohup bash scripts/queue_runner.sh <gpu> &
set -uo pipefail
gpu=${1:?GPU index required}
[[ $gpu =~ ^[0-9]+$ ]] || exit 2
queue_dir=${QUEUE_DIR:-/work/queue}
mkdir -p "$queue_dir"
queue=$queue_dir/gpu$gpu.txt
log=$queue_dir/gpu$gpu.log
max_attempts=${MAX_ATTEMPTS:-3}
[[ $max_attempts =~ ^[1-9][0-9]*$ ]] || exit 2
source "${VENV_ACTIVATE:-/work/venv/bin/activate}" || exit 1
touch "$queue"
exec 9>"$queue.runner.lock"
flock -n 9 || { echo "GPU $gpu already has a runner" >&2; exit 1; }
while true; do
    IFS= read -r command < "$queue" || { sleep 30; continue; }
    attempts=0
    if [ -s "$queue.attempts" ] && [ "$(tail -n +2 "$queue.attempts")" = "$command" ]; then
        IFS= read -r attempts < "$queue.attempts"
    fi
    if [ "$attempts" -ge "$max_attempts" ]; then
        status=125
        echo "$(date '+%F %T') RETRY LIMIT $command" >> "$log"
    else
        printf '%s\n%s\n' "$((attempts + 1))" "$command" > "$queue.attempts.tmp" || exit 1
        mv "$queue.attempts.tmp" "$queue.attempts" || exit 1
        echo "$(date '+%F %T') START $command" >> "$log"
        CUDA_VISIBLE_DEVICES=$gpu bash -c "$command" >> "$log" 2>&1
        status=$?
    fi
    echo "$(date '+%F %T') END exit=$status $command" >> "$log"
    # Enqueue uses the same edit lock; an append cannot be lost during the atomic replacement.
    (
        flock 8 || exit 1
        IFS= read -r head < "$queue" || exit 1
        [ "$head" = "$command" ] || exit 1
        if [ "$status" -ne 0 ]; then printf '%s\n' "$command" >> "$queue.failed" || exit 1; fi
        tail -n +2 "$queue" > "$queue.tmp" || exit 1
        mv "$queue.tmp" "$queue" || exit 1
        rm -f "$queue.attempts"
    ) 8>"$queue.edit.lock" || exit 1
done
