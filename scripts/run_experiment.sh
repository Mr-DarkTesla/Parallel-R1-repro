#!/usr/bin/env bash
# One SFT experiment on the pod: SFT, authors' eval, LIMO eval, tag validator on the final checkpoint.
# Re-running the same name resumes: every finished stage (its result file exists) is skipped.
# Usage (venv active): bash scripts/run_experiment.sh <name> [SFT hydra overrides...]   ->  /work/runs/<name>/results
set -euo pipefail

name=$1
shift
repo=${EXPERIMENT_REPO:-$(cd "$(dirname "$0")/.." && pwd)}
work=${PR1_WORK_ROOT:-/work}
run=$work/runs/$name
data=$repo/verl/data_preprocess_scripts/data
mkdir -p "$run/results"
export RAY_TMPDIR=/tmp/ray_$name

if [ ! -s "$run/results/sft_metrics.txt" ]; then
    if [ -d "$run/ckpt" ]; then
        previous=$run/interrupted/$(date +%Y%m%dT%H%M%S%N)
        mkdir -p "$previous"
        mv "$run/ckpt" "$previous/ckpt"
        [ ! -f "$run/train.log" ] || mv "$run/train.log" "$previous/train.log"
    fi
    bash "$repo/scripts/sft_qwen3_0.6b.sh" "$work/assets/Qwen3-0.6B-Base-add-special-token" "$run/ckpt" "$@" > "$run/train.log" 2>&1
    grep -a -o "step:[0-9]* - [a-z/]*loss:[0-9.]*\|train/grad_norm:[0-9.e+-]*" "$run/train.log" > "$run/sft_metrics.tmp"
    mv "$run/sft_metrics.tmp" "$run/results/sft_metrics.txt"
fi
final=$(ls -d "$run"/ckpt/global_step_* | sort -V | tail -1)

evaluate() {
    [ -s "$run/results/eval_$1.txt" ] && return
    rm -rf "$run/eval_$1"
    bash "$repo/scripts/eval_qwen3_0.6b.sh" "$final" "$run/eval_$1" "$2" > "$run/eval_$1.log" 2>&1
    (cd "$repo/verl" && python ../scripts/summarize_eval.py "$run/eval_$1/generations/0.jsonl" "$2") > "$run/eval_$1.tmp"
    mv "$run/eval_$1.tmp" "$run/results/eval_$1.txt"
}
evaluate apo "$data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet"
evaluate limo "$data/limo/test.parquet"
evaluate math300_x8 "$data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/math300_x8.parquet"

if [ ! -s "$run/results/free_generation_tags.jsonl" ]; then
    (cd "$repo/verl" && python ../scripts/check_tags.py "$final" "$run/check_tags" 2>> "$run/check_tags.log" | grep "^{") > "$run/free_generation_tags.tmp"
    mv "$run/free_generation_tags.tmp" "$run/results/free_generation_tags.jsonl"
fi
