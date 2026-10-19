from pathlib import Path
import os,json,time,subprocess,traceback
R=Path('${PROJECT_ROOT}');os.chdir(R)
E=Path(os.environ['PARALLEL_RANDOM2_EVAL_ROOT']);C=E/'control'
PY=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
rank=int(os.environ.get('RANK',os.environ.get('OMPI_COMM_WORLD_RANK','-1')))
world=int(os.environ.get('WORLD_SIZE',os.environ.get('OMPI_COMM_WORLD_SIZE','0')))
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
try:
 assert world==8 and 0<=rank<8
 with (C/f'entry-claim-{rank}.json').open('x') as f:json.dump(dict(pid=os.getpid(),rank=rank,time=time.time()),f)
 if rank==0:
  subprocess.run([str(PY),'-u',str(E/'controller.py'),'--root',str(E),'--node','0'],cwd=R,check=True)
 while not (C/'completed.json').exists():
  if list(C.glob('failure-node-*')):raise RuntimeError('Evaluation controller failed; preserve all traces')
  time.sleep(3)
except BaseException:
 save(C/f'failure-entry-{rank}.json',dict(rank=rank,error=traceback.format_exc(),time=time.time()));raise
