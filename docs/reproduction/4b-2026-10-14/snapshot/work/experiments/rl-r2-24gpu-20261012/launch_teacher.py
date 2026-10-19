from pathlib import Path
import json, os, subprocess, socket

R=Path.cwd(); B=R/'work/experiments/rl-r2-24gpu-20261012'
assert str(R)=='${PROJECT_ROOT}'
assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
s=socket.socket(); assert s.connect_ex(('127.0.0.1',8005))!=0; s.close()
old=json.loads((R/'work/experiments/deep-sft-20261010/teacher-launch.json').read_text())
env=dict(os.environ,CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',PYTHONDONTWRITEBYTECODE='1')
cache=B/'teacher-cache'
for name,variable in [('tmp','TMPDIR'),('hf','HF_HOME'),('cuda','CUDA_CACHE_PATH'),('triton','TRITON_CACHE_DIR'),('inductor','TORCHINDUCTOR_CACHE_DIR'),('vllm','VLLM_CACHE_ROOT'),('extensions','TORCH_EXTENSIONS_DIR')]:
    p=cache/name; p.mkdir(parents=True,exist_ok=True); env[variable]=str(p)
short=R/'t/r2audit';short.mkdir(parents=True,exist_ok=True)
env.update(TMPDIR=str(short),TMP=str(short),TEMP=str(short),VLLM_RPC_BASE_PATH=str(short),RAY_TMPDIR=str(short/'ray'))
command=old['command'][:]
command[command.index('--max-model-len')+1]='16384'
command[command.index('--max-num-seqs')+1]='128'
with (B/'teacher.log').open('ab') as log:
    child=subprocess.Popen(command,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
(B/'teacher-launch.json').write_text(json.dumps(dict(pid=child.pid,command=command,purpose='gold-blind verification of expanded public RL references'),indent=2))
print(json.dumps(dict(pid=child.pid,state='loading')))
