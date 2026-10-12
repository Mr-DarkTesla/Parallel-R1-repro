#!/bin/bash
set -euo pipefail
cd ${PROJECT_ROOT}
exec "$PARALLEL_R1_PYTHON" ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/production-runner/launch-r1-independent.py --config ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/config.json --receipt ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/direct-full500/r1-repair/approved.json
