#!/usr/bin/env bash
# Forty fixed dev problems, autonomous tags with SFT path mask and positions.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export PYTHONPATH=/work/parallel-r1/verl:/work/assets/ifeval/pkg
export NLTK_DATA=/work/assets/ifeval/nltk_data SCORE_IFEVAL_SEED=0
export EXP21_TOKENIZER=/work/runs/exp21-sol-deep75/model EXP21_COMMIT=d774d24
cd /work/parallel-r1/verl
data=/work/exp21/masked_pilot
model=/work/runs/exp21-sol-deep75/model

run_one() {
    local short=$1 source=$2 budget=$3
    local test="$data/$source.parquet" output="$data/$short.jsonl"
    if [ -e "$data/$short-blocks.json" ]; then
        echo "$short already scored"
        return
    fi
    python ../scripts/exp21/generate_masked_multiverse.py \
        "$model" "$test" "$output" 10 "$budget" thinking > "$data/$short.log" 2>&1
    python ../scripts/bench/score.py "$output" "$test" \
        "$data/$short-score.json" "$data/$short-rows.jsonl" >> "$data/$short.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
        "$output" "$data/$short-rows.jsonl" "$data/$short-blocks.json" \
        "$data/$short-block-rows.jsonl" masked >> "$data/$short.log" 2>&1
}

run_one deep75-gsm10 gsm8k_dev10 2048
run_one deep75-gsmnext10 gsm8k_devnext10 2048
run_one deep75-math10 math_dev10 4096
run_one deep75-mathnext10 math_devnext10 4096
date -Is > "$data/DEEP75_MASKED_DONE"
