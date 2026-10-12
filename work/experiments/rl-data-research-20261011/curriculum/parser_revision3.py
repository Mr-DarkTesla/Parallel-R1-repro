import json,hashlib,importlib.util
from pathlib import Path
D=Path('work/experiments/rl-instruct-20261011/data/revision3')
p=Path('work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py')
sp=importlib.util.spec_from_file_location('actual',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);assert m.check()==13
cases=[];inputs={}
for path in D.glob('*/*.candidate.jsonl'):
 inputs[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
 for r in map(json.loads,open(path)):
  grade=m.grade('Final Answer: \\boxed{'+r['answer']+'}',r['answer']);cases.append({'id':r['id'],'path':str(path),'pass':grade['correct'] and grade['valid'] and grade['error'] is None})
proof={'passed':all(c['pass'] for c in cases),'inputs_sha256':inputs,'scorer_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'contracttests':13,'cases':cases,'limitation':'Parser selfequivalence only; independent oracle/source validation separate'}
(D/'actual-parser-preflight.json').write_text(json.dumps(proof,indent=2))
contam=json.load(open(D/'contamination-audit.json'));contam['inputs_sha256']=inputs;(D/'contamination-audit.json').write_text(json.dumps(contam,indent=2))
print(proof['passed'],len(cases))
