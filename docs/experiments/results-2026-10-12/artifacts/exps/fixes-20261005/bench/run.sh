#!/usr/bin/env bash
set -u
root=${PROJECT_ROOT}
out=$root/exps/fixes-20261005/bench
cd "$root/verl"
export PATH="$root/.venv/bin:$PATH" PYTHONPATH="$root/verl" CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 R1_MODEL_PATH=${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2 OMP_NUM_THREADS=1
for variant in seen unseen; do
  config=sft_qwen3_06b
  if [ "$variant" = seen ]; then config=sft_qwen3_06b_seen; fi
  for micro in 1 2 4 8; do
    export BENCH_RESULT="$out/$variant-mb$micro.json"
    python -m torch.distributed.run --standalone --nproc_per_node=8 "$out/benchmark.py" --config-name="$config" data.max_length=3072 data.parse_prompt_tags=false data.micro_batch_size_per_gpu="$micro" model.enable_gradient_checkpointing=false > "$out/$variant-mb$micro.log" 2>&1
    echo "$?" > "$out/$variant-mb$micro.exit_code"
  done
done
date -u +%FT%TZ > "$out/finished"
