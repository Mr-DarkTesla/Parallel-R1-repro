#!/usr/bin/env bash
# Compatibility entry point; the common launcher uses the active environment.
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
variant=${1:-seen}
if [ "$#" -gt 0 ]; then shift; fi
case "$variant" in
  seen) name=Parallel-SFT-Seen-Qwen3-0.6B ;;
  unseen) name=Parallel-SFT-Unseen-Qwen3-0.6B ;;
  *) echo "Usage: $0 [seen|unseen] [Hydra overrides...]" >&2; exit 2 ;;
esac
cd "$repo/verl"
scratch=${PARALLEL_R1_SCRATCH_ROOT:-$PWD/checkpoints}
output=${PARALLEL_R1_OUTPUT_ROOT:-checkpoints}
exec "${PARALLEL_R1_PYTHON:-python}" "$repo/scripts/qwen3.py" sft "$variant" \
  --gpus "${NPROC_PER_NODE:-8}" --name "$name" \
  --run-dir "$scratch/$name" --final-dir "$output/$name/final" -- "$@"
