#!/usr/bin/env bash
# Read-only bounded poll (<=120 s) of 13-control on A (executor_launch owns it). Exit 0 when /work/runs/13-control/DONE exists.
# Usage: wait13.sh [iterations] [sleep_s]
D=$(cd "$(dirname "$0")" && pwd); P=$D/..; log=$D/wait13.log
N=${1:-4}; S=${2:-120}; [ "$S" -le 120 ] || S=120
for i in $(seq "$N"); do
  out=$(timeout 90 "$P/executor/k.sh" vcharkin-exp-vm-a-0 "r=/work/runs/13-control; echo pair: \$(tail -n 1 /work/runs/pairs/13-control/pair.log 2>&1 | cut -c1-120)
    echo files: \$(ls \$r 2>&1 | tr '\n' ' '); grep -aE 'micro|updates' \$r/results/recipe.txt 2>/dev/null | cut -c1-200 | head -3
    tr '\r' '\n' < \$r/train.log 2>/dev/null | grep -aoE 'step:[0-9]+ - [^ ]*loss:[0-9.]+' | tail -n 1
    tr '\r' '\n' < \$r/train.log 2>/dev/null | grep -aE 'OutOfMemory|CUDA out of memory|Traceback' | tail -n 1 | cut -c1-200" 2>&1 | grep -v setlocale | tr '\n' ' ')
  echo "$(date '+%F %T') $out" >> "$log"
  case $out in *files:*DONE*) echo "DONE13 $(date '+%F %T')" >> "$log"; exit 0 ;; esac
  sleep "$S"
done
exit 1
