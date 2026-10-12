"""Prepare exact full-SFT memory/replay engineering probe; no production launch."""
from pathlib import Path
import json,hashlib
here=Path(__file__).resolve().parent;root=next(p for p in here.parents if (p/'verl').is_dir() and (p/'exps').is_dir());base=here.parent;full=root/'work/experiments/instruct-full-20261011';model=full/'runs/epoch1/final';reward=base/'reward.py'
assert hashlib.sha256(reward.read_bytes()).hexdigest()=='b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce'
common=dict(model=str(model),system=str(full/'system.txt'),scorer=str(root/'work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py'),format_validator=str(root/'work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py'),replay=str(here/'structured_replay.py'),reward=str(reward),train=str(here/'technical-probes.jsonl'),val=str(here/'technical-probes.jsonl'),seed=20261011,validation_seed=91261011,world_size=8,group=4,steps=1,lr=1e-6,clip=.2,max_grad_norm=1.,response_budget=4096,path_budget=768,max_context=16384,checkpoint_every=1,max_replay_drift=.01,actor_dtype='fp32',zero1_optimizer=True,tf32=False,std_normalization=False,batch_decoder=str(here/'microbatch_decoder.py'),max_batched_paths=2,reward_mode='strong_width',lane='tmp3',engineering_only=True,curriculum_allowed=False,production_allowed=False)
cfg=base/'technical-configs';cfg.mkdir(exist_ok=True)
first=dict(common,output=str(base/'runs/technical-step1'));second=dict(common,steps=2,resume=str(base/'runs/technical-step1/checkpoint-0001'),output=str(base/'runs/technical-resume-step2'))
for name,x in [('step1',first),('resume-step2',second)]:
 p=cfg/(name+'.json');assert not p.exists();p.write_text(json.dumps(x,indent=2)+'\n')
(base/'technical-config-seal.json').write_text(json.dumps(dict(approved=False,model=str(model),requires=['Verified full SFT export bound audit','Root review before retained queue dispatch','All8ranks finite actual updates','Actual replay parity','Save/resume optimizer + RNG identity','Peakmemory and clean launcher/NCCL exit'],sha256={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*[p for p in here.glob('*.py') if not p.name.startswith('._')],*cfg.glob('*.json'),reward,here/'technical-probes.jsonl']}),indent=2)+'\n')
print(cfg)
