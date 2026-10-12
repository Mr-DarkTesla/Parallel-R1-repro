import collections, hashlib, json, pathlib, random, statistics, time
R=pathlib.Path.cwd()
B=R/'work/experiments/rl-instruct-20261011'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    fs=sorted(p.glob('rank-*.jsonl'))
    a=[json.loads(l) for f in fs for l in f.read_text().splitlines()]
    assert len(a)==500 and len({x['id'] for x in a})==500
    assert all(not x['grade'].get('error') for x in a)
    for x in a:
        assert x['instrumented_forward_calls']==x['stats']['actual_model_forward_calls']
        for z in x.get('fork_batch_ledger',[]):
            assert z['microbatch_max_paths']==8 and z['sequential_subgroup_count']==1
    return {x['id']:x for x in a}, {str(f):sha(f) for f in fs}
def correct(x): return bool(x['grade'].get('correct',x['grade'].get('is_correct',False)))
def summary(a):
    v=list(a.values()); widths=[w for x in v for w in x['widths']]
    return dict(correct=sum(map(correct,v)),accuracy=sum(map(correct,v))/500,format_valid=sum(x['format_valid'] for x in v),parallel_valid=sum(x['parallel_valid'] for x in v),correct_parallel=sum(correct(x) and x['parallel_valid'] for x in v),fork_samples=sum(x['stats']['forks']>0 for x in v),rounds=sum(x['stats']['forks'] for x in v),width_histogram=dict(collections.Counter(widths)),mean_width=statistics.mean(widths) if widths else 0,actual_F=sum(x['instrumented_forward_calls'] for x in v),mean_actual_F=statistics.mean(x['instrumented_forward_calls'] for x in v),sampled_T=sum(x['stats']['sampled_tokens'] for x in v),forced_T=sum(x['stats']['forced_tokens'] for x in v),question_wall_seconds=sum(x['seconds'] for x in v))
baseline, bm=rows(B/'math500-fullwidth8/runs/001-fullSFT-baseline')
baseline_terminal=B/'math500-fullwidth8/baseline-native500-audit.json'
bt=json.loads(baseline_terminal.read_text())
assert bt['passed'] and bt['completed']==500 and bt['missing']==0 and bt['technical_unknowns']==0 and bt['all8worker_exit_zero']
assert all({pathlib.Path(k).name:v for k,v in bm.items()}[pathlib.Path(k).name]==v for k,v in bt['trace_sha256'].items())
bm[str(baseline_terminal)]=sha(baseline_terminal)
for arm in ['R1','R2']:
    result=B/f'math500-priority-RL64/results/{arm}-checkpoint-0064.json'
    if not result.exists(): continue
    terminal=json.loads(result.read_text()); assert terminal['passed'] and terminal['completed']==500 and terminal['missing']==0 and terminal['exit_codes']==[0]*8
    candidate,cm=rows(B/f'math500-priority-RL64/runs/{arm}-checkpoint-0064')
    assert candidate.keys()==baseline.keys()
    assert terminal['protocol']==bt['protocol']
    assert all(candidate[k]['index']==baseline[k]['index'] for k in baseline)
    delta=[int(correct(candidate[k]))-int(correct(baseline[k])) for k in sorted(baseline)]
    rng=random.Random(42161011); boot=sorted(sum(rng.choices(delta,k=500))/500 for _ in range(20000))
    report=dict(passed=True,checkpoint=64,arm=arm,coverage=500,technical_unknown=0,protocol=terminal['protocol'],baseline=summary(baseline),candidate=summary(candidate),paired=dict(improved=sum(d==1 for d in delta),regressed=sum(d==-1 for d in delta),same=sum(d==0 for d in delta),accuracy_difference=sum(delta)/500,bootstrap_95_percentile=[boot[500],boot[19499]],bootstrap_replicates=20000,seed=42161011),inputs_sha256={**bm,**cm,str(result):sha(result)},selection_allowed=False,created=time.time())
    output=B/f'math500-paired-audit/{arm}-checkpoint-0064.json'; output.parent.mkdir(exist_ok=True); output.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps({k:report[k] for k in ['arm','baseline','candidate','paired']}))
