import hashlib,json,os,subprocess,sys,time,traceback
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('${PROJECT_ROOT}'); RUN=Path(__file__).resolve().parent
CODE=ROOT/'exps/rl-unseen-s2-bs32-500-20261007/code'
MODEL=ROOT/'exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final'
def status(state,**kw):
    data=dict(state=state,observed_utc=datetime.now(timezone.utc).isoformat(),controller_pid=os.getpid(),**kw)
    temp=RUN/'status.tmp';temp.write_text(json.dumps(data,indent=2)+'\n');temp.replace(RUN/'status.json');print(json.dumps(data),flush=True)
env=os.environ.copy()
env.update(PATH=str(ROOT/'.venv/bin')+':'+env['PATH'],CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',NPROC_PER_NODE='8',
    PARALLEL_R1_OUTPUT_ROOT=str(RUN/'results'),PARALLEL_R1_SCRATCH_ROOT=str(ROOT/'cache'),HF_HOME=str(ROOT/'cache/huggingface'),
    TMPDIR=str(ROOT/'t'),RAY_TMPDIR=str(ROOT),XDG_CACHE_HOME=str(ROOT/'cache'),VLLM_CACHE_ROOT=str(ROOT/'cache/vllm-aligned'),
    TRITON_CACHE_DIR=str(ROOT/'cache/triton'),TORCHINDUCTOR_CACHE_DIR=str(ROOT/'cache/inductor-aligned'),
    TORCH_EXTENSIONS_DIR=str(ROOT/'cache/torch-extensions'),CUDA_CACHE_PATH=str(ROOT/'cache/cuda'),CUDA_HOME='${CUDA_HOME}',
    PYTHONPATH=str(ROOT/'exps/rl-s1-seen-20261006-1112/flashinfer-deps'),WANDB_MODE='offline',PYTHONUNBUFFERED='1',TOKENIZERS_PARALLELISM='false')
env.pop('RAY_ADDRESS',None)
queue=['gsm_infinite','dapo']; completed=[]
try:
    audit=json.loads((RUN/'data-audit.json').read_text())
    for name in queue:
        assert hashlib.sha256((RUN/f'{name}.parquet').read_bytes()).hexdigest()==audit[name]['sha256']
        out=RUN/'results/eval'/name;out.mkdir(parents=True,exist_ok=True)
        env.update(PARALLEL_R1_EVAL_NAME=name,PARALLEL_R1_TRACE_DIR=str(out/'traces'))
        cmd=['bash',str(CODE/'verl/training_scripts/eval_qwen3_06b.sh'),str(MODEL),
             f'data.val_files={RUN}/{name}.parquet','data.val_batch_size=32',
             'actor_rollout_ref.rollout.val_kwargs.n=8','actor_rollout_ref.rollout.agent.num_workers=32',
             'actor_rollout_ref.rollout.agent.num_paths=2','actor_rollout_ref.rollout.agent.max_path_response_length=3000',
             'actor_rollout_ref.rollout.max_num_seqs=64',f'custom_reward_function.path={RUN}/score.py',
             'ray_init.num_cpus=64',f'+ray_init.temp_dir={ROOT}',f'+ray_init.plasma_directory={ROOT}/plasma',
             '+ray_init.object_store_memory=8589934592']
        (out/'command.json').write_text(json.dumps(cmd,indent=2)+'\n')
        with (out/'resolved-config.yaml').open('w') as log:
            subprocess.run(cmd+['--cfg','job','--resolve'],env=env,cwd=CODE,stdout=log,stderr=subprocess.STDOUT,check=True)
        if '--preflight' in sys.argv:continue
        for attempt in range(12):
            pids=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
            if not pids:break
            status('waiting_for_free_gpus',dataset=name,completed=completed);time.sleep(5)
        assert not pids,'GPU processes exist; refusing to interfere'
        started=time.time()
        with (out/'driver.log').open('w') as log:
            proc=subprocess.Popen(cmd,env=env,cwd=CODE,stdout=log,stderr=subprocess.STDOUT)
            status('running',dataset=name,pid=proc.pid,gpus=list(range(8)),questions=256,answers=2048,completed=completed,queued=queue[queue.index(name)+1:],blocked=audit['blocked'])
            rc=proc.wait()
        (out/'exit_code').write_text(str(rc)+'\n')
        assert rc==0,(name,rc)
        files=list(out.glob('[0-9]*.jsonl'));assert len(files)==1,files
        with (out/'scoring.log').open('w') as log:
            subprocess.run([sys.executable,str(RUN/'summarize.py'),str(files[0])],cwd=RUN,stdout=log,stderr=subprocess.STDOUT,check=True)
        report=json.loads((out/'summary.json').read_text());report['total_wall_seconds']=time.time()-started
        (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');completed.append(name)
    status('preflight_passed' if '--preflight' in sys.argv else 'available_sets_complete_bigmath_blocked',completed=completed,blocked=audit['blocked'])
except Exception as error:
    status('failed',completed=completed,error=repr(error));traceback.print_exc();raise
