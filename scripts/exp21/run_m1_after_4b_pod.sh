#!/usr/bin/env bash
# Start the 0.6B M1-367 matched run after the serial 4B pair process exits.
set -euo pipefail

pidfile=/work/exp21/teacher_sft/four_b_pair.pid
test -s "$pidfile"
pid=$(cat "$pidfile")
for _ in $(seq 1 7200); do
    state=$(ps -p "$pid" -o stat= 2>/dev/null | tr -d ' ' || true)
    case "$state" in ""|Z*) break ;; esac
    sleep 5
done
state=$(ps -p "$pid" -o stat= 2>/dev/null | tr -d ' ' || true)
case "$state" in ""|Z*) ;; *) echo "4B pair still running: $state" >&2; exit 1 ;; esac
for _ in $(seq 1 120); do
    if ! pgrep -f 'torchrun.*fsdp_parallel_sft_trainer' >/dev/null; then break; fi
    sleep 5
done
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer' >/dev/null; then
    echo "prior SFT trainer remains active" >&2
    exit 1
fi
cd /work/parallel-r1
bash scripts/exp21/run_m1_rewrapped_pair_pod.sh
