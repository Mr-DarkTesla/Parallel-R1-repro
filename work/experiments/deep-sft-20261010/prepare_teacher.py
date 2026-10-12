"""Use published teacher checkpoint/runtime read-only; isolate all writes."""
from pathlib import Path
import hashlib, json, os, subprocess

P=Path.cwd();B=P/'work/experiments/deep-sft-20261010'
assert str(P)=='/home/jovyan/shares/SR004.nfs3/larin/tmp/r1'
S=Path('/home/jovyan/shares/SR004.nfs3/edge-llms-shared')
release=(S/'serving/current').resolve()
profile=release/'profiles/reference/deepseek-v4.1-flash/profile.json'
config=json.loads(profile.read_text());assert config['required_gpu_count']==8
runtime=B/'teacher-runtime';runtime.mkdir(exist_ok=True)
for name in ['tmp','hf','cuda','triton','inductor','vllm','extensions','ray']:(B/'teacher-cache'/name).mkdir(parents=True,exist_ok=True)
short_tmp=P/'t/dsdeep';short_tmp.mkdir(parents=True,exist_ok=True)
archive=S/'venvs/serving/deepseek-v41-00d577a6a63281e15336029d5bcee4e9a2cf182214a4f20ba6111b1c8e79893d/rootfs.tar'
patch=release/'runtime/deepseek-v41/patch.tar'
site=runtime/'usr/local/lib/python3.12/dist-packages'
if not (runtime/'.ready').exists():
    print('Extracting published runtime into isolated project arm',flush=True)
    subprocess.run(['tar','--no-same-owner','-xf',str(archive),'-C',str(runtime)],check=True)
    subprocess.run(['tar','--no-same-owner','-xf',str(patch),'-C',str(site)],check=True)
    (runtime/'.ready').write_text('runtime archive + serving release patch extracted\n')
wrapper=f'''#!/usr/bin/env bash
set -euo pipefail
RUNTIME={runtime}
SITE=$RUNTIME/usr/local/lib/python3.12/dist-packages
export PYTHONPATH={release}/runtime/deepseek-v41/helpers:$SITE
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
export CUDA_HOME=$RUNTIME/usr/local/cuda-13.0
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$SITE/torch/lib:$CUDA_HOME/targets/x86_64-linux/lib:/usr/local/nvidia/lib:/usr/local/nvidia/lib64
for lib in "$SITE"/nvidia/*/lib; do
 [[ ! -d "$lib" ]] || export LD_LIBRARY_PATH="$lib:$LD_LIBRARY_PATH"
done
export TORCH_CUDA_ARCH_LIST=8.0
exec {S}/venvs/python/cpython-3.12.13-linux-x86_64-gnu/bin/python3.12 "$@"
'''
f=B/'teacher-python';f.write_text(wrapper);f.chmod(0o755)
command=[str(f),'-m','vllm.entrypoints.openai.api_server','--model',config['model'],'--served-model-name',config['served_model_name'],
         '--host','127.0.0.1','--port','8005','--tensor-parallel-size','4',*config['vllm_args']]
env=dict(os.environ,CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',VLLM_LOGGING_LEVEL='INFO',
    PYTHONDONTWRITEBYTECODE='1',PYTHONPYCACHEPREFIX=str(B/'teacher-cache/tmp/pycache'),
    TMPDIR=str(short_tmp),TMP=str(short_tmp),TEMP=str(short_tmp),VLLM_RPC_BASE_PATH=str(short_tmp),
    HF_HOME=str(B/'teacher-cache/hf'),CUDA_CACHE_PATH=str(B/'teacher-cache/cuda'),
    TRITON_CACHE_DIR=str(B/'teacher-cache/triton'),TORCHINDUCTOR_CACHE_DIR=str(B/'teacher-cache/inductor'),
    VLLM_CACHE_ROOT=str(B/'teacher-cache/vllm'),TORCH_EXTENSIONS_DIR=str(B/'teacher-cache/extensions'),RAY_TMPDIR=str(short_tmp/'ray'))
gpu=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid,used_gpu_memory','--format=csv,noheader'],text=True)
assert not gpu.strip(), 'GPU compute processes appeared before teacher launch'
import socket
test=socket.socket();assert test.connect_ex(('127.0.0.1',8005))!=0;test.close()
with (B/'teacher.log').open('ab') as log:
    child=subprocess.Popen(command,env=env,cwd=P,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
manifest=dict(pid=child.pid,state='loading',command=command,release=str(release),profile_sha256=sha(profile),
    runtime_archive_bytes=archive.stat().st_size,patch_sha256=sha(patch),launcher_sha256=sha(f),
    checkpoint=config['model'],gpu_count=8,write_root=str(P),artifact_root=str(B),short_ipc_root=str(short_tmp),note='Published checkpoint/launcher helpers read-only; isolated runtime/cache/logs inside r1.')
(B/'teacher-launch.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2),flush=True)
