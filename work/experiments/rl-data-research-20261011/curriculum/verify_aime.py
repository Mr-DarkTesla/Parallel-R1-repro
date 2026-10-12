from pathlib import Path
import pandas as pd,json,re,hashlib
b=Path('work/experiments/rl-instruct-20261011/data')
p=next(b.glob('benchmark-cache/datasets--allenai--aime-2022-2025/snapshots/*/data/*.parquet'))
f=pd.read_parquet(p);rows=f[f.year.astype(str)=='2025'].to_dict('records')
keys=[(re.search(r'AIME_(II|I)_',r['url']).group(1),int(re.search(r'Problem_(\d+)',r['url']).group(1))) for r in rows]
assert len(rows)==30 and set(keys)=={(exam,n) for exam in ['I','II'] for n in range(1,16)}
original=[json.loads(x) for x in open(b/'aime2025.raw.jsonl')]
def fix(q):
 q=q.replace('\\\x0crac','\\frac').replace('\\\x08egin','\\begin')
 q=re.sub(r'\s+','',q)
 q=q.replace('\\frac','rac').replace('\\right','ight').replace('\\ight','ight')
 return q
a={fix(r['problem']):r for r in rows};matched=[]
for r in original:
 k=fix(r['problem']);assert k in a,(r['id'],r['problem'][:50]);assert int(r['answer'])==int(a[k]['answer'])
 matched.append({'mathai_id':r['id'],'url':a[k]['url'],'answer':str(r['answer'])})
proof={'passed':True,'year':2025,'count':30,'numbered_inventory':keys,'cross_source_matched':30,'mathai_revision':'563bb8404243c5f09de6ec262f2db674fe5bce9b','allenai_revision':'73e1eba765ad5847cdb5d1e2e7aaf7b22b585798','allenai_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'matches':matched,'normalization':'remove whitespace and fix known formfeed-corrupted frac in AllenAI copy only'}
(b/'aime2025-inventory-proof.json').write_text(json.dumps(proof,indent=2))
m=json.load(open(b/'manifest.json'));m['reserved_aime_inventory']['2025']['numbered_inventory_proof_sha256']=hashlib.sha256((b/'aime2025-inventory-proof.json').read_bytes()).hexdigest();m['blockers']=[x for x in m['blockers'] if 'AIME2025' not in x];(b/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('AIME2025 cross-source 30/30 numbered I/II passed')
