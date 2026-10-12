from pathlib import Path
import json,os,subprocess,time,hashlib,traceback,socket
R=Path('${PROJECT_ROOT}');os.chdir(R);B=Path(__file__).resolve().parent
python=R/'work/experiments/rl-r2-32gpu-batch32-20261012/portable-venv/bin/python'
def status(state,**kw):
    p=B/'status.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(dict(state=state,time=time.time(),pid=os.getpid(),host=socket.gethostname(),**kw),indent=2)+'\n');os.replace(tmp,p)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for c in iter(lambda:f.read(8<<20),b''):h.update(c)
    return h.hexdigest()
def environment(rank):
    env=dict(os.environ,CUDA_VISIBLE_DEVICES=str(rank),OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false',PYTHONNOUSERSITE='1',VLLM_USE_V1='0',VLLM_WORKER_MULTIPROC_METHOD='spawn')
    for k in ['RANK','WORLD_SIZE','LOCAL_RANK','LOCAL_WORLD_SIZE','GROUP_RANK','MASTER_ADDR','MASTER_PORT','TORCHELASTIC_RUN_ID','TORCHELASTIC_USE_AGENT_STORE']:env.pop(k,None)
    env['PYTHONPATH']=str(B)
    site=R/'.venv/lib/python3.12/site-packages';env['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'${NVIDIA_ROOT}/lib','${NVIDIA_ROOT}/lib64'])
    cache=B/'cache'/str(rank);cache.mkdir(parents=True,exist_ok=True)
    for var,leaf in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda'),('TRITON_CACHE_DIR','triton'),('VLLM_CACHE_ROOT','vllm')]:
        p=cache/leaf;p.mkdir(exist_ok=True);env[var]=str(p)
    return env
def child(rank,stage):
    log=(B/f'{stage}-rank-{rank}.log').open('ab',buffering=0)
    p=subprocess.Popen([str(python),str(B/(stage+'_worker.py')),'--job',str(B/(stage+'-job.json')),'--rank',str(rank)],env=environment(rank),cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    (B/f'{stage}-rank-{rank}-launch.json').write_text(json.dumps(dict(pid=p.pid,rank=rank,stage=stage,time=time.time()))+'\n');return p,log
try:
    assert not (B/'result.json').exists()
    manifest=json.loads((B/'manifest.json').read_text());assert manifest['passed']
    for p,h in manifest['sha256'].items():assert sha(p)==h,p
    assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
    procs={rank:('rl',*child(rank,'rl')) for rank in range(8)};exits={str(rank):{} for rank in range(8)}
    status('rl32k',question_batch_size=2,native_batch_size=8)
    native_verified=False
    while procs:
        for rank,(stage,p,log) in list(procs.items()):
            code=p.poll()
            if code is None:continue
            log.close();exits[str(rank)][stage]=code;(B/'exits.json').write_text(json.dumps(exits,indent=2)+'\n')
            if code!=0:raise RuntimeError(f'{stage} rank{rank} failed rc{code}; preserve healthy children')
            del procs[rank]
            if stage=='rl':
                if not native_verified:
                    cfg=json.loads((B/'native-job.json').read_text())
                    for name,h in cfg['native_source_proof']['files'].items():assert sha(Path(cfg['model'])/name)==h,name
                    (B/'native-original-hashes-proof.json').write_text(json.dumps(dict(passed=True,revision=cfg['native_source_proof']['revision'],time=time.time())))
                    native_verified=True
                procs[rank]=('native',*child(rank,'native'))
            status('rl32k_and_native' if any(s=='rl' for s,_,_ in procs.values()) else 'native32k',stages={str(r):s for r,(s,_,_) in procs.items()},exits=exits)
        time.sleep(2)
    subprocess.run([str(python),str(B/'finalize.py')],cwd=R,check=True)
    status('completed')
except BaseException as e:status('failed',error=repr(e),traceback=traceback.format_exc());raise
