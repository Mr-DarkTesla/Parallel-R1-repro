"""One longest-example canary followed by one fresh eight-GPU SFT; no retries."""
from pathlib import Path
import datetime as dt,fcntl,hashlib,json,math,os,re,subprocess,sys,time,traceback
RUN=Path(__file__).resolve().parent;ROOT=RUN.parents[3];PYTHON=Path(os.environ.get('PARALLEL_R1_PYTHON',str(ROOT/'.venv/bin/python')));CODE=RUN/'code'
def save(p,data):
    q=p.with_suffix('.tmp');q.write_text(json.dumps(data,indent=2)+'\n');q.replace(p)
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def command(name,canary=False):
    out=RUN/'runs'/name;data=RUN/'data';base=RUN/'base'
    return [str(PYTHON),'-m','torch.distributed.run','--standalone','--nnodes=1','--nproc_per_node=8','-m','verl.trainer.fsdp_parallel_sft_trainer','--config-name=sft_qwen3_06b',
        f'data.train_files={data/("canary-train.parquet" if canary else "train.parquet")}',f'data.val_files={data/("canary-val.parquet" if canary else "val.parquet")}',
        'data.prompt_key=problem','data.response_key=response','data.prompt_dict_keys=[]','data.response_dict_keys=[]',
        '+data.prompt_messages_key=prompt_messages','+data.defer_parallel_mask=true','data.parallel_attention=true','data.multiturn.enable=false','data.truncation=error','data.max_length=16384',
        'data.train_batch_size=8' if canary else 'data.train_batch_size=128','data.micro_batch_size_per_gpu=1','data.num_workers=2','data.trim_padding=true',
        'model.enable_gradient_checkpointing=true',f'model.partial_pretrain={base}','use_remove_padding=false','ulysses_sequence_parallel_size=1','optim.lr=1e-5',
        'trainer.total_epochs=1' if canary else 'trainer.total_epochs=5','trainer.resume_mode=disable','trainer.logger=[console]','trainer.seed=1',
        f'trainer.experiment_name={name}',f'trainer.default_local_dir={out}/checkpoints',f'trainer.final_dir={out}/final',f'hydra.run.dir={out}/hydra']+(['trainer.total_training_steps=1'] if canary else [])
def main():
    lock=(RUN/'controller.lock').open('w')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        print('SFT controller lock held; leaving existing status untouched',flush=True);return
    assert not (RUN/'status.json').exists(),'Refuse duplicate/restart'
    assert json.loads((RUN/'structure-check.json').read_text())['passed']
    assert json.loads((RUN/'data-report.json').read_text())['rows']==3000
    assert json.loads((RUN/'validation.json').read_text())['passed']
    assert json.loads((RUN/'initialization-proof.json').read_text())['preserved_all_other_rows_exactly']
    assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPU occupied'
    env=os.environ.copy();env.update(PYTHONPATH=str(CODE),CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
        WANDB_MODE='disabled',PYTHONUNBUFFERED='1',PYTORCH_CUDA_ALLOC_CONF='expandable_segments:True',TMPDIR=str(ROOT/'tmp'),XDG_CACHE_HOME=str(RUN/'cache'),HF_HOME=str(RUN/'cache/huggingface'),CUDA_CACHE_PATH=str(RUN/'cache/cuda'))
    hashes={str(p.relative_to(CODE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in CODE.rglob('*.py')}
    save(RUN/'sft-code-sha256.json',hashes)
    for name,canary in [('01_sft',False)]:
        out=RUN/'runs'/name;out.mkdir(exist_ok=False);cmd=command(name,canary);save(out/'command.json',cmd)
        state=dict(state='running',stage=name,started_at=now(),controller_pid=os.getpid(),gpus=list(range(8)),log=str(out/'sft.log'),target_steps=1 if canary else 105)
        with (out/'sft.log').open('w') as log:
            p=subprocess.Popen(cmd,cwd=CODE,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            state['pid']=p.pid;state['owned_process_group']=p.pid;save(RUN/'status.json',state)
            while p.poll() is None:
                time.sleep(15)
                contents=(out/'sft.log').read_text(errors='replace')
                done=len(re.findall(r'train/loss:\s*([-+\w.eE]+)',contents))
                elapsed=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(state['started_at'])).total_seconds()
                state.update(completed_steps=done,elapsed_seconds=elapsed,eta_seconds=(elapsed/done*(state['target_steps']-done) if done else None),heartbeat_at=now())
                save(RUN/'status.json',state)
            rc=p.returncode
        (out/'exit_code').write_text(str(rc)+'\n')
        losses=[float(x) for x in re.findall(r'train/loss:\s*([-+\w.eE]+)',(out/'sft.log').read_text(errors='replace'))]
        expected=1 if canary else 105
        assert rc==0 and len(losses)==expected and all(math.isfinite(x) for x in losses),(name,rc,len(losses),expected)
        assert (out/'final/model.safetensors').stat().st_size>1_000_000_000
        state.update(state='complete',finished_at=now(),steps=len(losses),final=str(out/'final'));save(out/'result.json',state)
    save(RUN/'status.json',state)
if __name__=='__main__':
    try:main()
    except BaseException as e:
        save(RUN/'status.json',dict(state='failed',at=now(),error=repr(e)));traceback.print_exc();raise
