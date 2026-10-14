"""Prepare portable phase config and bind restored inputs to historical evidence.
Does not allocate GPUs, submit jobs, or claim a new GPU qualification.
"""
import argparse,hashlib,json
from pathlib import Path
PHASES={
 'rl50':('rl-r2-24gpu-20261012/recovery-20261012-global-parity','production-config-v2.json','runner/train.py',50),
 'rl300':('rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory','production-config.json','src/train.py',300),
 'rl150-new-reward':('rl-r4-dapo2k-sft-16gpu-20261013','production-config.json','src/train.py',150),
}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--phase',choices=PHASES,required=True);a=p.parse_args();root=a.root.resolve()
 rel,name,worker,target=PHASES[a.phase];base=root/'work/experiments'/rel;cfg=json.loads((base/name).read_text());original_receipt=json.loads((base/'control/production-approved.json').read_text())
 cfg.update(steps=target,total_training_iterations=target,output=str(base/'reproduction-output'))
 if a.phase=='rl300':
  checkpoint=root/'work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity/reproduction-output/checkpoint-0050'
  cfg.update(model=str(checkpoint/'hf'),initial_checkpoint=str(checkpoint))
 cfg['checkpoint_steps']=[x for x in cfg['checkpoint_steps'] if x<=target]
 # Historical sealed_inputs can include their own config; avoid a circular hash.
 cfg['sealed_inputs']={k:v for k,v in cfg['sealed_inputs'].items() if Path(v).resolve()!=(base/name).resolve()}
 for value in cfg['sealed_inputs'].values():assert Path(value).is_file(),value
 assert not Path(cfg['output']).exists(),'Phase output already exists'
 audit=Path(cfg['gpu_audit']);assert audit.is_file() and json.loads(audit.read_text())['passed']
 smoke=Path(original_receipt['distributed_smoke']['path']);assert smoke.is_file()
 path=base/'portable-config.json';path.write_text(json.dumps(cfg,indent=2)+'\n')
 receipt=dict(approved=True,config_sha256=sha(path),sha256={k:sha(v) for k,v in cfg['sealed_inputs'].items()},distributed_smoke=dict(path=str(smoke),sha256=sha(smoke)),evidence_scope='Historical semantic/optimizer proof on the original machines; no fresh hardware validation claimed',phase=a.phase,target_step=target)
 (base/'portable-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(dict(config=str(path),receipt=str(base/'portable-receipt.json'),worker=str(base/worker),world_size=cfg['expected_world_size'],phase=a.phase)))
if __name__=='__main__':main()
