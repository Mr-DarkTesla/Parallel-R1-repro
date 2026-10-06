#!/usr/bin/env bash
# Run both comparisons sequentially; restart only from each run's own checkpoint.
set -euo pipefail
ROOT=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
MODEL="$ROOT/models/sft-epoch5/global_step_230"
STATE="$ROOT/runs/night"
mkdir -p "$STATE"
exec 9>"$STATE/queue.lock"
flock -n 9 || { echo 'Another overnight queue is already running'; exit 1; }
exec > >(tee -a "$STATE/queue.log") 2>&1
printf '%s Queue started on %s\n' "$(date -Is)" "$(hostname)"
export PYTHONUNBUFFERED=1
export SMOKE=0
trap 'code=$?; printf "%s Queue exit=%s\n" "$(date -Is)" "$code"; exit "$code"' EXIT
for mode in s1 s2; do
  name="qwen06-$mode-seed1"
  run="$ROOT/runs/$name"
  mkdir -p "$run"
  if [[ -f "$STATE/$mode.done" ]]; then
    printf '%s %s already complete\n' "$(date -Is)" "$mode"
    continue
  fi
  printf '%s\n' "$mode" > "$STATE/current_mode"
  printf '%s Starting %s (300 steps, own checkpoint resume)\n' "$(date -Is)" "$mode"
  validation_args=()
  if [[ -f "$run/checkpoints/latest_checkpointed_iteration.txt" ]]; then
    latest=$(cat "$run/checkpoints/latest_checkpointed_iteration.txt")
    # A reboot during final validation must not cause a 301st optimizer update.
    if [[ "$latest" -ge 300 ]]; then
      validation_args=(trainer.val_before_train=True trainer.val_only=True)
    fi
  fi
  RUN_NAME="$name" bash "$ROOT/repo/experiments/qwen06/run_rl.sh" "$mode" "$MODEL" \
    trainer.resume_mode=auto trainer.save_freq=1 trainer.max_actor_ckpt_to_keep=3 \
    "${validation_args[@]}" \
    2>&1 | tee -a "$run/train.log"
  # Successful completion must include the final persisted training step.
  latest=$(cat "$run/checkpoints/latest_checkpointed_iteration.txt")
  [[ "$latest" -ge 300 ]] || { echo "Run exited before step 300: $mode step $latest"; exit 1; }
  printf '%s step=%s\n' "$(date -Is)" "$latest" > "$STATE/$mode.done"
done
printf '%s\n' complete > "$STATE/current_mode"
printf '%s Both comparisons complete\n' "$(date -Is)"
