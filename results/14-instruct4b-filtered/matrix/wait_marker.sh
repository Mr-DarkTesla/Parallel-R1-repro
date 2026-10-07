#!/usr/bin/env bash
# Read-only bounded poll (<=120 s) for root MIGRATION_READY.json. Logs local gates + pod list. No pod exec, no writes outside this dir.
# Usage: wait_marker.sh [iterations] [sleep_s]   exit 0 marker present, 1 timeout
D=$(cd "$(dirname "$0")" && pwd); P=$D/..; log=$D/wait.log
N=${1:-30}; S=${2:-120}; [ "$S" -le 120 ] || S=120
for i in $(seq "$N"); do
  pods=$(timeout 60 kubectl --context tele.corp.mail.ru-k8s_ml_MNTINFRA_3322 -n shared-dzen-ml --request-timeout=30s get pods -o wide --no-headers 2>&1 \
         | awk '/^vcharkin-exp-vm|rror|nauthor|xpired/{print $1":"$2":"$3":"$7}' | tr '\n' ' ')
  ex=$(grep -c . "$P/executor_continue/progress.md" 2>/dev/null)
  m=$([ -s "$P/MIGRATION_READY.json" ] && echo Y || echo n)
  echo "$(date '+%F %T') migr=$m exec_cont_progress_lines=${ex:-0} exec_cont_resp=$(head -c 60 "$P/executor_continue/response.json" | tr -d '\n') | $pods" >> "$log"
  [ "$m" = Y ] && { echo "MARKER $(date '+%F %T')" >> "$log"; exit 0; }
  sleep "$S"
done
echo "$(date '+%F %T') TIMEOUT" >> "$log"; exit 1
