#!/usr/bin/env bash
# compact read-only B eval status (one line per queue + finished rows), appended to st.log
O=/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06
s=$("$O/executor/k.sh" vcharkin-exp-vm-b-0 "for g in 0 1; do echo gpu\$g left=\$(wc -l < /work/queue/gpu\$g.txt) \$(grep -E ' (START|END) ' /work/queue/gpu\$g.log | tail -1 | cut -c1-20,21-30 ; grep -E ' (START|END) ' /work/queue/gpu\$g.log | tail -1 | grep -oE 'run_eval.sh [^ ]+' ) fails=\$(wc -l < /work/queue/gpu\$g.txt.failed 2>/dev/null || echo 0); done
  for d in /work/bench/instruct4b/1[45]*; do echo \${d##*/}: \$(ls \$d/rows 2>/dev/null | sed 's/.jsonl//' | tr '\n' ' '); done; df -h /work | tail -1 | awk '{print \"free\",\$4}'" 2>&1 | grep -v setlocale)
echo "$(date '+%F %T') $(echo "$s" | tr '\n' '|')" >> "$O/matrix_continue/st.log"; echo "$s"
