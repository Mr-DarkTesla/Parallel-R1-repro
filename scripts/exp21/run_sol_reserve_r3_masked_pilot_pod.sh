#!/usr/bin/env bash
# Forty fixed dev problems shared with the earlier inside-thinking masked pilots.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export PYTHONPATH=/work/parallel-r1/verl:/work/assets/ifeval/pkg
export NLTK_DATA=/work/assets/ifeval/nltk_data SCORE_IFEVAL_SEED=0
export EXP21_COMMIT=3c39df9
model=/tmp/exp21-r3-runs/exp21-sol-reserve-r3/model
export EXP21_TOKENIZER="$model"
data=/work/exp21/masked_pilot
out=/work/exp21/sol_r3/masked_pilot
test -e /work/exp21/sol_r3/EVAL_PAIR_DONE
test -e "$model/config.json"
mkdir -p "$out"
cd /work/parallel-r1/verl

run_one() {
    local short=$1 source=$2 budget=$3
    local test="$data/$source.parquet" output="$out/$short.jsonl"
    if [ -e "$out/$short-blocks.json" ]; then
        echo "$short already scored"
        return
    fi
    python ../scripts/exp21/generate_masked_multiverse.py \
        "$model" "$test" "$output" 10 "$budget" thinking > "$out/$short.log" 2>&1
    python ../scripts/bench/score.py "$output" "$test" \
        "$out/$short-score.json" "$out/$short-rows.jsonl" >> "$out/$short.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
        "$output" "$out/$short-rows.jsonl" "$out/$short-blocks.json" \
        "$out/$short-block-rows.jsonl" masked >> "$out/$short.log" 2>&1
}

run_one r3-gsm10 gsm8k_dev10 2048
run_one r3-gsmnext10 gsm8k_devnext10 2048
run_one r3-math10 math_dev10 4096
run_one r3-mathnext10 math_devnext10 4096
date -Is > "$out/R3_MASKED_DONE"
