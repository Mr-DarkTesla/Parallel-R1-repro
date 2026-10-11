#!/usr/bin/env bash
# Two further masked generations per leak-checked task, on one owned GPU.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
root=/checkpoints/exp21-qwen4b-onpolicy189-seeds12
model=${QWEN4B_ONPOLICY_MODEL:-/checkpoints/exp21-global-top5/qwen4b-mixed401-tagged-step128/model}
candidates=/tmp/exp21-qwen4b-onpolicy189-candidates.jsonl
pair_done=/work/exp21/qwen4b_onpolicy189/EVAL_DONE

test -s "$pair_done" || { echo "paired fixed40 unfinished: $pair_done" >&2; exit 1; }
test -s "$model/config.json"
test -s "$candidates"
test -s "$repo/scripts/exp21/generate_onpolicy_masked.py"
test -s "$repo/scripts/exp21/filter_onpolicy_rollouts.py"
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|generate_onpolicy_masked.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU job is active on the owned pod' >&2
    exit 1
fi

mkdir -p "$root"
exec 9>"$root/runner.lock"
flock -n 9 || { echo 'seeds12 generation already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$root/ATTEMPT_DONE"' EXIT

cd "$repo"
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1
python - "$candidates" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, 'scripts/exp21')
from generate_onpolicy_masked import read_candidates, select_candidates
rows = select_candidates(read_candidates(Path(sys.argv[1])), 94, 95)
assert len(rows) == 189 and sum(row['source'] == 'math' for row in rows) == 94
PY

python scripts/exp21/generate_onpolicy_masked.py "$model" "$candidates" "$root/rollouts.jsonl" \
    --math-count 94 --gsm-count 95 --seeds 1 2 \
    --temperature 0.6 --top-p 0.95 --top-k 20
test "$(wc -l < "$root/rollouts.jsonl")" -eq 378
date -Is > "$root/GENERATION_DONE"

if [ ! -s "$root/filter/summary.json" ]; then
    python scripts/exp21/filter_onpolicy_rollouts.py "$root/rollouts.jsonl" "$root/filter" \
        --candidates "$candidates"
fi
python - "$root/filter/summary.json" <<'PY'
import json, sys
x = json.load(open(sys.argv[1]))
assert x['rollouts'] == 378
assert x['provisional'] + x['rejected'] == 378
PY
date -Is > "$root/FILTER_DONE"
