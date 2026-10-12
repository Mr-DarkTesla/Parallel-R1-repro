"""Seal new Instruct inputs only after export and independent curriculum audits."""
import argparse,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--export-audit',required=True);p.add_argument('--train',required=True);p.add_argument('--val',required=True);p.add_argument('--data-audit',required=True);p.add_argument('--system',required=True);p.add_argument('--scorer',required=True);a=p.parse_args();here=Path(__file__).resolve().parent;root=next(x for x in here.parents if (x/'verl').is_dir() and (x/'exps').is_dir());base=here.parent
sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
export=json.loads(Path(a.export_audit).read_text());data=json.loads(Path(a.data_audit).read_text());model=Path(a.model).resolve()
assert model.is_relative_to(root) and 'instruct-full' in str(model),'Must be full Instruct SFT export'
assert export.get('passed') and export.get('checkpoint',export.get('model'))==str(model),'Audit must bind exact model'
assert data.get('passed') and data.get('math_all_train_test_excluded') and data.get('reserved_aime_excluded'),'Independent leak audit required'
assert data.get('train_sha256')==sha(a.train) and data.get('val_sha256')==sha(a.val)
assert data.get('group_disjoint'),'Independent split provenance required'
reward=base/'reward.py';assert sha(reward)=='b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce'
sealed={str(x.relative_to(root)):str(x) for x in [*[p for p in here.glob('*.py') if not p.name.startswith('._')],here/'source/parallel_structure.py',reward,Path(a.export_audit),Path(a.data_audit),Path(a.train),Path(a.val),Path(a.system),Path(a.scorer)]}
common=dict(model=str(model),system=a.system,scorer=a.scorer,format_validator=a.scorer,replay=str(here/'structured_replay.py'),reward=str(reward),train=a.train,val=a.val,seed=20261011,validation_seed=91261011,world_size=8,group=4,steps=64,lr=1e-6,clip=.2,max_grad_norm=1.,response_budget=4096,path_budget=768,max_context=16384,checkpoint_every=16,max_replay_drift=.01,actor_dtype='fp32',zero1_optimizer=True,tf32=False,std_normalization=False,batch_decoder=str(here/'microbatch_decoder.py'),max_batched_paths=2,sealed_inputs=sealed,bonus_schedule='constant_no_annealing',readiness='pending exact full Instruct replay+2steps+exit GPUmemory proof')
directory=base/'configs';directory.mkdir(exist_ok=False)
for lane,mode in [('tmp2','forward_only'),('tmp3','strong_width')]:
 cfg=dict(common,lane=lane,reward_mode=mode,output=str(base/'runs'/mode));(directory/(mode+'.json')).write_text(json.dumps(cfg,indent=2)+'\n')
smoke=dict(common,lane='tmp3',reward_mode='strong_width',steps=2,checkpoint_every=2,output=str(base/'runs/two-step-readiness'));(directory/'smoke.json').write_text(json.dumps(smoke,indent=2)+'\n')
(base/'config-seal.json').write_text(json.dumps(dict(approved=False,sha256={k:sha(v) for k,v in sealed.items()},configs={x.name:sha(x) for x in directory.glob('*.json')}),indent=2)+'\n')
print('Sealed unapproved Instruct configs; no launch performed')
