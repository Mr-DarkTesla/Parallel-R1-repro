#!/usr/bin/env bash
# One owned H100: matched Qwen3-0.6B SFT from the same post-trained init.
set -euo pipefail

data=/work/exp21/q06_distill447
runroot=/tmp/exp21-selective-runs
model=/work/assets/models/Qwen3-0.6B-mv
marker=$data/ATTEMPT_DONE
mkdir -p "$data"
exec 9>"$data/runner.lock"
flock -n 9 || { echo 'q06 distill447 runner already active' >&2; exit 1; }
trap 'rc=$?; printf "%s status=%s\n" "$(date -Is)" "$rc" > "$marker"' EXIT

test -s "$model/config.json"
test -s /checkpoints/exp21-global-top5/GLOBAL_TOP5.json
test -s /work/exp21/qwen4b_clean46/EVAL_DONE
if pgrep -f 'torchrun.*fsdp_parallel_sft_trainer|generate_masked_multiverse.py|generate_onpolicy_masked.py|scripts/instruct4b_eval/generate.py|scripts/bench/generate_plain.py' >/dev/null; then
    echo 'another GPU job is active on the owned pod' >&2
    exit 1
fi
for arm in tagged plain; do
    test -s "$data/${arm}_train.parquet"
    test -s "$data/${arm}_val.parquet"
done
test -s "$data/build_report.json"
/work/venv/bin/python - "$data/build_report.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
assert r['status'] == 'ready_for_paired_sft' and r['target'] == 'Qwen/Qwen3-0.6B'
assert r['distinct_positive'] == 447 and r['train_distinct_positive'] == 439
assert r['rows_per_arm'] == {'train': 2659, 'val': 50}
assert r['train_kind_counts'] == {'parallel_th': 1489, 'replay_th': 588, 'replay_nt': 582}
assert r['plain_only_removes_tags']
assert r['train_val_question_overlap'] == r['fixed40_question_overlap'] == 0
assert max(n for split in r['max_total_tokens'].values() for n in split.values()) <= 4096
PY

cd /work/parallel-r1
source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
for arm in tagged plain; do
    RUN_ROOT="$runroot" RUN_NAME="exp21-q06-distill447-${arm}-p128" \
    MODEL="$model" DATA_PATH="$data/${arm}_train.parquet" \
    VAL_PATH="$data/${arm}_val.parquet" \
    NGPUS=1 STEPS=128 SAVE_STEPS=16,32,64,96,128 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
    MAX_LENGTH=4096 MIN_FREE_GB=20 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
date -Is > "$data/TRAIN_PAIR_DONE"
for arm in tagged plain; do
    run="$runroot/exp21-q06-distill447-${arm}-p128"
    test -s "$run/DONE"
    EXP21_RUN="$run" EXP21_EVAL_ROOT="/tmp/exp21-q06-distill447-${arm}-p128-eval" \
        EXP21_STEPS=16,32,64,96,128 bash scripts/exp21/eval_checkpoint_steps_pod.sh
done
date -Is > "$data/EVAL_DONE"
