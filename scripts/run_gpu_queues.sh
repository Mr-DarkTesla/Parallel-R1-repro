#!/usr/bin/env bash
# Container entrypoint: restart the pod if either persistent GPU runner exits.
set -euo pipefail
count=${1:?GPU count required}
[[ $count =~ ^[1-9][0-9]*$ ]] || exit 2
repo=$(cd "$(dirname "$0")/.." && pwd)
pids=()
stop_runners() {
    for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done
    wait || true
}
trap stop_runners EXIT
trap 'exit 143' TERM
trap 'exit 130' INT
for ((gpu=0; gpu<count; gpu++)); do
    bash "$repo/scripts/queue_runner.sh" "$gpu" &
    pids+=("$!")
done
wait -n || true
exit 1
