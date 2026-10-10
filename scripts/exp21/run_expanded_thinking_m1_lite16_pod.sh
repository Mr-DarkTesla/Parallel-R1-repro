#!/usr/bin/env bash
# Same 367 M1 examples, 16 updates at 3e-6; dev-only masked pilot.
set -euo pipefail

source /work/venv/bin/activate
export CUDA_VISIBLE_DEVICES=${EXP21_GPU:-1} PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
export PYTHONPATH=/work/parallel-r1/verl:/work/assets/ifeval/pkg
export NLTK_DATA=/work/assets/ifeval/nltk_data SCORE_IFEVAL_SEED=0
cd /work/parallel-r1
root=/work/exp21/expanded_th
scratch=/tmp/exp21-expanded-th-runs
name=exp21-expanded-th-m1-lite16
train=$root/sft_expanded_th_m1_tagged_train.parquet
val=$root/sft_expanded_th_m1_tagged_val.parquet
test -e "$train" && test -e "$val"
mkdir -p "$scratch" "$root/m1_lite16/masked_pilot"
if [ ! -e "$scratch/$name/DONE" ]; then
    if [ -e "$scratch/$name" ]; then
        echo "$scratch/$name exists but is incomplete; inspect before resuming" >&2
        exit 1
    fi
    RUN_ROOT="$scratch" RUN_NAME="$name" DATA_PATH="$train" VAL_PATH="$val" \
      MODEL=/work/assets/models/Qwen3-0.6B-mv NGPUS=1 \
      STEPS=16 LR=3e-6 BATCH=32 MICRO_BATCH=4 MAX_LENGTH=4096 MIN_FREE_GB=10 \
      bash scripts/instruct4b/sft.sh +data.structure=multiverse optim.tag_lr_mult=100
fi
model=$scratch/$name/model
test -e "$scratch/$name/DONE" && test -e "$model/config.json"
date -Is > "$root/m1_lite16/TRAIN_DONE"

cd /work/parallel-r1/verl
data=/work/exp21/masked_pilot
out=$root/m1_lite16/masked_pilot
export EXP21_TOKENIZER="$model"
run_one() {
    local short=$1 source=$2 budget=$3
    local test=$data/$source.parquet output=$out/m1-lite16-$short.jsonl
    if [ -e "$out/m1-lite16-$short-blocks.json" ]; then return; fi
    python ../scripts/exp21/generate_masked_multiverse.py \
      "$model" "$test" "$output" 10 "$budget" thinking > "$out/m1-lite16-$short.log" 2>&1
    python ../scripts/bench/score.py "$output" "$test" \
      "$out/m1-lite16-$short-score.json" "$out/m1-lite16-$short-rows.jsonl" >> "$out/m1-lite16-$short.log" 2>&1
    python ../scripts/exp21/score_thinking_blocks.py \
      "$output" "$out/m1-lite16-$short-rows.jsonl" \
      "$out/m1-lite16-$short-blocks.json" "$out/m1-lite16-$short-block-rows.jsonl" masked >> "$out/m1-lite16-$short.log" 2>&1
}
run_one gsm10 gsm8k_dev10 2048
run_one gsmnext10 gsm8k_devnext10 2048
run_one math10 math_dev10 4096
run_one mathnext10 math_devnext10 4096
date -Is > "$out/MASKED_PILOT_DONE"
