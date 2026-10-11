#!/usr/bin/env bash
# Generate and structurally screen fresh 4B traces after the current one-GPU queue.
set -euo pipefail

repo=${EXP21_REPO:-/tmp/exp21-eval-clean-299074e}
model=${QWEN4B_ONPOLICY_MODEL:-/checkpoints/exp21-global-top5/qwen4b-mixed401-tagged-step128/model}
root=${QWEN4B_ONPOLICY_ROOT:-/checkpoints/exp21-qwen4b-onpolicy189}
candidates=/tmp/exp21-qwen4b-onpolicy189-candidates.jsonl
focus_done=/work/exp21/qwen4b_focus34/EVAL_DONE

[[ "$root" = /checkpoints/exp21-* ]] || { echo "refusing output outside owned checkpoint PVC: $root" >&2; exit 2; }
test -s "$focus_done" || { echo "4B focus34 fixed40 not finished: $focus_done" >&2; exit 1; }
test -s "$model/config.json"
test -s "$repo/scripts/exp21/generate_onpolicy_masked.py"
test -s "$candidates"
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|generate_onpolicy_masked.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU job is active on the owned pod' >&2
    exit 1
fi

mkdir -p "$root"
exec 9>"$root/runner.lock"
flock -n 9 || { echo '4B on-policy runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$root/ATTEMPT_DONE"' EXIT

cd "$repo"
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1
python - "$candidates" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, 'scripts/exp21')
from generate_onpolicy_masked import read_candidates, select_candidates
selected = select_candidates(read_candidates(Path(sys.argv[1])), 94, 95)
assert len(selected) == 189
PY

python scripts/exp21/generate_onpolicy_masked.py "$model" "$candidates" "$root/rollouts.jsonl" \
    --math-count 94 --gsm-count 95 --seeds 0 \
    --temperature 0.6 --top-p 0.95 --top-k 20
test "$(wc -l < "$root/rollouts.jsonl")" -eq 189
date -Is > "$root/GENERATION_DONE"

if [ ! -s "$root/filter/summary.json" ]; then
    python scripts/exp21/filter_onpolicy_rollouts.py "$root/rollouts.jsonl" "$root/filter" \
        --candidates "$candidates"
fi
python - "$root/filter/summary.json" <<'PY'
import json, sys
report = json.load(open(sys.argv[1]))
assert report['rollouts'] == 189
assert report['provisional'] + report['rejected'] == 189
PY
date -Is > "$root/FILTER_DONE"
