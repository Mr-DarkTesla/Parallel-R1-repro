#!/usr/bin/env bash
# Runs one 2-GPU command on two idle single-GPU queues and keeps both queues occupied until it ends.
# Usage on the pod (detached, e.g. setsid nohup ... &):
#   bash scripts/instruct4b/gpu_pair.sh <g1> <g2> <name> <command...>
# Under both queue edit locks (as scripts/enqueue.sh on A/B): each queue must be empty, its runner's last log entry END,
# and its GPU without memory or processes. Then a hold line (this script with "hold") goes to both queues; the command
# starts with CUDA_VISIBLE_DEVICES=<g1>,<g2> only after both runners have started their hold, and the holds end when
# the command ends or its owner process is gone. Runners and other queues are not touched.
# Markers and log: /work/runs/pairs/<name>/{owner, hold-<g>, finished, pair.log}; a second start with the same name refuses.
set -euo pipefail
queues=${QUEUE_DIR:-/work/queue}

if [ "$1" = hold ]; then  # hold <dir> <gpu>: run by a queue runner
    dir=$2
    echo "$(date '+%F %T') hold gpu$3" > "$dir/hold-$3"
    while [ ! -e "$dir/finished" ]; do
        kill -0 "$(cut -d' ' -f1 "$dir/owner")" 2>/dev/null || { echo "owner of $dir is gone"; exit 1; }
        sleep 30
    done
    exit 0
fi

g1=$1 g2=$2 name=$3
shift 3
dir=${PAIRS_DIR:-/work/runs/pairs}/$name
mkdir -p "$(dirname "$dir")"
mkdir "$dir" || { echo "$dir exists: one owner per name"; exit 1; }
exec >> "$dir/pair.log" 2>&1
echo "$(date '+%F %T') $$ pair gpu$g1,gpu$g2: $*"
echo "$$ $(hostname) $(date '+%F %T')" > "$dir/owner"
finish() { status=$?; echo "$status $(date '+%F %T')" > "$dir/finished.tmp"; mv "$dir/finished.tmp" "$dir/finished"; echo "$(date '+%F %T') finished exit=$status"; }
trap finish EXIT

idle() {  # queue empty, runner finished its last command, GPU without memory and processes
    local g=$1
    [ ! -s "$queues/gpu$g.txt" ] || { echo "gpu$g queue not empty"; return 1; }
    ! grep -E " (START|END) " "$queues/gpu$g.log" 2>/dev/null | tail -1 | grep -q " START " || { echo "gpu$g runner busy"; return 1; }
    [ -z "$(nvidia-smi -i "$g" --query-compute-apps=pid --format=csv,noheader)" ] || { echo "gpu$g has processes"; return 1; }
    [ "$(nvidia-smi -i "$g" --query-gpu=memory.used --format=csv,noheader,nounits)" -lt 100 ] || { echo "gpu$g memory used"; return 1; }
}

exec 7>"$queues/gpu$g1.txt.edit.lock" 8>"$queues/gpu$g2.txt.edit.lock"
flock -w 60 7
flock -w 60 8
idle "$g1"
idle "$g2"
for g in "$g1" "$g2"; do printf '%s\n' "bash $(realpath "$0") hold $dir $g" >> "$queues/gpu$g.txt"; done
flock -u 8
flock -u 7
echo "$(date '+%F %T') holds queued"

for _ in $(seq 40); do [ -e "$dir/hold-$g1" ] && [ -e "$dir/hold-$g2" ] && break; sleep 5; done
[ -e "$dir/hold-$g1" ] && [ -e "$dir/hold-$g2" ] || { echo "holds did not start in 200 s"; exit 1; }
for g in "$g1" "$g2"; do [ -z "$(nvidia-smi -i "$g" --query-compute-apps=pid --format=csv,noheader)" ] || { echo "gpu$g busy"; exit 1; }; done
echo "$(date '+%F %T') start"
CUDA_VISIBLE_DEVICES=$g1,$g2 "$@"
