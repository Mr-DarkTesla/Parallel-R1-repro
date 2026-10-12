from pathlib import Path
import json, hashlib, shutil, ast, collections
R=Path('${PROJECT_ROOT}')
B=R/'work/experiments/paperbench-32k-20261012'
OLD=R/'work/experiments/paperbench-rl50-20261012'
M=R/'work/experiments/rl-r2-32gpu-batch32-20261012'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(8<<20),b''):h.update(chunk)
    return h.hexdigest()
B.mkdir(exist_ok=True); (B/'data').mkdir(exist_ok=True)
assert json.loads((OLD/'result.json').read_text())['completed']
allrows=[]; kept=[]; selected=[]; references={}
for name in ['aime24-25-amc23','aime26']:
    job=json.loads((OLD/(name+'-job.json')).read_text())
    source=[json.loads(l) for l in Path(job['questions']).read_text().splitlines()]
    traces=[json.loads(l) for p in (OLD/'runs'/name).glob('rank-*.jsonl') for l in p.read_text().splitlines()]
    assert len(traces)==len(source) and len({r['id'] for r in traces})==len(source)
    byid={r['id']:r for r in traces}
    for i,row in enumerate(source):
        row=dict(row,seed=job['seed']+i*1000,original_index=i,original_suite=name)
        allrows.append(row)
        trace=byid[row['id']];assert not trace['technical_unknown']
        if trace['stats']['truncated']:
            selected.append(row); references[row['id']]=trace['policy_calls'][0]
        else:kept.append(trace)
assert len(allrows)==130 and len(selected)==53 and len(kept)==77
for name,rows in [('all130',allrows),('truncated53',selected),('kept77',kept)]:
    (B/'data'/(name+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
(B/'data/reference-first-calls.json').write_text(json.dumps(references))
src=R/'work/experiments/rl-acceleration-20261012/lanes/cohort_batching/src'
shutil.copytree(src,B/'core',ignore=shutil.ignore_patterns('._*','*.pyc','__pycache__'),dirs_exist_ok=True)
oldjob=json.loads((OLD/'aime26-job.json').read_text())
native=R/'work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model'
nativeproof=json.loads((native.parent/'model-proof.json').read_text())
assert nativeproof['repo']=='Qwen/Qwen3-4B' and nativeproof['original_weights_tokenizer'] and not nativeproof['added_tokens']
common=dict(response_budget=32768,path_budget=768,max_context=40960,samples_per_question=1,world_size=8,temperature=1.,top_p=1.,max_batched_paths=8,scorer=oldjob['scorer'],model=oldjob['model'],system=oldjob['system'],model_sha256=oldjob['model_sha256'])
rl=dict(common,questions=str(B/'data/truncated53.jsonl'),output=str(B/'runs/rl50-retries'),question_batch_size=2,cohort_rows=16,precision='fp32',runtime='HF structured phase cohorts',global_vs_episode_counters_separate=True)
base=dict(common,model=str(native),questions=str(B/'data/all130.jsonl'),output=str(B/'runs/native-instruct'),max_num_seqs=8,precision='bfloat16',runtime='vLLM 0.8.5.post1 V0 TP1 continuous batching',native_source_proof=nativeproof,system='Solve the following mathematics problem. Reason carefully and put the final answer in \\boxed{...}.',native_thinking=True)
for name,cfg in [('rl',rl),('native',base)]: (B/(name+'-job.json')).write_text(json.dumps(cfg,indent=2)+'\n')
files=[*B.glob('*.py'),*B.glob('*-job.json'),*B.joinpath('core').rglob('*.py'),*B.joinpath('data').glob('*')]
for p in files:
    if p.suffix=='.py':ast.parse(p.read_text())
manifest=dict(passed=True,rerun_only_truncated=True,selected=collections.Counter(r['dataset'] for r in selected),kept=77,total=130,model_sha256=oldjob['model_sha256'],native_source_proof=nativeproof,sha256={str(p):sha(p) for p in files},benchmark_only=True)
(B/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n'); print(json.dumps({k:manifest[k] for k in ['passed','selected','kept','total']}))
