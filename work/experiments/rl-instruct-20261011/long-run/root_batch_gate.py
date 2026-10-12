"""CPU-only automatic engineering release binds independent source and actual predecessor."""
import argparse,json,hashlib,time,os
from pathlib import Path
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for x in iter(lambda:f.read(8*1024*1024),b''):h.update(x)
 return h.hexdigest()
p=argparse.ArgumentParser();p.add_argument('--review',required=True);p.add_argument('--review-sha',required=True);p.add_argument('--seal-sha',required=True);a=p.parse_args();here=Path(__file__).resolve().parent;root=next(x for x in here.parents if (x/'verl').is_dir() and (x/'exps').is_dir());seal=here/'batch-proof-source-seal.json';state=here/'batch-proof-gate-status.json';receipt=here/'batch-proof-root-approved.json'
while True:
 try:
  assert sha(seal)==a.seal_sha and sha(a.review)==a.review_sha;review=json.loads(Path(a.review).read_text());assert review['passed']
  s=json.loads(seal.read_text());assert all(sha(k)==v for k,v in s['sha256'].items());pre=root/s['predecessor_result']
  if pre.exists():
   assert json.loads(pre.read_text())['returncode']==0
   run=here.parent/'production-runs/strong_width-stage16';assert json.loads((run/'result.json').read_text())['completed']
   r=dict(approved=True,batch_proof_source_seal_sha256=sha(seal),predecessor_result_sha256=sha(pre),full_sft_export_audit_sha256=sha(s['full_sft_export_audit']),independent_source_review_sha256=a.review_sha,engineering_only=True)
   tmp=receipt.with_suffix('.tmp');tmp.write_text(json.dumps(r,indent=2)+'\n');os.replace(tmp,receipt);state.write_text(json.dumps(dict(state='released',receipt_sha256=sha(receipt)))+'\n');break
  state.write_text(json.dumps(dict(state='waiting_exact306terminal',pid=os.getpid(),updated=time.time()))+'\n')
 except BaseException as e:
  state.write_text(json.dumps(dict(state='failed',error=repr(e),updated=time.time()))+'\n');raise
 time.sleep(30)
