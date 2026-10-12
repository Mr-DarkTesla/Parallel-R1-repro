import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=next(x for x in HERE.parents if (x/'verl').is_dir() and (x/'exps').is_dir())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(v,indent=2)+'\n');os.replace(tmp,p)
def source_gate():
 seal=HERE/'source-seal.json';r=read(HERE/'source-root-approved.json');assert r['approved'] and r['source_seal_sha256']==sha(seal);s=read(seal);assert all(sha(k)==v for k,v in s['sha256'].items());return s,r
