from pathlib import Path
import json,os,subprocess,sys,time
R=Path('${PROJECT_ROOT}');os.chdir(R);E=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013';C=E/'control';C.mkdir(parents=True,exist_ok=True)
node=int(sys.argv[1]);assert 0<=node<4
receipt=C/f'controller-launch-node-{node}.json';assert not receipt.exists(),'Reconcile existing controller; do not duplicate'
py=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python';log=(E/f'controller-node-{node}.log').open('ab',buffering=0)
child=subprocess.Popen([str(py),'-u',str(E/'controller.py'),'--node',str(node)],cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
raw=Path(f'/proc/{child.pid}/stat').read_text();fields=raw[raw.rfind(')')+2:].split();d=dict(pid=child.pid,start_ticks=fields[19],node=node,time=time.time(),command=str(E/'controller.py'))
receipt.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
