#!/usr/bin/env bash
# Wait for the existing 0.6B fixed40 runner, then evaluate the selected 4B pair.
set -euo pipefail

previous=/work/exp21/q06_distill447
root=/checkpoints/exp21-qwen4b-clean46-full-dev
mkdir -p "$root"
exec 9>"$root/launch.lock"
flock -n 9 || { echo 'clean46 full-dev launcher already active' >&2; exit 1; }

until test -s "$previous/EVAL_DONE" && grep -q 'status=0' "$previous/ATTEMPT_DONE" 2>/dev/null; do
    if test -s "$previous/ATTEMPT_DONE"; then
        echo "previous runner did not complete successfully: $(cat "$previous/ATTEMPT_DONE")" >&2
        exit 1
    fi
    sleep 15
done

test "$(hostname)" = vcharkin-exp-vm-0
test -s /work/exp21/qwen4b_clean46/EVAL_DONE
test -s /tmp/exp21-eval-code/scripts/exp21/run_qwen4b_selected_full_dev_pod.sh
echo "$(date -Is) previous run complete; starting matched clean46 full dev"

EXP21_REPO=/tmp/exp21-eval-code \
FOCUS34_ROOT="$previous" \
QWEN4B_FULL_DEV_ROOT="$root" \
SELECTED_RUN=/tmp/exp21-selective-runs/exp21-4b-clean46-tagged-p32 \
PLAIN_RUN=/tmp/exp21-selective-runs/exp21-4b-clean46-plain-p32 \
SELECTED_STEP=32 PLAIN_STEP=32 INCLUDE_BASE=1 RUN_MASKED_BLOCKS=0 \
EVAL_BUDGET=16384 EXP21_GPU=0 \
bash /tmp/exp21-eval-code/scripts/exp21/run_qwen4b_selected_full_dev_pod.sh
