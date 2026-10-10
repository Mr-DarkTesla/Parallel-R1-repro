#!/usr/bin/env bash
# Full matched dev and IFEval after the balanced one-GPU training pair.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
test -e /work/exp21/deep_balanced/TRAIN_PAIR_DONE
test -z "$(git status --porcelain --untracked-files=no -- scripts verl)"

eval_arm() {
    local short=$1 run=$2 model=/tmp/exp21-balanced-runs/$2/model
    test -e "$model/config.json"
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-mvth" "$model" dev multiverse-thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-th" "$model" dev thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-nt" "$model" dev no-thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-ifeval-th" "$model" frozen thinking ifeval
    bash scripts/exp21/pod_jobs.sh eval "$short-ifeval-nt" "$model" frozen no-thinking ifeval
}

eval_arm deep75-bal exp21-sol-deep75-balanced
eval_arm deep75-bal-control exp21-sol-deep75-balanced-control
date -Is > /work/exp21/deep_balanced/EVAL_PAIR_DONE
