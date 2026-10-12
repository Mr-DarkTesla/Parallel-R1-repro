#!/usr/bin/env bash
# One or four H100 workers for Parallel-only evaluation.
# Usage inside the owned pod: EXP21_COMMIT=<git commit> bash run_full_parallel_pair_pod.sh dev|frozen
set -euo pipefail

stage=${1:?dev or frozen}
case "$stage" in dev|frozen) ;; *) exit 2 ;; esac
: "${EXP21_COMMIT:?record the committed code revision}"
root=${EXP21_FULL_ROOT:-/work/exp21-full-parallel-pair}
backup=${EXP21_FULL_BACKUP:-/checkpoints/exp21-full-parallel-pair-backup}
code=${EXP21_FULL_CODE:-/work/exp21-full-eval-code/scripts}
model=${EXP21_FULL_MODEL:-/checkpoints/exp21-global-top5/qwen4b-clean46-tagged-step32/model}
venv=${EXP21_VENV:-/work/venv}
repo=${EXP21_REPO_ROOT:-/work/parallel-r1}
ifeval_pkg=${EXP21_IFEVAL_PKG:-/work/assets/ifeval/pkg}
python_extra=${EXP21_PYTHON_EXTRA:-}
test -s "$model/config.json"
test -s "$root/input/manifest.json"
mkdir -p "$root/output" "$root/logs" "$backup"
exec 9>"$root/${stage}.lock"
flock -n 9 || { echo "another $stage runner holds the lock" >&2; exit 1; }
gpu_count=$(nvidia-smi --list-gpus | wc -l)
case "$gpu_count" in 1|4) ;; *) echo "expected one or four owned GPUs, got $gpu_count" >&2; exit 1 ;; esac
if test "$venv" != system; then source "$venv/bin/activate"; fi
export PYTHONDONTWRITEBYTECODE=1 EXP21_FSYNC_EVERY_ROW=1
export PYTHONPATH="$python_extra:$repo/verl:$ifeval_pkg"
export EXP21_TOKENIZER="$model" SCORE_IFEVAL_SEED=0 EXP21_LIGHT_SCORE=1
cd "$repo/verl"

run_one() {
    local bench=$1 input out count raw rows blocks
    input=$root/input/$stage/parallel/$bench.parquet
    out=$root/output/$stage/parallel/$bench
    test -s "$input"
    mkdir -p "$out"
    count=$(python - "$input" <<'PY'
import pandas as pd, sys
print(len(pd.read_parquet(sys.argv[1])))
PY
)
    raw=$out/raw.jsonl
    rows=$out/score_rows.jsonl
    blocks=$out/block_rows.jsonl
    if test -s "$out/DONE"; then
        test "$(wc -l < "$raw")" -eq "$count"
        test "$(wc -l < "$rows")" -eq "$count"
        test "$(wc -l < "$blocks")" -eq "$count"
        return
    fi
    echo "$(date -Is) START $stage/parallel/$bench count=$count budget=16384 gpu=$CUDA_VISIBLE_DEVICES" | tee -a "$root/progress.log"
    python "$code/exp21/generate_masked_multiverse.py" "$model" "$input" "$raw" "$count" 16384 thinking sample >> "$out/generate.log" 2>&1
    test "$(wc -l < "$raw")" -eq "$count"
    python "$code/bench/score.py" "$raw" "$input" "$out/score.json.tmp" "$rows.tmp" >> "$out/score.log" 2>&1
    mv "$rows.tmp" "$rows"
    mv "$out/score.json.tmp" "$out/score.json"
    python "$code/exp21/score_thinking_blocks.py" "$raw" "$rows" "$out/blocks.json.tmp" "$blocks.tmp" masked >> "$out/score.log" 2>&1
    mv "$blocks.tmp" "$blocks"
    mv "$out/blocks.json.tmp" "$out/blocks.json"
    test "$(wc -l < "$rows")" -eq "$count"
    test "$(wc -l < "$blocks")" -eq "$count"
    cp "$raw.meta.json" "$out/generation_meta.json"
    printf '%s\n' "$(date -Is)" > "$out/DONE"
    mkdir -p "$backup/$stage/parallel/$bench"
    cp "$raw" "$rows" "$blocks" "$out/score.json" "$out/blocks.json" "$out/generation_meta.json" "$out/DONE" "$backup/$stage/parallel/$bench/"
    echo "$(date -Is) DONE $stage/parallel/$bench" | tee -a "$root/progress.log"
}

worker() {
    local group=$1
    if test "$stage" = frozen; then
        case "$group" in
            0) run_one apo ;;
            1) run_one limo ;;
            2) run_one arc; run_one ifeval ;;
            3) run_one mmlu_pro ;;
        esac
        return
    fi
    case "$group" in
        0) run_one gsm8k_dev ;;
        1) run_one math_dev ;;
        2) run_one arc_dev ;;
        3) run_one mmlu_pro_dev ;;
    esac
}

worker_all() {
    local bench
    if test "$stage" = dev; then
        for bench in gsm8k_dev math_dev arc_dev mmlu_pro_dev; do run_one "$bench"; done
    else
        for bench in apo arc mmlu_pro limo ifeval; do run_one "$bench"; done
    fi
}

snapshot() {
    while true; do
        find "$root/output/$stage" -type f -name raw.jsonl -print0 2>/dev/null | while IFS= read -r -d '' raw; do
            rel=${raw#"$root/output/"}
            target=$backup/snapshots/${rel%/*}
            mkdir -p "$target"
            cp "$raw" "$target/raw.jsonl.tmp"
            mv "$target/raw.jsonl.tmp" "$target/raw.jsonl"
        done
        sleep 180
    done
}

snapshot >> "$root/logs/${stage}-snapshot.log" 2>&1 &
snapshot_pid=$!
trap 'kill "$snapshot_pid" 2>/dev/null || true' EXIT
status=0
if test "$gpu_count" -eq 1; then
    CUDA_VISIBLE_DEVICES=0 worker_all > "$root/logs/${stage}-gpu0.log" 2>&1 || status=1
else
    CUDA_VISIBLE_DEVICES=0 worker 0 > "$root/logs/${stage}-gpu0.log" 2>&1 & p0=$!
    CUDA_VISIBLE_DEVICES=1 worker 1 > "$root/logs/${stage}-gpu1.log" 2>&1 & p1=$!
    CUDA_VISIBLE_DEVICES=2 worker 2 > "$root/logs/${stage}-gpu2.log" 2>&1 & p2=$!
    CUDA_VISIBLE_DEVICES=3 worker 3 > "$root/logs/${stage}-gpu3.log" 2>&1 & p3=$!
    for pid in "$p0" "$p1" "$p2" "$p3"; do wait "$pid" || status=1; done
fi
if test "$status" -ne 0; then
    echo "$(date -Is) FAILED $stage; inspect worker logs and resume" | tee -a "$root/progress.log"
    exit 1
fi
printf '%s\n' "$(date -Is) commit=$EXP21_COMMIT" > "$root/${stage^^}_DONE"
echo "$(date -Is) STAGE_DONE $stage" | tee -a "$root/progress.log"
