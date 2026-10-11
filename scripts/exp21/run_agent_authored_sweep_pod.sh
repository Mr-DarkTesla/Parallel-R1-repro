#!/usr/bin/env bash
# Same fixed40 masked greedy pilot for every tagged/plain eight-step export.
set -euo pipefail

exec 9>/tmp/exp21-agent-authored-eval.lock
flock -n 9 || { echo "agent-authored evaluation already running" >&2; exit 1; }
test -s /work/exp21/agent_authored_sft/TRAIN_PAIR_DONE
for arm in tagged plain; do
    run=/tmp/exp21-selective-runs/exp21-agent-authored-${arm}-p8
    test -s "$run/DONE"
done

for step in 8 4 6 2 1 3 5 7; do
    for arm in tagged plain; do
        run=/tmp/exp21-selective-runs/exp21-agent-authored-${arm}-p8
        outroot=/tmp/exp21-agent-authored-${arm}-eval
        if [ -s "$outroot/step_$step/DONE" ]; then
            continue
        fi
        EXP21_RUN="$run" EXP21_EVAL_ROOT="$outroot" EXP21_STEPS="$step" \
            bash /work/parallel-r1/scripts/exp21/eval_checkpoint_steps_pod.sh
    done
done
date -Is > /work/exp21/agent_authored_sft/SWEEP_DONE
