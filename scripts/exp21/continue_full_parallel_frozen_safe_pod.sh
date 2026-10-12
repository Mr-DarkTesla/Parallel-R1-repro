#!/usr/bin/env bash
# Continue frozen evaluation on GPUs released by dev and APO, without overlap.
set -euo pipefail

root=${EXP21_FULL_ROOT:?}
code=${EXP21_FULL_CODE:?}
runner="$code/exp21/run_full_parallel_pair_pod.sh"
dev_pid=$(cat "$root/dev-runner.pid")

while ! test -s "$root/DEV_DONE"; do
    if grep -q 'FAILED dev' "$root/progress.log"; then
        echo 'dev failed; frozen continuation stopped' >&2
        exit 1
    fi
    if ! kill -0 "$dev_pid" 2>/dev/null; then
        echo 'dev runner exited without DEV_DONE' >&2
        exit 1
    fi
    sleep 30
done

echo "$(date -Is) dev complete; ARC assigned GPU 3" | tee -a "$root/progress.log"
EXP21_ONLY_BENCHMARK=arc EXP21_ONLY_GPU=3 bash "$runner" frozen &
arc_pid=$!

(
    while ! test -s "$root/output/frozen/parallel/apo/DONE"; do
        if grep -q 'FAILED frozen' "$root/progress.log"; then
            echo 'APO failed; IFEval not started' >&2
            exit 1
        fi
        sleep 30
    done
    echo "$(date -Is) APO complete; IFEval assigned GPU 1" | tee -a "$root/progress.log"
    EXP21_ONLY_BENCHMARK=ifeval EXP21_ONLY_GPU=1 bash "$runner" frozen
) &
ifeval_pid=$!

wait "$arc_pid"
wait "$ifeval_pid"

for bench in apo arc mmlu_pro limo ifeval; do
    while ! test -s "$root/output/frozen/parallel/$bench/DONE"; do
        if grep -q 'FAILED frozen' "$root/progress.log"; then
            echo "frozen failed before $bench completed" >&2
            exit 1
        fi
        sleep 30
    done
done
printf '%s\n' "$(date -Is) commit=$EXP21_COMMIT" > "$root/FROZEN_DONE"
echo "$(date -Is) STAGE_DONE frozen" | tee -a "$root/progress.log"
