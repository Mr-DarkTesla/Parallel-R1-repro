#!/usr/bin/env bash
# syncpar.sh <14|15>: bundle the owned branch to B and add a SEPARATE detached worktree /work/exps/<arm>-par at the branch HEAD
# (parallel evals with the reviewed post-check fix). The existing /work/exps/<arm> worktrees (baad652/dbe704b, used by running
# no-thinking/thinking jobs) are not touched. Refuses if the -par worktree exists at another commit.
set -euo pipefail
O=/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06; k() { "$O/executor/k.sh" vcharkin-exp-vm-b-0 "$@" 2> >(grep -v setlocale >&2); }
case $1 in
14) W=/Users/v.charkin/Documents/dev/projects/parallel-r1-instruct4b-filtered B=exp/14-instruct4b-filtered R=/work/exps/14-instruct4b-filtered ;;
15) W=/Users/v.charkin/Documents/dev/projects/parallel-r1-instruct4b-random B=exp/15-instruct4b-random R=/work/exps/15-instruct4b-random ;;
esac
[ -z "$(git -C "$W" status --short --untracked-files=no)" ] || { echo "$W dirty"; exit 1; }
c=$(git -C "$W" rev-parse --short HEAD); old=$(k "git -C $R rev-parse HEAD" | tr -dc 0-9a-f)
tmp=$(mktemp -d); git -C "$W" bundle create "$tmp/a.bundle" "$old..$B" 2>/dev/null
"$O/executor/ki.sh" vcharkin-exp-vm-b-0 "cat > /tmp/matrixpar$1.bundle" < "$tmp/a.bundle" 2>/dev/null; rm -rf "$tmp"
k "set -e; git -C /work/parallel-r1 fetch -q /tmp/matrixpar$1.bundle $B:refs/matrix/exp$1; rm -f /tmp/matrixpar$1.bundle
   if [ -d $R-par ]; then test \"\$(git -C $R-par rev-parse --short HEAD)\" = $c || { echo '$R-par at another commit'; exit 1; }
   else git -C /work/parallel-r1 worktree add -q --detach $R-par $c; fi
   echo par HEAD=\$(git -C $R-par rev-parse --short HEAD) status=\$(git -C $R-par status --short | wc -l) '|' main HEAD=\$(git -C $R rev-parse --short HEAD)"
