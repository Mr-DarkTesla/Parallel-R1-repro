#!/usr/bin/env bash
set -uo pipefail
root=${PROJECT_ROOT}
source "$root/.venv/bin/activate"
cd "$root/verl"
export R1_OUTPUT_ROOT="$root/verl/checkpoints/eval/qwen3-06b-unseen-20261005"
export NPROC_PER_NODE=8
for epoch in 0 1 2 3 4 5; do
  if [ "$epoch" = 0 ]; then
    model=${MODEL_ROOT}/Qwen3-0.6B-Base-special
    name=base
  else
    model=${MODEL_ROOT}/Parallel-SFT-Unseen-Qwen3-0.6B/global_step_$((46 * epoch))
    name=epoch-$epoch
  fi
  export R1_EVAL_NAME="$name"
  printf '%s\t%s\tstart\n' "$(date -u +%FT%TZ)" "$name" >> "$R1_OUTPUT_ROOT/status.tsv"
  bash training_scripts/eval_qwen3_06b.sh "$model" data.val_batch_size=256 ray_init.num_cpus=32 > "$R1_OUTPUT_ROOT/$name.driver.log" 2>&1
  rc=$?
  printf '%s\n' "$rc" > "$R1_OUTPUT_ROOT/$name.exit_code"
  printf '%s\t%s\tend\t%s\n' "$(date -u +%FT%TZ)" "$name" "$rc" >> "$R1_OUTPUT_ROOT/status.tsv"
done
printf 'done\n' > "$R1_OUTPUT_ROOT/finished"
