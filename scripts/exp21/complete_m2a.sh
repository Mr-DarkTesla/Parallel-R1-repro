#!/usr/bin/env bash
set -euo pipefail
jobs=/work/exps/21-qwen3-0.6b-multiverse/scripts/exp21/pod_jobs.sh
model=/work/runs/exp21-m2-audited/model
bash "$jobs" eval m2a-ifeval-nt "$model" frozen no-thinking ifeval
bash "$jobs" eval m2a-ifeval-th "$model" frozen thinking ifeval
bash "$jobs" eval m2a-dev-mv "$model" dev multiverse
bash "$jobs" eval m2a-dev-mvb "$model" dev multiverse-branch
