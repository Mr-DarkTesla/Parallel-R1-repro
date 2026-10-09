#!/usr/bin/env bash
# Evaluate the matched deep75 SFT arms sequentially on this pod's one GPU.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
test -e /work/exp21/deep_round2/TRAIN_PAIR_DONE

eval_arm() {
    local short=$1 run=$2 model=/work/runs/$2/model
    test -e "$model/config.json"
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-mvth" "$model" dev multiverse-thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-th" "$model" dev thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-nt" "$model" dev no-thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-ifeval-th" "$model" frozen thinking ifeval
    bash scripts/exp21/pod_jobs.sh eval "$short-ifeval-nt" "$model" frozen no-thinking ifeval
}

eval_arm deep75 exp21-sol-deep75
eval_arm deep75-control exp21-sol-deep75-control
date -Is > /work/exp21/deep_round2/EVAL_PAIR_DONE
