"""Exact16→500 artifact-bound automatic continuation, immutable campaign decision."""
import argparse,subprocess,sys,copy,os
from common import *
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['strong_width','forward_only'],required=True);a=p.parse_args();s,r=source_gate();decision=read(HERE/'decision.json');stagecfg=BASE/'production-configs'/(a.mode+'-stage16.json');cfg=read(stagecfg);prior=ROOT/'work/experiments/night-20261010/cloud-continued'/cfg['lane']/'results'/('306-instruct-rl-strong-width-stage16.json' if a.mode=='strong_width' else '232-instruct-rl-forward-only-stage16.json');assert read(prior)['returncode']==0
run=Path(cfg['output']);assert read(run/'result.json')['completed'];checkpoint=run/'checkpoint-0016';assert read(checkpoint/'complete.json')['step']==16
assert all(sha(decision[k])==decision[k+'_sha256'] for k in ['train','val','manifest'])
assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
baseline=run/'validation-0000/summary.json'
if decision['data_choice'].startswith('independently_admitted_public'):
 baseline_run=HERE/'runs'/(a.mode+'-new-curriculum-sft-baseline');bcfg=copy.deepcopy(cfg);bcfg.update(train=decision['train'],val=decision['val'],steps=0,output=str(baseline_run),resume=None,engineering_only=False);bp=HERE/(a.mode+'-baseline-config.json');write(bp,bcfg)
 subprocess.run([sys.executable,'-m','torch.distributed.run','--standalone','--nproc_per_node=8',str(BASE/'production-runner/train.py'),'--config',str(bp),'--smoke'],cwd=ROOT,check=True)
 baseline=baseline_run/'validation-0000/summary.json';assert read(baseline)['completed']==decision['val_count']
if decision['data_choice'].startswith('independently_admitted_public'):
 assert all(sha(decision[k])==decision[k+'_sha256'] for k in ['admission_review','difficulty_review'])
files=[p for p in checkpoint.rglob('*') if p.is_file() and not p.name.startswith('._')]+[baseline,run/'validation-0016/summary.json',stagecfg,run/'result.json',HERE/'decision.json',prior]
manifest=HERE/(a.mode+'-resume16-manifest.json');assert not manifest.exists();write(manifest,dict(checkpoint=str(checkpoint),files={str(p):sha(p) for p in files}))
proof=BASE/'long-run/actual-batch32-proof.json';actor=BASE/('long-run/runner/train.py' if decision['batch32_passed'] else 'production-runner/train.py');cfg.update(resume=str(checkpoint),resume_manifest=str(manifest),resume_manifest_sha256=sha(manifest),steps=500,checkpoint_steps=[32,64,128,256,500],output=str(HERE/'runs'/(a.mode+'-full500')),train=decision['train'],val=decision['val'],prompts_per_rank=decision['prompts_per_rank'],actor_train=str(actor),initial_sft_validation=str(baseline),batch32_failed_fallback=not decision['batch32_passed'],global_batch=dict(prompts_per_step=decision['global_prompts'],rollouts_per_prompt=4,responses_per_step=decision['global_prompts']*4),data_reuse=dict(additional_exposures=484*decision['global_prompts'],additional_passes=484*decision['global_prompts']/decision['train_count']),curriculum=decision['data_choice'],validation_protocol='matched immutable clean curriculum validation; original fullSFT baseline; no MATH500 selection',total_steps_not_additional=True,campaign_seal=str(HERE/(a.mode+'-seal.json')))
if decision['batch32_passed']:
 cfg.update(replay=str(BASE/'long-run/runner/structured_replay.py'),batch_decoder=str(BASE/'long-run/runner/microbatch_decoder.py'),long_batch_proof=str(proof),long_batch_proof_sha256=sha(proof))
for p in [manifest,baseline,HERE/'decision.json',Path(decision['train']),Path(decision['val']),Path(decision['manifest'])]:cfg['sealed_inputs'][str(p.relative_to(ROOT))]=str(p)
if decision['data_choice'].startswith('independently_admitted_public'):
 for k in ['admission_review','difficulty_review']:cfg['sealed_inputs'][str(Path(decision[k]).relative_to(ROOT))]=decision[k]
result307=ROOT/'work/experiments/night-20261010/cloud-continued/tmp2/results/307-instruct-rl-bs32-technical-step-resume.json';assert sha(result307)==decision['result307_sha256'];cfg['sealed_inputs'][str(result307.relative_to(ROOT))]=str(result307)
if decision['batch32_passed']:
 review=BASE/'long-run/independent-batch32-runtime-review.json';assert read(review)['passed'] and sha(review)==decision['runtime_review_sha256'];assert read(review)['actual_batch32_proof_sha256']==sha(proof)
 for p in [proof,review]:cfg['sealed_inputs'][str(p.relative_to(ROOT))]=str(p)
config=HERE/(a.mode+'-full500.json');assert not config.exists();write(config,cfg)
hashes={str(Path(k).relative_to(ROOT)):v for k,v in s['sha256'].items()};hashes.update({str(Path(v).relative_to(ROOT)):sha(v) for v in cfg['sealed_inputs'].values()});hashes[str(config.relative_to(ROOT))]=sha(config)
seal=Path(cfg['campaign_seal']);write(seal,dict(sha256=hashes,model=cfg['model'],full_sft_export_audit=str(BASE.parent/'instruct-full-20261011/epoch1-export-proof.json')))
technical=BASE/'technical-launch.json';result=ROOT/'work/experiments/night-20261010/cloud-continued/tmp2/results/305-instruct-rl-technical-step-resume.json';receipt=HERE/(a.mode+'-root-approved.json');write(receipt,dict(approved=True,campaign_seal_sha256=sha(seal),config_sha256=sha(config),technical_proof_sha256=sha(technical),technical_result_sha256=sha(result),source_root_receipt_sha256=sha(HERE/'source-root-approved.json'),decision_sha256=sha(HERE/'decision.json'),user_authorized_total500=True))
subprocess.run([sys.executable,str(HERE/'launch.py'),'--config',str(config),'--receipt',str(receipt)],cwd=ROOT,check=True)
