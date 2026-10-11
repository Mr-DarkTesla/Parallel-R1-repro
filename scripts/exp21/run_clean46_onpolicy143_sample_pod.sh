#!/usr/bin/env bash
# One owned GPU: sample clean46 on new train questions, then CPU-prefilter.
set -euo pipefail

repo=${EXP21_REPO:-/tmp/exp21-eval-code}
venv=${EXP21_VENV:-/work/venv}
root=${EXP21_RUN_ROOT:-/checkpoints/exp21-clean46-onpolicy143}
holdout=${EXP21_HOLDOUT_ROOT:-/checkpoints/exp21-masked-holdout40-eval}
model=${EXP21_MODEL:-/checkpoints/exp21-global-top5/qwen4b-clean46-tagged-step32/model}
candidates=${EXP21_CANDIDATES:-$root/candidates.jsonl}
: "${EXP21_COMMIT:?set EXP21_COMMIT to the committed recipe revision}"

test -s "$holdout/EVAL_DONE" || { echo 'fresh masked holdout is not complete' >&2; exit 1; }
test -s "$model/config.json"
test -s "$candidates"
test -s "$repo/scripts/exp21/generate_onpolicy_masked.py"
test -s "$repo/scripts/exp21/filter_onpolicy_rollouts.py"
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|generate_onpolicy_masked.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU task is active' >&2
    exit 1
fi

mkdir -p "$root"
exec 9>"$root/runner.lock"
flock -n 9 || { echo 'on-policy sampler already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$root/ATTEMPT_DONE"' EXIT
source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo/verl"
export PYTHONPATH="$PWD"

python ../scripts/exp21/generate_onpolicy_masked.py \
    "$model" "$candidates" "$root/rollouts.jsonl" \
    --gsm-count 68 --math-count 75 --seeds 0 1 2 3 4 5 6 7 \
    --temperature 0.7 --top-p 0.95 --top-k 20 \
    --gsm-max-new-tokens 2048 --math-max-new-tokens 4096 \
    > "$root/generation.log" 2>&1
python - "$root/rollouts.jsonl" <<'PY'
import json, sys
rows = [json.loads(line) for line in open(sys.argv[1]) if line.strip()]
assert len(rows) == 143 * 8, len(rows)
assert len({(row['id'], row['seed']) for row in rows}) == len(rows)
assert len({row['id'] for row in rows}) == 143
assert sum(row['source'] == 'gsm8k' for row in rows) == 68 * 8
assert sum(row['source'] == 'math' for row in rows) == 75 * 8
PY
date -Is > "$root/GENERATION_DONE"
python ../scripts/exp21/filter_onpolicy_rollouts.py \
    "$root/rollouts.jsonl" "$root/filter" --candidates "$candidates" \
    > "$root/filter.log" 2>&1
test -s "$root/filter/summary.json"
date -Is > "$root/FILTER_DONE"
