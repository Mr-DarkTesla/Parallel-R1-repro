#!/usr/bin/env bash
# One SFT experiment on the pod: SFT, authors' eval, LIMO eval, tag validator on every epoch checkpoint.
# Usage (venv active): bash scripts/run_experiment.sh <name>   ->  /work/runs/<name>/results
set -euo pipefail

name=$1
repo=$(cd "$(dirname "$0")/.." && pwd)
run=/work/runs/$name
data=$repo/verl/data_preprocess_scripts/data
mkdir -p "$run/results"

bash "$repo/scripts/sft_qwen3_0.6b.sh" /work/assets/Qwen3-0.6B-Base-add-special-token "$run/ckpt" > "$run/train.log" 2>&1
grep -a -o "step:[0-9]* - [a-z/]*loss:[0-9.]*" "$run/train.log" > "$run/results/sft_metrics.txt"

evaluate() {
    bash "$repo/scripts/eval_qwen3_0.6b.sh" "$run/ckpt/global_step_230" "$run/eval_$1" "$2" > "$run/eval_$1.log" 2>&1
    (cd "$repo/verl" && python ../scripts/summarize_eval.py "$run/eval_$1/generations/0.jsonl" "$2") > "$run/results/eval_$1.txt"
}
evaluate apo "$data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet"
evaluate limo "$data/limo/test.parquet"

cd "$repo/verl"
for checkpoint in "$run"/ckpt/global_step_*; do
    python ../scripts/check_tags.py "$checkpoint" 2> /dev/null | grep "^{"
done > "$run/results/free_generation_tags.jsonl"
