#!/usr/bin/env bash
# cmp.sh <out-name> <suite dev|frozen> <base run dir> <cand run dir> [--cross-prompt]: reviewed paired_compare.py (84e2140 copy in
# the exp/14 worktree), CPU, local. Output compare/<out-name>.json + .txt.
set -euo pipefail
O=/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06; W=/Users/v.charkin/Documents/dev/projects/parallel-r1-instruct4b-filtered
out=$1 suite=$2 base=$3 cand=$4; shift 4
mkdir -p "$O/matrix_continue/compare"
meta=(--meta-dir "$O/eval_finalize/data/meta/$suite"); [ "${1:-}" = --cross-prompt ] && meta=()
cd "$W/verl" && PYTHONDONTWRITEBYTECODE=1 python3 ../scripts/instruct4b_eval/paired_compare.py --base "$base" --cand "$cand" "${meta[@]}" "$@" \
  --out "$O/matrix_continue/compare/$out.json" > "$O/matrix_continue/compare/$out.txt" 2>&1
echo "$(date '+%F %T') cmp.sh $out $suite $base $cand $*" >> "$O/matrix_continue/commands.log"
