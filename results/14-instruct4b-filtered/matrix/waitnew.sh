#!/usr/bin/env bash
# waitnew.sh: block <= ~9 min (3 polls x 170 s), return early when the set of finished 14f/15r rows or the failed-line count changes.
D=$(cd "$(dirname "$0")" && pwd)
snap() { "$D/../executor/k.sh" vcharkin-exp-vm-b-0 "ls /work/bench/instruct4b/1[45]*/rows/ 2>/dev/null | tr '\n' ' '; cat /work/queue/gpu*.txt.failed 2>/dev/null | wc -l" 2>/dev/null; }
a=$(snap); for i in 1 2 3; do sleep 170; b=$(snap); [ -n "$b" ] && [ "$a" != "$b" ] && break; done
bash "$D/st.sh" 2>&1 | grep -v "No such\|stale"
