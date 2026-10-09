#!/usr/bin/env bash
# Paired 20-problem GSM8K/MATH dev diagnostic on one fixed short Multiverse prompt.
# Usage on own GPU pod: bash scripts/exp21/run_short_prompt_pilot.sh NAME MODEL
set -euo pipefail

name=$1
model=$2
repo=${EXP21_REPO:-$(cd "$(dirname "$0")/../.." && pwd)}
base=/work/exp21/prompt_pilot
out="$base/$name"
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 PYTHONPATH="$repo"
cd "$repo/verl"

for bench in gsm8k_dev20-short math_dev20-short; do
    input="$base/$bench.parquet"
    dump="$out/$bench.jsonl"
    rows="$out/$bench.rows.jsonl"
    python ../scripts/instruct4b_eval/generate.py "$model" "$input" "$dump" 16384 thinking
    EXP21_TOKENIZER="$model" python ../scripts/bench/score.py "$dump" "$input" "$out/$bench.score.json" "$rows"
    python ../scripts/exp21/score_thinking_blocks.py "$dump" "$rows" "$out/$bench.blocks.json" "$out/$bench.block_rows.jsonl" sequential
done
