"""One MPI process per GPU: real 32-rank smoke, then a weights-only continuation to global step500 run."""
from pathlib import Path
import hashlib,json,os,socket,subprocess,time,traceback

R=Path('${PROJECT_ROOT}');B=R/'work/experiments/rl-r2-32gpu-batch32-20261012'
os.chdir(R)
rank=int(os.environ.get('RANK',os.environ.get('OMPI_COMM_WORLD_RANK','-1')))
world=int(os.environ.get('WORLD_SIZE',os.environ.get('OMPI_COMM_WORLD_SIZE','0')))
local=int(os.environ.get('LOCAL_RANK',os.environ.get('OMPI_COMM_WORLD_LOCAL_RANK','-1')))
early=B/'bootstrap-pytorch';early.mkdir(exist_ok=True)
(early/(socket.gethostname()+'-'+str(os.getpid())+'.json')).write_text(json.dumps(dict(rank=rank,world=world,local=local,hostname=socket.gethostname(),pid=os.getpid(),environment={k:os.environ.get(k) for k in ['RANK','WORLD_SIZE','LOCAL_RANK','OMPI_COMM_WORLD_RANK','OMPI_COMM_WORLD_SIZE','OMPI_COMM_WORLD_LOCAL_RANK']}),indent=2))
assert world==32 and 0<=rank<32 and 0<=local<8,(rank,world,local)
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
    assert runtime['passed'] and runtime['world_size']==32
    for path,digest in runtime['sha256'].items():
        assert sha(path)==digest,path
    save(C/f'node-rank-{rank}.json',dict(rank=rank,local_rank=local,world_size=world,hostname=socket.gethostname(),pid=os.getpid(),time=time.time()))
    if rank==0:
        records=[wait(C/f'node-rank-{r}.json',300) for r in range(32)]
        assert len({r['hostname'] for r in records})==4
        assert all(sum(r['hostname']==h for r in records)==8 for h in {r['hostname'] for r in records})
        s=socket.socket();s.bind(('',0));port=s.getsockname()[1];s.close()
        save(C/'master.json',dict(address=socket.gethostbyname(socket.gethostname()),port=port,nodes=records,world_size=32))
    master=wait(C/'master.json',300)
    cache=B/'cache'/socket.gethostname();cache.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,RANK=str(rank),WORLD_SIZE='32',LOCAL_RANK=str(local),MASTER_ADDR=master['address'],MASTER_PORT=str(master['port']),
             OMP_NUM_THREADS='4',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false',NCCL_DEBUG='WARN')
    # These children use their own rank0 TCPStore, independent of torchrun's agent.
    env['TORCHELASTIC_USE_AGENT_STORE']='False'
    env.pop('PYTHONPATH',None)
    env['PYTHONNOUSERSITE']='1'
    site=R/'.venv/lib/python3.12/site-packages'
    env['LD_LIBRARY_PATH']=':'.join([str(site/'torch/lib'),*[str(p) for p in (site/'nvidia').glob('*/lib')],'/usr/local/nvidia/lib','/usr/local/nvidia/lib64'])
    for variable,name in [('TMPDIR','tmp'),('HF_HOME','hf'),('CUDA_CACHE_PATH','cuda'),('TRITON_CACHE_DIR','triton'),('TORCHINDUCTOR_CACHE_DIR','inductor'),('TORCH_EXTENSIONS_DIR','extensions')]:
        path=cache/name;path.mkdir(exist_ok=True);env[variable]=str(path)
    for stage in ['evaluation','smoke','production']:
        if stage=='production':wait(C/'production-approved.json')
        if stage=='evaluation':
            job=B/'evaluation-job.json'
            evalenv=dict(env,CUDA_VISIBLE_DEVICES=str(local))
            command=[str(B/'portable-venv/bin/python'),str(B/'eval_worker.py'),'--job',str(job),'--rank',str(rank)]
            with (B/f'evaluation-rank-{rank}.log').open('ab',buffering=0) as log:
                child=subprocess.Popen(command,env=evalenv,cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
                save(C/f'evaluation-child-rank-{rank}.json',dict(pid=child.pid,rank=rank,command=command,time=time.time()))
                code=child.wait()
            save(C/f'evaluation-exit-rank-{rank}.json',dict(rank=rank,returncode=code,time=time.time()))
            if code:raise RuntimeError('evaluation worker returned '+str(code))
            for r in range(32):assert wait(C/f'evaluation-exit-rank-{r}.json',86400)['returncode']==0
            gpu=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True)
            assert not gpu.strip(),gpu
            save(C/f'evaluation-empty-rank-{rank}.json',dict(passed=True,rank=rank))
            if rank==0:
                for r in range(32):assert wait(C/f'evaluation-empty-rank-{r}.json')['passed']
                code=subprocess.run([str(B/'portable-venv/bin/python'),str(B/'eval_finalize.py')],env=env,cwd=R).returncode
                if code:raise RuntimeError('evaluation finalize returned '+str(code))
                save(C/'evaluation-completed.json',dict(passed=True,checkpoint=50,completed=500,all32_exit0=True,all_gpu_empty=True,summary=str(B/'evaluation-math500/summary.json')))
            wait(C/'evaluation-completed.json',86400)
            continue
        cfg=B/(stage+'-config-v2.json')
        command=[str(B/'portable-venv/bin/python'),str(B/'runner/train.py'),'--config',str(cfg)]
        command+=['--smoke'] if stage=='smoke' else ['--receipt',str(C/'production-approved.json')]
        with (B/f'{stage}-rank-{rank}.log').open('ab',buffering=0) as log:
            child=subprocess.Popen(command,env=env,cwd=R,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
            save(C/f'{stage}-child-rank-{rank}.json',dict(pid=child.pid,rank=rank,command=command,time=time.time()))
            code=child.wait()
        save(C/f'{stage}-exit-rank-{rank}.json',dict(rank=rank,returncode=code,time=time.time()))
        if code:raise RuntimeError(stage+' trainer returned '+str(code))
        if stage=='smoke':
            for r in range(32):assert wait(C/f'smoke-exit-rank-{r}.json')['returncode']==0
            gpu=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True)
            assert not gpu.strip(),gpu
            save(C/f'smoke-empty-rank-{rank}.json',dict(passed=True,rank=rank,hostname=socket.gethostname(),empty_gpu=True))
            if rank==0:
                for r in range(32):assert wait(C/f'smoke-empty-rank-{r}.json')['passed']
                metrics=[];fixtures=[]
                for r in range(32):
                    rows=list(map(json.loads,(B/'smoke'/f'metrics-rank-{r}.jsonl').read_text().splitlines()))
                    initial=json.loads((B/'production-config-v2.json').read_text())['initial_step']
                    assert [x['step'] for x in rows]==[initial+1,initial+2]
                    assert all(x['optimizer_step'] and x['trainable']>=4_000_000_000 and x['backbone_update_l2']>0 and x['max_replay_logp_drift']<=.01 and x['replay_guard_passed'] and x['group']==1 and x['reward_group']==4 for x in rows)
                    proof=json.loads((B/'smoke'/f'resident-fixtures-rank-{r}.json').read_text())
                    assert proof['passed'] and len(proof['cases'])==20
                    assert all(x['optimizer_resident'] and x['subgroups']==1 for x in proof['cases'])
                    metrics.extend(rows);fixtures.append(proof)
                proof=dict(passed=True,world_size=32,nodes=4,actual_optimizer_updates=2,all_ranks_positive=True,all_workers_exit0=True,all_gpu_empty=True,
                           max_replay_drift=max(x['max_replay_logp_drift'] for x in metrics),max_peak_bytes=max(x['peak_gpu_bytes'] for x in metrics),
                           resident_widths=[2,3,4,6,8],resident_rounds_per_width=4,fixtures=fixtures,
                           smoke_config_sha256=sha(B/'smoke-config-v2.json'),source_manifest_sha256=sha(B/'runtime-build-v2.json'))
                save(B/'distributed-smoke-proof.json',proof)
                production=json.loads((B/'production-config-v2.json').read_text())
                assert production['steps']==500 and production['checkpoint_steps']==list(range(50,501,50))
                assert production['global_batch']==dict(prompts_per_step=8,rollouts_per_prompt=4,responses_per_step=32)
                assert production['expected_world_size']==32
                assert production['reward_mode']=='strong_width' and production['max_batched_paths']==8
                receipt=dict(approved=True,config_sha256=sha(B/'production-config-v2.json'),sha256={k:sha(p) for k,p in production['sealed_inputs'].items()},
                             distributed_smoke=dict(path=str(B/'distributed-smoke-proof.json'),sha256=sha(B/'distributed-smoke-proof.json')),
                             authorization='User authorized careful migration32GPU, batch8prompts x4responses, preserve weights and continue global500',time=time.time())
                save(C/'production-approved.json',receipt)
        elif rank==0:
            for r in range(32):assert wait(C/f'production-exit-rank-{r}.json',86400)['returncode']==0
            save(C/'completed.json',dict(completed=True,steps=500,world_size=32,time=time.time()))
except BaseException as error:
    save(C/f'failure-rank-{rank}.json',dict(rank=rank,error=repr(error),traceback=traceback.format_exc(),time=time.time()))
    raise
