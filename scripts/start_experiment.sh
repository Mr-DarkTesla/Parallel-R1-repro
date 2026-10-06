#!/usr/bin/env bash
# Queue line for an experiment: checks out its branch into /work/exps/<name> and runs it there.
# Usage on the pod: bash scripts/start_experiment.sh <branch> <name> [SFT hydra overrides...]
set -euo pipefail
branch=$1
name=$2
shift 2
git -C /work/parallel-r1 worktree add --force "/work/exps/$name" "$branch"
cd "/work/exps/$name"
bash scripts/run_experiment.sh "$name" "$@"
