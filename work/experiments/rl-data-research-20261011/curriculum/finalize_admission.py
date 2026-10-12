import json,hashlib,collections,random,importlib.util
from pathlib import Path
B=Path('work/experiments/rl-instruct-20261011/data');D=B/'revision2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return list(map(json.loads,open(p)))
receipts={};verdict={};rejected=[]
for p in sorted((B/'independent-review').glob('*')):
 if p.suffix not in ['.json','.jsonl']:continue
 if p.suffix=='.jsonl':cases=load(p)
 else:
  d=json.load(open(p));cases=d.get('cases',[])
 if not cases:continue
 receipts[str(p)]=sha(p)
 for r in cases:
  if not r.get('id'):continue
  status=r.get('status',r.get('mathematical_self_containment_verdict'))
  passed=status in ['pass','PASS']
  verdict[r['id']]={'passed':passed,'receipt':str(p),'problem_sha256':r.get('problem_sha256'),'reason':r.get('notes',r.get('independent_derivation_or_reason'))}
  if not passed:rejected.append(r)
rows={}
for name in ['train.jsonl','val.jsonl','replacement-cn_k12.jsonl','replacement-orca_math.jsonl']:
 for r in load(B/name):rows[r['id']]=r
pilot=load(D/'pilot.jsonl');pilotids={r['id'] for r in pilot};admitted=[]
for ident,r in rows.items():
 v=verdict.get(ident)
 if not v or not v['passed'] or ident in pilotids:continue
 assert hashlib.sha256(r['problem'].encode()).hexdigest()==v['problem_sha256'],ident
 r=dict(r);r['answer_review_receipt']=v['receipt'];r['answer_review_reason']=v['reason'];admitted.append(r)
scorer_path=Path('work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py')
spec=importlib.util.spec_from_file_location('actualscorer',scorer_path);scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer);assert scorer.check()==13
parser_cases=[];parser_safe=[]
for r in admitted+pilot:
 result=scorer.grade('Final Answer: \\boxed{'+r['answer']+'}',r['answer'])
 parser_cases.append({'id':r['id'],'correct':result['correct'],'valid':result['valid'],'error':result['error']})
 if result['correct'] and result['valid'] and not result['error']:
  if r['id'] not in pilotids:parser_safe.append(r)
 else:rejected.append({'id':r['id'],'status':'quarantine_parser_self_equivalence','grade':result})
assert all(c['correct'] and c['valid'] and not c['error'] for c in parser_cases if c['id'] in pilotids)
admitted=parser_safe
(D/'reference-parser-preflight.json').write_text(json.dumps({'passed':True,'actual_scorer':str(scorer_path),'scorer_sha256':sha(scorer_path),'cases':parser_cases,'rejected_cases':[c for c in parser_cases if not c['correct'] or not c['valid'] or c['error']],'limitation':'Self equivalence checks parsing, not complete semantic retention of compound gold'},indent=2))
assert len(admitted)>=160,('insufficient independently admitted pool',len(admitted))
random.Random(20261011).shuffle(admitted)
# Keep source/topic spread in selection validation; selection uses source metadata only.
cn=[r for r in admitted if r['source']=='cn_k12'];orca=[r for r in admitted if r['source']=='orca_math']
val=cn[:16]+orca[:16];rest=cn[16:]+orca[16:];random.Random(20261012).shuffle(rest);train=rest[:128]
assert len(train)==128 and len(val)==32
sets=[{r['split_group'] for r in split} for split in [train,val,pilot]]
assert all(not(sets[i]&sets[j]) for i in range(3) for j in range(i))
for name,rs in [('train',train),('val',val),('quarantine',rejected)]:
 (D/(name+'.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in rs))
old=json.load(open(B/'manifest.json'));m={**old,'passed':True,'scope':'independently answer-reviewed source-whitelisted lexical-decontaminated RL curriculum','revision':2,'train':128,'val':32,'pilot':16,'train_sha256':sha(D/'train.jsonl'),'val_sha256':sha(D/'val.jsonl'),'pilot_sha256':sha(D/'pilot.jsonl'),'group_disjoint':True,'all_three_splits_group_disjoint':True,'review_receipts_sha256':receipts,'admitted_pool_excluding_pilot':len(admitted),'quarantined_cases':len({r['id'] for r in rejected}),'blockers':[],'limits':['Original peritem source URLs unavailable in publication; no identifiable benchmark features in manual text plus lexical filter; all semantic paraphrase absence cannot be proven'],'source_counts':{name:dict(collections.Counter(r['source'] for r in rs)) for name,rs in [('train',train),('val',val),('pilot',pilot)]},'reserved_aime_canonical_sha256':sha(B/'reserved-aime2024-2025-canonical.jsonl'),'selection':'source-balanced validation and seeded shuffled independently passing training; no solve-rate/benchmark-based selection'}
(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({k:m[k] for k in ['passed','train','val','pilot','train_sha256','val_sha256','admitted_pool_excluding_pilot','quarantined_cases','source_counts']},indent=2))
