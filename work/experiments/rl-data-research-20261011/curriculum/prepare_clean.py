import collections,glob,hashlib,json,random,re,unicodedata
from pathlib import Path
import pandas as pd

ROOT=Path('${PROJECT_ROOT}')
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
selected=[];rejected=[];seen=[];stats=collections.Counter()
for source in ['cn_k12','orca_math']:
 indices=list(f.index[f.source==source]);random.Random(20261011).shuffle(indices);accepted=0
 for i in indices:
  r=f.loc[i];q=str(r.prompt);a=str(r.solution).strip();reason=None
  if re.search(r'(?i)\baime\b|\bamc\b|olympiad|aops|artofproblemsolving|hendrycks|\bMATH[- ](?:500|dataset)',q):reason={'kind':'identifiable_benchmark_provenance'}
  elif re.search(r'(?i)https?://|!\[|\b(?:figure|diagram|pictured|graph below|prove that|show that|options|multiple.choice)\b',q):reason={'kind':'not_self_contained_or_proof'}
  elif not a or a.lower() in ['proof','none','nan'] or len(q)>5000:reason={'kind':'bad_answer_or_length'}
  else:reason=overlap(q)
  g=grams(q)
  if not reason:
   for oldg in seen:
    if g and len(g&oldg)/len(g|oldg)>=0.5:reason={'kind':'candidate_family_nearmatch'};break
  if reason:stats[reason['kind']]+=1;rejected.append({'source':source,'row':int(i),**reason});continue
  family=hashlib.sha256(masked(q).encode()).hexdigest();seen.append(g)
  selected.append({'id':f'bigmath/{source}/{i}','problem':q,'answer':a,'source':source,'source_repository':'open-r1/Big-Math-RL-Verified-Processed','source_revision':'c79efbb6d3b75e3a2bcc27a5c569119918132345','source_file':str(p.relative_to(ROOT)),'source_row_index':int(i),'source_file_sha256':source_digest,'domain':list(r.domain),'family_sha256':family,'split_group':family,'provenance_limit':'Original per-item URL unavailable in published source; semantic review required'})
  accepted+=1
  if accepted==80:break
 assert accepted==80,(source,accepted)
train=selected[:64]+selected[80:144];val=selected[64:80]+selected[144:160];pilot=train[:8]+train[64:72]
for name,rows in [('train',train),('val',val),('pilot',pilot),('first128-review',train)]:
 (OUT/f'{name}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
(OUT/'rejections.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rejected))
manifest={'passed':False,'train':128,'val':32,'pilot':16,'train_sha256':sha(OUT/'train.jsonl'),'val_sha256':sha(OUT/'val.jsonl'),'pilot_sha256':sha(OUT/'pilot.jsonl'),'group_disjoint':not({r['split_group'] for r in train}&{r['split_group'] for r in val}),'math_all_train_test_excluded':True,'reserved_aime_excluded':True,'reserved_aime_inventory':inventory,'sources_sha256':sources,'source_whitelist':['cn_k12','orca_math'],'benchmark_source_quarantine':'All non-whitelisted BigMath source categories excluded including math,amc_aime,harp,aops_forum,olympiads,omnimath; identifiable benchmark text rejected all years','excluded_rows':len(exclusions),'rejections':dict(stats),'filters':'normalized exact, numbermasked exact, numbermasked wordtrigram Jaccard>=0.5 against MATH12500,currentSFT3000,AIME2024/2025; same near-match threshold across all160selected candidates','selection':'seed20261011 shuffled source-balanced; no model solve-rate or benchmark accuracy selection','blockers':['Independent first128 source/answer/semantic near-match review pending','AIME2025 I/II numbered inventory cross-check pending'],'limits':['No original per-item URL in BigMath whitelist; absence of semantic paraphrase cannot be proven by lexical filters'],'benchmark_usage':'exclusion only; final evaluation-only'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:v for k,v in manifest.items() if k not in ['sources_sha256','reserved_aime_inventory']},indent=2))
