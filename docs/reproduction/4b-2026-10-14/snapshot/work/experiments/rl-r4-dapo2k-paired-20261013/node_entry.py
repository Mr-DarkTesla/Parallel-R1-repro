from pathlib import Path
import os,json,time,subprocess,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R)
Q=Path(os.environ['PARALLEL_POSTEVAL_ROOT']);C=Q/'control';C.mkdir(exist_ok=True)
cfg=json.loads((Q/'config.json').read_text());PY=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
def save(p,d):
 t=p.with_name(p.name+'.tmp-'+str(os.getpid()));t.write_text(json.dumps(d,indent=2)+'\n');os.replace(t,p)
rank=int(os.environ.get('RANK',os.environ.get('OMPI_COMM_WORLD_RANK','-1')));local=int(os.environ.get('LOCAL_RANK',os.environ.get('OMPI_COMM_WORLD_LOCAL_RANK','-1')));world=int(os.environ.get('WORLD_SIZE',os.environ.get('OMPI_COMM_WORLD_SIZE','0')))
try:
 assert world==16 and 0<=rank<16 and local==rank%8
 with (C/f'entry-claim-{rank}.json').open('x') as f:json.dump(dict(pid=os.getpid(),rank=rank,time=time.time()),f)
 if local==0:
  node=rank//8
  for step in cfg['checkpoints']:
   E=Q/f'checkpoint-{step:04}'
   with (Q/f'node-{node}-checkpoint-{step}.log').open('ab',buffering=0) as log:
    p=subprocess.Popen([str(PY),'-u',str(E/'controller.py'),'--root',str(E),'--node',str(node)],cwd=R,stdout=log,stderr=log,stdin=subprocess.DEVNULL,start_new_session=True)
    raw=Path(f'/proc/{p.pid}/stat').read_text();ss=raw[raw.rfind(')')+2:].split();save(C/f'controller-node-{node}-checkpoint-{step}.json',dict(pid=p.pid,start_ticks=ss[19],node=node,step=step,time=time.time()))
    code=p.wait()
   assert code==0,('Eval controller failed',step,node,code)
  save(C/f'node-complete-{node}.json',dict(passed=True,node=node,time=time.time()))
  if node==0:
   while not (C/'node-complete-1.json').exists():time.sleep(5)
   summaries=[json.loads((Q/f'checkpoint-{s:04}/result.json').read_text()) for s in cfg['checkpoints']];assert all(x['passed'] for x in summaries)
   save(Q/'result.json',dict(passed=True,lane=cfg['lane'],checkpoints=summaries,full_traces_retained=True,time=time.time()));save(C/'completed.json',dict(passed=True,all_checkpoints_completed=True,time=time.time()))
 while not (C/'completed.json').exists():
  if list(C.glob('failure-rank-*')):raise RuntimeError('Posteval peer failed; preserve evidence and healthychildren')
  time.sleep(5)
except BaseException:
 save(C/f'failure-rank-{rank}.json',dict(rank=rank,error=traceback.format_exc(),time=time.time()));raise
