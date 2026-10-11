#!/usr/bin/env bash
# Generate two planned masked trajectories for each fixed MATH-21 candidate, then prefilter them.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
root=/checkpoints/exp21-qwen4b-math-plan21
candidates=/tmp/exp21-qwen4b-math-plan21-candidates.jsonl
plans=/tmp/exp21-qwen4b-math-plan21-plans.jsonl
eval_done=/work/exp21/qwen4b_onpolicy189/EVAL_DONE
: "${QWEN4B_PLAN21_MODEL:?set QWEN4B_PLAN21_MODEL to the validated 4B model path}"
model=$QWEN4B_PLAN21_MODEL

[[ "$root" = /checkpoints/exp21-qwen4b-math-plan21 ]] || {
    echo "refusing output outside owned checkpoint PVC: $root" >&2
    exit 2
}
test -s "$repo/scripts/exp21/generate_onpolicy_masked.py"
test -s "$repo/scripts/exp21/filter_onpolicy_rollouts.py"
test -s "$candidates"
test -s "$plans"
test -s "$model/config.json"

mkdir -p "$root"
exec 9>"$root/runner.lock"
flock -n 9 || { echo 'Qwen4B MATH plan21 runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$root/ATTEMPT_DONE"' EXIT

# Do not share the owned GPU with the preceding paired evaluation or another local GPU job.
for _ in $(seq 1 7200); do
    if test -s "$eval_done" && ! pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|generate_onpolicy_masked.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
        break
    fi
    sleep 5
done
test -s "$eval_done" || { echo "paired evaluation did not finish: $eval_done" >&2; exit 1; }
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|generate_onpolicy_masked.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU job is active on the owned pod' >&2
    exit 1
fi

cd "$repo"
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1
python - "$candidates" "$plans" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, 'scripts/exp21')
from generate_onpolicy_masked import read_candidates, read_plans, select_candidates, select_plans

candidates = select_candidates(read_candidates(Path(sys.argv[1])), 21, 0)
plans = read_plans(Path(sys.argv[2]))
assert len(candidates) == 21
assert {row['source'] for row in candidates} == {'math'}
assert set(plans) == {row['id'] for row in candidates}
assert len(select_plans(plans, candidates)) == 21
PY

python scripts/exp21/generate_onpolicy_masked.py "$model" "$candidates" "$root/rollouts.jsonl" \
    --plans "$plans" --math-count 21 --gsm-count 0 --seeds 0,1 \
    --temperature 0.6 --top-p 0.95 --top-k 20
test "$(wc -l < "$root/rollouts.jsonl")" -eq 42
date -Is > "$root/GENERATION_DONE"

if [ ! -s "$root/filter/summary.json" ]; then
    python scripts/exp21/filter_onpolicy_rollouts.py "$root/rollouts.jsonl" "$root/filter" \
        --candidates "$candidates"
fi
python - "$root/filter/summary.json" <<'PY'
import json
import sys

summary = json.load(open(sys.argv[1]))
assert summary['rollouts'] == 42
assert summary['provisional'] + summary['rejected'] == 42
PY
date -Is > "$root/FILTER_DONE"
