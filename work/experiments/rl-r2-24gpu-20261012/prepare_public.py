import collections,glob,hashlib,json,random,re,unicodedata
from pathlib import Path
import pandas as pd

ROOT=Path('/home/jovyan/shares/SR004.nfs3/larin/tmp/r1')
OUT=ROOT/'work/experiments/rl-instruct-20261011/data'
OUT.mkdir(exist_ok=True)
B=ROOT/'work/experiments/rl-r2-24gpu-20261012'; D=B/'data'; D.mkdir(parents=True,exist_ok=True)
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
for r in map(json.loads,open(OUT/'reserved-aime2024-2025-canonical.jsonl')):
 exclusions.append(('canonicalAIME/'+r['id'],r['problem']))
for r in map(json.loads,open(OUT/'revision2/pilot.jsonl')):
 exclusions.append(('frozenpilot/'+r['id'],r['problem']))
for r in map(json.loads,open(OUT/'revision2/val.jsonl')):
 exclusions.append(('frozenval/'+r['id'],r['problem']))
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
p=next(ROOT.glob('cache/screen-hf/datasets--open-r1--Big-Math-RL-Verified-Processed/snapshots/c79efbb6d3b75e3a2bcc27a5c569119918132345/all/*.parquet'))
source_digest=sha(p);sources[str(p.relative_to(ROOT))]=source_digest;f=pd.read_parquet(p)

load=lambda p:list(map(json.loads,open(p)))
old=load(OUT/'revision2/train.jsonl');val=load(OUT/'revision2/val.jsonl');pilot=load(OUT/'revision2/pilot.jsonl')
reviewed={r['id']:r for r in load(OUT/'revision4-public/train.jsonl')}
reviewed.update({r['id']:r for r in old})
blocked={r['id'] for r in val+pilot}
blocked.update(r['id'] for r in load(OUT/'revision4-public/val.jsonl') if r['id'] not in {x['id'] for x in old})
quarantine=set()
for directory in [OUT,OUT/'revision4-public']:
 for path in directory.rglob('*quarantine*.jsonl'):
  for r in load(path):
   if r.get('id'):quarantine.add(r['id'])
reviewed={i:r for i,r in reviewed.items() if i not in blocked and i not in quarantine}
assert {r['id'] for r in old} <= reviewed.keys()
seen=[grams(r['problem']) for r in list(reviewed.values())+val+pilot]
selected=[];rejected=[];stats=collections.Counter()
for source in ['cn_k12','orca_math']:
 indices=list(f.index[f.source==source]);random.Random(20261012).shuffle(indices);accepted=0
 for i in indices:
  ident=f'bigmath/{source}/{i}'
  if ident in reviewed or ident in blocked or ident in quarantine:continue
  r=f.loc[i];q=str(r.prompt);a=str(r.solution).strip();reason=None
  if re.search(r'(?i)\baime\b|\bamc\b|olympiad|aops|artofproblemsolving|hendrycks|\bMATH[- ](?:500|dataset)',q):reason={'kind':'benchmark_provenance'}
  elif re.search(r'(?i)https?://|!\[|\b(?:figure|diagram|pictured|graph below|prove that|show that|options|multiple.choice)\b',q):reason={'kind':'not_self_contained'}
  elif not a or a.lower() in ['proof','none','nan'] or not 100<=len(q)<=3000 or len(a)>500:reason={'kind':'answer_or_length'}
  elif source=='orca_math' and (len(re.findall(r'\d+(?:\.\d+)?',q))<4 or len(q)<200):reason={'kind':'too_simple_word_problem'}
  else:reason=overlap(q)
  g=grams(q)
  if not reason:
   for oldg in seen:
    if g and len(g&oldg)/len(g|oldg)>=0.5:reason={'kind':'candidate_family_nearmatch'};break
  if reason:
   stats[reason['kind']]+=1;rejected.append({'source':source,'row':int(i),**reason});continue
  family=hashlib.sha256(masked(q).encode()).hexdigest();seen.append(g)
  selected.append({'id':ident,'problem':q,'answer':a,'source':source,'source_repository':'open-r1/Big-Math-RL-Verified-Processed','source_revision':'c79efbb6d3b75e3a2bcc27a5c569119918132345','source_file':str(p.relative_to(ROOT)),'source_row_index':int(i),'source_file_sha256':source_digest,'domain':list(r.domain),'family_sha256':family,'split_group':family,'reference_review':'pending_gold_blind_teacher','provenance_limit':'Original item URL absent; lexical filtering does not prove absence of all paraphrases'})
  accepted+=1
  if accepted==750:break
 assert accepted==750,(source,accepted)
for name,rows in [('reviewed',list(reviewed.values())),('candidates',selected),('val',val),('pilot',pilot)]:
 (D/(name+'.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in rows))
m=dict(state='candidates',passed=False,target_train=1024,previous_train_preserved=128,reviewed=len(reviewed),candidates=len(selected),source_whitelist=['cn_k12','orca_math'],sources_sha256=sources,protected_questions=len(exclusions),filters=dict(stats),rejections=rejected,benchmark_selection=False,semantic_contamination_absence_proven=False)
(D/'preparation.json').write_text(json.dumps(m,indent=2))
print(json.dumps({k:m[k] for k in ['state','reviewed','candidates','protected_questions']}))
