#!/usr/bin/env bash
# Evaluate every exported SFT step on the same 40 masked Multiverse prompts.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
work=${EXP21_WORK:-/work}
venv=${EXP21_VENV:-/work/venv}
run=${EXP21_RUN:?set EXP21_RUN to the SFT run directory}
outroot=${EXP21_EVAL_ROOT:-/tmp/exp21-checkpoint-eval}
final_eval=${EXP21_FINAL_EVAL:-}
steps=${EXP21_STEPS:-8,16,24,32,40,48,56,64}
source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
pilots=$work/exp21/masked_pilot
mkdir -p "$outroot"
cd "$repo/verl"
export PYTHONPATH="$PWD"

IFS=, read -r -a checkpoint_steps <<< "$steps"
for step in "${checkpoint_steps[@]}"; do
    model=$run/step_models/step_$step/model
    test -s "$model/config.json"
    export EXP21_TOKENIZER="$model"
    out=$outroot/step_$step
    mkdir -p "$out"
    if [ "$step" = 64 ] && [ -n "$final_eval" ] && [ -s "$final_eval/DONE" ]; then
        cp -a "$final_eval/." "$out/"
    fi
    for source in gsm8k_dev10 gsm8k_devnext10 math_dev10 math_devnext10; do
        test -s "$pilots/$source.parquet"
        case "$source" in math_*) budget=4096 ;; *) budget=2048 ;; esac
        if [ -s "$out/$source-block-rows.jsonl" ]; then continue; fi
        python ../scripts/exp21/generate_masked_multiverse.py \
            "$model" "$pilots/$source.parquet" "$out/$source.jsonl" 10 "$budget" thinking greedy \
            > "$out/$source.log" 2>&1
        python ../scripts/bench/score.py "$out/$source.jsonl" "$pilots/$source.parquet" \
            "$out/$source-score.json" "$out/$source-rows.jsonl" >> "$out/$source.log" 2>&1
        python ../scripts/exp21/score_thinking_blocks.py \
            "$out/$source.jsonl" "$out/$source-rows.jsonl" "$out/$source-blocks.json" \
            "$out/$source-block-rows.jsonl" masked >> "$out/$source.log" 2>&1
    done
    date -Is > "$out/DONE"
done
date -Is > "$outroot/DONE"
