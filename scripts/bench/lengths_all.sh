#!/usr/bin/env bash
# Answer lengths and decode steps (scripts/bench/lengths.py) for every finished benchmark of every run under /work/bench.
# Usage on the pod (venv active): bash scripts/bench/lengths_all.sh   ->  /work/bench/<run>/lengths/<bench>.json
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
models=/work/assets/models
cd "$repo/verl"
for run in /work/bench/*; do
    name=$(basename "$run")
    case $name in
        *qwen3-4b*) tokenizer=$models/Qwen3-4B ;;
        *sft*) tokenizer=$models/Parallel-SFT-Unseen ;;
        *rl200*) tokenizer=$models/Parallel-R1-Unseen_Step_200 ;;
        *base*) tokenizer=$models/Qwen3-4B-Base-add-special-token ;;
        *) continue ;;
    esac
    mkdir -p "$run/lengths"
    for result in "$run"/results/*.json; do
        [ -s "$result" ] || continue
        bench=$(basename "$result" .json)
        [ -s "$run/lengths/$bench.json" ] && continue
        if [ -s "$run/$bench.jsonl" ]; then
            python ../scripts/bench/lengths.py "$run/$bench.jsonl" "$tokenizer" "/work/bench_data/plain/$bench.parquet" "$run/lengths/$bench.json" > /dev/null
        else
            python ../scripts/bench/lengths.py "$run/$bench/generations/0.jsonl" "$tokenizer" "/work/bench_data/parallel/$bench.parquet" "$run/lengths/$bench.json" > /dev/null
        fi
    done
done
