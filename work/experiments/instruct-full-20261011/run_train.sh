#!/usr/bin/env bash
set -euo pipefail
ROOT=${PROJECT_ROOT}
B="$ROOT/work/experiments/instruct-full-20261011"
MODE="${1:?smoke or epoch1}"
case "$MODE" in
 smoke) TRAIN=smoke-train; VAL=smoke-val; BATCH=8; STEPS=2; WARMUP=0.0 ;;
 isolation) TRAIN=smoke-train; VAL=smoke-val; BATCH=8; STEPS=2; WARMUP=0.0 ;;
 epoch1) TRAIN=train; VAL=val; BATCH=64; STEPS=42; WARMUP=0.1 ;;
 *) exit 2 ;;
esac
RUN="$B/runs/$MODE"
test ! -e "$RUN"; mkdir -p "$RUN"
cd "$B/code"
export PYTHONPATH="$B/code:$B" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export TMPDIR="$B/tmp" WANDB_MODE=disabled
mkdir -p "$TMPDIR"
PY="${PARALLEL_R1_PYTHON:-$ROOT/.venv/bin/python}"
MODULE=verl.trainer.fsdp_parallel_sft_trainer
if [[ "$MODE" == isolation ]]; then MODULE=isolation; fi
nvidia-smi --query-gpu=index,name,memory.used,utilization.gpu --format=csv > "$RUN/gpus-before.csv"
exec "$PY" -B -m torch.distributed.run --standalone --nnodes=1 --nproc-per-node=8 -m "$MODULE" --config-name=sft_qwen3_06b \
 data.train_files="$B/data/$TRAIN.parquet" data.val_files="$B/data/$VAL.parquet" \
 data.custom_cls.path="$B/dataset.py" data.custom_cls.name=InstructDataset +data.defer_parallel_mask=true \
 data.max_length=8192 data.truncation=error data.trim_padding=true data.train_batch_size="$BATCH" data.micro_batch_size_per_gpu=1 data.num_workers=0 \
 model.partial_pretrain="$ROOT/work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final" model.strategy=fsdp model.lora_rank=0 \
 model.enable_gradient_checkpointing=true model.fsdp_config.model_dtype=fp32 optim.lr=1e-5 optim.warmup_steps_ratio="$WARMUP" \
 ulysses_sequence_parallel_size=1 use_remove_padding=false trainer.total_epochs=1 trainer.total_training_steps="$STEPS" \
 trainer.default_local_dir="$RUN" trainer.final_dir="$RUN/final" trainer.experiment_name="Instruct-4B-full-$MODE" trainer.logger='[console]' hydra.run.dir="$RUN/hydra"
