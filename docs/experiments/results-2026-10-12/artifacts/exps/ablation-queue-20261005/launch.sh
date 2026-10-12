#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
nohup ${PROJECT_ROOT}/.venv/bin/python -u run_queue.py > queue.log 2>&1 < /dev/null &
printf '%s\n' "$!" > runner.pid
cat runner.pid
