#!/usr/bin/env bash
# Re-scores every finished benchmark of every run under /work/bench with the current scripts/bench/score.py (no generation).
# Usage on the pod (venv active): bash scripts/bench/rescore_all.sh
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH=/work/assets/ifeval/pkg NLTK_DATA=/work/assets/ifeval/nltk_data
cd "$repo/verl"
for run in /work/bench/*; do
    for result in "$run"/results/*.json; do
        [ -s "$result" ] || continue
        bench=$(basename "$result" .json)
        if [ -s "$run/$bench.jsonl" ]; then
            python ../scripts/bench/score.py "$run/$bench.jsonl" "/work/bench_data/plain/$bench.parquet" "$result" > /dev/null
        else
            python ../scripts/bench/score.py "$run/$bench/generations/0.jsonl" "/work/bench_data/parallel/$bench.parquet" "$result" > /dev/null
        fi
    done
done
