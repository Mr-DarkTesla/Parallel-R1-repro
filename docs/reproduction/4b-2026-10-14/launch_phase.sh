#!/usr/bin/env bash
# Run on every node of a fresh, dedicated allocation sharing REPRO_ROOT.
set -euo pipefail
PHASE="${1:?rl50, rl300 or rl150-new-reward}"
: "${REPRO_ROOT:?absolute restored project directory}"
: "${MASTER_ADDR:?address reachable from every node}"
: "${NODE_RANK:?zero-based node index}"
case "$PHASE" in
 rl50) NNODES=3; BASE="$REPRO_ROOT/work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity"; WORKER=runner/train.py ;;
 rl300) NNODES=4; BASE="$REPRO_ROOT/work/experiments/rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory"; WORKER=src/train.py ;;
 rl150-new-reward) NNODES=2; BASE="$REPRO_ROOT/work/experiments/rl-r4-dapo2k-sft-16gpu-20261013"; WORKER=src/train.py ;;
 *) exit 2 ;;
esac
cd "$REPRO_ROOT"
export PYTHONPATH="$BASE/$(dirname "$WORKER")"
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export OMP_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1
export STRUCTURED_GPU_AUTHORIZED=1 VLLM_USE_V1=0 VLLM_WORKER_MULTIPROC_METHOD=spawn
export TORCHELASTIC_USE_AGENT_STORE=False NCCL_DEBUG=WARN
export TMPDIR="$BASE/reproduction-cache/$NODE_RANK/tmp"
export HF_HOME="$BASE/reproduction-cache/$NODE_RANK/hf"
export CUDA_CACHE_PATH="$BASE/reproduction-cache/$NODE_RANK/cuda"
export TRITON_CACHE_DIR="$BASE/reproduction-cache/$NODE_RANK/triton"
export VLLM_CACHE_ROOT="$BASE/reproduction-cache/$NODE_RANK/vllm"
mkdir -p "$TMPDIR" "$HF_HOME" "$CUDA_CACHE_PATH" "$TRITON_CACHE_DIR" "$VLLM_CACHE_ROOT"
exec python -m torch.distributed.run --nnodes="$NNODES" --nproc_per_node=8 \
 --node_rank="$NODE_RANK" --master_addr="$MASTER_ADDR" --master_port="${MASTER_PORT:-29600}" \
 "$BASE/$WORKER" --config "$BASE/portable-config.json" --receipt "$BASE/portable-receipt.json"
