#!/usr/bin/env bash
# Copy each completed v5 pilot to the local repository without touching GPU work.
set -euo pipefail

repo=$(cd "$(dirname "$0")/../.." && pwd)
archives="$repo/results/21-qwen3-0.6b-multiverse/eval_archives"
pod=vcharkin-exp-vm-0
namespace=shared-dzen-ml

for step in 24 32 40 48 56; do
  local_archive="$archives/selective_v5_step${step}_masked_pilot.tgz"
  if test -s "$local_archive"; then
    printf '%s step_%s already archived\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$step"
    continue
  fi
  until kubectl -n "$namespace" exec "$pod" -- test -f "/tmp/exp21-v5-step-eval/step_${step}/DONE" >/dev/null 2>&1; do
    sleep 30
  done
  kubectl -n "$namespace" exec "$pod" -- tar -czf "/tmp/exp21-v5-step${step}.tgz" -C /tmp/exp21-v5-step-eval "step_${step}"
  for attempt in 1 2 3; do
    if kubectl -n "$namespace" cp "$pod:/tmp/exp21-v5-step${step}.tgz" "$local_archive" --retries=3 &&
       tar -tzf "$local_archive" | grep -q 'block-rows.jsonl'; then
      printf '%s step_%s archived: %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$step" "$local_archive"
      break
    fi
    rm -f "$local_archive"
    if test "$attempt" -eq 3; then
      echo "step_$step archive failed after three attempts" >&2
      exit 1
    fi
    sleep 10
  done
done
