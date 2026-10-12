"""Launch user-authorized matched production only behind actual technical PASS."""
import argparse,json,hashlib,os,subprocess,sys,time
from pathlib import Path

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--receipt',required=True);a=p.parse_args();here=Path(__file__).resolve().parent;base=here.parent;root=next(x for x in here.parents if (x/'verl').is_dir() and (x/'exps').is_dir());config=Path(a.config);cfg=json.loads(config.read_text());receipt=json.loads(Path(a.receipt).read_text());seal=Path(cfg['campaign_seal'])
assert receipt.get('approved') and receipt.get('campaign_seal_sha256')==sha(seal) and receipt.get('config_sha256')==sha(config),'Concrete root production receipt required'
x=json.loads(seal.read_text());assert all(sha(root/k)==v for k,v in x['sha256'].items());technical=base/'technical-launch.json';proof=json.loads(technical.read_text());assert proof.get('passed') and proof['state']=='passed' and proof['lane']=='tmp2'
result=root/'work/experiments/night-20261010/cloud-continued/tmp2/results/305-instruct-rl-technical-step-resume.json';assert json.loads(result.read_text())['returncode']==0;assert receipt.get('technical_proof_sha256')==sha(technical) and receipt.get('technical_result_sha256')==sha(result)
ready=json.loads((root/'work/experiments/night-20261010/cloud-continued'/cfg['lane']/'ready.json').read_text());assert os.uname().nodename==ready['hostname'];assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
export=json.loads(Path(x['full_sft_export_audit']).read_text());assert export['passed'] and export['checkpoint']==cfg['model'];assert all(Path(k).resolve().is_relative_to(root) and sha(k)==v for k,v in export['manifest'].items())
if cfg.get('resume'):
 assert sha(cfg['resume_manifest'])==cfg['resume_manifest_sha256'],'Resume manifest drifted'
 resume_manifest=json.loads(Path(cfg['resume_manifest']).read_text())
 assert resume_manifest['checkpoint']==cfg['resume'] and all(Path(k).resolve().is_relative_to(root) and sha(k)==v for k,v in resume_manifest['files'].items()),'Resume artifacts or selection evidence drifted'
if cfg['lane']=='tmp3':
 recovered=base/'evaluations/initial-lr1e-3-structured500/recovery-terminal-proof.json';assert json.loads(recovered.read_text())['passed'];prior=root/'work/experiments/night-20261010/cloud-continued/tmp3/results/231-instruct-math500-worker1-repair.json';assert json.loads(prior.read_text())['returncode']==0
if cfg['prompts_per_rank']==4:
 assert sha(cfg['long_batch_proof'])==cfg['long_batch_proof_sha256'] and json.loads(Path(cfg['long_batch_proof']).read_text())['actual_8GPU_memory_pass']
else:
 assert cfg['prompts_per_rank']==1 and cfg['batch32_failed_fallback'] and cfg['global_batch']['prompts_per_step']==8
output=Path(cfg['output']);gate=output.with_name(output.name+'-root-gate.json');gate.parent.mkdir(parents=True,exist_ok=True);assert not gate.exists();gate.write_text(json.dumps(dict(approved=True,config_sha256=sha(config),sha256={k:sha(v) for k,v in cfg['sealed_inputs'].items()},distributed_smoke=dict(path=str(technical),sha256=sha(technical)),root_production_receipt_sha256=sha(a.receipt)),indent=2)+'\n')
env=os.environ.copy();env.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',NVIDIA_TF32_OVERRIDE='0',PYTHONUNBUFFERED='1')
log=output.with_name(output.name+'-launch.json');state=dict(state='running',started=time.time(),config_sha256=sha(config),receipt_sha256=sha(a.receipt),technical_pass=True,lane=cfg['lane']);log.write_text(json.dumps(state,indent=2)+'\n')
try:
 subprocess.run([sys.executable,'-m','torch.distributed.run','--standalone','--nproc_per_node=8',cfg['actor_train'],'--config',str(config),'--receipt',str(gate)],cwd=root,env=env,check=True)
 runresult=json.loads((output/'result.json').read_text());assert runresult['completed'];assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
 summaries=[json.loads(f.read_text()) for f in sorted(output.glob('validation-*/summary.json'))];baseline=next((q for q in summaries if q['step']==0),None)
 if baseline is None:
  baseline=json.loads(Path(cfg['initial_sft_validation']).read_text())
 comparison=dict(initial_sft_correct=baseline['correct'],planned=baseline['completed'],checkpoints=[dict(step=q['step'],correct=q['correct'],delta_correct=q['correct']-baseline['correct'],format_valid=q['format_valid'],generation_forwards=sum(q['actual_forward_calls'])) for q in summaries if q['step']],selection_allowed=True,MATH500_selection=False,continuation_target_step=500)
 (output/f'stage{cfg["steps"]}-quality-comparison.json').write_text(json.dumps(comparison,indent=2)+'\n');state.update(state='completed',finished=time.time(),completed=True)
except BaseException as e:state.update(state='failed',finished=time.time(),error=repr(e));raise
finally:log.write_text(json.dumps(state,indent=2)+'\n')
