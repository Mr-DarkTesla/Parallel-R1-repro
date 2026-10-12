#!/bin/bash
set -euo pipefail
cd ${PROJECT_ROOT}
exec "$PARALLEL_R1_PYTHON" work/experiments/rl-instruct-20261011/campaign500/continue_arm.py --mode "$1"
