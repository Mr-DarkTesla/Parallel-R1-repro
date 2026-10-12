from pathlib import Path
import os,json,hashlib,subprocess,socket,time
R=Path('${PROJECT_ROOT}');os.chdir(R)
B=R/'work/experiments/rl-acceleration-20261012/lanes/kv_replay/attempt6'
M=R/'work/experiments/rl-r2-32gpu-batch32-20261012'
proof=json.loads((B.parent/'attempt2/proof-zero-cpu.json').read_text())
assert proof['passed'] and proof['actual_gloo_ranks']==8
apps=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid,used_gpu_memory','--format=csv,noheader'],text=True)
assert not apps.strip(), apps
cohort_proof=json.loads((B.parent/'attempt5/proof-bf16-cohort-cpu.json').read_text())
assert cohort_proof['passed'] and cohort_proof['precision_namespaced_cache'] and cohort_proof['q_schedule_guard']['max']<=.01
abort_proof=json.loads((B.parent/'proof-cohort-abort.json').read_text());assert abort_proof['passed']
cfg=json.loads((M/'smoke-config-v2.json').read_text())
cfg.update(expected_world_size=8,world_size=8,processes_per_node=8,output=str(B/'smoke'),steps=52,skip_exports=True,skip_validation=True,resident_fixture_step=51,zero_advantage_replay=True,kv_preflight=True,cohort_rows=32,resident_cohort_rows=32,precision_mode='fp32',replay=str(B/'src/structured_replay.py'),batch_decoder=str(B/'src/microbatch_decoder.py'))
reward_hash=hashlib.sha256(Path(cfg['reward']).read_bytes()).hexdigest()
assert reward_hash=='b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce', reward_hash
cfg.update(ppo_epochs=1,updates_per_fresh_batch=1,async_rollout=False,actor_dtype='fp32',rollout_correction=dict(mode='token_tis',upper=2.,lower=0.,batch_normalize=False,bypass=False))
cfg['failed_fixture_reference']=str(B.parent/'attempt5/smoke')
cfg['sealed_inputs']={str(p.relative_to(R)):str(p) for p in (B/'src').rglob('*.py')}
cfgfile=B/'smoke-config.json';cfgfile.write_text(json.dumps(cfg,indent=2)+'\n')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest={str(p.relative_to(R)):sha(p) for p in [cfgfile,*list((B/'src').rglob('*.py'))]}
(B/'source-hashes.json').write_text(json.dumps(manifest,indent=2))
s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
py=str(M/'portable-venv/bin/python')
site=Path(subprocess.check_output([py,'-c','import site;print(site.getsitepackages()[0])'],text=True).strip())
cache=B/'cache';cache.mkdir(exist_ok=True)
base=dict(os.environ,MASTER_ADDR='127.0.0.1',MASTER_PORT=str(port),WORLD_SIZE='8',TORCHELASTIC_USE_AGENT_STORE='False',OMP_NUM_THREADS='4',PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false',NCCL_DEBUG='WARN',PYTORCH_CUDA_ALLOC_CONF='expandable_segments:True')
base.pop('PYTHONPATH',None)
base['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'${NVIDIA_ROOT}/lib','${NVIDIA_ROOT}/lib64'])
for variable,name in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda'),('TRITON_CACHE_DIR','triton'),('TORCHINDUCTOR_CACHE_DIR','inductor'),('TORCH_EXTENSIONS_DIR','extensions')]:
    q=cache/name;q.mkdir(exist_ok=True);base[variable]=str(q)
children=[]
for rank in range(8):
    env=dict(base,RANK=str(rank),LOCAL_RANK=str(rank))
    log=(B/f'rank-{rank}.log').open('ab',buffering=0)
    command=[py,str(B/'src/train.py'),'--config',str(cfgfile),'--smoke']
    child=subprocess.Popen(command,env=env,cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
    children.append(child)
    (B/f'child-rank-{rank}.json').write_text(json.dumps(dict(pid=child.pid,rank=rank,command=command,time=time.time())))
(B/'launch-status.json').write_text(json.dumps(dict(state='running',hostname=socket.gethostname(),assigned_node='mpiworker-0',launcher_pid=os.getpid(),child_pids=[c.pid for c in children],world=8,time=time.time(),source_hashes=manifest)))
exits=[None]*8;pending=set(range(8));failed=False
while pending:
    for rank in list(pending):
        code=children[rank].poll()
        if code is None:continue
        exits[rank]=code;pending.remove(rank)
        (B/f'exit-rank-{rank}.json').write_text(json.dumps(dict(rank=rank,returncode=code,time=time.time())))
        if code and not failed:
            failed=True
            (B/'failure-trigger.json').write_text(json.dumps(dict(rank=rank,pid=children[rank].pid,returncode=code,time=time.time(),reason='Owned distributed proof cannot finish after one child failure')))
            for other in pending:
                children[other].terminate()
    time.sleep(1)
(B/'launch-status.json').write_text(json.dumps(dict(state='completed' if not any(exits) else 'failed',launcher_pid=os.getpid(),exits=exits,time=time.time(),source_hashes=manifest)))
