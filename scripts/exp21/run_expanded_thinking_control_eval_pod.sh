#!/usr/bin/env bash
# Matched full dev and IFEval for selected tag-free control on one own GPU.
set -euo pipefail

method=${1:?use m1 or m2}
case "$method" in m1|m2) ;; *) exit 2;; esac
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=${EXP21_GPU:-0} PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
test -e "/work/exp21/expanded_th/CONTROL_${method}_TRAIN_DONE"
model=/tmp/exp21-expanded-th-runs/exp21-expanded-th-${method}-control/model
name=expanded-th-${method}-control
test -e "$model/config.json"
bash scripts/exp21/pod_jobs.sh eval "$name-dev-mvth" "$model" dev multiverse-thinking
bash scripts/exp21/pod_jobs.sh eval "$name-dev-th" "$model" dev thinking
bash scripts/exp21/pod_jobs.sh eval "$name-dev-nt" "$model" dev no-thinking
bash scripts/exp21/pod_jobs.sh eval "$name-ifeval-th" "$model" frozen thinking ifeval
bash scripts/exp21/pod_jobs.sh eval "$name-ifeval-nt" "$model" frozen no-thinking ifeval
date -Is > "/work/exp21/expanded_th/CONTROL_${method}_EVAL_DONE"
