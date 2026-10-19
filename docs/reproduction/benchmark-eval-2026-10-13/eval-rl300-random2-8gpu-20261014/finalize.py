from pathlib import Path
from statistics import mean
from collections import Counter
import json,time,sys
E=Path(sys.argv[1]);job=json.loads((E/'job.json').read_text())
assert all(json.loads((E/f'control/exit-rank-{i}.json').read_text())['returncode']==0 for i in range(8))
summaries=[]
for dataset,n in [('MATH500',500),('AIME2024',30),('AIME2025',30),('AIME2026',30)]:
 rows=[json.loads(l) for p in (E/'runs'/dataset).glob('rank-*.jsonl') for l in p.open() if l.strip()]
 raw=[json.loads(l) for p in (E/'runs'/dataset).glob('raw-rank-*.jsonl') for l in p.open() if l.strip()]
 assert len(rows)==len(raw)==len({r['id'] for r in rows})==n
 assert {r['id'] for r in raw}=={r['id'] for r in rows}
 assert all(r['model_identity']['sha256']==job['model_sha256'] and r['instrumented_forward_calls']==r['stats']['actual_model_forward_calls'] for r in rows)
 choices=[x for r in rows for x in r['branch_selection_ledger']]
 assert all(x['executed_width']==2 and len(set(x['selected_original_path_ids']))==2 and all(1<=v<=x['requested_width'] for v in x['selected_original_path_ids']) for x in choices)
 unknown=sum(r['technical_unknown'] for r in rows)
 summary=dict(passed=unknown==0,dataset=dataset,completed=n,technical_unknown=unknown,
  correct=sum(not r['technical_unknown'] and r['grade']['correct'] for r in rows),
  accuracy=sum(not r['technical_unknown'] and r['grade']['correct'] for r in rows)/n,
  actual_forwards_all=mean(r['instrumented_forward_calls'] for r in rows),
  sampled_tokens_all=mean(r['stats']['sampled_tokens'] for r in rows),
  format_valid=sum(r['format_valid'] for r in rows),strict_format_note='Deliberate pruning preserves original requested width and selected Path IDs; strict count/numbering violations can be intervention-induced.',
  tasks_with_fork=sum(bool(r['widths']) for r in rows),executed_forks=len(choices),
  executed_width_all=mean(x['executed_width'] for x in choices) if choices else None,
  requested_width_all=mean(x['requested_width'] for x in choices) if choices else None,
  requested_width_histogram=dict(Counter(x['requested_width'] for x in choices)),
  branches_dropped=sum(x['requested_width']-2 for x in choices),selection_ledger_passed=True,
  truncated=sum(r['stats']['truncated'] for r in rows),model_sha256=job['model_sha256'],precision='BF16',
  response_budget=32000,path_budget=4000,max_context=40960,samples_per_question=1,full_traces_retained=True)
 (E/'runs'/dataset/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');summaries.append(summary)
assert sum(x['completed'] for x in summaries)==590 and all(x['passed'] for x in summaries)
(E/'result.json').write_text(json.dumps(dict(passed=True,checkpoint=300,completed=590,datasets=summaries,all8exit0=True,full_traces_retained=True,intervention=job['branch_policy'],finished_at=time.time()),indent=2)+'\n')
print(json.dumps(summaries))
