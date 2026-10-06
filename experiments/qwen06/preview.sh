#!/usr/bin/env bash
set -euo pipefail
ROOT=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
MODEL=${1:?Provide the SFT model directory}
export RUN_NAME=${RUN_NAME:-sft-epoch5-preview}
export WORKERS=2
"$ROOT/.venv/bin/python" "$ROOT/repo/experiments/qwen06/prepare_preview.py"
# Both flags are necessary in upstream fit(): val_only is checked inside val_before_train.
exec bash "$ROOT/repo/experiments/qwen06/run_rl.sh" s1 "$MODEL" \
  trainer.val_only=True trainer.val_before_train=True \
  trainer.save_freq=-1 trainer.test_freq=-1 \
  data.val_files="['$ROOT/data/preview.parquet']" \
  actor_rollout_ref.rollout.val_kwargs.n=1
