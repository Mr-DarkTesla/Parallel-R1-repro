#!/usr/bin/env bash
# Generate new target-model thinking traces only after the balanced eval pair.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
data=/work/exp21/qwen_structured_thinking
test -e /work/exp21/deep_balanced/EVAL_PAIR_DONE
test "$(wc -l < "$data/inputs_clean_with_gold.jsonl")" -eq 1484
test ! -e "$data/GENERATION_DONE"

python scripts/exp21/generate_pool.py \
  /work/assets/models/Qwen3-0.6B \
  "$data/inputs_clean_with_gold.jsonl" \
  "$data/generated.jsonl" thinking 1 4096 structured > "$data/generate.log" 2>&1
python scripts/exp21/grade_gen.py \
  "$data/inputs_clean_with_gold.jsonl" \
  "$data/generated.jsonl" \
  "$data/graded.jsonl" > "$data/grade.log" 2>&1
date -Is > "$data/GENERATION_DONE"
