"""Finite, self-contained two-stage queue. Only tracks/cleans owned processes."""
import fcntl,hashlib,json,os,signal,subprocess,sys,time,traceback
from pathlib import Path
from datetime import datetime,timezone
import psutil
RUN=Path(__file__).resolve().parent;ROOT=RUN.parent.parent;CODE=RUN/'code'
M=json.loads((RUN/'manifest.json').read_text())
SMOKE='--smoke' in sys.argv;PREFLIGHT='--preflight' in sys.argv
STATUS=RUN/('smoke-status.json' if SMOKE else 'status.json')
def atomic(path,data):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,indent=2)+'\n');temp.replace(path)
def status(state,**extra):
    data=dict(state=state,observed_utc=datetime.now(timezone.utc).isoformat(),controller_pid=os.getpid(),**extra)
    atomic(STATUS,data);print(json.dumps(data),flush=True)
def integrity():
    for base,items in [(CODE,M['code_sha256']),(RUN,M['data_sha256']),(RUN,M['script_sha256'])]:
        for name,digest in items.items():assert hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,name
def environment(stage):
    env=os.environ.copy();env.pop('RAY_ADDRESS',None)
    env.update(PATH=str(ROOT/'.venv/bin')+':'+env['PATH'],CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',NPROC_PER_NODE='8',
        PARALLEL_R1_RL_NAME=f'{RUN.name}-{stage.name}',PARALLEL_R1_RL_DIR=str(stage/'results'),PARALLEL_R1_SCRATCH_ROOT=str(ROOT/'cache'),
        HF_HOME=str(ROOT/'cache/huggingface'),TMPDIR=str(ROOT/'t'),RAY_TMPDIR=str(ROOT),XDG_CACHE_HOME=str(ROOT/'cache'),
        VLLM_CACHE_ROOT=str(ROOT/'cache/vllm-aligned'),TRITON_CACHE_DIR=str(ROOT/'cache/triton'),TORCHINDUCTOR_CACHE_DIR=str(ROOT/'cache/inductor-aligned'),
        TORCH_EXTENSIONS_DIR=str(ROOT/'cache/torch-extensions'),CUDA_CACHE_PATH=str(ROOT/'cache/cuda'),
        WANDB_MODE='offline',PYTHONUNBUFFERED='1',TOKENIZERS_PARALLELISM='false')
    env.update(M['extra_env']);return env
def command(mode,stage,checkpoint=None):
    overrides=list(M['overrides'])+[f'+custom_reward_function.reward_kwargs.mode={mode}']
    if SMOKE:
        overrides += ['trainer.total_training_steps=2','trainer.save_freq=2','trainer.test_freq=2',f'data.val_files={RUN}/smoke-validation.parquet']
    if checkpoint:
        overrides += ['trainer.resume_mode=resume_path',f'trainer.resume_from_path={checkpoint}']
        if int(checkpoint.name.split('_')[-1])==(2 if SMOKE else 800):
            overrides += ['trainer.val_before_train=true']
    return ['bash',str(CODE/'scripts/qwen3.sh'),'rl','s2',M['checkpoint'],*overrides]
def latest_complete(stage):
    root=stage/'results/checkpoints';tracker=root/'latest_checkpointed_iteration.txt'
    committed=int(tracker.read_text()) if tracker.exists() else 0
    for p in sorted(root.glob('global_step_*'),key=lambda p:int(p.name.split('_')[-1]),reverse=True):
        if int(p.name.split('_')[-1])>committed:continue
        files=[p/'data.pt']+[p/f'actor/{kind}_world_size_8_rank_{i}.pt' for kind in ['model','optim','extra_state'] for i in range(8)]
        if all(f.exists() and f.stat().st_size>0 for f in files):return p
    return None
def cleanup(owned):
    live=[]
    for pid,created in owned.items():
        try:
            p=psutil.Process(int(pid))
            if p.create_time()==created and p.status()!=psutil.STATUS_ZOMBIE:live.append(p);p.terminate()
        except (psutil.NoSuchProcess,psutil.AccessDenied):pass
    _,alive=psutil.wait_procs(live,timeout=20)
    for p in alive:
        try:p.kill()
        except psutil.NoSuchProcess:pass
    psutil.wait_procs(alive,timeout=10)
def free_gpus():
    for _ in range(12):
        if not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip():return
        time.sleep(5)
    raise RuntimeError('GPU processes still present; refusing to touch unowned processes')
def attempt(mode,stage,number,checkpoint):
    free_gpus();env=environment(stage);cmd=command(mode,stage,checkpoint)
    atomic(stage/f'command-attempt-{number}.json',cmd)
    logpath=stage/f'driver-attempt-{number}.log';owned={};started=time.time();last_progress=started;last_step=-1
    with logpath.open('w') as log:
        p=subprocess.Popen(cmd,cwd=CODE,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        root_process=psutil.Process(p.pid)
        try:
            while True:
                try:
                    for child in [root_process,*root_process.children(recursive=True)]:owned[child.pid]=child.create_time()
                except psutil.NoSuchProcess:pass
                atomic(stage/'owned-processes.json',owned)
                paths=list((stage/'results/rollouts').glob('[0-9]*.jsonl'))
                step=max([int(x.stem) for x in paths],default=0)
                if step!=last_step:last_step=step;last_progress=time.time()
                status('running',stage=mode,attempt=number,pid=p.pid,step=step,target_steps=2 if SMOKE else 800,
                       initialized_from=M['checkpoint'],resumed_from=str(checkpoint) if checkpoint else None,
                       gpus=list(range(8)),queued=[] if SMOKE or mode=='depth' else ['depth'])
                rc=p.poll()
                if rc is not None:return rc
                if time.time()-last_progress>M['stall_timeout_seconds']:raise TimeoutError('No completed rollout step for 45 minutes')
                if time.time()-started>M['stage_attempt_timeout_seconds']:raise TimeoutError('Attempt exceeded 24 hours')
                if (RUN/'STOP').exists():raise InterruptedError('STOP file requested')
                time.sleep(15)
        finally:
            cleanup(owned)
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:pass
def preflight():
    integrity()
    for mode in ['s2','depth']:
        stage=RUN/(f'smoke-{mode}' if SMOKE else mode);stage.mkdir(exist_ok=True)
        with (stage/'resolved-config.yaml').open('w') as out:
            subprocess.run(command(mode,stage)+['--cfg','job','--resolve'],cwd=CODE,env=environment(stage),stdout=out,stderr=subprocess.STDOUT,check=True)
    env=environment(RUN/'depth');env['PYTHONPATH']=str(CODE/'verl')+':'+env['PYTHONPATH']
    with (RUN/'reward-checks.log').open('w') as out:
        subprocess.run([sys.executable,str(RUN/'check_reward.py')],env=env,cwd=RUN,stdout=out,stderr=subprocess.STDOUT,check=True)
    status('preflight_passed')
def main():
    with (RUN/('smoke.lock' if SMOKE else 'controller.lock')).open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        preflight()
        if PREFLIGHT:return
        if not SMOKE:assert json.loads((RUN/'smoke-depth/final-verification.json').read_text())['complete']
        completed=[]
        for mode in (['depth'] if SMOKE else ['s2','depth']):
            stage=RUN/(f'smoke-{mode}' if SMOKE else mode);stage.mkdir(exist_ok=True)
            steps=2 if SMOKE else 800
            if (stage/'final-verification.json').exists():completed.append(mode);continue
            success=False
            for number in range(1,M['max_attempts_per_stage']+1):
                integrity();checkpoint=latest_complete(stage)
                if checkpoint and int(checkpoint.name.split('_')[-1])==steps and (stage/f'results/validation/{steps}.jsonl').exists():
                    rc=0
                else:
                    try:rc=attempt(mode,stage,number,checkpoint)
                    except InterruptedError:raise
                    except Exception as exc:
                        (stage/f'error-attempt-{number}.txt').write_text(traceback.format_exc());rc=-1
                atomic(stage/f'exit-attempt-{number}.json',{'exit_code':rc})
                if rc==0:
                    with (stage/'verification.log').open('w') as log:
                        result=subprocess.run([sys.executable,str(RUN/'verify.py'),str(stage),str(steps)],cwd=RUN,stdout=log,stderr=subprocess.STDOUT)
                    if result.returncode==0:success=True;break
                status('retry_pending',stage=mode,attempt=number,exit_code=rc)
                time.sleep(15)
            if not success:raise RuntimeError(f'{mode}: attempts exhausted; outputs preserved')
            completed.append(mode)
        report={mode:json.loads((RUN/(f'smoke-{mode}' if SMOKE else mode)/'final-verification.json').read_text()) for mode in completed}
        atomic(RUN/('smoke-report.json' if SMOKE else 'report.json'),report)
        free_gpus();status('complete',completed=completed)
if __name__=='__main__':
    try:main()
    except Exception as exc:
        status('failed',error=repr(exc));traceback.print_exc();raise
