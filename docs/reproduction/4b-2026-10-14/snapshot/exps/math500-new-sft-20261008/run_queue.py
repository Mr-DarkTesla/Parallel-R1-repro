import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback
import psutil

ROOT=Path(__file__).resolve().parent
CURRENT=None
STOP=False

def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def write(path,value):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,indent=2)+'\n');temp.replace(path)
def on_stop(sig,frame):
    global STOP
    STOP=True
    if CURRENT and CURRENT.poll() is None:os.killpg(CURRENT.pid,signal.SIGTERM)

def cleanup(owned):
    # Only PIDs observed as descendants of this evaluation, with identity checks.
    targets=[]
    for pid,creation in owned.items():
        try:
            p=psutil.Process(pid)
            if p.create_time()==creation and p.is_running():p.terminate();targets.append(p)
        except psutil.NoSuchProcess:pass
    _,alive=psutil.wait_procs(targets,timeout=10)
    for p in alive:
        try:p.kill()
        except psutil.NoSuchProcess:pass

def command(model,folder):
    return ['bash','training_scripts/eval_qwen3_06b.sh',model['path'],
        f'data.val_files={ROOT}/math500.parquet','data.val_batch_size=512',
        'data.max_prompt_length=2048','data.max_response_length=30720',
        'actor_rollout_ref.rollout.mode=async','actor_rollout_ref.rollout.tensor_model_parallel_size=1',
        '++actor_rollout_ref.rollout.seed=42',
        'actor_rollout_ref.rollout.max_model_len=32768','actor_rollout_ref.rollout.max_num_batched_tokens=32768',
        'actor_rollout_ref.rollout.max_num_seqs=32','actor_rollout_ref.rollout.enable_chunked_prefill=true',
        'actor_rollout_ref.rollout.temperature=0.6','actor_rollout_ref.rollout.top_p=0.95','actor_rollout_ref.rollout.top_k=20',
        'actor_rollout_ref.rollout.val_kwargs.temperature=0.6','actor_rollout_ref.rollout.val_kwargs.top_p=0.95',
        'actor_rollout_ref.rollout.val_kwargs.top_k=20','actor_rollout_ref.rollout.val_kwargs.n=1',
        'actor_rollout_ref.rollout.agent.num_paths=2','actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking=0',
        'actor_rollout_ref.rollout.agent.max_path_response_length=8192','actor_rollout_ref.rollout.agent.num_workers=8',
        f'custom_reward_function.path={ROOT}/reward_bridge.py','custom_reward_function.name=compute_score',
        'ray_init.num_cpus=32',f'++ray_init.temp_dir=/tmp/math500sft-20261008/{model["name"]}',
        '++ray_init.object_store_memory=4294967296','++ray_init.plasma_directory=/dev/shm']

def main():
    global CURRENT
    lock=(ROOT/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    assert not (ROOT/'status.json').exists(),'Do not duplicate an existing queue'
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for rel,digest in manifest['code_sha256'].items():
        assert hashlib.sha256((ROOT/'code'/rel).read_bytes()).hexdigest()==digest,rel
    assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPUs occupied'
    state=dict(state='running',started_at=now(),controller_pid=os.getpid(),jobs=[dict(name=m['name'],state='pending') for m in manifest['models']])
    write(ROOT/'status.json',state)
    owned={}
    try:
        for model,job in zip(manifest['models'],state['jobs']):
            if STOP:raise InterruptedError('User stopped evaluation queue')
            folder=ROOT/'runs'/model['name'];folder.mkdir(parents=True,exist_ok=False)
            (folder/'traces').mkdir()
            env=os.environ.copy();env.update(PATH=str(Path(sys.executable).parent)+':'+env['PATH'],
                CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',NPROC_PER_NODE='8',OMP_NUM_THREADS='1',
                TOKENIZERS_PARALLELISM='false',PARALLEL_R1_EVAL_NAME=model['name'],
                PARALLEL_R1_OUTPUT_ROOT=str(folder/'results'),PARALLEL_R1_SCRATCH_ROOT=str(folder/'scratch'),
                PARALLEL_R1_TRACE_DIR=str(folder/'traces'),PARALLEL_R1_FORWARD_PROBE='0',
                HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',WANDB_MODE='disabled',
                RAY_ADDRESS='',PYTHONHASHSEED='42')
            args=command(model,folder);write(folder/'command.json',dict(argv=args,model=model,environment={k:env[k] for k in ('CUDA_VISIBLE_DEVICES','PARALLEL_R1_TRACE_DIR','PARALLEL_R1_OUTPUT_ROOT')}))
            job.update(state='running',started_at=now());write(ROOT/'status.json',state)
            print(now(),'START',model['name'],flush=True)
            owned={}
            with (folder/'driver.log').open('w') as log:
                CURRENT=subprocess.Popen(args,cwd=ROOT/'code',env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
                job['pid']=CURRENT.pid;write(ROOT/'status.json',state)
                while CURRENT.poll() is None:
                    try:
                        for p in psutil.Process(CURRENT.pid).children(recursive=True):owned[p.pid]=p.create_time()
                    except psutil.NoSuchProcess:pass
                    if (ROOT/'STOP').exists():on_stop(signal.SIGTERM,None)
                    job['completed_runtime_records']=sum(1 for p in (folder/'traces').glob('traces-*.jsonl') for line in p.open() if line.endswith('\n'))
                    job['updated_at']=now();write(ROOT/'status.json',state)
                    time.sleep(10)
                code=CURRENT.returncode
            CURRENT=None
            cleanup(owned);owned={}
            (folder/'exit_code').write_text(str(code)+'\n')
            if code:raise RuntimeError(f'{model["name"]} failed: exit {code}')
            job.update(state='analyzing',generation_finished_at=now());write(ROOT/'status.json',state)
            with (folder/'analysis.log').open('w') as log:
                subprocess.run([sys.executable,str(ROOT/'analyze.py'),model['name']],check=True,stdout=log,stderr=subprocess.STDOUT)
            summary=json.loads((folder/'summary.json').read_text())
            assert summary['complete'] and summary['questions']==500
            job.update(state='complete',finished_at=now(),accuracy=summary['accuracy'],parallel_ratio=summary['parallel_ratio'])
            write(ROOT/'status.json',state);print(now(),'COMPLETE',job,flush=True)
        summaries={m['name']:json.loads((ROOT/'runs'/m['name']/'summary.json').read_text()) for m in manifest['models']}
        write(ROOT/'summary.json',dict(complete=True,finished_at=now(),models=summaries))
        state.update(state='complete',finished_at=now());write(ROOT/'status.json',state)
    except BaseException as error:
        if CURRENT and CURRENT.poll() is None:os.killpg(CURRENT.pid,signal.SIGTERM)
        cleanup(owned)
        state.update(state='stopped' if STOP else 'failed',error=f'{type(error).__name__}: {error}',finished_at=now())
        write(ROOT/'status.json',state);traceback.print_exc();raise

if __name__=='__main__':
    signal.signal(signal.SIGTERM,on_stop);signal.signal(signal.SIGINT,on_stop);main()
