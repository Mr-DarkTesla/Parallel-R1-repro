#!/usr/bin/env bash
# Full matched dev and IFEval on one GPU in the temporary owned pod.
set -euo pipefail

variant=${1:?tagweighted or control}
case "$variant" in tagweighted|control) ;; *) exit 2 ;; esac
source /work/venv/bin/activate
export PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1
cd /work/parallel-r1
model=/work/exp21-expanded-th-runs/exp21-expanded-th-m1-twopath-tagweighted/model
if [ "$variant" = control ]; then model=/work/exp21-expanded-th-runs/exp21-expanded-th-m1-twopath-tagweighted-control/model; fi
test -e "$model/config.json"
name=m1-twopath-$variant

bash scripts/exp21/pod_jobs.sh eval "$name-dev-th" "$model" dev thinking
bash scripts/exp21/pod_jobs.sh eval "$name-dev-nt" "$model" dev no-thinking
bash scripts/exp21/pod_jobs.sh eval "$name-ifeval-th" "$model" frozen thinking ifeval
bash scripts/exp21/pod_jobs.sh eval "$name-ifeval-nt" "$model" frozen no-thinking ifeval
bash scripts/exp21/pod_jobs.sh eval "$name-dev-mvth" "$model" dev multiverse-thinking
date -Is > "/work/exp21/$name-EVAL_DONE"
