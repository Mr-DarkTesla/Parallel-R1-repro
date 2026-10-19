"""Sequential full32 eval after RL300; never starts training or stops GPU workers."""
from pathlib import Path
import argparse,fcntl,hashlib,json,os,socket,subprocess,time,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R)
Q=R/'work/experiments/eval-intermediates-vllm-rolling-32k-20261013';E=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013'
P=R/'work/experiments/rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory'
PY=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
STEPS=[50,100,150,200,250]
def save(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+'.tmp-'+str(os.getpid()));tmp.write_text(json.dumps(value,indent=2)+'\n');os.replace(tmp,path)
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(8388608),b''):h.update(b)
 return h.hexdigest()
def wait(path,fail_root):
 while not path.exists():
  failures=list(fail_root.glob('failure-node-*.json'))
  if failures:raise RuntimeError('Peer failure; preserve healthy children: '+str(failures))
  time.sleep(10)
 return json.loads(path.read_text())
def empty():return not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
def prepare(step):
 J=Q/f'checkpoint-{step:04d}';assert not (J/'job.json').exists(),'Reconcile existing stage before retry'
 cp=(R/'work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/production/checkpoint-0050') if step==50 else P/'production'/f'checkpoint-{step:04d}'
 receipt=json.loads((cp/'complete.json').read_text());assert receipt['step']==step and receipt['unsharded'] and not receipt.get('optimizer',False) and not receipt.get('rng',False)
 hf=cp/'hf';assert all((hf/name).exists() for name in ['model.safetensors','config.json','tokenizer_config.json'])
 digest=sha(hf/'model.safetensors')
 if step==50:assert digest=='727550dbcb49937625a451e02c8c0c700d80c95685b63d0fcff983e09c00f42c'
 else:
  for name,value in receipt['files'].items():assert (cp/name).stat().st_size==value['bytes'] and sha(cp/name)==value['sha256'],name
  assert digest==receipt['files']['hf/model.safetensors']['sha256']
 J.mkdir(parents=True,exist_ok=True);(J/'control').mkdir();(J/'control/queue.json').write_text(json.dumps(dict(next=0,total=590,leases={})))
 for name in ['controller.py','worker.py','finalize.py']:
  source=(Q/'templates'/name).read_text().replace("work/experiments/eval-rl300-vllm-rolling-32k-20261013",str(J.relative_to(R))).replace('checkpoint=300',f'checkpoint={step}')
  (J/name).write_text(source)
 (J/'questions.jsonl').write_bytes((Q/'templates/questions.jsonl').read_bytes())
 job=json.loads((Q/'templates/job.json').read_text());job.update(root=str(J),precision='BF16',created_at=time.time(),checkpoint=step,model=str(hf),model_sha256=digest,checkpoint_complete_sha256=sha(cp/'complete.json'),questions=str(J/'questions.jsonl'))
 save(J/'job.json',job)
 original=json.loads((Q/'templates/source-seal.json').read_text())
 shared={p:h for p,h in original['sha256'].items() if not Path(p).is_relative_to(E) or Path(p).is_relative_to(E/'engine')}
 files=[*J.glob('*.py'),J/'job.json',J/'questions.jsonl']
 save(J/'source-seal.json',dict(passed=True,sha256={**shared,**{str(p):sha(p) for p in files}},sources=original['sources'],scope='Same frozen RL300 eval runtime; 32k all tasks'))
 save(J/'checkpoint-proof.json',dict(passed=True,checkpoint=step,model_sha256=digest,receipt_sha256=sha(cp/'complete.json'),weights_only=True))
 save(J/'prepared.json',dict(passed=True,checkpoint=step,time=time.time()))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--node',type=int,required=True);node=ap.parse_args().node
 assert socket.gethostname().endswith(['mpimaster-0','mpiworker-0','mpiworker-1','mpiworker-2'][node])
 lock=(Q/f'node-{node}.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 for path,digest in json.loads((Q/'source-seal.json').read_text())['sha256'].items():assert sha(path)==digest,path
 save(Q/f'status-node-{node}.json',dict(state='waiting_for_rl300',time=time.time()))
 done=wait(E/'control/completed.json',E/'control');assert done['passed'] and done['all32exit0'] and done['all_gpu_empty']
 for step in STEPS:
  assert empty(),'Never launch over live GPU children'
  J=Q/f'checkpoint-{step:04d}'
  save(Q/f'status-node-{node}.json',dict(state='preparing',checkpoint=step,time=time.time()))
  if node==0:prepare(step)
  assert wait(J/'prepared.json',Q)['passed']
  log=(J/f'controller-node-{node}.log').open('ab',buffering=0)
  child=subprocess.Popen([str(PY),'-u',str(J/'controller.py'),'--node',str(node)],cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  fields=Path(f'/proc/{child.pid}/stat').read_text().split(') ',1)[1].split()
  save(J/'control'/f'controller-launch-node-{node}.json',dict(pid=child.pid,start_ticks=fields[19],node=node,time=time.time(),command=str(J/'controller.py')))
  save(Q/f'status-node-{node}.json',dict(state='evaluating',checkpoint=step,pid=child.pid,time=time.time()))
  code=child.wait();log.close();assert code==0,f'Stage {step} failed with {code}'
  result=wait(J/'control/completed.json',J/'control');assert result['passed'] and result['all32exit0'] and empty()
 if node==0:
  results=[json.loads((Q/f'checkpoint-{s:04d}'/'result.json').read_text()) for s in STEPS]
  assert all(x['passed'] and x['completed']==590 for x in results)
  save(Q/'result.json',dict(passed=True,order=[300,*STEPS],intermediate_results=results,first_result=str(E/'result.json'),full_traces_retained=True,finished_at=time.time()))
 wait(Q/'result.json',Q);save(Q/f'status-node-{node}.json',dict(state='completed',time=time.time()))
if __name__=='__main__':
 try:main()
 except BaseException as error:
  node=next((int(os.sys.argv[i+1]) for i,x in enumerate(os.sys.argv) if x=='--node'),-1)
  save(Q/f'failure-node-{node}.json',dict(error=repr(error),traceback=traceback.format_exc(),time=time.time()));raise
