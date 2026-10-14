#!/usr/bin/env bash
set -euo pipefail
cd ${PROJECT_ROOT}
exec "$PARALLEL_R1_PYTHON" -B ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/runner/launch_readiness.py --lane tmp2 --receipt ${PROJECT_ROOT}/work/experiments/rl-instruct-20261011/technical-root-approved.json
