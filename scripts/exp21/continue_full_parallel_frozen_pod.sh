#!/usr/bin/env bash
# Start the selected model's frozen masked evaluation only after full dev succeeds.
set -euo pipefail
root=${EXP21_FULL_ROOT:?}
dev_pid=$(cat "$root/dev-runner.pid")
while ! test -s "$root/DEV_DONE"; do
    if grep -q 'FAILED dev' "$root/progress.log"; then
        echo "dev failed; frozen not started" >&2
        exit 1
    fi
    if ! kill -0 "$dev_pid" 2>/dev/null; then
        echo "dev runner exited without DEV_DONE; frozen not started" >&2
        exit 1
    fi
    sleep 30
done
echo "$(date -Is) dev complete; starting selected-model frozen" >> "$root/progress.log"
exec bash "${EXP21_FULL_CODE:?}/exp21/run_full_parallel_pair_pod.sh" frozen
