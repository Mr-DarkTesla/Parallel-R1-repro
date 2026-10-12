"""Bind new unlaunched RL arms to pinned runner/data/audit/reward artifacts."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = next(p for p in HERE.parents if (p/"verl").is_dir() and (p/"exps").is_dir())


def main():
    base=P/'work/experiments/base-format-20261010'
    readiness=P/'work/experiments/rl-readiness-20261010'
    batched=readiness/'batched'
    audit=readiness/'gpu-fp32-full-proof.json'
    proof=json.loads(audit.read_text())
    if not proof['passed']:
        raise ValueError('Actual GPU audit must pass before configs')
    common=dict(model=str(base/'runs/production/final'),system=str(base/'system.txt'),
                scorer=str(P/'work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py'),
                format_validator=str(base/'evaluations/summary_metrics.py'),
                replay=str(readiness/'structured_replay.py'),reward=str(HERE/'reward.py'),
                gpu_audit=str(audit),train=str(HERE/'data/train.jsonl'),val=str(HERE/'data/val.jsonl'),
                seed=20261010,validation_seed=91261010,world_size=8,group=4,steps=64,
                lr=1e-6,clip=.2,max_grad_norm=1.,response_budget=4096,path_budget=768,
                max_context=16384,checkpoint_every=16,max_replay_drift=.01,
                actor_dtype='fp32',tf32=False,std_normalization=False,
                batch_decoder=str(batched/'microbatch_decoder.py'),max_batched_paths=2,
                batch_gpu_audit=str(batched/'gpu-proof.json'),
                initial_model_manifest=str(readiness/'base-final-sealed-manifest.json'),
                loss_normalization='fixed response budget4096 times group4, then DDPmean',
                validation_protocol='temp1 top_p1 top_kdisabled fixedselectionseed, noforcedthink',
                benchmark_protocol='Frozen128 mixedGSM/MATH oldBaseevaltemp.6 top_p.95 top_k20; sealedGSM512separate')
    sealed = {f.name:str(f) for f in [HERE/'train.py',HERE/'rollout.py',HERE/'run_job.py',HERE/'reward.py',
                  readiness/'structured_replay.py',readiness/'source/parallel_structure.py',
                  audit,HERE/'data/manifest.json',HERE/'data/train.jsonl',HERE/'data/val.jsonl',HERE/'data/final.jsonl',
                  base/'system.txt',base/'runs/production/final/model.safetensors.index.json',
                  Path(common['scorer']),Path(common['format_validator'])]}
    for f in [batched/'decoder.py',batched/'microbatch_decoder.py',batched/'gpu-proof.json']:
        sealed['batched-'+f.name]=str(f)
    sealed['initial-model-manifest']=str(readiness/'base-final-sealed-manifest.json')
    directory=HERE/'configs'
    directory.mkdir(exist_ok=False)
    for lane,mode in [('tmp2','forward_only'),('tmp3','strong_width')]:
        cfg=dict(common,lane=lane,reward_mode=mode,output=str(HERE/'runs'/mode),sealed_inputs=sealed)
        path=directory/f'{mode}.json'
        path.write_text(json.dumps(cfg,indent=2)+'\n')
    smoke_rows=[json.loads(x) for x in (HERE/'data/smoke.jsonl').read_text().splitlines()]
    all_train=[json.loads(x) for x in (HERE/'data/train.jsonl').read_text().splitlines()]
    longest=max(all_train,key=lambda r:len(r['problem']))
    smoke_rows[-1]=longest
    smoke_file=HERE/'smoke-memory.jsonl'
    smoke_file.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in smoke_rows))
    smoke=dict(common,lane='tmp3',reward_mode='strong_width',steps=2,
               train=str(smoke_file),val=str(smoke_file),
               output=str(HERE/'runs/distributed-smoke'),checkpoint_every=2,
               smoke_memory_row='Includes longest training problem by characters; actual peak GPU recorded')
    (directory/'smoke.json').write_text(json.dumps(smoke,indent=2)+'\n')
    report=dict(passed=True,config_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in directory.glob('*.json')},
                sealed_sha256={name:hashlib.sha256(Path(f).read_bytes()).hexdigest() for name,f in sealed.items()},
                gpu_audit=proof,train_manifest=json.loads((HERE/'data/manifest.json').read_text()))
    (HERE/'ready.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('gpu_audit','train_manifest')}))


if __name__=='__main__':
    main()
