#!/usr/bin/env bash
# Parallel-format SFT of Qwen3-4B (hybrid instruct) in its native non-thinking template: a fixed number of optimizer
# updates on 2 GPUs (the lr schedule spans exactly these updates), then a bf16 export.
# Usage on the pod (venv active), from this checkout, on GPUs reserved by scripts/instruct4b/gpu_pair.sh:
#   DATA_PATH=<train.parquet> VAL_PATH=<dev.parquet> RUN_NAME=<name> CUDA_VISIBLE_DEVICES=<g1>,<g2> bash scripts/instruct4b/sft.sh [hydra overrides]
# Optional: MODEL (prepared init), STEPS (default 64), MICRO_BATCH (default 2 per GPU); exp 21 (Qwen3-0.6B, 1 GPU) also sets
# NGPUS (default 2), BATCH (global batch, default 64), MAX_LENGTH (4096), LR (1e-5), MIN_FREE_GB (30),
# RUN_ROOT (default /work/runs); defaults = the exp 13-20 recipe. Use an ephemeral RUN_ROOT only if the final
# model and logs are copied to persistent storage before the pod stops.
# Output: /work/runs/$RUN_NAME/{train.log, model/ (bf16 HF), results/{recipe.txt, rows.csv, sft_metrics.txt}, DONE}.
# DONE: nothing is repeated. TRAINED (trainer exited 0): only the missing export is repeated. Otherwise the unfinished run dir
# is renamed to $RUN_NAME.interrupted-<time> (logs kept) and training starts again from the same init: the trainer
# saves only HF weights, so there is no optimizer state to resume from.
set -euo pipefail
: "${DATA_PATH:?}" "${VAL_PATH:?}" "${RUN_NAME:?}" "${CUDA_VISIBLE_DEVICES:?}"
model=${MODEL:-/work/assets/models/Qwen3-4B-instruct-add-special-token}
steps=${STEPS:-64}
micro=${MICRO_BATCH:-2}
ngpus=${NGPUS:-2} batch=${BATCH:-64} max_length=${MAX_LENGTH:-4096} lr=${LR:-1e-5} min_free=${MIN_FREE_GB:-30}
gpus=$(echo "$CUDA_VISIBLE_DEVICES" | tr ',' '\n' | grep -c .)
[ "$gpus" = "$ngpus" ] || { echo "need $ngpus GPUs, got CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"; exit 1; }
repo=$(cd "$(dirname "$0")/../.." && pwd)
run_root=${RUN_ROOT:-/work/runs}
mkdir -p "$run_root"
run=$run_root/$RUN_NAME
[ ! -e "$run/DONE" ] || { echo "$run is done"; exit 0; }
if [ -e "$run" ] && [ ! -e "$run/TRAINED" ]; then mv "$run" "$run.interrupted-$(date +%Y%m%d-%H%M%S)"; fi

cd "$repo/verl"
export PYTHONPATH=$PWD  # the venv also has an editable verl from /work/setup-src
python -c "import os, verl; assert verl.__file__.startswith(os.getcwd()), verl.__file__"

if [ ! -e "$run/TRAINED" ]; then
    # fp32 trainer checkpoint (16 GB) and bf16 export (8 GB) exist together for a moment
    [ "$(df --output=avail -BG "$run_root" | tail -1 | tr -dc 0-9)" -ge "$min_free" ] || { echo "need $min_free GB free on $run_root"; exit 1; }
    mkdir -p "$run/results"
    # Rows of each update: the trainer's DistributedSampler (seed 0, epoch-wise shuffle, drop_last) on $ngpus ranks
    epochs=$(python - "$DATA_PATH" "$VAL_PATH" "$model" "$steps" "$run/results" "$ngpus" "$batch" <<'EOF'
import math, os, sys

import pandas as pd
from torch.utils.data import DistributedSampler
from transformers import AutoConfig

data, val, model, steps, out, ranks, batch = *sys.argv[1:4], int(sys.argv[4]), sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
train = pd.read_parquet(data)
per_rank = batch // ranks
steps_per_epoch = len(train) // ranks // per_rank
epochs = math.ceil(steps / steps_per_epoch)
ids = train["index"] if "index" in train else pd.Series(range(len(train)))
lines = ["step,rank,row,source_index"]
for epoch in range(epochs):
    for rank in range(ranks):
        sampler = DistributedSampler(range(len(train)), num_replicas=ranks, rank=rank, shuffle=True, drop_last=True)
        sampler.set_epoch(epoch)
        order = list(sampler)
        for k in range(steps_per_epoch):
            step = epoch * steps_per_epoch + k + 1
            if step <= steps:
                lines += [f"{step},{rank},{row},{ids.iloc[row]}" for row in order[k * per_rank:(k + 1) * per_rank]]
open(os.path.join(out, "rows.csv"), "w").write("\n".join(lines) + "\n")
config = AutoConfig.from_pretrained(model)
with open(os.path.join(out, "recipe.txt"), "a") as f:
    for name, path, frame in [("train", data, train), ("val", val, pd.read_parquet(val))]:
        f.write(f"{name}={path} rows={len(frame)} bytes={os.path.getsize(path)} columns={list(frame.columns)}\n")
    f.write(f"steps_per_epoch={steps_per_epoch} epochs={epochs} updates={steps} rows_processed={len(lines) - 1}"
            f" distinct_rows_processed={len({line.split(',')[2] for line in lines[1:]})}\n")
    f.write(f"model={model} vocab_size={config.vocab_size} dtype={config.torch_dtype} tied={config.tie_word_embeddings}\n")
print(epochs)
EOF
)
    { date; git -C "$repo" rev-parse HEAD; git -C "$repo" status --short
      echo "GPUs=$CUDA_VISIBLE_DEVICES updates=$steps global_batch=$batch micro_batch_per_gpu=$micro max_length=$max_length lr=$lr epochs=$epochs overrides=$*"; } >> "$run/results/recipe.txt"

    torchrun --standalone --nnodes=1 --nproc_per_node="$ngpus" -m verl.trainer.fsdp_parallel_sft_trainer \
        data.train_files="$DATA_PATH" \
        data.val_files="$VAL_PATH" \
        data.prompt_key=extra_info \
        data.response_key=extra_info \
        +data.prompt_dict_keys=['question'] \
        +data.response_dict_keys=['answer'] \
        +data.enable_thinking=False \
        data.max_length="$max_length" \
        data.truncation=error \
        data.train_batch_size="$batch" \
        data.micro_batch_size_per_gpu="$micro" \
        model.partial_pretrain="$model" \
        model.enable_gradient_checkpointing=True \
        model.strategy=fsdp2 \
        optim.lr="$lr" \
        optim.betas=[0.9,0.95] \
        optim.weight_decay=0.01 \
        optim.warmup_steps_ratio=0.1 \
        optim.clip_grad=1.0 \
        optim.lr_scheduler=cosine \
        trainer.total_epochs="$epochs" \
        trainer.total_training_steps="$steps" \
        trainer.default_local_dir="$run/ckpt" \
        trainer.project_name=Parallel-R1-instruct4b \
        trainer.experiment_name="$RUN_NAME" \
        trainer.logger=['console'] \
        trainer.default_hdfs_dir=null "$@" > "$run/train.log" 2>&1
    tr '\r' '\n' < "$run/train.log" | grep -a -o "step:[0-9]* - .*" > "$run/results/sft_metrics.txt"
    grep -q "^step:$steps - " "$run/results/sft_metrics.txt" || { echo "step $steps not logged"; exit 1; }
    touch "$run/TRAINED"
fi

# bf16 export, checked before the fp32 checkpoint is removed; model/ appears atomically, DONE only after it
if [ ! -e "$run/model" ]; then
    rm -rf "$run/model.tmp"
    python - "$run/ckpt/global_step_$steps" "$run/model.tmp" "$model" <<'EOF'
import glob, sys

import torch
from safetensors import safe_open
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

source, target, init = sys.argv[1:]
AutoModelForCausalLM.from_pretrained(source, torch_dtype=torch.bfloat16).save_pretrained(target)
AutoTokenizer.from_pretrained(source).save_pretrained(target)

model = AutoModelForCausalLM.from_pretrained(target, torch_dtype="auto")
assert model.dtype == torch.bfloat16 and model.config.vocab_size == AutoConfig.from_pretrained(init).vocab_size
assert model.config.tie_word_embeddings and model.get_output_embeddings().weight is model.get_input_embeddings().weight
assert all(torch.isfinite(p).all() for p in model.parameters())
for path in glob.glob(f"{target}/*.safetensors"):
    with safe_open(path, "pt") as f:
        assert len(list(f.keys())) > 0, path
assert AutoTokenizer.from_pretrained(target).chat_template == AutoTokenizer.from_pretrained(init).chat_template
print(f"export ok: {target}")
EOF
    mv "$run/model.tmp" "$run/model"
fi
date > "$run/DONE.tmp" && mv "$run/DONE.tmp" "$run/DONE"
rm -rf "$run/ckpt"  # only this run's temporary fp32 trainer checkpoint
