#!/usr/bin/env bash
# One-GPU matched eight-step SFT with doubled exposure to reviewed Deep51 blocks.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
work=${EXP21_WORK:-/work}
venv=${EXP21_VENV:-/work/venv}
data=$work/exp21/expanded_th
model=/checkpoints/exp21-v4-recovery8/step_8/model
runroot=/tmp/exp21-selective-runs

test -s "$model/config.json"
test -s "$data/sft_deep51_2x_pair_quality.json"
test -s "$data/sft_deep51_pair_val.parquet"
for arm in tagged plain; do
    test -s "$data/sft_deep51_2x_${arm}_train.parquet"
done
"$venv/bin/python" - "$data/sft_deep51_2x_pair_quality.json" <<'PY'
import json, sys
audit = json.load(open(sys.argv[1]))
checks = audit["checks"]
assert audit["status"] == "audited"
assert checks["tagged_train_rows"] == checks["plain_train_rows"] == 256
assert checks["tagged_deep51_verbatim"] == 102
assert checks["plain_underlying_solution_equivalent"] == 102
assert checks["over_4096"] == checks["deep51_eval_leaks"] == 0
PY

source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo"
for arm in tagged plain; do
    RUN_ROOT="$runroot" RUN_NAME="exp21-deep51-2x-${arm}-p8" \
    MODEL="$model" DATA_PATH="$data/sft_deep51_2x_${arm}_train.parquet" \
    VAL_PATH="$data/sft_deep51_pair_val.parquet" \
    NGPUS=1 STEPS=8 SAVE_STEPS=4,8 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
    MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
