#!/usr/bin/env bash
# Full matched dev and IFEval for corrected-Qwen-thinking SFT.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
test -e /work/exp21/qwen_rewrite180/TRAIN_DONE
model=/tmp/exp21-qwen-rewrite-runs/exp21-qwen-rewrite180/model
name=qwen-rewrite180
test -e "$model/config.json"
bash scripts/exp21/pod_jobs.sh eval "$name-dev-mvth" "$model" dev multiverse-thinking
bash scripts/exp21/pod_jobs.sh eval "$name-dev-th" "$model" dev thinking
bash scripts/exp21/pod_jobs.sh eval "$name-dev-nt" "$model" dev no-thinking
bash scripts/exp21/pod_jobs.sh eval "$name-ifeval-th" "$model" frozen thinking ifeval
bash scripts/exp21/pod_jobs.sh eval "$name-ifeval-nt" "$model" frozen no-thinking ifeval
date -Is > /work/exp21/qwen_rewrite180/EVAL_DONE
