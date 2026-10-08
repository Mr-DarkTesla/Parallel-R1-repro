#!/usr/bin/env bash
# GPU jobs of exp 21 on pod B, one at a time from the single queue (/work/queue/gpu0.txt, CUDA_VISIBLE_DEVICES set by the runner).
# Usage: bash scripts/exp21/pod_jobs.sh <job> [args]
#   prep            Qwen3-0.6B + 10 Multiverse tags -> $M/Qwen3-0.6B-mv (P06); Multiverse prompt parquets for dev and frozen
#   gen             Qwen3-0.6B answers on the pool: non-thinking x4 (4096 tokens), thinking x1 (8192 tokens) -> $W/gen
#   eval <name> <model> <suite> <mode> [benches]   scripts/instruct4b_eval/run_eval.sh with budget 16384 (BENCHES optional)
#   sft <name> <train> <val> [hydra overrides]     scripts/instruct4b/sft.sh, 1 GPU, exp 21 recipe (env STEPS, LR, BATCH...)
# Every job writes $W/logs/<job-name>.{log,exit}; a job with exit 0 is not repeated.
set -uo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
M=/work/assets/models W=/work/exp21
mkdir -p "$W/logs" "$W/gen" "$W/sft"
export PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
job=$1; shift
tag=$job${1:+-$1}
[ "$(cat "$W/logs/$tag.exit" 2>/dev/null)" = 0 ] && { echo "$tag done"; exit 0; }
run() {
    case $job in
    prep)
        python "$repo/scripts/exp21/prepare_model.py" "$M/Qwen3-0.6B" "$M/Qwen3-0.6B-mv" || return 1
        python "$repo/scripts/exp21/make_mv_prompts.py" /work/bench_data/instruct4b/eval/dev/plain /work/bench_data/instruct4b/eval/dev/multiverse || return 1
        python "$repo/scripts/exp21/make_mv_prompts.py" /work/bench_data/plain /work/bench_data/multiverse ;;
    gen)
        cd "$repo/verl" && \
        python ../scripts/exp21/generate_pool.py "$M/Qwen3-0.6B" "$W/data/gen_nt.jsonl" "$W/gen/nt.jsonl" no-thinking 4 4096 && \
        python ../scripts/exp21/generate_pool.py "$M/Qwen3-0.6B" "$W/data/gen_th.jsonl" "$W/gen/th.jsonl" thinking 1 8192 ;;
    eval)
        local name=$1 model=$2 suite=$3 mode=$4
        BENCHES=${5:-} EVAL_OUT=$W/eval bash "$repo/scripts/instruct4b_eval/run_eval.sh" "$name" "$model" "$suite" "$mode" 16384 ;;
    sft)
        local name=$1 train=$2 val=$3; shift 3
        RUN_NAME=$name DATA_PATH=$train VAL_PATH=$val MODEL=${MODEL:-$M/Qwen3-0.6B-mv} NGPUS=1 BATCH=${BATCH:-32} \
            MICRO_BATCH=${MICRO_BATCH:-4} MAX_LENGTH=${MAX_LENGTH:-4096} MIN_FREE_GB=10 \
            bash "$repo/scripts/instruct4b/sft.sh" +data.structure=multiverse optim.tag_lr_mult=${TAG_LR_MULT:-100} "$@" ;;
    *) echo "unknown job $job"; return 2 ;;
    esac
}
{ date; echo "job $tag: $*"; git -C "$repo" log --oneline -1; } > "$W/logs/$tag.log"
run "$@" >> "$W/logs/$tag.log" 2>&1
status=$?
echo "$status" > "$W/logs/$tag.exit"
date >> "$W/logs/$tag.log"
exit $status
