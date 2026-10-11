#!/usr/bin/env bash
# Fresh masked-greedy comparison of the two strongest 4B block checkpoints.
# Invoke only after the existing full-dev runner has completed.
set -euo pipefail

repo=${EXP21_REPO:-/tmp/exp21-eval-code}
venv=${EXP21_VENV:-/work/venv}
data=${EXP21_HOLDOUT_DATA:-/checkpoints/exp21-masked-holdout40}
root=${EXP21_HOLDOUT_RUN:-/checkpoints/exp21-masked-holdout40-eval}
previous=${EXP21_PREVIOUS_RUN:-/checkpoints/exp21-qwen4b-clean46-full-dev}
: "${EXP21_COMMIT:?set EXP21_COMMIT to the committed evaluator revision}"

test -s "$previous/EVAL_DONE" || { echo 'previous full-dev evaluation is not complete' >&2; exit 1; }
test -s "$data/manifest.json"
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU task is active' >&2
    exit 1
fi

mkdir -p "$root"
exec 9>"$root/runner.lock"
flock -n 9 || { echo 'holdout40 runner already active' >&2; exit 1; }
source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo/verl"
export PYTHONPATH="$PWD"

for arm in clean46 mixed401; do
    case "$arm" in
        clean46) model=/checkpoints/exp21-global-top5/qwen4b-clean46-tagged-step32/model ;;
        mixed401) model=/checkpoints/exp21-global-top5/qwen4b-mixed401-tagged-step128/model ;;
    esac
    test -s "$model/config.json"
    export EXP21_TOKENIZER="$model"
    out=$root/$arm
    mkdir -p "$out"
    for source in gsm8k math; do
        input=$data/${source}_holdout20.parquet
        test -s "$input"
        case "$source" in gsm8k) budget=2048 ;; math) budget=4096 ;; esac
        raw=$out/$source.jsonl
        rows=$out/$source-rows.jsonl
        blocks=$out/$source-block-rows.jsonl
        if test -s "$blocks" && test "$(wc -l < "$blocks")" -eq 20 \
            && test -s "$rows" && test "$(wc -l < "$rows")" -eq 20 \
            && test -s "$raw" && test "$(wc -l < "$raw")" -eq 20; then
            python - "$raw.meta.json" "$model" "$input" "$budget" <<'PY'
import json, sys
meta = json.load(open(sys.argv[1]))
assert meta["model"] == sys.argv[2] and meta["data"] == sys.argv[3], meta
assert meta["count"] == 20 and meta["max_tokens"] == int(sys.argv[4]), meta
assert meta["mode"] == "thinking" and meta["policy"] == "greedy", meta
PY
            continue
        fi
        python ../scripts/exp21/generate_masked_multiverse.py \
            "$model" "$input" "$raw" 20 "$budget" thinking greedy > "$out/$source.log" 2>&1
        python ../scripts/bench/score.py "$raw" "$input" \
            "$out/$source-score.json" "$rows" >> "$out/$source.log" 2>&1
        python ../scripts/exp21/score_thinking_blocks.py "$raw" "$rows" \
            "$out/$source-blocks.json" "$blocks" masked >> "$out/$source.log" 2>&1
    done
    date -Is > "$out/DONE"
done
date -Is > "$root/EVAL_DONE"
