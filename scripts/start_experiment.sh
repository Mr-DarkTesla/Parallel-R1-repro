#!/usr/bin/env bash
# Queue line for an experiment: checks out its branch into /work/exps/<name> and runs (or resumes) it there.
# Usage on the pod: bash scripts/start_experiment.sh <branch> <name> [SFT hydra overrides...]
set -euo pipefail
runner_repo=$(cd "$(dirname "$0")/.." && pwd)
branch=$1
name=$2
shift 2
[[ $name =~ ^[a-zA-Z0-9][a-zA-Z0-9_.-]*$ ]] || exit 2
work=${PR1_WORK_ROOT:-/work}
run=$work/runs/$name
mkdir -p "$run"
exec 7>"$run/start.lock"
flock -n 7 || { echo "Run $name already has a launcher" >&2; exit 1; }
if [ ! -s "$run/source_commit" ]; then
    if [ -d "$work/exps/$name" ]; then
        git -C "$work/exps/$name" rev-parse HEAD > "$run/source_commit.tmp"
    else
        git -C "$work/parallel-r1" rev-parse "$branch^{commit}" > "$run/source_commit.tmp"
    fi
    mv "$run/source_commit.tmp" "$run/source_commit"
fi
commit=$(cat "$run/source_commit")
if [ -d "$work/exps/$name" ]; then
    [ "$(git -C "$work/exps/$name" rev-parse HEAD)" = "$commit" ] || { echo "Run $name changed source commit" >&2; exit 1; }
    git -C "$work/exps/$name" diff --quiet
    git -C "$work/exps/$name" diff --cached --quiet
else
    git -C "$work/parallel-r1" worktree add -q --detach "$work/exps/$name" "$commit"
fi
cd "$work/exps/$name"
EXPERIMENT_REPO="$work/exps/$name" bash "$runner_repo/scripts/run_experiment.sh" "$name" "$@"
