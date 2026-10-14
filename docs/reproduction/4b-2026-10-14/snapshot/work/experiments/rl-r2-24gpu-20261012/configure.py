from pathlib import Path
import hashlib,json
R=Path.cwd();B=R/'work/experiments/rl-r2-24gpu-20261012'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((B/'runtime-build.json').read_text())['passed']
cfg=json.loads((R/'work/experiments/rl-instruct-20261011/direct-full500/strong_width-config.json').read_text())
for key,filename in [('replay','structured_replay.py'),('batch_decoder','microbatch_decoder.py')]:cfg[key]=str(B/'runner'/filename)
cfg.update(train=str(B/'data/train.jsonl'),val=str(B/'data/val.jsonl'),seed=20261012,data_seed=20261012,
           validation_seed=91261011,world_size=24,expected_world_size=24,max_batched_paths=8,checkpoint_steps=[50,100,200,300,400,500],
           steps=500,output=str(B/'production'),resume=None,lane='one_cloud_job_3x8',gpu_audit=str(B/'distributed-smoke-proof.json'),
           curriculum='1024 pinned public CNK12/Orca, preserve prior128; gold-blind teacher corroborated expansion',
           global_batch=dict(prompts_per_step=24,rollouts_per_prompt=4,responses_per_step=96),
           checkpoint_format=dict(single_safetensors=True,optimizer=False,rng=False),data_reuse=dict(train1024_passes_if_all500=500*24/1024))
cfg['sealed_inputs']={str(p.relative_to(R)):str(p) for p in (B/'runner').rglob('*') if p.is_file() and p.suffix in ['.py','.json']}
for key in ['reward','scorer','system']:cfg['sealed_inputs'][key]=cfg[key]
for name in ['manifest.json','train.jsonl','val.jsonl']:cfg['sealed_inputs']['data/'+name]=str(B/'data'/name)
cfg['sealed_inputs']['original-fullSFT-export-proof']=str(R/'work/experiments/instruct-full-20261011/epoch1-export-proof.json')
(B/'production-config.json').write_text(json.dumps(cfg,indent=2)+'\n')
smoke={**cfg,'steps':2,'output':str(B/'smoke'),'skip_validation':True,'skip_exports':True,'checkpoint_steps':[],
       'resident_fixture_step':2,'sealed_inputs':{}}
(B/'smoke-config.json').write_text(json.dumps(smoke,indent=2)+'\n')
entry=B/'entry.sh';entry.write_text('#!/usr/bin/env bash\nset -euo pipefail\ncd '+str(R)+'\nexport PYTHONDONTWRITEBYTECODE=1\nexec '+str(R/'.venv/bin/python')+' '+str(B/'node_entry.py')+'\n');entry.chmod(0o755)
print(json.dumps(dict(config_sha256=sha(B/'production-config.json'),batch=cfg['global_batch'],checkpoints=cfg['checkpoint_steps'])))
