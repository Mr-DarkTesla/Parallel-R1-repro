#!/usr/bin/env bash
set -euo pipefail
cd ${PROJECT_ROOT}
export PYTHONDONTWRITEBYTECODE=1
exec ${PROJECT_ROOT}/.venv/bin/python ${PROJECT_ROOT}/work/experiments/rl-r2-24gpu-20261012/node_entry.py
