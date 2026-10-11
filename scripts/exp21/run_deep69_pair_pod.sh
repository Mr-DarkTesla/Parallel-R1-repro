#!/usr/bin/env bash
# Matched one-GPU SFT of reviewed 51 MATH plus 18 GSM positive blocks.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
work=${EXP21_WORK:-/work}
venv=${EXP21_VENV:-/work/venv}
data=$work/exp21/expanded_th
model=/checkpoints/exp21-v4-recovery8/step_8/model
runroot=/tmp/exp21-selective-runs

test -s "$model/config.json"
test -s "$data/sft_deep69_pair_quality.json"
test -s "$data/sft_deep51_pair_val.parquet"
for arm in tagged plain; do
    test -s "$data/sft_deep69_${arm}_train.parquet"
done
"$venv/bin/python" - "$data/sft_deep69_pair_quality.json" <<'PY'
import json, sys
audit = json.load(open(sys.argv[1]))
checks = audit["checks"]
assert audit["status"] == "audited"
assert checks["tagged_train_rows"] == checks["plain_train_rows"] == 256
assert checks["unique_positive_ids"] == checks["positive_rows"] == 69
assert checks["deep51_math_positive_rows"] == 51
assert checks["recovery8_gsm_positive_rows"] == 18
assert checks["replay_th_rows"] == checks["replay_nt_rows"] == 71
assert checks["plain_underlying_solution_equivalent"] == 69
assert checks["tagged_grammar_inside_think"] == 69
assert checks["global_eval_leaks"] == checks["deep51_eval_leaks"] == 0
assert checks["over_4096"] == 0
PY

source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo"
for arm in tagged plain; do
    RUN_ROOT="$runroot" RUN_NAME="exp21-deep69-${arm}-p8" \
    MODEL="$model" DATA_PATH="$data/sft_deep69_${arm}_train.parquet" \
    VAL_PATH="$data/sft_deep51_pair_val.parquet" \
    NGPUS=1 STEPS=8 SAVE_STEPS=4,8 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
    MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
