#!/usr/bin/env bash
# All benchmarks for one model / mode / budget. Finished benchmarks (their result file exists) are skipped, so a rerun resumes.
# mode: parallel (authors' prompt + parallel rollout) | plain (same answer format, no parallel instructions; plain vLLM generation)
#       | thinking / no-thinking (plain, Qwen3 chat template with enable_thinking on / off)
# Usage on the pod (venv active): bash scripts/bench/run_bench.sh <name> <model> <mode> <response_budget>   ->  /work/bench/<name>/results
set -euo pipefail

name=$1
model=$2
mode=$3
budget=$4
repo=$(cd "$(dirname "$0")/../.." && pwd)
run=/work/bench/$name
mkdir -p "$run/results"
export RAY_TMPDIR=/tmp/ray_$name
export PYTHONPATH=/work/assets/ifeval/pkg NLTK_DATA=/work/assets/ifeval/nltk_data

for bench in apo arc ifeval mmlu_pro limo; do
    [ -s "$run/results/$bench.json" ] && continue
    if [ "$mode" = parallel ]; then
        test=/work/bench_data/parallel/$bench.parquet
        rm -rf "$run/$bench"
        bash "$repo/scripts/bench/eval_rollout.sh" "$model" "$run/$bench" "$test" "$budget" > "$run/$bench.log" 2>&1
        generations=$run/$bench/generations/0.jsonl
    else
        test=/work/bench_data/plain/$bench.parquet
        generations=$run/$bench.jsonl
        thinking=$([ "$mode" = plain ] && echo default || echo "$mode")
        (cd "$repo/verl" && python ../scripts/bench/generate_plain.py "$model" "$test" "$generations" "$budget" "$thinking") > "$run/$bench.log" 2>&1
    fi
    (cd "$repo/verl" && python ../scripts/bench/score.py "$generations" "$test" "$run/results/$bench.json") >> "$run/$bench.log" 2>&1
done
