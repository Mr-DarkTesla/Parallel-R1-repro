#!/usr/bin/env bash
# Evaluate untouched prepared Qwen3-4B on the identical masked greedy fixed40.
set -euo pipefail

for _ in $(seq 1 900); do
    test -s /work/exp21/qwen4b_teacher/GENERATE_DONE && break
    sleep 5
done
test -s /work/exp21/qwen4b_teacher/GENERATE_DONE
model=/tmp/exp21-qwen3-4b-mv10
out=/tmp/exp21-4b-init-fixed40
pilots=/work/exp21/masked_pilot
test -s "$model/config.json"
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 EXP21_TOKENIZER="$model"
mkdir -p "$out"
cd /work/parallel-r1/verl
export PYTHONPATH="$PWD"
for src in gsm8k_dev10 gsm8k_devnext10 math_dev10 math_devnext10; do
    test -s "$pilots/$src.parquet"
    case "$src" in math_*) budget=4096 ;; *) budget=2048 ;; esac
    if test -s "$out/$src-block-rows.jsonl"; then continue; fi
    python ../scripts/exp21/generate_masked_multiverse.py "$model" "$pilots/$src.parquet" \
        "$out/$src.jsonl" 10 "$budget" thinking greedy > "$out/$src.log" 2>&1
    python ../scripts/bench/score.py "$out/$src.jsonl" "$pilots/$src.parquet" \
        "$out/$src-score.json" "$out/$src-rows.jsonl" >> "$out/$src.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py "$out/$src.jsonl" "$out/$src-rows.jsonl" \
        "$out/$src-blocks.json" "$out/$src-block-rows.jsonl" masked >> "$out/$src.log" 2>&1
done
date -Is > "$out/DONE"
