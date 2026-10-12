"""Own eight isolated evaluation workers; incremental durable traces and status."""
from pathlib import Path
import datetime as dt,fcntl,json,os,signal,subprocess,sys,time,traceback
WORK=Path(__file__).resolve().parent;PROJECT=WORK.parents[3]
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def status(**values):
    values['updated_at']=now();p=WORK/'status.tmp';p.write_text(json.dumps(values,indent=2)+'\n');p.replace(WORK/'status.json')
def main():
    lock=(WORK/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    assert not (WORK/'status.json').exists(),'Refuse duplicate controller'
    assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPUs occupied'
    status(state='starting',started_at=now(),completed=0,total=500)
    children=[];started=time.time()
    def interrupted(sig,frame):raise KeyboardInterrupt(f'Signal {sig}')
    signal.signal(signal.SIGTERM,interrupted)
    try:
        for rank in range(8):
            env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=str(rank),PYTHONPATH=str(WORK/'code'),OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',
                TMPDIR=str(PROJECT/'t/w5145'),XDG_CACHE_HOME=str(WORK/'cache'),HF_HOME=str(PROJECT/'cache/huggingface'),
                VLLM_CACHE_ROOT=str(WORK/'cache/vllm'),CUDA_CACHE_PATH=str(WORK/'cache/cuda'),TRITON_CACHE_DIR=str(WORK/'cache/triton'),
                TORCHINDUCTOR_CACHE_DIR=str(WORK/'cache/inductor'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',WANDB_MODE='disabled',PYTHONUNBUFFERED='1')
            env.pop('PARALLEL_R1_TRACE_DIR',None)
            with (WORK/f'worker-{rank}.log').open('w') as log:
                p=subprocess.Popen([sys.executable,str(WORK/'evaluate.py'),'--worker',str(rank)],cwd=PROJECT,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
            children.append(p)
        while True:
            rows=[]
            for trace in WORK.glob('traces-*.jsonl'):
                for line in trace.read_text().splitlines():
                    try:rows.append(json.loads(line))
                    except json.JSONDecodeError:pass  # Only a currently-written final line.
            count=len(rows);elapsed=time.time()-started
            values=dict(state='running',started_at=dt.datetime.fromtimestamp(started,dt.timezone.utc).isoformat(),completed=count,total=500,worker_pids=[p.pid for p in children],elapsed_seconds=elapsed)
            if count:values.update(total_sampled_tokens=sum(r['sampled_tokens'] for r in rows),mean_trace_seconds=sum(r['elapsed_seconds'] for r in rows)/count,eta_utc=dt.datetime.fromtimestamp(time.time()+elapsed/count*(500-count),dt.timezone.utc).isoformat())
            status(**values)
            failed=[(i,p.returncode) for i,p in enumerate(children) if p.poll() is not None and p.returncode!=0]
            if failed:raise RuntimeError(f'Evaluation worker failed: {failed}')
            if all(p.poll() is not None for p in children):
                assert count==500 and len({r['id'] for r in rows})==500
                status(**{**values,'state':'generated','finished_at':now()});break
            time.sleep(15)
    except BaseException as error:
        status(state='failed',error=repr(error))
        for p in children:
            if p.poll() is None:p.terminate()
        for p in children:
            try:p.wait(timeout=15)
            except subprocess.TimeoutExpired:p.kill()
        raise
if __name__=='__main__':main()
