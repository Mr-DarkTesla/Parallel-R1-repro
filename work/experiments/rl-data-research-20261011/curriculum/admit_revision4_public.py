import json,hashlib,random,collections,importlib.util
from pathlib import Path
B=Path('work/experiments/rl-instruct-20261011/data');D=B/'revision4-public'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:list(map(json.loads,open(p)))
verdict={};receipts={};quarantined={}
paths=list((B/'independent-review').glob('*.json'))+list((B/'independent-review').glob('*.jsonl'))+list((D/'independent-review').glob('*.json'))+list((D/'independent-review').glob('*.jsonl'))
for p in paths:
 if p.suffix=='.jsonl':cases=load(p)
 else:cases=json.load(open(p)).get('cases',[])
 if not cases:continue
 receipts[str(p)]=sha(p)
 for c in cases:
  if not c.get('id'):continue
  passed=c.get('status',c.get('mathematical_self_containment_verdict')) in ['pass','PASS']
  if passed:verdict[c['id']]={**c,'receipt':str(p)}
  else:quarantined[c['id']]=c
rows={}
for name in ['train','val','replacement-cn_k12','replacement-orca_math']:
 for r in load(B/(name+'.jsonl')):rows[r['id']]=r
for p in D.glob('expansion-*.candidate.jsonl'):
 for r in load(p):rows[r['id']]=r
pilot=load(B/'revision2/pilot.jsonl');pid={r['id'] for r in pilot}
sp=Path('work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py')
spec=importlib.util.spec_from_file_location('actual',sp);scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer);assert scorer.check()==13
admitted={};parser=[]
for ident,r in rows.items():
 c=verdict.get(ident)
 if not c or ident in quarantined or ident in pid:continue
 assert c['problem_sha256']==hashlib.sha256(r['problem'].encode()).hexdigest(),ident
 ref=c.get('answer',c.get('original_answer',c.get('unchanged_answer',c.get('unchangedanswer',r['answer']))));assert ref==r['answer'],ident
 if 'revision4-public' in c['receipt']:
  assert c.get('input_sha256')==sha(D/('expansion-'+r['source']+'.candidate.jsonl')),ident
 result=scorer.grade('Final Answer: \\boxed{'+r['answer']+'}',r['answer']);parser.append({'id':ident,**result})
 if not result['correct'] or not result['valid'] or result['error']:
  quarantined[ident]={'id':ident,'status':'quarantine_actual_parser','grade':result};continue
 admitted[ident]={**r,'answer_review_receipt':c['receipt']}
# Preserve every prior admitted validation question as validation, never move into training.
oldval=load(B/'revision2/val.jsonl');vid={r['id'] for r in oldval};assert vid<=admitted.keys()
new={source:[r for ident,r in admitted.items() if ident not in vid and r['source']==source] for source in ['cn_k12','orca_math']}
for source in new:random.Random(20261014).shuffle(new[source])
val=oldval+new['cn_k12'][:16]+new['orca_math'][:16];vid={r['id'] for r in val}
trainpool={source:[r for ident,r in admitted.items() if ident not in vid and r['source']==source] for source in new}
for source in trainpool:random.Random(20261015).shuffle(trainpool[source])
assert min(map(len,trainpool.values()))>=128,{s:len(x) for s,x in trainpool.items()}
train=trainpool['cn_k12'][:128]+trainpool['orca_math'][:128];random.Random(20261016).shuffle(train)
assert len(train)==256 and len(val)==64
sets=[{r['split_group'] for r in rs} for rs in [train,val,pilot]];assert all(not(sets[i]&sets[j]) for i in range(3) for j in range(i))
for name,rs in [('train',train),('val',val),('quarantine',list(quarantined.values()))]:
 (D/(name+'.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in rs))
(D/'actual-parser-preflight.json').write_text(json.dumps({'passed':True,'actual_scorer_sha256':sha(sp),'cases':parser,'rejected':[r for r in parser if not r['correct'] or not r['valid'] or r['error']]},indent=2))
prep=json.load(open(D/'preparation-manifest.json'));familyaudit=json.load(open(D/'combined-candidate-family-audit.json'));assert familyaudit['passed']
m={'passed':True,'revision':'4-public','train':256,'val':64,'pilot':16,'pilot_path':str(B/'revision2/pilot.jsonl'),'train_sha256':sha(D/'train.jsonl'),'val_sha256':sha(D/'val.jsonl'),'pilot_sha256':sha(B/'revision2/pilot.jsonl'),'group_disjoint':True,'all_three_splits_group_disjoint':True,'prior_validation32_preserved':True,'math_all_train_test_excluded':True,'reserved_aime_excluded':True,'current_sft_excluded':True,'frozen_pilot_excluded':True,'source_whitelist':['cn_k12','orca_math'],'independent_actual_answer_review':True,'reference_parser_compatible':True,'long_run_admitted':False,'long_run_requires':'Current4B family/source/topic rollout k-of4/8 informative and not uniformlycorrect/wrong/too short, plus independent MATH/AIME quality floor','selection':'sourcebalanced random from independently passing rows; no model or benchmark solve-rate selection','review_receipts_sha256':receipts,'preparation_manifest_sha256':sha(D/'preparation-manifest.json'),'candidate_sha256':{str(p):sha(p) for p in D.glob('expansion-*.candidate.jsonl')},'actual_parser_preflight_sha256':sha(D/'actual-parser-preflight.json'),'combined_family_audit_sha256':sha(D/'combined-candidate-family-audit.json'),'admitted_pool_excluding_pilot':len(admitted),'quarantined_cases':len(quarantined),'source_counts':{split:dict(collections.Counter(r['source'] for r in rs)) for split,rs in [('train',train),('val',val)]},'limits':['Original peritem source URLs unavailable; whitelist provenance, lexicalfilter and manual identifiablebenchmark content review do not prove absence of allsemanticparaphrases','Templatefamh keys are normalized numbermaskedquestion; do not imply independent mathematical concepts'],'benchmark_selection':False,'no_jobs_launched':True}
screen=[]
for source in ['cn_k12','orca_math']:
 screen.extend([r for r in train if r['source']==source][:16])
(D/'difficulty-screen32.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in screen))
m['difficulty_screen32_sha256']=sha(D/'difficulty-screen32.jsonl')
m['difficulty_screen_scope']='Fixed sourcebalanced16+16subsettrain; independentlyanswerchecked; noactualmodeldifficultyclaim'
(D/'manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({k:m[k] for k in ['passed','train','val','train_sha256','val_sha256','admitted_pool_excluding_pilot','quarantined_cases']},indent=2))
