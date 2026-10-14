"""Finalize complete MATH500 traces; never use benchmark results for training selection."""
from pathlib import Path
import json,hashlib,statistics,time
R=Path.cwd();M=R/'work/experiments/rl-r2-32gpu-batch32-20261012'
job=json.loads((M/'evaluation-job.json').read_text());out=Path(job['output'])
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
questions=[json.loads(l) for l in Path(job['questions']).read_text().splitlines() if l.strip()]
assert len(questions)==500 and len({r['id'] for r in questions})==500
paths=[out/f'rank-{rank}.jsonl' for rank in range(32)]
rows=[json.loads(l) for p in paths for l in p.read_text().splitlines() if l.strip()]
assert len(rows)==500 and {r['index'] for r in rows}==set(range(500)) and len({r['id'] for r in rows})==500
for r in rows:
 assert r['id']==questions[r['index']]['id'] and not r['grade'].get('error') and not r.get('technical_unknown')
 assert r['instrumented_forward_calls']==r['stats']['actual_model_forward_calls']
 assert all(g['microbatch_max_paths']==8 and g['sequential_subgroup_count']==1 for g in r['fork_batch_ledger'])
valid=[r for r in rows if r['format_valid']]
widths=[w for r in rows for w in r['widths']]
conditional_widths=[w for r in valid for w in r['widths']]
mean=lambda a:statistics.mean(a) if a else None
summary=dict(passed=True,checkpoint=50,completed=500,missing=0,technical_unknowns=0,
 correct=sum(r['grade']['correct'] for r in rows),format_valid=len(valid),parallel_valid=sum(r['parallel_valid'] for r in rows),
 correct_and_parallel=sum(r['grade']['correct'] and r['parallel_valid'] for r in rows),fork_tasks=sum(r['stats']['forks']>0 for r in rows),
 format_and_fork_count_all=sum(r['format_valid'] and r['stats']['forks']>0 for r in rows),
 mean_actual_forwards=mean([r['instrumented_forward_calls'] for r in rows]),mean_sampled_tokens=mean([r['stats']['sampled_tokens'] for r in rows]),
 mean_width=mean(widths),mean_depth=mean([r['stats']['forks'] for r in rows]),
 format_conditioned=dict(n=len(valid),mean_actual_forwards=mean([r['instrumented_forward_calls'] for r in valid]),mean_width=mean(conditional_widths),mean_depth=mean([r['stats']['forks'] for r in valid])),
 all32_worker_exit0=True,traces={str(p):sha(p) for p in paths},traces_always_retained=True,
 eval_worker_sha256=sha(M/'eval_worker.py'),questions_sha256=sha(job['questions']),model_sha256=job['model_sha256'],
 protocol='FP32 fullwidth8; native think prefix; temperature1 top_p1; response4096 path768 context16384; seed42161011+index*1000; corrected final-answer scorer; instrumented F',
 selection_allowed=False,benchmark=True,finished_at=time.time())
summary['accuracy']=summary['correct']/500
summary['format_and_fork_fraction_all']=summary['format_and_fork_count_all']/500
base_dir=R/'work/experiments/rl-instruct-20261011/math500-fullwidth8/runs/001-fullSFT-baseline'
base=[json.loads(l) for p in base_dir.glob('rank-*.jsonl') for l in p.read_text().splitlines() if l.strip()]
assert len(base)==500 and len({r['id'] for r in base})==500
baseline={r['id']:r for r in base}
assert set(baseline)=={r['id'] for r in rows}
summary['matched_fullSFT_baseline']=dict(correct=sum(r['grade']['correct'] for r in base),completed=500,
 mean_actual_forwards=mean([r['instrumented_forward_calls'] for r in base]),
 improved=sum(r['grade']['correct'] and not baseline[r['id']]['grade']['correct'] for r in rows),
 regressed=sum(not r['grade']['correct'] and baseline[r['id']]['grade']['correct'] for r in rows),
 source=str(base_dir))
p=out/'summary.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(summary,indent=2)+'\n');tmp.replace(p)
print(json.dumps({k:summary[k] for k in ['passed','completed','correct','format_valid','format_and_fork_count_all','mean_actual_forwards','mean_width','mean_depth']}))
