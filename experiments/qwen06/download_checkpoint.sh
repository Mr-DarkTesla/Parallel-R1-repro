#!/usr/bin/env bash
set -euo pipefail
ROOT=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
CHECKPOINT_URL=${1:?Usage: download_checkpoint.sh GOOGLE_DRIVE_URL}
export PATH="$HOME/.local/bin:$PATH"
uv pip install --python "$ROOT/.venv/bin/python" 'gdown==5.2.0'
mkdir -p "$ROOT/incoming"
"$ROOT/.venv/bin/gdown" --fuzzy "$CHECKPOINT_URL" -O "$ROOT/incoming/qwen3-0.6b-unseen-epoch-5.tar.gz"
"$ROOT/.venv/bin/python" "$ROOT/repo/experiments/qwen06/check_checkpoint.py" "$ROOT/incoming/qwen3-0.6b-unseen-epoch-5.tar.gz" --extract-to "$ROOT/models/sft-epoch5"
