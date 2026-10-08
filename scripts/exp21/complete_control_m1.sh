#!/usr/bin/env bash
set -euo pipefail
jobs=/work/exps/21-qwen3-0.6b-multiverse/scripts/exp21/pod_jobs.sh
model=/work/runs/exp21-control-m1/model
bash "$jobs" eval control-m1-ifeval-nt "$model" frozen no-thinking ifeval
bash "$jobs" eval control-m1-ifeval-th "$model" frozen thinking ifeval
bash "$jobs" eval control-m1-dev-mv "$model" dev multiverse
bash "$jobs" eval control-m1-dev-mvb "$model" dev multiverse-branch
