from pathlib import Path
import json,os,subprocess,sys,time
R=Path('${PROJECT_ROOT}');os.chdir(R);Q=R/'work/experiments/eval-intermediates-vllm-rolling-32k-20261013'
node=int(sys.argv[1]);receipt=Q/f'controller-launch-node-{node}.json';assert not receipt.exists(),'Reconcile existing queue controller'
PY=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python';log=(Q/f'node-{node}.log').open('ab',buffering=0)
child=subprocess.Popen([str(PY),'-u',str(Q/'node_queue.py'),'--node',str(node)],cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
fields=Path(f'/proc/{child.pid}/stat').read_text().split(') ',1)[1].split();d=dict(pid=child.pid,start_ticks=fields[19],node=node,time=time.time());receipt.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
