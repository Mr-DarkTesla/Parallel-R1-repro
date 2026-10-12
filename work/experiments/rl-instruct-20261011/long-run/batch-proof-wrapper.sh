#!/bin/bash
set -euo pipefail
cd ${PROJECT_ROOT}
exec "$PARALLEL_R1_PYTHON" work/experiments/rl-instruct-20261011/long-run/launch_batch_proof.py --receipt work/experiments/rl-instruct-20261011/long-run/batch-proof-root-approved.json
