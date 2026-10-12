import collections,glob,hashlib,json,random,re,unicodedata
from pathlib import Path
import pandas as pd

ROOT=Path('/home/jovyan/shares/SR004.nfs3/larin/tmp/r1')
OUT=ROOT/'work/experiments/rl-instruct-20261011/data'
OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(q):return ' '.join(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',q).lower()))
def masked(q):return re.sub(r'\d+','NUM',norm(q))
def grams(q):
 w=masked(q).split();return set(zip(w,w[1:],w[2:]))
exclusions=[];sources={}; inventory={}
for p in sorted(ROOT.glob('cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots/*/*/*.parquet')):
 f=pd.read_parquet(p);sources[str(p.relative_to(ROOT))]=sha(p)
 exclusions.extend((str(p.relative_to(ROOT))+':'+str(i),str(q)) for i,q in enumerate(f.problem))
assert len(exclusions)==12500
for split in ['train','val']:
 p=ROOT/f'work/experiments/instruct-full-20261011/data/{split}.parquet';f=pd.read_parquet(p);sources[str(p.relative_to(ROOT))]=sha(p)
 exclusions.extend(('currentSFT/'+str(r.id),str(r.problem)) for r in f.itertuples())
for year in [2024,2025]:
 p=OUT/f'aime{year}.raw.jsonl';rows=[json.loads(x) for x in open(p)];assert len(rows)==30
 assert len({norm(r['problem']) for r in rows})==30
 inventory[str(year)]={'count':30,'sha256':sha(p),'ids':[str(r['id']) for r in rows],'urls':[r.get('url') for r in rows]}
 exclusions.extend((f'AIME{year}/'+str(r['id']),r['problem']) for r in rows)
 if year==2024:
  expected={(exam,n) for exam in ['I','II'] for n in range(1,16)}
  actual={(re.search(r'AIME_(II|I)_',r['url']).group(1),int(re.search(r'Problem_(\d+)',r['url']).group(1))) for r in rows};assert actual==expected
for r in map(json.loads,open(ROOT/'work/experiments/rl-instruct-20261011/data/revision2/pilot.jsonl')):
 exclusions.append(('frozenpilot/'+r['id'],r['problem']))
for r in map(json.loads,open(OUT/'reserved-aime2024-2025-canonical.jsonl')):
 exclusions.append(('canonicalreserved/'+r['id'],r['problem']))
exact={norm(q):i for i,q in exclusions};families={masked(q):i for i,q in exclusions}
gs=[grams(q) for _,q in exclusions];index=collections.defaultdict(list)
for i,g in enumerate(gs):
 for t in g:index[t].append(i)
def overlap(q):
 if norm(q) in exact:return {'kind':'normalized_exact','match':exact[norm(q)]}
 if masked(q) in families:return {'kind':'numbermasked_exact','match':families[masked(q)]}
 g=grams(q)
 if len(g)<5:return None
 counts=collections.Counter(i for t in g for i in index.get(t,[]))
 for i,n in counts.items():
  score=n/len(g|gs[i])
  if score>=0.5:return {'kind':'numbermasked_trigram_jaccard','score':score,'match':exclusions[i][0]}
 return None

D=OUT/"revision3"
case=[]
for phase in ["stage256","full1024"]:
 for split in ["train","val"]:
  seen=set()
  for r in map(json.loads,open(D/phase/(split+".candidate.jsonl"))):
   key=norm(r["problem"]);match=overlap(r["problem"])
   case.append({"id":r["id"],"phase":phase,"split":split,"overlap":match,"duplicate_problem":key in seen})
   seen.add(key)
proof={"passed":not any(r["overlap"] or r["duplicate_problem"] for r in case),"excluded_rows":len(exclusions),"source_hashes":sources,"cases":case,"method":"exactnormalized,numbermaskedexact,wordtrigramJaccard>=0.5 againstallMATH12500currentSFT3000AIME60canonicalAIME60frozenpilot16","source_generation_independence":"Originalgenerator no benchmark inputs; benchmarktextusedonlyforrejection,notgeneration","limitation":"Lexicalauditnotsemanticabsenceproof"}
(D/"contamination-audit.json").write_text(json.dumps(proof,indent=2))
print(proof["passed"],[(r["id"],r["overlap"],r["duplicate_problem"]) for r in case if r["overlap"] or r["duplicate_problem"]][:30])
