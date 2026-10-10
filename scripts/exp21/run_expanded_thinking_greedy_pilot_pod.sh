#!/usr/bin/env bash
# Greedy masked decoding on the same forty dev questions as the sampled pilot.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export PYTHONPATH=/work/parallel-r1/verl:/work/assets/ifeval/pkg
data=/work/exp21/masked_pilot
out=/work/exp21/expanded_th/greedy_pilot
mkdir -p "$out"
cd /work/parallel-r1/verl

run_one() {
    local method=$1 short=$2 source=$3 budget=$4
    local model=/tmp/exp21-expanded-th-runs/exp21-expanded-th-$method/model
    local test=$data/$source.parquet output=$out/$method-$short.jsonl
    test -e "$model/config.json" && test -e "$test"
    export EXP21_TOKENIZER="$model"
    if [ -e "$out/$method-$short-blocks.json" ]; then
        return
    fi
    python ../scripts/exp21/generate_masked_multiverse.py \
        "$model" "$test" "$output" 10 "$budget" thinking greedy > "$out/$method-$short.log" 2>&1
    python ../scripts/bench/score.py "$output" "$test" \
        "$out/$method-$short-score.json" "$out/$method-$short-rows.jsonl" >> "$out/$method-$short.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
        "$output" "$out/$method-$short-rows.jsonl" "$out/$method-$short-blocks.json" \
        "$out/$method-$short-block-rows.jsonl" masked >> "$out/$method-$short.log" 2>&1
}

for method in m1 m2; do
    run_one "$method" gsm10 gsm8k_dev10 2048
    run_one "$method" gsmnext10 gsm8k_devnext10 2048
    run_one "$method" math10 math_dev10 4096
    run_one "$method" mathnext10 math_devnext10 4096
done
date -Is > "$out/DONE"
