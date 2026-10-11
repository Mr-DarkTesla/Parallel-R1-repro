#!/usr/bin/env bash
# Matched eight-step tagged/plain SFT arms from one reviewed recovery8 model.
set -euo pipefail

: "${PARENT_STEP:?set PARENT_STEP to 4, 8 or v4-56 after reviewing recovery8 pilots}"
[[ "$PARENT_STEP" == 4 || "$PARENT_STEP" == 8 || "$PARENT_STEP" == v4-56 ]]

repo=${EXP21_REPO:-/work/parallel-r1}
work=${EXP21_WORK:-/work}
venv=${EXP21_VENV:-/work/venv}
data=$work/exp21/expanded_th
if [[ "$PARENT_STEP" == v4-56 ]]; then
    model=/checkpoints/exp21-m1-selective-v4/step_56/model
else
    model=/checkpoints/exp21-v4-recovery8/step_${PARENT_STEP}/model
fi
runroot=/tmp/exp21-selective-runs

test -s /tmp/exp21-v4-recovery8-eval/DONE || {
    echo "Finish the recovery8 GPU evaluation before Deep51 SFT" >&2
    exit 1
}
test -s "$model/config.json"
test -s "$data/sft_deep51_pair_quality.json"
test -s "$data/sft_deep51_pair_val.parquet"
for arm in tagged plain; do
    test -s "$data/sft_deep51_${arm}_train.parquet"
done
"$venv/bin/python" - "$data/sft_deep51_pair_quality.json" <<'PY'
import json, sys
audit = json.load(open(sys.argv[1]))
checks = audit["checks"]
assert audit["status"] == "audited"
assert checks["tagged_train_rows"] == checks["plain_train_rows"] == 256
assert checks["tagged_deep51_verbatim"] == checks["deep51_independence_evidence"] == 51
assert checks["plain_underlying_solution_equivalent"] == 51
assert checks["over_4096"] == checks["deep51_eval_leaks"] == 0
PY

source "$venv/bin/activate"
export CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd "$repo"
for arm in tagged plain; do
    RUN_ROOT="$runroot" RUN_NAME="exp21-deep51-${arm}-p${PARENT_STEP}" \
    MODEL="$model" DATA_PATH="$data/sft_deep51_${arm}_train.parquet" \
    VAL_PATH="$data/sft_deep51_pair_val.parquet" \
    NGPUS=1 STEPS=8 SAVE_STEPS=4,8 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
    MAX_LENGTH=4096 MIN_FREE_GB=10 \
    bash scripts/instruct4b/sft.sh +data.structure=multiverse \
        +data.parallel_text_loss_weight=1.0 optim.tag_lr_mult=100
done
