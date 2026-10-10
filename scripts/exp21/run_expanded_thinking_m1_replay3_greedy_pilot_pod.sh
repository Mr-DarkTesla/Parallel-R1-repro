#!/usr/bin/env bash
# Same forty dev questions and greedy masked decoder as the M1/M2 comparison.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export PYTHONPATH=/work/parallel-r1/verl:/work/assets/ifeval/pkg
data=/work/exp21/masked_pilot
out=${OUT_DIR:-/work/exp21/expanded_th/m1_replay3_greedy_pilot}
model=${MODEL_PATH:-/tmp/exp21-expanded-th-runs/exp21-expanded-th-m1-replay3-lr3e6-tag300/model}
test -e "$model/config.json"
export EXP21_TOKENIZER="$model"
mkdir -p "$out"
cd /work/parallel-r1/verl

run_one() {
    local short=$1 source=$2 budget=$3
    local test=$data/$source.parquet output=$out/$short.jsonl
    test -e "$test"
    if [ -e "$out/$short-blocks.json" ]; then
        return
    fi
    python ../scripts/exp21/generate_masked_multiverse.py \
        "$model" "$test" "$output" 10 "$budget" thinking greedy > "$out/$short.log" 2>&1
    python ../scripts/bench/score.py "$output" "$test" \
        "$out/$short-score.json" "$out/$short-rows.jsonl" >> "$out/$short.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
        "$output" "$out/$short-rows.jsonl" "$out/$short-blocks.json" \
        "$out/$short-block-rows.jsonl" masked >> "$out/$short.log" 2>&1
}

run_one gsm10 gsm8k_dev10 2048
run_one gsmnext10 gsm8k_devnext10 2048
run_one math10 math_dev10 4096
run_one mathnext10 math_devnext10 4096
date -Is > "$out/DONE"
