#!/usr/bin/env bash
# Matched full dev and IFEval on one own GPU for expanded inside-thinking M1/M2.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
test -e /work/exp21/expanded_th/TRAIN_PAIR_DONE

eval_one() {
    local method=$1 model=/tmp/exp21-expanded-th-runs/exp21-expanded-th-$1/model
    local name=expanded-th-$method
    test -e "$model/config.json"
    bash scripts/exp21/pod_jobs.sh eval "$name-dev-mvth" "$model" dev multiverse-thinking
    bash scripts/exp21/pod_jobs.sh eval "$name-dev-th" "$model" dev thinking
    bash scripts/exp21/pod_jobs.sh eval "$name-dev-nt" "$model" dev no-thinking
    bash scripts/exp21/pod_jobs.sh eval "$name-ifeval-th" "$model" frozen thinking ifeval
    bash scripts/exp21/pod_jobs.sh eval "$name-ifeval-nt" "$model" frozen no-thinking ifeval
}

eval_one m1
eval_one m2
date -Is > /work/exp21/expanded_th/EVAL_PAIR_DONE
