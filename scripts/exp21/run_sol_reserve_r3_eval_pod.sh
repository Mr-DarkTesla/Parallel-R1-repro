#!/usr/bin/env bash
# Full matched dev and IFEval on one own GPU after both SFT arms finish.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
test -e /work/exp21/sol_r3/TRAIN_PAIR_DONE

eval_arm() {
    local short=$1 run=$2 model=/tmp/exp21-r3-runs/$2/model
    test -e "$model/config.json"
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-mvth" "$model" dev multiverse-thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-th" "$model" dev thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-dev-nt" "$model" dev no-thinking
    bash scripts/exp21/pod_jobs.sh eval "$short-ifeval-th" "$model" frozen thinking ifeval
    bash scripts/exp21/pod_jobs.sh eval "$short-ifeval-nt" "$model" frozen no-thinking ifeval
}

eval_arm reserve-r3 exp21-sol-reserve-r3
eval_arm reserve-r3-control exp21-sol-reserve-r3-control
date -Is > /work/exp21/sol_r3/EVAL_PAIR_DONE
