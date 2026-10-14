"""Check published closure, original data hashes, AST and configuration invariants."""
import ast,hashlib,json,tarfile,warnings
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 manifest=json.loads((HERE/'input-manifest.json').read_text());count=0
 with tarfile.open(HERE/'source-snapshot.tar.gz') as archive:
  for rel,info in manifest.items():
   if 'published_sha256' not in info:continue
   b=archive.extractfile(rel).read();assert sha(b)==info['published_sha256'],rel
   local=HERE/'snapshot'/rel
   if local.exists():assert local.read_bytes()==b,rel
   with warnings.catch_warnings():
    warnings.simplefilter('ignore',SyntaxWarning)
    if rel.endswith('.py'):ast.parse(b.decode(),filename=rel)
   if rel.endswith('.json'):json.loads(b)
   assert b'hf_' not in b or not __import__('re').search(rb'hf_[A-Za-z0-9]{20,}',b),rel
   assert b'${HOME}' not in b and b'${HOME}' not in b,rel
   count+=1
 progress=json.loads((HERE/'training-progress.json').read_text())
 for label,n,first,last in [('rl50',24,1,50),('rl300',32,51,300),('new_reward_rl150',16,1,150)]:
  ranks={k:v for k,v in progress[label].items() if k.startswith('metrics-rank-')};assert len(ranks)==n
  for v in ranks.values():assert (v['first_step'],v['last_step'],v['accepted'],v['rejected'])==(first,last,last-first+1,0)
 weights=json.loads((HERE/'weights-manifest.json').read_text())['files']['model.safetensors']
 assert weights==progress['rl300']['weights']
 print(json.dumps(dict(passed=True,published_source_files=count,all_rank_optimizer_history_verified=True,rl300_weights_consistent=True)))
if __name__=='__main__':main()
