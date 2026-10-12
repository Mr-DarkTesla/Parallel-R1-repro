"""Retained-worker entrypoint; reports distributed failures and exact run inputs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
P = next(p for p in HERE.parents if (p/"verl").is_dir() and (p/"exps").is_dir())


def save(path,value):
    tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value,indent=2)+'\n')
    os.replace(tmp,path)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',required=True)
    parser.add_argument('--receipt')
    parser.add_argument('--smoke',action='store_true')
    args=parser.parse_args()
    cfg=json.loads(Path(args.config).read_text())
    lane=cfg['lane']
    if lane not in ['tmp2','tmp3']:
        raise ValueError('Only the two existing authorized Cloud lanes are allowed')
    ready=json.loads((P/'work/experiments/night-20261010/cloud-continued'/lane/'ready.json').read_text())
    if os.uname().nodename!=ready['hostname']:
        raise ValueError('Refuse execution outside the retained Cloud host')
    audit=json.loads(Path(cfg['gpu_audit']).read_text())
    if not audit.get('passed') or audit.get('model')!=cfg['model']:
        raise ValueError('Actual model GPU parity proof missing or failed')
    if cfg.get('batch_decoder'):
        batch_audit=json.loads(Path(cfg['batch_gpu_audit']).read_text())
        if not batch_audit.get('passed') or batch_audit.get('model')!=cfg['model']:
            raise ValueError('Actual batched decoder GPU proof missing or failed')
    manifest_path=cfg.get('initial_model_manifest')
    if manifest_path:
        manifest=json.loads(Path(manifest_path).read_text())
        if not manifest.get('passed') or manifest.get('model')!=cfg['model']:
            raise ValueError('Initial model manifest does not bind this checkpoint')
        for name,entry in manifest['files'].items():
            artifact=(Path(cfg['model'])/name).resolve()
            if not artifact.is_relative_to(Path(cfg['model']).resolve()):
                raise ValueError('Initial model artifact escapes checkpoint')
            digest=hashlib.sha256()
            with artifact.open('rb') as handle:
                for block in iter(lambda:handle.read(8*1024*1024),b''):
                    digest.update(block)
            if artifact.stat().st_size!=entry['bytes'] or digest.hexdigest()!=entry['sha256']:
                raise ValueError('Initial model artifact changed: '+name)
    log=Path(cfg['output']).with_name(Path(cfg['output']).name+'-launch.json')
    if not log.resolve().is_relative_to(P):
        raise ValueError('Output is outside the authorized project root')
    log.parent.mkdir(parents=True,exist_ok=True)
    if log.exists():
        raise FileExistsError(log)
    if not args.smoke and not args.receipt:
        raise ValueError('Production requires root receipt')
    env=os.environ.copy()
    env.update(OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',HF_HUB_OFFLINE='1',
               TRANSFORMERS_OFFLINE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',
               NCCL_ASYNC_ERROR_HANDLING='1',TORCH_NCCL_ASYNC_ERROR_HANDLING='1')
    env['NVIDIA_TF32_OVERRIDE']='0'
    argv=[sys.executable,'-m','torch.distributed.run','--standalone','--nnodes=1',
          '--nproc_per_node='+str(cfg.get('world_size',8)),str(HERE/'train.py'),'--config',args.config]
    if args.smoke:
        argv.append('--smoke')
    else:
        argv+=['--receipt',args.receipt]
    identity=dict(state='starting',started=time.time(),argv=argv,hostname=os.uname().nodename,
                  config_sha256=hashlib.sha256(Path(args.config).read_bytes()).hexdigest(),
                  gpu_audit_sha256=hashlib.sha256(Path(cfg['gpu_audit']).read_bytes()).hexdigest(),
                  world_size=cfg.get('world_size',8),smoke=args.smoke)
    save(log,identity)
    process=subprocess.Popen(argv,cwd=P,env=env)
    rc=process.wait()
    identity.update(state='completed' if rc==0 else 'failed',returncode=rc,finished=time.time())
    save(log,identity)
    if rc:
        status=Path(cfg['output'])/'status.json'
        if status.parent.exists():
            save(status,dict(state='failed',distributed_launcher_returncode=rc,
                             evidence_preserved=True,at=time.time()))
        raise SystemExit(rc)
    result=json.loads((Path(cfg['output'])/'result.json').read_text())
    if not result.get('completed'):
        raise ValueError('Distributed launcher exited without verified training result')
    if args.smoke:
        rows=[json.loads(x) for x in (Path(cfg['output'])/'metrics.jsonl').read_text().splitlines()]
        metrics=[r for step in rows for r in step['ranks']]
        proof=dict(passed=bool(metrics) and all(r['trainable']>=4_000_000_000 and
              r['optimizer_step'] and r['backbone_update_l2']>0 and r['max_replay_logp_drift']<=.01 and
              r['mean_replay_logp_drift']<=.002 and r['p95_replay_logp_drift']<=.005 for r in metrics),
              world_size=cfg.get('world_size',8),optimizer_updates=sum(r['optimizer_step'] for r in metrics),
              max_gpu_bytes=max(r['peak_gpu_bytes'] for r in metrics),
              mean_group_accuracy=sum(r['correct'] for r in metrics)/sum(r['group'] for r in metrics),
              zero_advantage_groups=sum(r['zero_advantage_group'] for r in metrics),
              max_replay_logp_drift=max(r['max_replay_logp_drift'] for r in metrics),
              source_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in HERE.glob('*.py')},
              output=cfg['output'],config_sha256=identity['config_sha256'])
        save(Path(cfg['output'])/'smoke-proof.json',proof)
        if not proof['passed']:
            raise ValueError('Distributed optimizer smoke did not meet readiness gate')


if __name__=='__main__':
    main()
