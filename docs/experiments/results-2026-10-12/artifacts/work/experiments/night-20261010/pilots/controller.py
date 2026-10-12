from pathlib import Path
import subprocess,os,json,time,signal,fcntl,sys
R=Path(__file__).resolve().parent;P=R.parents[3]; start=time.time();lock=(R/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert not (R/'status.json').exists(),'duplicate'
uuids={int(l.split(',')[0]):l.split(',')[1].strip() for l in subprocess.check_output(['nvidia-smi','--query-gpu=index,uuid','--format=csv,noheader'],text=True).splitlines()}
occupied=subprocess.check_output(['nvidia-smi','--query-compute-apps=gpu_uuid,pid','--format=csv,noheader'],text=True);assert all(uuids[i] not in occupied for i in range(1,7)),occupied
children=[];handles=[]
def save(state):
 q=R/'status.tmp';q.write_text(json.dumps({'state':state,'elapsed':time.time()-start,'children':children,'pids_owned':True,'max_seconds':300},indent=2));q.replace(R/'status.json')
for rank,gpu in enumerate(range(1,7)):
 mode='native' if rank<3 else 'structured';worker=rank%3;env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=str(gpu),PYTHONPATH=str(R/'code'),OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONUNBUFFERED='1',WANDB_MODE='disabled',XDG_CACHE_HOME=str(R/'cache'),TMPDIR=str(R/'tmp'))
 for d in ['cache','tmp']:(R/d).mkdir(exist_ok=True)
 f=(R/f'{mode}-{worker}.log').open('w');handles.append(f);proc=subprocess.Popen([sys.executable,str(R/'pilot.py'),'--worker',str(worker),'--mode',mode,'--max-tokens','2048'],cwd=P,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True);children.append({'pid':proc.pid,'gpu':gpu,'mode':mode,'worker':worker});children[-1]['proc']=proc
# Proc objects excluded when persisting state.
processes=[x.pop('proc') for x in children];save('running')
while any(p.poll() is None for p in processes) and time.time()-start<300:
 time.sleep(5);save('running')
for p,c in zip(processes,children):
 if p.poll() is None:
  os.killpg(p.pid,signal.SIGTERM);c['timed_out']=True
for p,c in zip(processes,children):
 try:c['returncode']=p.wait(timeout=15)
 except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);c['returncode']=p.wait()
save('complete' if all(c['returncode']==0 for c in children) else 'partial_or_failed')
