"""Post-RL-eval baseline queue on the SAME32 GPUs; no active-source mutations."""
from pathlib import Path
import argparse,fcntl,hashlib,json,os,socket,subprocess,time,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R)
A=R/'work/experiments/eval-baselines-32k-20261013';Q=R/'work/experiments/eval-intermediates-vllm-rolling-32k-20261013';E=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013'
PY=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python';STAGES=['original-instruct','full-sft']
def save(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_name(path.name+'.tmp-'+str(os.getpid()));temp.write_text(json.dumps(value,indent=2)+'\n');os.replace(temp,path)
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(8388608),b''):h.update(b)
 return h.hexdigest()
def wait(path,failroot):
 while not path.exists():
  failures=list(failroot.glob('failure-node-*.json'))
  if failures:raise RuntimeError('Peer failure; keep healthy workers and full traces: '+str(failures))
  time.sleep(10)
 return json.loads(path.read_text())
def empty():return not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
def prepare(label):
 J=A/label;assert not (J/'job.json').exists(),'Existing stage must be reconciled before retry'
 template=json.loads((A/'templates/job.json').read_text());native=json.loads((A/'native-reference.json').read_text());original=label=='original-instruct'
 model=Path(native['model']) if original else R/'work/experiments/instruct-full-20261011/runs/epoch1/final'
 if original:
  hashes=native['native_source_proof']['files']
  for name,digest in hashes.items():assert sha(model/name)==digest,'Original model changed: '+name
 else:
  hashes={p.name:sha(p) for p in model.iterdir() if p.is_file()};assert 'model.safetensors.index.json' in hashes
  index=json.loads((model/'model.safetensors.index.json').read_text());assert set(index['weight_map'].values())<=set(hashes)
 identity=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
 J.mkdir(parents=True,exist_ok=True);(J/'control').mkdir()
 rows=[json.loads(l) for l in (A/'templates/questions.jsonl').read_text().splitlines() if l.strip()]
 if original:rows=[r for r in rows if r['dataset']=='MATH500']
 counts={ds:sum(r['dataset']==ds for r in rows) for ds in ['MATH500','AIME2024','AIME2025','AIME2026'] if any(r['dataset']==ds for r in rows)}
 assert counts==({'MATH500':500} if original else {'MATH500':500,'AIME2024':30,'AIME2025':30,'AIME2026':30})
 (J/'questions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));save(J/'control/queue.json',dict(next=0,total=len(rows),leases={}))
 worker=A/'native_worker.py' if original else A/'templates/worker.py';(J/'worker.py').write_bytes(worker.read_bytes())
 if original:(J/'counting_worker.py').write_bytes((A/'counting_worker.py').read_bytes())
 for name in ['controller.py','finalize.py']:
  source=(A/'templates'/name).read_text().replace(str(E.relative_to(R)),str(J.relative_to(R)))
  source=source.replace('checkpoint=300',"checkpoint=json.loads((E/'job.json').read_text()).get('checkpoint'),model_label=json.loads((E/'job.json').read_text())['model_label']")
  (J/name).write_text(source)
 job={**template,'root':str(J),'created_at':time.time(),'checkpoint':None if original else 0,'model_label':label,'model':str(model),'model_sha256':identity,'model_identity_kind':'SHA256 of sorted actual all model/tokenizer file hash map','model_file_hashes':hashes,'questions':str(J/'questions.jsonl'),'counts':counts,'precision':'BF16','backend':'native-vllm-continuous8' if original else 'vllm-structured-DAG BF16 rolling4','native_system':native['system'],'native_source_proof':native['native_source_proof'],'already_completed_AIME_reference':str(R/'work/experiments/paperbench-32k-20261012/attempt2-main-thread/result.json') if original else None,'protocol':'ALL32k32768/4096040960 n1 t1 p1 seeds identical. Native Instruct uses original thinking/noParallel instructions; fullSFT structured runtime matches current RL BF16. Full raw/physical ledgers preserved.'}
 save(J/'job.json',job);oldseal=json.loads((A/'templates/source-seal.json').read_text());shared={p:h for p,h in oldseal['sha256'].items() if not Path(p).is_relative_to(E) or Path(p).is_relative_to(E/'engine')}
 files=[*J.glob('*.py'),J/'job.json',J/'questions.jsonl'];save(J/'source-seal.json',dict(passed=True,sha256={**shared,**{str(p):sha(p) for p in files}},sources=oldseal['sources'],scope='Post-eval baseline missing scores32k; native installedcounter and rollingDAG engines; no GPU tests'))
 save(J/'model-proof.json',dict(passed=True,label=label,model=str(model),identity=identity,all_actual_file_hashes=hashes,time=time.time()))
 save(J/'prepared.json',dict(passed=True,label=label,time=time.time()))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--node',type=int,required=True);node=ap.parse_args().node;assert socket.gethostname().endswith(['mpimaster-0','mpiworker-0','mpiworker-1','mpiworker-2'][node])
 lock=(A/f'node-{node}.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 for path,digest in json.loads((A/'source-seal.json').read_text())['sha256'].items():assert sha(path)==digest,path
 save(A/f'status-node-{node}.json',dict(state='waiting_for_all_RL_checkpoint_evals',time=time.time()))
 done=wait(Q/'result.json',Q);assert done['passed']
 for label in STAGES:
  assert empty(),'Never launch over active GPU processes';J=A/label
  save(A/f'status-node-{node}.json',dict(state='preparing',stage=label,time=time.time()))
  if node==0:prepare(label)
  assert wait(J/'prepared.json',A)['passed']
  log=(J/f'controller-node-{node}.log').open('ab',buffering=0)
  child=subprocess.Popen([str(PY),'-u',str(J/'controller.py'),'--node',str(node)],cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  fields=Path(f'/proc/{child.pid}/stat').read_text().split(') ',1)[1].split();save(J/'control'/f'controller-launch-node-{node}.json',dict(pid=child.pid,start_ticks=fields[19],node=node,time=time.time()))
  save(A/f'status-node-{node}.json',dict(state='evaluating',stage=label,pid=child.pid,time=time.time()))
  code=child.wait();log.close();assert code==0,f'{label} child failed {code}'
  assert wait(J/'control/completed.json',J/'control')['passed'] and empty()
 if node==0:
  results=[json.loads((A/label/'result.json').read_text()) for label in STAGES];assert all(r['passed'] for r in results)
  save(A/'result.json',dict(passed=True,models=results,original_AIME_previously_completed=str(R/'work/experiments/paperbench-32k-20261012/attempt2-main-thread/result.json'),all_raw_traces_retained=True,finished_at=time.time()))
 wait(A/'result.json',A);save(A/f'status-node-{node}.json',dict(state='completed',time=time.time()))
if __name__=='__main__':
 try:main()
 except BaseException as error:
  node=next((int(os.sys.argv[i+1]) for i,x in enumerate(os.sys.argv) if x=='--node'),-1);save(A/f'failure-node-{node}.json',dict(error=repr(error),traceback=traceback.format_exc(),time=time.time()));raise
