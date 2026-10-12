"""Machine evidence for the exact 50-task review; never releases production."""
from pathlib import Path
import collections, hashlib, json
import numpy as np

P=Path.cwd();B=P/'work/experiments/deep-sft-20261010';D=B/'pilot'
tasks={r['id']:r for r in map(json.loads,(B/'pilot-tasks.jsonl').read_text().splitlines())}
records=[json.loads(l) for l in (D/'journal.jsonl').open()]
assert len(tasks)==len(records)==50 and {r['id'] for r in records}==tasks.keys()
first=[r['attempts'][0] for r in records]
raw_correct=sum(r.get('grade',{}).get('correct') is True and not r.get('grade',{}).get('error') for r in first)
raw_canonical=sum(r.get('structure',{}).get('valid') is True and r.get('finish_reason')=='stop' and '<think>' not in r.get('output','') for r in first)
raw_all=sum(r.get('grade',{}).get('correct') is True and r.get('structure',{}).get('valid') is True and r.get('judge',{}).get('accept') is True and not r.get('error') for r in first)
accepted=[r['row'] for r in records if r['decision']=='accepted'];rounds=[r['fork_count'] for r in accepted];widths=[w for r in accepted for w in r['branch_schedule']]
paths=[n for r in accepted for n in r['metrics']['path_tokens']]
checks=dict(all_exactly_50_planned_tasks_accounted=True,raw_at_least_45_correct_canonical_judgeok=raw_all>=45,
    all_accepted_reference_correct=all(r['verification']['final_answer']['correct'] is True for r in accepted),
    all_accepted_explicit_arithmetic_consistent=all(not r['verification']['explicit_arithmetic']['mismatches'] for r in accepted),
    accepted_mean_width_target=bool(widths) and 3.5<=np.mean(widths)<=4.5,
    accepted_mean_rounds_target=bool(rounds) and 3.5<=np.mean(rounds)<=4.5,
    accepted_80percent_at_least_3_rounds=bool(rounds) and np.mean(np.array(rounds)>=3)>=.8)
report=dict(planned=50,completed=50,accepted=len(accepted),rejected=50-len(accepted),
    first_attempt=dict(correct=raw_correct,canonical=raw_canonical,correct_canonical_judgeok=raw_all),
    retries=sum(len(r['attempts'])-1 for r in records),criteria_machine=checks,machine_pass=all(checks.values()),
    manual_review_required=True,production_released=False,
    actual_mean_width=float(np.mean(widths)) if widths else None,actual_mean_rounds=float(np.mean(rounds)) if rounds else None,
    path_tokens_median=float(np.median(paths)) if paths else None,path_tokens_p95=float(np.percentile(paths,95)) if paths else None,
    width_histogram=dict(collections.Counter(widths)),round_histogram=dict(collections.Counter(rounds)),
    all_flagged=[dict(id=r['id'],errors=[a.get('error') for a in r['attempts'] if a.get('error')]) for r in records if any(a.get('error') for a in r['attempts'])],
    sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [B/'teacher-prompt.txt',B/'judge-prompt.txt',B/'pilot-tasks.jsonl',D/'journal.jsonl',D/'report.json']})
(D/'machine-audit.json').write_text(json.dumps(report,indent=2)+'\n')
with (D/'actual-traces-for-review.jsonl').open('w') as f:
    for r in sorted(records,key=lambda r:r['id']):
        f.write(json.dumps(dict(id=r['id'],problem=tasks[r['id']]['question'],reference_answer=tasks[r['id']]['reference'],decision=r['decision'],attempts=r['attempts']),ensure_ascii=False)+'\n')
print(json.dumps(report,indent=2))
