#!/usr/bin/env bash
# Matched tag-free control for the selected expanded thinking method.
set -euo pipefail

method=${1:?use m1 or m2}
case "$method" in m1|m2) ;; *) exit 2;; esac
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=${EXP21_GPU:-0} PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
scratch=/tmp/exp21-expanded-th-runs
data=/work/exp21/expanded_th
name=exp21-expanded-th-${method}-control
train=$data/sft_expanded_th_${method}_control_train.parquet
val=$data/sft_expanded_th_${method}_control_val.parquet
test -e "$train" && test -e "$val"
if [ ! -e "$scratch/$name/DONE" ]; then
    if [ -e "$scratch/$name" ]; then
        echo "$scratch/$name exists but is incomplete; inspect before resuming" >&2
        exit 1
    fi
    RUN_ROOT="$scratch" RUN_NAME="$name" DATA_PATH="$train" VAL_PATH="$val" \
      MODEL=/work/assets/models/Qwen3-0.6B-mv NGPUS=1 \
      STEPS=64 LR=1e-5 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
      bash scripts/instruct4b/sft.sh +data.structure=multiverse optim.tag_lr_mult=100
fi
test -e "$scratch/$name/DONE" && test -e "$scratch/$name/model/config.json"
date -Is > "$data/CONTROL_${method}_TRAIN_DONE"
