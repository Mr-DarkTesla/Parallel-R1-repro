"""Actual long32prompt engineering proof after exact stage16 predecessor release."""
import argparse,json,hashlib,os,sys,subprocess,time,math
from pathlib import Path
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
p=argparse.ArgumentParser();p.add_argument('--receipt',required=True);a=p.parse_args();here=Path(__file__).resolve().parent;root=next(x for x in here.parents if (x/'verl').is_dir() and (x/'exps').is_dir());seal=here/'batch-proof-source-seal.json';s=json.loads(seal.read_text());r=json.loads(Path(a.receipt).read_text());assert r['approved'] and r['batch_proof_source_seal_sha256']==sha(seal)
assert all(sha(k)==v for k,v in s['sha256'].items());pre=root/s['predecessor_result'];assert json.loads(pre.read_text())['returncode']==0 and r['predecessor_result_sha256']==sha(pre)
audit=json.loads(Path(s['full_sft_export_audit']).read_text());assert audit['passed'] and audit['checkpoint']==s['model'];assert r['full_sft_export_audit_sha256']==sha(s['full_sft_export_audit']);assert all(Path(k).resolve().is_relative_to(root) and sha(k)==v for k,v in audit['manifest'].items())
ready=json.loads((root/'work/experiments/night-20261010/cloud-continued/tmp2/ready.json').read_text());assert os.uname().nodename==ready['hostname']
assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
proof=here/'actual-batch32-proof.json';assert not proof.exists();report=dict(state='running',passed=False,actual_8GPU_memory_pass=False,started=time.time(),source_seal_sha256=sha(seal),root_receipt_sha256=sha(a.receipt),global_prompt_batch=32,global_response_batch=128,unique_engineering_probes=16,prompt_slots=32,probe_repetition_disclosed=True,selection_allowed=False)
env=os.environ.copy();env.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',NVIDIA_TF32_OVERRIDE='0',PYTHONUNBUFFERED='1')
try:
 all_metrics=[]
 for name in ['step1','resume-step2']:
  cfgpath=here/'batch-proof-configs'/(name+'.json');cfg=json.loads(cfgpath.read_text())
  subprocess.run([sys.executable,'-m','torch.distributed.run','--standalone','--nproc_per_node=8',str(here/'runner/train.py'),'--config',str(cfgpath),'--smoke'],cwd=root,env=env,check=True)
  run=Path(cfg['output']);assert json.loads((run/'result.json').read_text())['completed'];metrics=[m for l in (run/'metrics.jsonl').read_text().splitlines() for m in json.loads(l)['ranks']];assert len(metrics)==8 and {m['rank'] for m in metrics}==set(range(8)) and {m['step'] for m in metrics}=={cfg['steps']} and json.loads((run/'result.json').read_text())['world_size']==8
  assert all(m['peak_gpu_bytes']>0 and all(0<=z['allocated']<=z['reserved']<=z['total'] and m['peak_gpu_bytes']<z['total'] and z['free']>=0 for z in m['memory_stages']) for m in metrics),'Memory envelope invalid'
  assert all(m['global_prompt_batch']==32 and m['global_rollouts']==128 and m['prompts_per_rank']==4 and m['within_prompt_group']==4 and m['optimizer_step'] and m['backbone_update_l2']>0 and all(math.isfinite(m[k]) for k in ['loss','grad_norm','backbone_update_l2']) and m['max_replay_logp_drift']<=.01 and m['mean_replay_logp_drift']<=.002 and m['p95_replay_logp_drift']<=.005 for m in metrics)
  if name=='resume-step2':assert all(all(m['resume_proof'].get(k) for k in ['exact_local_adam_state','exact_cpu_rng','exact_cuda_rng','exact_python_rng']) for m in metrics)
  assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip()
  all_metrics+=metrics
 report.update(state='passed',passed=True,actual_8GPU_memory_pass=True,finished=time.time(),peak_gpu_bytes=max(m['peak_gpu_bytes'] for m in all_metrics),metrics=all_metrics,clean_exits=True)
except BaseException as e:report.update(state='failed',finished=time.time(),error=repr(e));raise
finally:proof.write_text(json.dumps(report,indent=2)+'\n')
