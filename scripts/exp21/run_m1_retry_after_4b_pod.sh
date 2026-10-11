#!/usr/bin/env bash
# Retry M1 after the 4B attempt; all use the same single GPU serially.
set -euo pipefail

data=/work/exp21/m1_rewrapped_sft
marker=$data/M1_RETRY_ATTEMPT_DONE
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$marker"' EXIT

for _ in $(seq 1 7200); do
    test -s /work/exp21/teacher_sft/FOUR_B_RETRY_ATTEMPT_DONE && break
    sleep 5
done
test -s /work/exp21/teacher_sft/FOUR_B_RETRY_ATTEMPT_DONE
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py' >/dev/null; then
    echo 'another GPU task is active' >&2
    exit 1
fi
cd /work/parallel-r1
python3 scripts/exp21/evict_own_file_cache_pod.py \
    /tmp/exp21-selective-runs/exp21-4b-sol61-tagged-p16 \
    /tmp/exp21-selective-runs/exp21-4b-sol61-plain-p16 \
    /tmp/exp21-selective-runs/exp21-m1-rewrapped-tagged-p70 \
    /tmp/exp21-selective-runs/exp21-teacher-sol61-tagged-lr1-p24
bash scripts/exp21/run_m1_rewrapped_pair_pod.sh

for arm in tagged plain; do
    run=/tmp/exp21-selective-runs/exp21-m1-rewrapped-${arm}-p70
    test -s "$run/DONE"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="/tmp/exp21-m1-rewrapped-${arm}-eval" \
        EXP21_STEPS=16,35,70 bash scripts/exp21/eval_checkpoint_steps_pod.sh
done
date -Is > "$data/M1_RETRY_EVAL_DONE"
