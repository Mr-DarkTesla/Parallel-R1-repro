#!/usr/bin/env bash
# One-GPU Qwen3-4B reasoning pilot after the Sol6.1 step-24 paired evaluation.
set -euo pipefail

data=/work/exp21/qwen4b_teacher
for _ in $(seq 1 900); do
    test -s /work/exp21/teacher_sft/STEP24_PILOT_DONE && break
    sleep 5
done
test -s /work/exp21/teacher_sft/STEP24_PILOT_DONE
test -s "$data/pool320.jsonl"
test -s /work/assets/models/Qwen3-4B/config.json
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
python scripts/exp21/generate_pool.py /work/assets/models/Qwen3-4B \
    "$data/pool320.jsonl" "$data/raw320.jsonl" thinking 1 1536 structured \
    > "$data/generate.log" 2>&1
python scripts/exp21/grade_gen.py "$data/pool320.jsonl" "$data/raw320.jsonl" \
    "$data/graded320.jsonl" > "$data/grade.log" 2>&1
date -Is > "$data/GENERATE_DONE"
