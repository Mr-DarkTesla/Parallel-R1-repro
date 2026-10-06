#!/usr/bin/env bash
# Append one command without racing queue_runner.sh. Usage: bash scripts/enqueue.sh <gpu> '<command>'
set -euo pipefail
gpu=${1:?GPU index required}
command=${2:?Command required}
[[ $gpu =~ ^[0-9]+$ && $command != *$'\n'* ]] || exit 2
queue_dir=${QUEUE_DIR:-/work/queue}
mkdir -p "$queue_dir"
queue=$queue_dir/gpu$gpu.txt
exec 8>"$queue.edit.lock"
flock 8
printf '%s\n' "$command" >> "$queue"
