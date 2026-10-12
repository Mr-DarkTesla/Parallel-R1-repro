"""Pin canonical evaluation-only AIME24/25, AMC23, AIME26; one sample per task."""
from pathlib import Path
import json,hashlib,requests,re,collections,ast
import pyarrow.parquet as pq
R=Path('${PROJECT_ROOT}');B=R/'work/experiments/paperbench-rl50-20261012';B.mkdir(exist_ok=True);D=B/'data';D.mkdir(exist_ok=True)
M=R/'work/experiments/rl-r2-32gpu-batch32-20261012';N=R/'work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'work/experiments/rl-instruct-20261011/data';proof=json.loads((old/'reserved-aime-canonical-proof.json').read_text());assert sha(old/'reserved-aime2024-2025-canonical.jsonl')==proof['sha256']
aime=[json.loads(l) for l in (old/'reserved-aime2024-2025-canonical.jsonl').read_text().splitlines() if l.strip()]
rows=[dict(id=r['id'],problem=r['problem'],answer=str(r['answer']),dataset='AIME'+str(r['year']),url=r['url']) for r in aime]
assert collections.Counter(r['dataset'] for r in rows)=={'AIME2024':30,'AIME2025':30}
sources=dict(AIME24_25_canonical_proof=proof)
for label,repo,rev,expected in [('AMC2023','math-ai/amc23','80815d37005feb82cd7f8fbc6901d5d3eff43057',40),('AIME2026','MathArena/aime_2026','d2de22f3c656b4f56cf8981212186377d1e23bc3',30)]:
 response=requests.get('https://huggingface.co/api/datasets/'+repo+'/revision/'+rev,timeout=60);response.raise_for_status();info=response.json();assert info['sha']==rev
 files=[x['rfilename'] for x in info['siblings'] if x['rfilename'].endswith(('.jsonl','.parquet'))];assert len(files)==1,files
 name=files[0];raw=requests.get('https://huggingface.co/datasets/'+repo+'/resolve/'+rev+'/'+name,timeout=120);raw.raise_for_status();p=D/(label+Path(name).suffix);p.write_bytes(raw.content)
 data=pq.read_table(p).to_pylist() if p.suffix=='.parquet' else [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
 assert len(data)==expected,(label,len(data))
 parsed=[]
 for i,r in enumerate(data):
  question=r['problem'] if 'problem' in r else r['question'];answer=str(r['answer']);identifier=r.get('problem_idx',r.get('id',i))
  assert isinstance(question,str) and len(question)>20 and not re.search(r'(?<![\\a-zA-Z])rac\s*\{',question),identifier
  if label.startswith('AIME'):assert answer.isdigit() and 0<=int(answer)<=999
  parsed.append(dict(id=label+'/'+str(identifier),problem=question,answer=answer,dataset=label,url=r.get('url'),source_revision=rev))
 assert len({r['id'] for r in parsed})==expected
 sources[label]=dict(repo=repo,revision=rev,raw_sha256=sha(p),file=name,rows=expected,upstream_schema=list(data[0]),usage='evaluation-only; not training, curriculum, reward or checkpoint selection')
 if label=='AMC2023':rows.extend(parsed)
 else:next_rows=parsed
assert len(rows)==100 and len(next_rows)==30
for name,data in [('aime24-25-amc23',rows),('aime26',next_rows)]:
 p=D/(name+'.jsonl');p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
train=json.loads((M/'production-config-v2.json').read_text())
training=[json.loads(l) for l in Path(train['train']).read_text().splitlines() if l.strip()]
norm=lambda s:re.sub(r'\s+','',s).lower()
known={norm(r.get('problem',r.get('question',''))) for r in training}
exact=[r['id'] for r in [*rows,*next_rows] if norm(r['problem']) in known]
assert not exact,exact
model=N/'production/checkpoint-0050/hf';model_proof=json.loads((M/'checkpoint-0050-handoff-proof.json').read_text());assert model_proof['passed']
jobs=[]
for name in ['aime24-25-amc23','aime26']:
 job=dict(model=str(model),system=train['system'],scorer=train['scorer'],questions=str(D/(name+'.jsonl')),output=str(B/'runs'/name),world_size=8,samples_per_question=1,temperature=1,response_budget=4096,path_budget=768,max_context=16384,max_batched_paths=8,seed=42161011,model_sha256=model_proof['model_sha256'],selection_allowed=False,benchmark=True)
 p=B/(name+'-job.json');p.write_text(json.dumps(job,indent=2)+'\n');jobs.append(str(p))
files=[B/'worker.py',B/'finalize.py',B/'launch.py',*map(Path,jobs),*D.glob('*.jsonl')]
for p in sorted((R/'work/experiments/rl-instruct-20261011/production-runner').rglob('*.py')):files.append(p)
for p in files:
 if p.suffix=='.py':ast.parse(p.read_text())
manifest=dict(passed=True,gpus=8,host_role='mpiworker-2',checkpoint=50,model_sha256=model_proof['model_sha256'],samples_per_question=1,jobs=jobs,sources=sources,question_counts=collections.Counter(r['dataset'] for r in [*rows,*next_rows]),exact_problem_overlaps_with_train1024=exact,semantic_decontamination_not_exhaustive=True,all_eval_only=True,full_traces=True,sha256={str(p):sha(p) for p in files})
(B/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:manifest[k] for k in ['passed','gpus','checkpoint','samples_per_question','question_counts','exact_problem_overlaps_with_train1024']}))
