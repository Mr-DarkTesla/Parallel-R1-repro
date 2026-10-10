#!/usr/bin/env bash
# M1 frontblock: same rows, split, optimizer and schedule as two-path tagweighted.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
repo=/tmp/parallel-r1-eval
data=/work/exp21/expanded_th
pilots=/work/exp21/masked_pilot
run=/tmp/exp21-expanded-th-runs/exp21-expanded-th-m1-frontblock
out=/tmp/exp21-frontblock-eval
train=$data/sft_expanded_th_m1_frontblock_replay3_tagged_train.parquet
val=$data/sft_expanded_th_m1_frontblock_replay3_tagged_val.parquet
test -e "$train" && test -e "$val" && test -e "$repo/scripts/instruct4b/sft.sh"

if [ ! -e "$run/DONE" ]; then
    cd "$repo"
    RUN_ROOT=/tmp/exp21-expanded-th-runs RUN_NAME=exp21-expanded-th-m1-frontblock \
    DATA_PATH="$train" VAL_PATH="$val" MODEL=/work/assets/models/Qwen3-0.6B-mv \
    NGPUS=1 STEPS=64 LR=1e-5 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=0.1 optim.tag_lr_mult=100
fi
test -e "$run/DONE" && test -e "$run/model/config.json"

mkdir -p "$out"
cd "$repo/verl"
export PYTHONPATH="$PWD" EXP21_TOKENIZER="$run/model"
for source in gsm8k_dev10 gsm8k_devnext10 math_dev10 math_devnext10; do
    test -e "$pilots/$source.parquet"
    case "$source" in math_*) budget=4096 ;; *) budget=2048 ;; esac
    if [ -e "$out/$source-block-rows.jsonl" ]; then continue; fi
    python ../scripts/exp21/generate_masked_multiverse.py \
        "$run/model" "$pilots/$source.parquet" "$out/$source.jsonl" 10 "$budget" thinking greedy \
        > "$out/$source.log" 2>&1
    python ../scripts/bench/score.py "$out/$source.jsonl" "$pilots/$source.parquet" \
        "$out/$source-score.json" "$out/$source-rows.jsonl" >> "$out/$source.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
        "$out/$source.jsonl" "$out/$source-rows.jsonl" "$out/$source-blocks.json" \
        "$out/$source-block-rows.jsonl" masked >> "$out/$source.log" 2>&1
done
date -Is > "$out/DONE"
