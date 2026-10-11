#!/usr/bin/env bash
# Matched one-GPU 32-step SFT on all 46 fully reviewed positive tasks.
set -euo pipefail

data=/work/exp21/qwen4b_clean46
test -s "$data/build_report.json"
python3 - "$data/build_report.json" <<'PY'
import json, sys
x = json.load(open(sys.argv[1]))
assert x['accepted']['count'] == 46
assert x['rows_per_arm'] == {'train': 247, 'val': 50}
assert x['train']['positive_rows'] == 138
assert x['train']['replay_thinking'] == 55
assert x['train']['replay_no_thinking'] == 54
assert x['checks']['plain_equals_tagged_after_removing_only_tags']
assert x['checks']['candidate_eval_leakcheck'] == 'passed'
assert x['checks']['train_validation_question_overlap'] == 0
assert x['checks']['train_fixed40_question_overlap'] == 0
PY

export QWEN4B_PAIR_DATA_ROOT="$data"
export QWEN4B_PAIR_PREREQ_DONE=/work/exp21/qwen4b_onpolicy189/EVAL_DONE
export QWEN4B_PAIR_REQUIRE_GENERATOR=0
export QWEN4B_PAIR_RUN_PREFIX=exp21-4b-clean46
exec bash /work/parallel-r1/scripts/exp21/run_qwen4b_onpolicy189_pair_pod.sh
