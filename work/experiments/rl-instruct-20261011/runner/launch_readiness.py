"""Gate retained-worker technical step1→resume-step2 on exact root receipt."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
def sha(path):
 digest=hashlib.sha256()
 with Path(path).open('rb') as handle:
  for block in iter(lambda:handle.read(8*1024*1024),b''):digest.update(block)
 return digest.hexdigest()

p=argparse.ArgumentParser();p.add_argument('--lane',choices=['tmp2','tmp3'],required=True);p.add_argument('--receipt',required=True);a=p.parse_args();here=Path(__file__).resolve().parent;base=here.parent;root=next(x for x in here.parents if (x/'verl').is_dir() and (x/'exps').is_dir());receipt=json.loads(Path(a.receipt).read_text());seal=base/'technical-config-seal.json'
assert receipt.get('approved') and receipt.get('lane')==a.lane and receipt.get('technical_config_seal_sha256')==sha(seal),'Root receipt must bind lane and current seal'
predecessor=root/'work/experiments/night-20261010/cloud-continued/tmp2/results/304-instruct-full-matched-guard128.json'
assert a.lane=='tmp2' and predecessor.exists() and json.loads(predecessor.read_text())['returncode']==0,'Exact matched evaluation must finish successfully first'
assert receipt.get('predecessor_result_sha256')==sha(predecessor),'Root receipt must bind completed matched evaluation'
ready=json.loads((root/'work/experiments/night-20261010/cloud-continued'/a.lane/'ready.json').read_text());assert os.uname().nodename==ready['hostname'];assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'Retained GPU already occupied'
sealed=json.loads(seal.read_text());assert all(sha(root/k)==v for k,v in sealed['sha256'].items());export=json.loads(Path(sealed['full_sft_export_audit']).read_text());assert export['passed'] and export['checkpoint']==sealed['model']
assert export.get('manifest') and all(Path(k).resolve().is_relative_to(root) and sha(k)==v for k,v in export['manifest'].items()),'Full-SFT export artifacts drifted after audit'
launch=base/'technical-launch.json';assert not launch.exists();report=dict(state='running',lane=a.lane,hostname=os.uname().nodename,root_receipt_sha256=sha(a.receipt),started=time.time());launch.write_text(json.dumps(report,indent=2)+'\n');env=os.environ.copy();env.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false',NVIDIA_TF32_OVERRIDE='0',PYTHONUNBUFFERED='1')
try:
 for name in ['step1','resume-step2']:
  config=base/'technical-configs'/(name+'.json');assert receipt['config_sha256'][name]==sha(config)
  cfg=json.loads(config.read_text());assert cfg['lane']==a.lane
  subprocess.run([sys.executable,'-m','torch.distributed.run','--standalone','--nproc_per_node=8',str(here/'train.py'),'--config',str(config),'--smoke'],cwd=root,env=env,check=True)
  cfg=json.loads(config.read_text());assert cfg['lane']==a.lane;run=Path(cfg['output']);result=json.loads((run/'result.json').read_text());assert result['completed'];rows=[json.loads(l) for l in (run/'metrics.jsonl').read_text().splitlines()];metrics=[m for row in rows for m in row['ranks']];assert len(metrics)==8
  assert all(m['trainable']>=4_000_000_000 and m['optimizer_step'] and m['backbone_update_l2']>0 and m['max_replay_logp_drift']<=.01 and m['mean_replay_logp_drift']<=.002 and m['p95_replay_logp_drift']<=.005 for m in metrics)
  if name=='resume-step2':
   assert all(m['resume_proof'] and all(m['resume_proof'].get(k) for k in ['exact_local_adam_state','exact_cpu_rng','exact_cuda_rng','exact_python_rng']) for m in metrics),'Exact resume identity proof missing'
  assert not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip(),'GPU process remains after NCCL/launcher exit'
 report.update(state='passed',finished=time.time(),passed=True)
except BaseException as e:
 report.update(state='failed',finished=time.time(),passed=False,error=repr(e));raise
finally:launch.write_text(json.dumps(report,indent=2)+'\n')
