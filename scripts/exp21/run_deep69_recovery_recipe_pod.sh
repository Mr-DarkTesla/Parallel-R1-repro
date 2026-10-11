#!/usr/bin/env bash
# One tagged Deep69 arm with the reviewed recovery8 recipe; does not change PVC retention.
set -euo pipefail

repo=${EXP21_REPO:-/work/parallel-r1}
work=${EXP21_WORK:-/work}
venv=${EXP21_VENV:-/work/venv}
data=$work/exp21/expanded_th
train=$data/sft_deep69_tagged_train.parquet
val=$data/sft_deep51_pair_val.parquet
audit=$data/sft_deep69_pair_quality.json
model=/checkpoints/exp21-v4-recovery8/step_8/model
runroot=/tmp/exp21-selective-runs
run_name=exp21-deep69-recovery-recipe-tagged-p8

test -s "$model/config.json"
test -s "$train" && test -s "$val" && test -s "$audit"
"$venv/bin/python" - "$audit" <<'PY'
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
PYTHONPATH="$repo/verl" python "$repo/scripts/exp21/check_weighted_sft_mask.py" \
    "$model" "$train" "$train" > /tmp/exp21-deep69-recovery-recipe-loss-mask.json
test -s /tmp/exp21-deep69-recovery-recipe-loss-mask.json

cd "$repo"
RUN_ROOT="$runroot" RUN_NAME="$run_name" \
MODEL="$model" DATA_PATH="$train" VAL_PATH="$val" \
NGPUS=1 STEPS=8 SAVE_STEPS=4,8 LR=3e-6 BATCH=32 MICRO_BATCH=4 \
MAX_LENGTH=4096 MIN_FREE_GB=10 \
bash scripts/instruct4b/sft.sh +data.structure=multiverse \
    +data.parallel_text_loss_weight=0.1 optim.tag_lr_mult=1 trainer.seed=1
