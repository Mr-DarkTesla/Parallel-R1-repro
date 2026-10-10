#!/usr/bin/env bash
# Same forty fixed dev problems as the earlier inside-thinking masked pilots.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export PYTHONPATH=/work/parallel-r1/verl:/work/assets/ifeval/pkg
export NLTK_DATA=/work/assets/ifeval/nltk_data SCORE_IFEVAL_SEED=0
export EXP21_COMMIT=d774d24
model=/tmp/exp21-balanced-runs/exp21-sol-deep75-balanced/model
export EXP21_TOKENIZER="$model"
data=/work/exp21/masked_pilot
out=/work/exp21/deep_balanced/masked_pilot
test -e /work/exp21/deep_balanced/EVAL_PAIR_DONE
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

run_one bal-gsm10 gsm8k_dev10 2048
run_one bal-gsmnext10 gsm8k_devnext10 2048
run_one bal-math10 math_dev10 4096
run_one bal-mathnext10 math_devnext10 4096
date -Is > "$out/BALANCED_MASKED_DONE"
