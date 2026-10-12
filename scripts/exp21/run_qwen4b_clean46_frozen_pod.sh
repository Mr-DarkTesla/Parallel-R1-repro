#!/usr/bin/env bash
# Frozen suites for the 4B checkpoint selected before opening these splits.
set -euo pipefail

repo=${EXP21_REPO:-/tmp/exp21-eval-code}
venv=${EXP21_VENV:-/work/venv}
root=${EXP21_FROZEN_ROOT:-/checkpoints/exp21-qwen4b-clean46-frozen-final}
model=${EXP21_FROZEN_MODEL:-/checkpoints/exp21-global-top5/qwen4b-clean46-tagged-step32/model}
budget=${EXP21_FROZEN_BUDGET:-16384}
benches='apo arc mmlu_pro limo'

test -s /checkpoints/exp21-agent-parallel150-holdout40/EVAL_DONE
test -s /checkpoints/exp21-qwen4b-clean46-full-dev/EVAL_DONE
test "$model" = /checkpoints/exp21-global-top5/qwen4b-clean46-tagged-step32/model
test "$root" = /checkpoints/exp21-qwen4b-clean46-frozen-final
test -s "$model/config.json"
for bench in $benches; do test -s "/work/bench_data/plain/$bench.parquet"; done
test "$budget" = 16384
test "$(git -C "$repo" rev-parse --short HEAD)" = 14880be
test -z "$(git -C "$repo" status --porcelain --untracked-files=no -- scripts verl)"
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU task is active' >&2
    exit 1
fi

mkdir -p "$root"
python3 - "$root" <<'PY'
import shutil, sys
free = shutil.disk_usage(sys.argv[1]).free
assert free >= 4 * 1024 ** 3, f"need 4 GiB free on personal checkpoint PVC, have {free / 1024 ** 3:.1f}"
PY
exec 9>"$root/runner.lock"
flock -n 9 || { echo 'frozen runner already active' >&2; exit 1; }
trap 'status=$?; printf "%s status=%s\n" "$(date -Is)" "$status" > "$root/ATTEMPT_DONE"' EXIT
python3 - "$root/runner_meta.json" "$model" "$budget" "$benches" <<'PY'
import json, os, pathlib, sys
path, model, budget, benches = sys.argv[1:]
meta = {"protocol": "selected-qwen4b-clean46-frozen-v1", "model": model,
        "budget": int(budget), "benches": benches.split(),
        "modes": ["no-thinking", "thinking"], "evaluator_commit": "14880be",
        "selection_commit": "73995bf", "gpu": 0}
file = pathlib.Path(path)
if file.exists():
    assert json.loads(file.read_text()) == meta, "frozen runner settings changed"
else:
    temporary = file.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(meta, indent=2) + "\n")
    os.replace(temporary, file)
PY
source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export EVAL_OUT="$root/eval" BENCHES="$benches"
cd "$repo"
for mode in no-thinking thinking; do
    name="qwen4b-clean46-selected-frozen-$mode"
    bash scripts/instruct4b_eval/run_eval.sh "$name" "$model" frozen "$mode" "$budget"
done
date -Is > "$root/EVAL_DONE"
