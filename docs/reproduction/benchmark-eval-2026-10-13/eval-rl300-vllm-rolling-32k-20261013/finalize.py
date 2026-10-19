from pathlib import Path
import json,statistics,time
R=Path.cwd();E=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013';job=json.loads((E/'job.json').read_text())
questions=[json.loads(l) for l in Path(job['questions']).read_text().splitlines()];mean=lambda xs:statistics.mean(xs) if xs else None
for rank in range(32):assert json.loads((E/'control'/f'exit-rank-{rank}.json').read_text())['returncode']==0
summaries=[]
for dataset,n in job['counts'].items():
 out=E/'runs'/dataset;rows=[json.loads(l) for p in out.glob('rank-*.jsonl') for l in p.read_text().splitlines() if l.strip()];expected=[r for r in questions if r['dataset']==dataset]
 assert len(rows)==n and len({r['id'] for r in rows})==n and {r['id'] for r in rows}=={r['id'] for r in expected}
 assert all(r['model_identity']['sha256']==job['model_sha256'] and r['instrumented_forward_calls']==r['stats']['actual_model_forward_calls'] for r in rows)
 unknown=sum(r['technical_unknown'] for r in rows);valid=[r for r in rows if r['format_valid']]
 s=dict(passed=unknown==0,checkpoint=300,dataset=dataset,completed=n,technical_unknown=unknown,correct=sum(not r['technical_unknown'] and r['grade']['correct'] for r in rows),format_valid=len(valid),correct_and_parallel=sum(not r['technical_unknown'] and r['grade']['correct'] and r['parallel_valid'] for r in rows),format_and_fork_count_all=sum(r['format_valid'] and r['stats']['forks']>0 for r in rows),actual_forwards_all=mean([r['instrumented_forward_calls'] for r in rows]),sampled_tokens_all=mean([r['stats']['sampled_tokens'] for r in rows]),width_valid=mean([w for r in valid for w in r['widths']]),depth_valid=mean([r['stats']['forks'] for r in valid]),actual_forwards_valid=mean([r['instrumented_forward_calls'] for r in valid]),truncated=sum(r['stats']['truncated'] for r in rows),mean_task_seconds=mean([r['seconds'] for r in rows]),model_sha256=job['model_sha256'],samples_per_question=1,response_budget=32768,max_context=40960,prior_4096_results_not_matched=True,precision=job['precision'],backend=job['backend'],precision_counts=dict(__import__('collections').Counter(r['precision'] for r in rows)),full_traces_retained=True,selection_allowed=False,finished_at=time.time())
 s['accuracy']=s['correct']/n;s['format_and_fork_fraction_all']=s['format_and_fork_count_all']/n
 (out/'summary.json').write_text(json.dumps(s,indent=2)+'\n');summaries.append(s)
result=dict(passed=all(s['passed'] for s in summaries),checkpoint=300,completed=sum(s['completed'] for s in summaries),datasets=summaries,all32exit0=True,wall_seconds=time.time()-job['created_at'],full_traces_retained=True)
(E/'result.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'],'Technical unknown benchmark outcomes: investigate rather than count as wrong'
print(json.dumps(result))
