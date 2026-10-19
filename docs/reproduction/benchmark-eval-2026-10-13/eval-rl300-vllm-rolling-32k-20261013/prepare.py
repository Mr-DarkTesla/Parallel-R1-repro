from pathlib import Path
import json,hashlib,tarfile,time,importlib.util,sys
R=Path('${PROJECT_ROOT}');old=R/'work/experiments/eval-rl300-vllm-32k-20261013';E=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013'
with tarfile.open(E/'sources.tar.gz') as t:
 for m in t.getmembers():assert (R/m.name).resolve().is_relative_to(E)
 t.extractall(R)
for n in range(4):assert json.loads((E/'stop-receipts'/f'node-{n}.json').read_text())['gpu_empty']
job=json.loads((old/'job.json').read_text());job.update(root=str(E),created_at=time.time(),questions=str(E/'questions.jsonl'),engine_runtime=str(E/'engine'),backend='vllm0.8.5.post1 structured-DAG BF16 rolling4',precision='MIXED: preserved FP32 completed + BF16 vLLM remaining',questions_per_gpu=4,aggregate_rows=16,slot_capacity=196608,protocol='ALL590tasks n1 32768/768/40960 identical seeds; preserved completed FP32 outputs, remaining BF16 vLLM; physical per-episode participation plus global backend ledger')
(E/'questions.jsonl').write_bytes((old/'questions.jsonl').read_bytes());(E/'job.json').write_text(json.dumps(job,indent=2)+'\n')
questions=[json.loads(l) for l in (E/'questions.jsonl').read_text().splitlines()];done={}
for p in (old/'runs').glob('*/rank-*.jsonl'):
 for line in p.read_text().splitlines():
  r=json.loads(line);assert r['task_index'] not in done;done[r['task_index']]=r
spec=importlib.util.spec_from_file_location('scorer',job['scorer']);scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer)
sys.path.insert(0,job['runtime']);from train import format_flags
recovered=0
for p in (old/'runs').glob('*/raw-rank*.jsonl'):
 for line in p.read_text().splitlines():
  r=json.loads(line)
  if r['task_index'] in done:continue
  valid,parallel=format_flags(r['output'],r['stats']);grade=scorer.grade('<think>\n'+r['output'],r['reference_answer']);unknown=bool(grade.get('error'))
  r.update(grade=grade,technical_unknown=unknown,format_valid=valid,parallel_valid=parallel,seconds=0,seconds_unavailable_recovered_raw=True,finished_at=time.time(),recovered_saved_raw_without_resampling=True)
  done[r['task_index']]=r;recovered+=1
for index,r in done.items():
 assert r['id']==questions[index]['id'] and r['model_identity']['sha256']==job['model_sha256']
 out=E/'runs'/r['dataset'];out.mkdir(parents=True,exist_ok=True)
 for leaf in [f"rank-{r['rank']}.jsonl",f"raw-rank-{r['rank']}.jsonl"]:
  with (out/leaf).open('a') as f:f.write(json.dumps(r,ensure_ascii=False)+'\n')
C=E/'control';C.mkdir()
(C/'queue.json').write_text(json.dumps(dict(next=0,total=590,leases={str(i):dict(state='done',preserved_from=str(old),id=r['id'],dataset=r['dataset']) for i,r in done.items()}))+'\n')
seal0=json.loads((old/'source-seal.json').read_text());shared={p:h for p,h in seal0['sha256'].items() if not Path(p).is_relative_to(old)}
files=[*E.glob('*.py'),*E.joinpath('engine').rglob('*.py'),E/'job.json',E/'questions.jsonl']
(E/'source-seal.json').write_text(json.dumps(dict(passed=True,sha256={**shared,**{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},sources=seal0['sources'],scope='Existing actual vLLM qualified runtime, direct evaluation without smoke'),indent=2)+'\n')
(E/'switch-receipt.json').write_text(json.dumps(dict(passed=True,preserved=len(done),recovered_raw=recovered,remaining=590-len(done),user_authorized=True,old_root=str(old),precision_changed=True,questions_per_gpu=4,time=time.time()),indent=2)+'\n')
print(json.dumps(dict(prepared=True,preserved=len(done),recovered_raw=recovered,remaining=590-len(done))))
