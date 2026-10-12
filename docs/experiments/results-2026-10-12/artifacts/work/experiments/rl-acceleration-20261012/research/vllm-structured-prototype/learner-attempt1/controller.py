"""Owned worker1 8GPU learner+TP1 actor buddies, automatic source/CPU gates."""
from pathlib import Path
import os,sys,json,time,subprocess,hashlib,socket,signal,traceback,fcntl
R=Path('${PROJECT_ROOT}');os.chdir(R);T=Path(__file__).resolve().parent;sys.path.insert(0,str(T.parent));import gpu_controller as common
common.A=T;PYTHON=common.PYTHON

def write(name,value):common.write(name,value)
def status(state,**kw):common.status(state,**kw)
def stop_owned(records):
 for record in records:
  observed=common.state(record['pid']);identity=record.get('identity') or dict(start_ticks=record.get('start_ticks'))
  if observed and observed['state']!='Z' and str(observed['start_ticks'])==str(identity['start_ticks']):os.kill(record['pid'],signal.SIGTERM)

def main():
 lock=(T/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);assert '-mpiworker-1' in socket.gethostname();assert common.free()
 cfg=json.loads((T/'config.json').read_text());assert cfg['skip_exports'] and cfg['skip_validation'] and cfg['steps']==52 and not cfg['async_rollout'];assert not Path(cfg['output']).exists(),'Never replace a prior training output'
 seal={str(p.relative_to(T)):common.sha(p) for p in (T/'src').rglob('*.py')};write('SOURCE-SEAL.json',dict(sha256=seal,config_sha256=common.sha(T/'config.json')))
 status('CPU_source_API_loss_gate')
 env=common.environment(0);env.update(CUDA_VISIBLE_DEVICES='',PYTHONPATH=str(T/'src'));env.pop('STRUCTURED_GPU_AUTHORIZED',None)
 with (T/'cpu-gate.log').open('w') as log:
  subprocess.run([str(PYTHON),str(T/'src/proof_integration_cpu.py')],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
  subprocess.run([str(PYTHON),str(T/'src/proof_tis_kernel.py')],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 assert json.loads((T/'CPU-INTEGRATION-PROOF.json').read_text())['passed'];assert json.loads((T/'cpu-kernel-proof.json').read_text())['passed']
 assert all(common.sha(T/k)==v for k,v in seal.items());assert common.free();write('INPUT-SEAL.json',{key:dict(path=cfg[key],sha256=common.sha(cfg[key])) for key in ['train','val','system','scorer','reward','replay']})
 with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
 env=common.environment(0);env.update(CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',WORLD_SIZE='8',LOCAL_WORLD_SIZE='8',MASTER_ADDR='127.0.0.1',MASTER_PORT=str(port),TORCHELASTIC_USE_AGENT_STORE='False',PYTHONPATH=str(T/'src'),OMP_NUM_THREADS='1')
 procs={};records=[];exits={};start=time.time()
 for rank in range(8):
  log=(T/f'learner-rank-{rank}.log').open('ab',buffering=0);p=subprocess.Popen([str(PYTHON),'-u',str(T/'src/train.py'),'--config',str(T/'config.json'),'--smoke'],cwd=R,env=dict(env,RANK=str(rank),LOCAL_RANK=str(rank)),stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);record=dict(rank=rank,pid=p.pid,identity=common.state(p.pid),time=time.time());records.append(record);procs[rank]=(p,log);write(f'learner-rank-{rank}-launch.json',record)
 write('launch.json',dict(pid=os.getpid(),learners=records,world8=True,actor_TP1_buddies_per_GPU=True,port=port,config_sha256=common.sha(T/'config.json')))
 failed=False
 while procs:
  for rank,(p,log) in list(procs.items()):
   code=p.poll()
   if code is None:continue
   log.close();exits[str(rank)]=code;del procs[rank];write('exits.json',exits)
   if code and not failed:
    failed=True;actors=[json.loads(p.read_text()) for p in Path(cfg['output']).glob('actor-rank-*-launch.json')];stop_owned([*records,*actors])
  if time.time()-start>3600 and not failed:failed=True;stop_owned([*records,*[json.loads(p.read_text()) for p in Path(cfg['output']).glob('actor-rank-*-launch.json')]])
  status('failed_draining_owned_group' if failed else 'vLLM_actor_BF16_learner_two_Adam',active={str(r):p.pid for r,(p,_) in procs.items()},exits=exits);time.sleep(3)
 if failed or any(code!=0 for code in exits.values()):raise RuntimeError('Owned integration failed; identities/exits/logs preserved')
 assert common.free();rows=[json.loads(line) for rank in range(8) for line in (Path(cfg['output'])/f'metrics-rank-{rank}.jsonl').read_text().splitlines()]
 assert len(rows)==16 and all(r['optimizer_step'] and r['backbone_update_l2']>0 and r['replay_guard_passed'] for r in rows)
 assert all(r['trainable']==4_022_468_096 and r['master_parameter_dtypes']==['torch.float32'] and r['gradient_storage_dtypes']==['torch.float32'] for r in rows)
 write('proof.json',dict(passed=True,all8exit0_GPUempty=True,two_actual_Adam_updates=True,rows=rows,source_seal_sha256=common.sha(T/'SOURCE-SEAL.json'),config_sha256=common.sha(T/'config.json'),scope='Actual full32 vLLM CUDA-IPC actor +BF16 HF learner/teacher FP32master/gradient/Adam single-fresh-update TIS; no async lag'))
 status('completed',exits=exits)
if __name__=='__main__':
 try:main()
 except BaseException as error:status('failed',error=repr(error),traceback=traceback.format_exc());raise
