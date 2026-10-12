"""Exact computational replay and explicit known heldout/input coverage inventory."""
from pathlib import Path
import collections, hashlib, json, re, unicodedata
import pandas as pd

P=Path.cwd();B=P/'work/experiments/deep-sft-20261010'
def norm(s):return ' '.join(re.findall('[a-z0-9]+',unicodedata.normalize('NFKC',s).lower()))
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
pool=[json.loads(l) for l in (B/'candidate-pool.jsonl').open()]
oracles={r['id']:r for r in map(json.loads,(B/'oracle-source.jsonl').read_text().splitlines())}
assert len(pool)==len(oracles)==7500 and {r['id'] for r in pool}==oracles.keys()
maximum=0;all_nodes=0
for r in pool:
    o=oracles[r['id']];prev=o['initial'];n=len(prev)
    for layer in o['stages']:
        assert {x['parents'][0] for x in layer}==set(range(n))
        values=[]
        for x in layer:
            a,b=x['parents'];value=x['coefficient']*prev[a]+prev[b]+(x['offset'] if x['offset_sign']=='+' else -x['offset'])
            assert x['operands']==[prev[a],prev[b]] and x['result']==value>0
            values.append(value);all_nodes+=1;maximum=max(maximum,value)
        prev=values
    answer=sum(x*w for x,w in zip(prev,o['final_weights']))
    assert prev==o['final_values'] and answer==o['answer']==int(r['reference'])
    assert hashlib.sha256(r['question'].encode()).hexdigest()==r['question_sha256']==o['question_sha256']
    maximum=max(maximum,answer)
    expected_group=hashlib.sha256(json.dumps(o['graph'],sort_keys=True).encode()).hexdigest()
    assert expected_group==r['split_group']

inputs={};missing=[];unknown=[]
for m in sorted((P/'work/experiments').glob('*/evaluations/*/manifest.json')):
    data=json.loads(m.read_text());q=data.get('fixed_questions')
    if not q:unknown.append(str(m));continue
    f=Path(q)
    if not f.exists():missing.append(str(f));continue
    inputs.setdefault(str(f),dict(kind='fixed_eval_questions',sha256=sha(f),manifests=[]))
    inputs[str(f)]['manifests'].append(str(m))
old=json.loads((B/'attempts/01-opcount-only-prescreen/pool-manifest.json').read_text())
for name,expected in old['source_hashes'].items():
    f=Path(name)
    if not f.exists():missing.append(name);continue
    assert sha(f)==expected,(f,'immutable exclusion input changed')
    if f.suffix=='.parquet':inputs[name]=dict(kind='cached_heldout_parquet',sha256=expected)
    elif f.name.startswith('accepted'):inputs[name]=dict(kind='previous_train_acceptance',sha256=expected)
questions=set();ids=set()
for name,metadata in inputs.items():
    f=Path(name);rows=pd.read_parquet(f).to_dict('records') if f.suffix=='.parquet' else [json.loads(l) for l in f.open()]
    count=0
    for r in rows:
        if 'id' in r:ids.add(r['id'])
        q=r.get('problem',r.get('question'))
        if q is None:
            pr=r.get('prompt',[])
            q='\n'.join(x['content'] for x in pr if isinstance(x,dict))
        if q:questions.add(norm(str(q)));count+=1
    metadata['rows_with_question']=count
overlap_ids=ids&{r['id'] for r in pool};overlap_problems=questions&{norm(r['question']) for r in pool}
assert not overlap_ids and not overlap_problems
report=dict(passed=not missing and not unknown,oracle_replay_passed=True,listed_input_screening_passed=True,
    known_eval_coverage_status='pass' if not missing and not unknown else 'pending',
    source='independently-generated-layered-arithmetic-v1',candidates=7500,oracle_nodes_replayed=all_nodes,
    all_answers_replayed=True,all_intermediates_exact_and_positive=True,all_nodes_reachable_to_requested_answer=True,max_node_or_answer=maximum,
    contamination_known_ids=len(ids),contamination_normalized_questions=len(questions),exact_id_overlap=0,exact_problem_overlap=0,
    exclusion_inventory=inputs,missing_exclusion_inputs=missing,manifests_without_fixed_questions_field=unknown,
    hashes={f.name:sha(f) for f in [B/'candidate-pool.jsonl',B/'pilot-tasks.jsonl',B/'oracle-source.jsonl',B/'pool-manifest.json']},
    split_group_definition='Graph parents, +/- choices, final merge weights, and story topic; excludes initial values/coefficient/offset. Not a graph-isomorphism invariant.',
    limitation='Explicit listed heldouts screened exactly; semantic resemblance or unlisted legacy artifacts are not proven absent. Synthetic source is not MATH-derived.')
(B/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='exclusion_inventory'},indent=2))
