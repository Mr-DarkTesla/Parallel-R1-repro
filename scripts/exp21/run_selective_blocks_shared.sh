#!/usr/bin/env bash
# Same SFT/pilot as run_selective_blocks_pod.sh on the personal shared pod.
set -euo pipefail

venv=${EXP21_VENV:-/tmp/exp21_venv}
work=${EXP21_WORK:-/tmp/exp21_overlay/work}
repo=${EXP21_REPO:-/tmp/parallel-r1-eval}
source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
data=$work/exp21/expanded_th
pilots=$work/exp21/masked_pilot
runroot=/tmp/exp21-selective-runs
name=${EXP21_RUN_NAME:-exp21-m1-selective-text1}
run=$runroot/$name
out=${EXP21_EVAL_OUT:-/tmp/exp21-selective-eval}
prefix=${EXP21_DATA_PREFIX:-sft_selective_blocks_m1_text1}
train=$data/${prefix}_train.parquet
val=$data/${prefix}_val.parquet
test -e "$train" && test -e "$val" && test -e "$work/assets/models/Qwen3-0.6B-mv/config.json"
test -e "$pilots/gsm8k_dev10.parquet" && test -e "$pilots/math_devnext10.parquet"
test -e "$repo/scripts/tag_validator.py" && test -e "$repo/scripts/bench/score.py"

if [ ! -e "$run/DONE" ]; then
    if [ -e "$run" ]; then
        echo "Incomplete run exists at $run; inspect before resuming" >&2
        exit 1
    fi
    cd "$repo"
    RUN_ROOT="$runroot" RUN_NAME="$name" DATA_PATH="$train" VAL_PATH="$val" \
    MODEL=$work/assets/models/Qwen3-0.6B-mv NGPUS=1 \
    STEPS=64 LR=1e-5 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
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
