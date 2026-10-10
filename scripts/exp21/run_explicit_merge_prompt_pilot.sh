#!/usr/bin/env bash
# One model on the same 40 dev questions with an explicit merge instruction.
set -euo pipefail

model=$1
name=$2
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
repo=/tmp/parallel-r1-eval
data=/tmp/exp21-explicit-merge-prompt
out=/tmp/exp21-explicit-merge-$name
test -e "$model/config.json"
mkdir -p "$out"
cd "$repo/verl"
export PYTHONPATH="$PWD" EXP21_TOKENIZER="$model"
for part in gsm8k_dev10 gsm8k_devnext10 math_dev10 math_devnext10; do
    test -e "$data/$part.parquet"
    case "$part" in math_*) budget=4096 ;; *) budget=2048 ;; esac
    if [ -e "$out/$part-block-rows.jsonl" ]; then continue; fi
    python ../scripts/exp21/generate_masked_multiverse.py \
        "$model" "$data/$part.parquet" "$out/$part.jsonl" 10 "$budget" thinking greedy \
        > "$out/$part.log" 2>&1
    python ../scripts/bench/score.py "$out/$part.jsonl" "$data/$part.parquet" \
        "$out/$part-score.json" "$out/$part-rows.jsonl" >> "$out/$part.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
        "$out/$part.jsonl" "$out/$part-rows.jsonl" "$out/$part-blocks.json" \
        "$out/$part-block-rows.jsonl" masked >> "$out/$part.log" 2>&1
done
date -Is > "$out/DONE"
