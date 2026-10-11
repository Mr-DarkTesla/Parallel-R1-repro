#!/usr/bin/env bash
# Full matched ordinary-prompt dev and IFEval for the selected Qwen3-4B pair.
# Block metrics are a separate masked fixed40 protocol; never compare them to
# ordinary sequential generation as if the decoder were part of the model.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
venv=${EXP21_VENV:-/work/venv}
focus_root=${FOCUS34_ROOT:-/work/exp21/qwen4b_focus34}
root=${QWEN4B_FULL_DEV_ROOT:-/checkpoints/exp21-qwen4b-full-dev}
run_root=${QWEN4B_RUN_ROOT:-/tmp/exp21-selective-runs}
selected_arm=${SELECTED_ARM:-tagged}
selected_step=${SELECTED_STEP:-32}
plain_arm=${PLAIN_ARM:-plain}
plain_step=${PLAIN_STEP:-$selected_step}
selected_run=${SELECTED_RUN:-$run_root/exp21-4b-focus34-${selected_arm}-p32}
plain_run=${PLAIN_RUN:-$run_root/exp21-4b-focus34-${plain_arm}-p32}
selected_model=${SELECTED_MODEL:-$selected_run/step_models/step_${selected_step}/model}
plain_model=${PLAIN_MODEL:-$plain_run/step_models/step_${plain_step}/model}
base_model=${BASE_MODEL:-/work/assets/models/Qwen3-4B}
include_base=${INCLUDE_BASE:-0}
run_masked_blocks=${RUN_MASKED_BLOCKS:-0}
gpu=${EXP21_GPU:-0}
budget=${EVAL_BUDGET:-16384}
wait_seconds=${FOCUS34_WAIT_SECONDS:-36000}
marker=$root/ATTEMPT_DONE
done_marker=$root/EVAL_DONE
eval_out=$root/eval
masked_out=$root/masked_fixed40

case "$selected_arm:$plain_arm:$include_base:$run_masked_blocks" in
    tagged:plain:0:0|tagged:plain:0:1|tagged:plain:1:0|tagged:plain:1:1) ;;
    *) echo 'SELECTED_ARM=tagged, PLAIN_ARM=plain, INCLUDE_BASE and RUN_MASKED_BLOCKS must be 0 or 1' >&2; exit 2 ;;
esac
[[ "$selected_step" =~ ^[0-9]+$ && "$plain_step" =~ ^[0-9]+$ && "$budget" =~ ^[0-9]+$ ]] \
    || { echo 'steps and EVAL_BUDGET must be non-negative integers' >&2; exit 2; }
[ "$gpu" = 0 ] || { echo 'this single-owned-GPU protocol requires EXP21_GPU=0' >&2; exit 2; }

mkdir -p "$root"
python3 - "$root" <<'PY'
import pathlib, shutil, sys
root = pathlib.Path(sys.argv[1]).resolve()
if not (str(root).startswith('/checkpoints/exp21-') or str(root).startswith('/tmp/exp21-')):
    raise SystemExit(f'refusing non-owned evaluation root: {root}')
free = shutil.disk_usage(root).free
if free < 10 * 1024 ** 3:
    raise SystemExit(f'need at least 10 GiB free before full dev; have {free / 1024 ** 3:.1f} GiB')
PY
exec 9>"$root/runner.lock"
flock -n 9 || { echo 'Qwen3-4B full-dev runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$marker"' EXIT

# focus34 writes EVAL_DONE only after both arms passed their fixed40 evaluation.
for _ in $(seq 1 "$wait_seconds"); do
    test -s "$focus_root/EVAL_DONE" && break
    sleep 1
done
test -s "$focus_root/EVAL_DONE" || { echo "focus34 did not complete: $focus_root/EVAL_DONE" >&2; exit 1; }

# One visible device and no training or masked decoder already using the owned GPU.
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU evaluation or training process is active' >&2
    exit 1
fi

test -s "$selected_model/config.json"
test -s "$plain_model/config.json"
if [ "$include_base" = 1 ]; then test -s "$base_model/config.json"; fi
test -s "$repo/scripts/instruct4b_eval/run_eval.sh"
test -s "$repo/scripts/exp21/eval_checkpoint_steps_pod.sh"
if [ -n "$(git -C "$repo" status --porcelain --untracked-files=no -- scripts verl)" ]; then
    echo "evaluation checkout has uncommitted scripts/verl changes: $repo" >&2
    exit 1
fi

source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES="$gpu" PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export EVAL_OUT="$eval_out" FOCUS34_ROOT="$focus_root" SELECTED_ARM="$selected_arm" SELECTED_STEP="$selected_step"
export SELECTED_MODEL="$selected_model" PLAIN_ARM="$plain_arm" PLAIN_STEP="$plain_step" PLAIN_MODEL="$plain_model"
export BASE_MODEL="$base_model" INCLUDE_BASE="$include_base" RUN_MASKED_BLOCKS="$run_masked_blocks"
export EVAL_BUDGET="$budget" EXP21_GPU="$gpu" MASKED_OUT="$masked_out"
cd "$repo"

# Resume only under identical immutable protocol settings. Per-suite completeness
# is checked again below before a whole suite is skipped.
python - "$root/runner_meta.json" <<'PY'
import json
import os
import subprocess
import sys

path = sys.argv[1]
repo = os.getcwd()
head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], text=True, capture_output=True).stdout.strip()
meta = {
    "protocol": "qwen3-4b-selected-full-dev-v1",
    "focus34_eval_done": os.environ["FOCUS34_ROOT"] + "/EVAL_DONE",
    "selected_arm": os.environ["SELECTED_ARM"],
    "selected_step": int(os.environ["SELECTED_STEP"]),
    "selected_model": os.environ["SELECTED_MODEL"],
    "plain_arm": os.environ["PLAIN_ARM"],
    "plain_step": int(os.environ["PLAIN_STEP"]),
    "plain_model": os.environ["PLAIN_MODEL"],
    "base_model": os.environ["BASE_MODEL"],
    "include_base": int(os.environ["INCLUDE_BASE"]),
    "run_masked_blocks": int(os.environ["RUN_MASKED_BLOCKS"]),
    "budget": int(os.environ["EVAL_BUDGET"]),
    "gpu": os.environ["EXP21_GPU"],
    "eval_out": os.environ["EVAL_OUT"],
    "masked_out": os.environ["MASKED_OUT"],
    "commit": head,
}
if os.path.exists(path):
    old = json.load(open(path))
    if old != meta:
        raise SystemExit(f"resume metadata differs: old={old}, now={meta}")
else:
    tmp = path + ".tmp"
    with open(tmp, "w") as file:
        json.dump(meta, file, indent=2, sort_keys=True)
        file.write("\n")
    os.replace(tmp, path)
PY

validate_suite() {
    local name=$1 model=$2 suite=$3 mode=$4 benches=$5
    python - "$eval_out/$name" "$model" "$suite" "$mode" "$budget" "$benches" <<'PY'
import json
import os
import sys
import pandas as pd

run, model, suite, mode, budget, benches = sys.argv[1:]
budget = int(budget)
benches = benches.split()
meta_path = os.path.join(run, "meta.json")
if not os.path.exists(meta_path):
    raise SystemExit(10)
meta = json.load(open(meta_path))
prompts = (os.path.join(os.environ.get("EVAL_DATA", "/work/bench_data/instruct4b/eval"), "dev", "plain")
           if suite == "dev" else "/work/bench_data/plain")
expected = {"model": model, "suite": suite, "mode": mode, "budget": budget,
            "temperature": 1.0, "top_p": 1.0, "prompts": prompts,
            "generator": "scripts/instruct4b_eval/generate.py" if suite == "dev" else "scripts/bench/generate_plain.py",
            "ifeval_scorer_seed": 0}
if {key: meta.get(key) for key in expected} != expected:
    raise SystemExit(f"{run}: incompatible metadata")
for bench in benches:
    test = (os.path.join(os.environ.get("EVAL_DATA", "/work/bench_data/instruct4b/eval"), "dev", "plain", bench + ".parquet")
            if suite == "dev" else os.path.join("/work/bench_data", "plain", bench + ".parquet"))
    rows_path = os.path.join(run, "rows", bench + ".jsonl")
    result_path = os.path.join(run, "results", bench + ".json")
    if not (os.path.exists(test) and os.path.exists(rows_path) and os.path.exists(result_path)):
        raise SystemExit(10)
    rows, test_rows = pd.read_json(rows_path, lines=True), pd.read_parquet(test)
    problems = pd.Series([p[0]["content"] for p in test_rows["prompt"]])
    sources = test_rows["data_source"].str.removeprefix("APO_")
    order = {p: n for n, p in enumerate(dict.fromkeys(problems))}
    expected_rows = {"source": sources, "problem": problems, "sample": problems.groupby(problems).cumcount(),
                     "problem_id": [i.get("id") or f"{s}/{order[p]}" for i, s, p in zip(test_rows["extra_info"], sources, problems)]}
    if len(rows) != len(test_rows) or any(column not in rows or (rows[column].astype(str).to_numpy() != pd.Series(values).astype(str).to_numpy()).any()
                                        for column, values in expected_rows.items()):
        raise SystemExit(f"{run}/{bench}: rows do not match current prompt parquet")
    summary = json.load(open(result_path))
    if not summary:
        raise SystemExit(f"{result_path}: empty summary")
print("validated")
PY
}

eval_suite() {
    local family=$1 model=$2 suite=$3 mode=$4 benches=$5
    local name="qwen4b-${family}-${suite}-${mode}"
    local status
    if validate_suite "$name" "$model" "$suite" "$mode" "$benches"; then
        echo "validated completed suite: $name"
        return
    else
        status=$?
    fi
    if [ "$status" -ne 10 ]; then
        echo "refusing to overwrite incompatible or partial suite: $name" >&2
        exit "$status"
    fi
    BENCHES="$benches" bash scripts/instruct4b_eval/run_eval.sh "$name" "$model" "$suite" "$mode" "$budget"
    validate_suite "$name" "$model" "$suite" "$mode" "$benches"
}

ordinary_eval() {
    local family=$1 model=$2
    # All arms use the same plain parquet by mode and suite. IFEval is the
    # frozen IFEval parquet only; no other frozen benchmark is opened here.
    eval_suite "$family" "$model" dev thinking 'gsm8k_dev math_dev arc_dev mmlu_pro_dev'
    eval_suite "$family" "$model" dev no-thinking 'gsm8k_dev math_dev arc_dev mmlu_pro_dev'
    eval_suite "$family" "$model" frozen thinking ifeval
    eval_suite "$family" "$model" frozen no-thinking ifeval
}

verify_matched_pair() {
    local suite=$1 mode=$2 benches=$3
    python - "$eval_out/qwen4b-selected-${suite}-${mode}" "$eval_out/qwen4b-plain-${suite}-${mode}" "$benches" <<'PY'
import sys
import pandas as pd

tagged, plain, benches = sys.argv[1:]
for bench in benches.split():
    tagged_rows = pd.read_json(f"{tagged}/rows/{bench}.jsonl", lines=True)
    plain_rows = pd.read_json(f"{plain}/rows/{bench}.jsonl", lines=True)
    fields = ("source", "problem_id", "problem", "input", "sample")
    if len(tagged_rows) != len(plain_rows) or any(
        field not in tagged_rows or field not in plain_rows or
        (tagged_rows[field].astype(str).to_numpy() != plain_rows[field].astype(str).to_numpy()).any()
        for field in fields
    ):
        raise SystemExit(f"{bench}: tagged/plain prompts or row order differ")
print("tagged/plain rows and rendered prompts match")
PY
}

ordinary_eval selected "$selected_model"
ordinary_eval plain "$plain_model"
if [ "$include_base" = 1 ]; then ordinary_eval base "$base_model"; fi
verify_matched_pair dev thinking 'gsm8k_dev math_dev arc_dev mmlu_pro_dev'
verify_matched_pair dev no-thinking 'gsm8k_dev math_dev arc_dev mmlu_pro_dev'
verify_matched_pair frozen thinking ifeval
verify_matched_pair frozen no-thinking ifeval

if [ "$run_masked_blocks" = 1 ]; then
    # Fixed40 is intentionally separate: decoder-enforced visibility and
    # positions belong only to the block-formation measurement.
    EXP21_REPO="$repo" EXP21_VENV="$venv" EXP21_RUN="$selected_run" \
    EXP21_EVAL_ROOT="$masked_out/selected" EXP21_STEPS="$selected_step" \
        bash scripts/exp21/eval_checkpoint_steps_pod.sh
    EXP21_REPO="$repo" EXP21_VENV="$venv" EXP21_RUN="$plain_run" \
    EXP21_EVAL_ROOT="$masked_out/plain" EXP21_STEPS="$plain_step" \
        bash scripts/exp21/eval_checkpoint_steps_pod.sh
fi

date -Is > "$done_marker"
