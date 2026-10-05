#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

variant=${1:-unseen}
if [ "$#" -gt 0 ]; then shift; fi
case "$variant" in
  unseen) config=sft_qwen3_06b ;;
  seen) config=sft_qwen3_06b_seen ;;
  *) echo "Usage: $0 [unseen|seen] [Hydra overrides...]" >&2; exit 2 ;;
esac

export R1_SCRATCH_ROOT=${R1_SCRATCH_ROOT:-/dev/shm/r1}
export R1_MODEL_PATH=${R1_MODEL_PATH:-$R1_SCRATCH_ROOT/Qwen3-0.6B-Base-special}
export HF_HOME=${HF_HOME:-$R1_SCRATCH_ROOT/huggingface}
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

if [ ! -f "$R1_MODEL_PATH/model.safetensors" ]; then
  python training_scripts/prepare_qwen3_parallel.py "$R1_MODEL_PATH"
fi

python -m torch.distributed.run --standalone --nnodes=1 --nproc_per_node="${NPROC_PER_NODE:-8}" \
  -m verl.trainer.fsdp_parallel_sft_trainer --config-name="$config" "$@"
