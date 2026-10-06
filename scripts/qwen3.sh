#!/usr/bin/env bash
# Common entry point; all remaining arguments are passed to the stage launcher.
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd)
stage=${1:-help}
if [ "$#" -gt 0 ]; then shift; fi
case "$stage" in
  sft|eval|rl) exec bash "$repo/verl/training_scripts/${stage}_qwen3_06b.sh" "$@" ;;
  help|-h|--help)
    echo 'Usage: bash scripts/qwen3.sh sft [seen|unseen] [Hydra overrides...]'
    echo '       bash scripts/qwen3.sh eval CHECKPOINT [Hydra overrides...]'
    echo '       bash scripts/qwen3.sh rl s1|s2 CHECKPOINT [Hydra overrides...]'
    echo 'Shared settings: active Python, NPROC_PER_NODE, PARALLEL_R1_OUTPUT_ROOT, PARALLEL_R1_SCRATCH_ROOT'
    ;;
  *) echo "Unknown stage: $stage" >&2; exit 2 ;;
esac
