#!/bin/bash
set -euo pipefail
cd /home/jovyan/shares/SR004.nfs3/larin/tmp/r1
exec "$PARALLEL_R1_PYTHON" work/experiments/rl-instruct-20261011/campaign500/continue_arm.py --mode "$1"
