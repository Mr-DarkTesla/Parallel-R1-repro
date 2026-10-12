"""One MPI process per GPU: configurable distributed smoke, then a weights-only continuation to global step500 run."""
from pathlib import Path
import hashlib,json,os,socket,subprocess,time,traceback,sys

HERE=Path(__file__).resolve().parent
R=next(p for p in HERE.parents if (p/'verl').is_dir() and (p/'README.md').is_file())
B=Path(os.environ['PARALLEL_R1_RUN_ROOT']).resolve()
if not B.is_relative_to(R): raise ValueError('Run output must be inside project root')
os.chdir(R)
production_config=json.loads((B/'production-config-v2.json').read_text())
expected_world=production_config['expected_world_size']
processes_per_node=production_config.get('processes_per_node',8)
assert expected_world % processes_per_node == 0
expected_nodes=expected_world//processes_per_node
rank=int(os.environ.get('RANK',os.environ.get('OMPI_COMM_WORLD_RANK','-1')))
world=int(os.environ.get('WORLD_SIZE',os.environ.get('OMPI_COMM_WORLD_SIZE','0')))
local=int(os.environ.get('LOCAL_RANK',os.environ.get('OMPI_COMM_WORLD_LOCAL_RANK','-1')))
early=B/'bootstrap-pytorch';early.mkdir(exist_ok=True)
(early/(socket.gethostname()+'-'+str(os.getpid())+'.json')).write_text(json.dumps(dict(rank=rank,world=world,local=local,hostname=socket.gethostname(),pid=os.getpid(),environment={k:os.environ.get(k) for k in ['RANK','WORLD_SIZE','LOCAL_RANK','OMPI_COMM_WORLD_RANK','OMPI_COMM_WORLD_SIZE','OMPI_COMM_WORLD_LOCAL_RANK']}),indent=2))
assert world==expected_world and 0<=rank<world and 0<=local<processes_per_node,(rank,world,local)
C=B/'control';C.mkdir(exist_ok=True)
def save(p,x):
    t=p.with_name(p.name+'.tmp-'+str(os.getpid()));t.write_text(json.dumps(x,indent=2));os.replace(t,p)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wait(p,seconds=3600):
    started=time.monotonic()
    while not p.exists():
        failed=list(C.glob('failure-rank-*.json'))
        if failed:raise RuntimeError('Another rank failed: '+failed[0].read_text())
        if time.monotonic()-started>seconds:raise TimeoutError(str(p))
        time.sleep(2)
    return json.loads(p.read_text())
try:
    runtime=json.loads((B/'runtime-build-v2.json').read_text())
    assert runtime['passed'] and runtime['world_size']==world
    for path,digest in runtime['sha256'].items():
        assert sha(path)==digest,path
    save(C/f'node-rank-{rank}.json',dict(rank=rank,local_rank=local,world_size=world,hostname=socket.gethostname(),pid=os.getpid(),time=time.time()))
    if rank==0:
        records=[wait(C/f'node-rank-{r}.json',300) for r in range(world)]
        assert len({r['hostname'] for r in records})==expected_nodes
        assert all(sum(r['hostname']==h for r in records)==processes_per_node for h in {r['hostname'] for r in records})
        s=socket.socket();s.bind(('',0));port=s.getsockname()[1];s.close()
        save(C/'master.json',dict(address=socket.gethostbyname(socket.gethostname()),port=port,nodes=records,world_size=world))
    master=wait(C/'master.json',300)
    cache=B/'cache'/socket.gethostname();cache.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,RANK=str(rank),WORLD_SIZE=str(world),LOCAL_RANK=str(local),MASTER_ADDR=master['address'],MASTER_PORT=str(master['port']),
             OMP_NUM_THREADS='4',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false',NCCL_DEBUG='WARN')
    # These children use their own rank0 TCPStore, independent of torchrun's agent.
    env['TORCHELASTIC_USE_AGENT_STORE']='False'
    env.pop('PYTHONPATH',None)
    env['PYTHONNOUSERSITE']='1'
    python_exec=production_config.get('python_executable',sys.executable)
    site=Path(subprocess.check_output([python_exec,'-c','import site;print(site.getsitepackages()[0])'],text=True).strip())
    env['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'/usr/local/nvidia/lib','/usr/local/nvidia/lib64'])
    for variable,name in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda'),('TRITON_CACHE_DIR','triton'),('TORCHINDUCTOR_CACHE_DIR','inductor'),('TORCH_EXTENSIONS_DIR','extensions')]:
        path=cache/name;path.mkdir(exist_ok=True);env[variable]=str(path)
    for stage in ['smoke','production']:
        if stage=='production':wait(C/'production-approved.json')
        cfg=B/(stage+'-config-v2.json')
        command=[python_exec,str(HERE/'train.py'),'--config',str(cfg)]
        command+=['--smoke'] if stage=='smoke' else ['--receipt',str(C/'production-approved.json')]
        with (B/f'{stage}-rank-{rank}.log').open('ab',buffering=0) as log:
            child=subprocess.Popen(command,env=env,cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
            save(C/f'{stage}-child-rank-{rank}.json',dict(pid=child.pid,rank=rank,command=command,time=time.time()))
            code=child.wait()
        save(C/f'{stage}-exit-rank-{rank}.json',dict(rank=rank,returncode=code,time=time.time()))
        if code:raise RuntimeError(stage+' trainer returned '+str(code))
        if stage=='smoke':
            for r in range(world):assert wait(C/f'smoke-exit-rank-{r}.json')['returncode']==0
            gpu=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True)
            assert not gpu.strip(),gpu
            save(C/f'smoke-empty-rank-{rank}.json',dict(passed=True,rank=rank,hostname=socket.gethostname(),empty_gpu=True))
            if rank==0:
                for r in range(world):assert wait(C/f'smoke-empty-rank-{r}.json')['passed']
                metrics=[];fixtures=[]
                for r in range(world):
                    rows=list(map(json.loads,(B/'smoke'/f'metrics-rank-{r}.jsonl').read_text().splitlines()))
                    initial=production_config.get('initial_step',0)
                    assert [x['step'] for x in rows]==[initial+1,initial+2]
                    assert all(x['optimizer_step'] and x['trainable']>=4_000_000_000 and x['backbone_update_l2']>0 and x['max_replay_logp_drift']<=.01 and x['replay_guard_passed'] and x['reward_group']==production_config['global_batch']['rollouts_per_prompt'] for x in rows)
                    proof=json.loads((B/'smoke'/f'resident-fixtures-rank-{r}.json').read_text())
                    assert proof['passed'] and len(proof['cases'])==20
                    assert all(x['optimizer_resident'] and x['subgroups']==1 for x in proof['cases'])
                    metrics.extend(rows);fixtures.append(proof)
                proof=dict(passed=True,world_size=world,nodes=expected_nodes,actual_optimizer_updates=2,all_ranks_positive=True,all_workers_exit0=True,all_gpu_empty=True,
                           max_replay_drift=max(x['max_replay_logp_drift'] for x in metrics),max_peak_bytes=max(x['peak_gpu_bytes'] for x in metrics),
                           resident_widths=[2,3,4,6,8],resident_rounds_per_width=4,fixtures=fixtures,
                           smoke_config_sha256=sha(B/'smoke-config-v2.json'),source_manifest_sha256=sha(B/'runtime-build-v2.json'))
                save(B/'distributed-smoke-proof.json',proof)
                production=json.loads((B/'production-config-v2.json').read_text())
                assert production['steps']>production.get('initial_step',0)
                assert all(0<s<=production['steps'] for s in production['checkpoint_steps'])
                assert production['expected_world_size']==world
                assert production['reward_mode'] in ('strong_width','forward_only') and production['max_batched_paths']==8
                receipt=dict(approved=True,config_sha256=sha(B/'production-config-v2.json'),sha256={k:sha(p) for k,p in production['sealed_inputs'].items()},
                             distributed_smoke=dict(path=str(B/'distributed-smoke-proof.json'),sha256=sha(B/'distributed-smoke-proof.json')),
                             authorization='Actual distributed smoke passed for the configured GPU count and fixed response batch',time=time.time())
                save(C/'production-approved.json',receipt)
        elif rank==0:
            for r in range(world):assert wait(C/f'production-exit-rank-{r}.json',86400)['returncode']==0
            save(C/'completed.json',dict(completed=True,steps=production_config['steps'],world_size=world,time=time.time()))
except BaseException as error:
    save(C/f'failure-rank-{rank}.json',dict(rank=rank,error=repr(error),traceback=traceback.format_exc(),time=time.time()))
    raise
