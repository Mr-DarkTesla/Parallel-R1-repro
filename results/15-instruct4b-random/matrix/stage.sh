#!/usr/bin/env bash
# stage.sh: copy matrix results into the owned worktrees (results/<arm>/), no weights, no raw dumps.
set -euo pipefail
D=$(cd "$(dirname "$0")" && pwd)
for a in 14:filtered:14-instruct4b-filtered:14f 15:random:15-instruct4b-random:15r; do
  IFS=: read n w dir short <<< "$a"; R=/Users/v.charkin/Documents/dev/projects/parallel-r1-instruct4b-$w/results/$dir
  mkdir -p "$R/eval" "$R/matrix"
  [ -f "$R/train.log" ] && gzip -kf "$R/train.log"
  rm -rf "$R/eval"/*; for e in "$D"/eval/$short-*; do cp -R "$e" "$R/eval/"; done
  cp -R "$D/compare" "$R/matrix/"; cp "$D"/{DEV_DECISION.md,FINDING-parallel-dump-check.md,progress.md,commands.log,diag-unicode.log,rows-check.log,sft-verify.log,fix-runtime-check.log,audit-*.txt,*.sh,*.py} "$R/matrix/" 2>/dev/null || true
  cp -R "$D/parallel_check_review" "$R/matrix/"; rm -f "$R/matrix/parallel_check_review/response.json"
  [ -f "$D/eval/manifest.json" ] && cp "$D/eval/manifest.json" "$R/eval/manifest-matrix.json"
done
