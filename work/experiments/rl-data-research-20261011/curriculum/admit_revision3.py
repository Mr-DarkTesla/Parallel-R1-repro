"""Assemble a new admitted dataset only after independent final-snapshot evidence."""
import argparse,json,hashlib,shutil,collections
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--oracle-receipt',required=True);ap.add_argument('--source-receipt',required=True);args=ap.parse_args()
D=Path('work/experiments/rl-instruct-20261011/data/revision3')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
snapshot=json.load(open(D/'candidate-snapshot-sha256.json'))
for p,digest in snapshot.items():
 if p=='generator':p='work/experiments/rl-instruct-20261011/data/generate_revision3.py'
 assert sha(p)==digest,(p,'snapshot changed')
contam=json.load(open(D/'contamination-audit.json'));parser=json.load(open(D/'actual-parser-preflight.json'))
assert contam['passed'] and parser['passed']
for p in [args.oracle_receipt,args.source_receipt]:
 receipt=json.load(open(p));assert receipt.get('passed') is True,(p,'independent receipt not passed')
 # A receipt must bind both entire full-split snapshots, rather than approve a code fragment.
 bound=receipt.get('inputs_sha256',receipt.get('input_sha256',receipt.get('candidate_sha256',{})))
 assert isinstance(bound,dict),(p,'hash-binding map required')
 for split in ['train','val']:
  source=str(D/'full1024'/(split+'.candidate.jsonl'));digest=snapshot[source]
  assert digest in bound.values(),(p,source,'not bound')
for phase in ['stage256','full1024']:
 target=D/phase
 data={split:[json.loads(x) for x in open(target/(split+'.candidate.jsonl'))] for split in ['train','val']}
 tf={r['split_group'] for r in data['train']};vf={r['split_group'] for r in data['val']};assert not(tf&vf)
 for split in ['train','val']:
  p=str(target/(split+'.candidate.jsonl'));assert contam['inputs_sha256'][p]==snapshot[p] and parser['inputs_sha256'][p]==snapshot[p]
  shutil.copyfile(p,target/(split+'.jsonl'))
 # Keep the previously admitted pilot frozen, and bind its unchanged bytes without copying it.
 pilot=Path('work/experiments/rl-instruct-20261011/data/revision2/pilot.jsonl')
 manifest={'passed':True,'revision':3,'phase':phase,'train':len(data['train']),'val':len(data['val']),'pilot':16,'train_sha256':sha(target/'train.jsonl'),'val_sha256':sha(target/'val.jsonl'),'pilot_path':str(pilot),'pilot_sha256':sha(pilot),'group_disjoint':True,'math_all_train_test_excluded':True,'reserved_aime_excluded':True,'current_sft_excluded':True,'frozen_pilot_excluded':True,'independent_exact_oracle_all_rows':True,'reference_parser_compatible':True,'source':'original_exact_math_generator','different_data_arm':True,'train_family_count':len(tf),'val_family_count':len(vf),'source_counts':{split:dict(collections.Counter(r['template_family'] for r in rows)) for split,rows in data.items()},'evidence_sha256':{str(p):sha(p) for p in [args.oracle_receipt,args.source_receipt,D/'contamination-audit.json',D/'actual-parser-preflight.json',D/'generation-manifest.json',D/'candidate-snapshot-sha256.json']},'generator_sha256':snapshot['generator'],'benchmark_selection':False,'family_answer_prior_risks':json.load(open(D/'answer-prior-audit.json')),'long_run_admitted':False,'long_run_requires':'Current4Btrainpilot k-of4/8: reject if groups almostalluniformlycorrect/incorrect orreasoningtoo short; protectedMATH/AIMEqualityfloor independentlychecked','difficulty_status':'Not established by exact gold or nominal parameters; requires actual current4B family-stratified rollouts','fairness_limit':'Different original procedural mathematics data arm, not reward-only comparison with cached BigMath','overfitting_risks':['Only8trainingtemplatefamilies; parameter variants are structural clones within training','500stepsx32prompts/1024rows=15.625data passes; curriculum expansion alone does not eliminate overfitting'],'split_generalization_limit':'Literal template families are disjoint; recurrence, coefficient and linear-algebra algorithms overlap across splits; not unseen mathematical concepts','decontamination_limit':'Original source independence plus exact/normalized/numbermasked and wordtrigram filtering; not proof against all semantic textbook equivalences'}
 (target/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:manifest[k] for k in ['passed','phase','train','val','train_sha256','val_sha256']},indent=2))
