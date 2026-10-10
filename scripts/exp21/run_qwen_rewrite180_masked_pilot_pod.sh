#!/usr/bin/env bash
# Forty fixed dev questions, autonomous decoding with independent Path masks.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export PYTHONPATH=/work/parallel-r1/verl:/work/assets/ifeval/pkg
export NLTK_DATA=/work/assets/ifeval/nltk_data SCORE_IFEVAL_SEED=0
model=${EXP21_PILOT_MODEL:-/tmp/exp21-qwen-rewrite-runs/exp21-qwen-rewrite180/model}
data=/work/exp21/masked_pilot
out=${EXP21_PILOT_OUT:-/work/exp21/qwen_rewrite180/masked_pilot}
test -e "${EXP21_PILOT_READY:-/work/exp21/qwen_rewrite180/EVAL_DONE}"
test -e "$model/config.json"
mkdir -p "$out"
cd /work/parallel-r1/verl
export EXP21_TOKENIZER="$model"

run_one() {
    local short=$1 source=$2 budget=$3
    local test=$data/$source.parquet output=$out/qwen-rewrite180-$short.jsonl
    if [ -e "$out/qwen-rewrite180-$short-blocks.json" ]; then
        echo "$short already scored"
        return
    fi
    python ../scripts/exp21/generate_masked_multiverse.py \
        "$model" "$test" "$output" 10 "$budget" thinking > "$out/qwen-rewrite180-$short.log" 2>&1
    python ../scripts/bench/score.py "$output" "$test" \
        "$out/qwen-rewrite180-$short-score.json" \
        "$out/qwen-rewrite180-$short-rows.jsonl" >> "$out/qwen-rewrite180-$short.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
        "$output" "$out/qwen-rewrite180-$short-rows.jsonl" \
        "$out/qwen-rewrite180-$short-blocks.json" \
        "$out/qwen-rewrite180-$short-block-rows.jsonl" masked >> "$out/qwen-rewrite180-$short.log" 2>&1
}

run_one gsm10 gsm8k_dev10 2048
run_one gsmnext10 gsm8k_devnext10 2048
run_one math10 math_dev10 4096
run_one mathnext10 math_devnext10 4096
date -Is > "$out/MASKED_PILOT_DONE"
