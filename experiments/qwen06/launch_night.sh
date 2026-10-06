#!/usr/bin/env bash
# Idempotent launcher for manual use and the boot-time systemd unit.
set -euo pipefail
ROOT=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
SESSION=parallel-r1-rl
STATE="$ROOT/runs/night"
mkdir -p "$STATE"
if [[ -f "$STATE/s1.done" && -f "$STATE/s2.done" ]]; then
  echo 'Both runs already complete; nothing to launch'
  exit 0
fi
if tmux has-session -t "$SESSION" 2>/dev/null; then
  if [[ "$(tmux display-message -p -t "$SESSION" '#{pane_dead}')" != 1 ]]; then
    echo 'Overnight tmux session is already active'
    exit 0
  fi
  tmux kill-session -t "$SESSION"
fi
tmux new-session -d -s "$SESSION" "bash '$ROOT/repo/experiments/qwen06/overnight.sh'"
tmux set-option -t "$SESSION" remain-on-exit on
echo "Started tmux session $SESSION"
