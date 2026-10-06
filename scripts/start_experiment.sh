#!/usr/bin/env bash
# Queue line for an experiment: checks out its branch into /work/exps/<name> and runs (or resumes) it there.
# Usage on the pod: bash scripts/start_experiment.sh <branch> <name> [SFT hydra overrides...]
set -euo pipefail
branch=$1
name=$2
shift 2
if [ -d "/work/exps/$name" ]; then
    git -C "/work/exps/$name" checkout -q --force --detach "$branch"
else
    git -C /work/parallel-r1 worktree add -q --force --detach "/work/exps/$name" "$branch"
fi
cd "/work/exps/$name"
bash scripts/run_experiment.sh "$name" "$@"
