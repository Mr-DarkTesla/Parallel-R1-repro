"""Fresh exact-oracle GSM-style DAGs; every stage is naturally wide and needed."""
from pathlib import Path
import collections, hashlib, json, random, re, unicodedata

P=Path.cwd();B=P/'work/experiments/deep-sft-20261010';SEED=2026101001
TOPICS=[
    ('production lines','completed units',['Aster','Birch','Cedar','Dahlia','Elm','Fir']),
    ('warehouses','packages',['North','South','East','West','Central','Harbor']),
    ('account ledgers','credit units',['Amber','Blue','Coral','Denim','Emerald','Flint']),
    ('greenhouse sections','seed packets',['Apple','Basil','Carrot','Dill','Endive','Fennel']),
    ('game teams','score points',['Eagles','Foxes','Hawks','Lynx','Owls','Ravens']),
    ('processing stations','items',['Alpha','Beta','Gamma','Delta','Epsilon','Zeta']),
]
def norm(s):return ' '.join(re.findall('[a-z0-9]+',unicodedata.normalize('NFKC',s).lower()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
evals=set()
for f in (P/'work/experiments').glob('*/evaluations/*/manifest.json'):
    v=json.loads(f.read_text());q=Path(v.get('fixed_questions',''))
    if q.is_file():
        for l in q.open():
            r=json.loads(l);evals.add(norm(r.get('problem',r.get('question',''))))
old=[P/'exps/deepseek-gsm-wide3000-v2-20261009/production/accepted.jsonl',P/'exps/deepseek-gsm-only-20261009/production/accepted-at-user-stop.jsonl']
for f in old:
    if f.exists():
        for l in f.open():evals.add(norm(json.loads(l)['problem']))
source=[];oracle=[];seen=set()
for index in range(7500):
    rng=random.Random(SEED+index)
    # Exact 25/50/25 width and 20/60/20 stage distributions in each block of 100.
    width=[3]*25+[4]*50+[5]*25;stages=[3]*20+[4]*60+[5]*20
    batch=rng.randrange(100);n=width[batch];depth=stages[(37*batch+index)%100]
    topic,units,available=TOPICS[index%len(TOPICS)];names=rng.sample(available,n)
    initial=[rng.randint(3,15) for _ in range(n)];values=initial[:];layers=[];equations=[]
    for s in range(1,depth+1):
        primary=list(range(n));rng.shuffle(primary)
        secondary=primary[1:]+primary[:1]
        layer=[];next_values=[]
        for i in range(n):
            a,b=primary[i],secondary[i];k=rng.choice([1,2,2,3]);offset=rng.randint(1,5);sign=rng.choice(['+','+','-'])
            if sign=='-':offset=min(offset,k*values[a]+values[b]-1)
            value=k*values[a]+values[b]+(offset if sign=='+' else -offset)
            assert value>0
            layer.append(dict(node=i,parents=[a,b],coefficient=k,offset=offset,offset_sign=sign,operands=[values[a],values[b]],result=value))
            equations.append(f'Stage {s}, {names[i]}: take {k} times the previous-stage amount of {names[a]}, add the previous-stage amount of {names[b]}, then {"add" if sign=="+" else "subtract"} {offset}.')
            next_values.append(value)
        assert {x['parents'][0] for x in layer}==set(range(n))
        layers.append(layer);values=next_values
    # Last-stage weighted sum sometimes introduces nontrivial final merge.
    weights=[rng.choice([1,1,2]) for _ in range(n)];answer=sum(x*w for x,w in zip(values,weights))
    intro=(f'A coordinator maintains {units} for {n} {topic}: {", ".join(names)}. '
        f'There are {depth} simultaneous update stages. Initially, '+', '.join(f'{name} has {v}' for name,v in zip(names,initial))+'. '
        'Every update rule below uses only the amounts after the preceding stage, or the initial amounts at stage 1. '
        'All amounts for a stage are updated simultaneously: never use another amount from that same stage. '
        'These rules define the entire process; there are no other changes.\n\n')
    query='After the final stage, what is '+ ' + '.join((f'the amount of {name}' if w==1 else f'{w} times the amount of {name}') for name,w in zip(names,weights))+'?'
    q=intro+'\n'.join(equations)+'\n\n'+query
    key=norm(q);assert key not in evals and key not in seen;seen.add(key)
    graph=dict(width=n,stages=depth,parents=[[x['parents'] for x in layer] for layer in layers],operators=[[x['offset_sign'] for x in layer] for layer in layers],final_weights=weights,topic=index%len(TOPICS))
    group=hashlib.sha256(json.dumps(graph,sort_keys=True).encode()).hexdigest()
    ident=f'synthetic-layered-dag-v1/{SEED+index}'
    row=dict(id=ident,source='Synthetic_Layered_DAG_Arithmetic',source_file=str(B/'oracle-source.jsonl'),source_row_index=index,
        question=q,core_problem=q,reference=str(answer),source_dataset='independently-generated-layered-arithmetic-v1',source_revision=sha(Path(__file__)),
        op=3*n*depth+n-1,d=depth,length=len(q),mode='forward_layered',template=topic,question_sha256=hashlib.sha256(q.encode()).hexdigest(),split_group=group,
        reachable_dag_width=n,reachable_dag_stages=depth)
    source.append(row);oracle.append(dict(id=ident,initial=initial,names=names,stages=layers,final_values=values,final_weights=weights,answer=answer,graph=graph,question_sha256=row['question_sha256']))
# Pilot balanced jointly: width mean4, stages mean4, 20%3/60%4/20%5 stages.
pilot=[]
for n,depth,count in [(3,3,5),(3,4,5),(4,3,5),(4,4,20),(4,5,5),(5,4,5),(5,5,5)]:
    options=[r for r in source if r['reachable_dag_width']==n and r['reachable_dag_stages']==depth]
    assert len(options)>=count
    pilot.extend(options[:count])
assert len(pilot)==50 and len({r['id'] for r in pilot})==50
random.Random(SEED).shuffle(source);random.Random(SEED+1).shuffle(pilot)
for name,rows in [('candidate-pool.jsonl',source),('pilot-tasks.jsonl',pilot),('oracle-source.jsonl',oracle)]:
    f=B/name;assert not f.exists(),f;f.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
report=dict(candidates=len(source),pilot=50,source='NEW independently generated GSM-style layered arithmetic, not GSM-Infinite or MATH-derived',
    oracle='Exact integer Python evaluation of every node and final weighted sum',
    width_histogram=dict(collections.Counter(r['reachable_dag_width'] for r in source)),stages_histogram=dict(collections.Counter(r['reachable_dag_stages'] for r in source)),
    pilot_width_histogram=dict(collections.Counter(r['reachable_dag_width'] for r in pilot)),pilot_stages_histogram=dict(collections.Counter(r['reachable_dag_stages'] for r in pilot)),
    pilot_true_width_mean=sum(r['reachable_dag_width'] for r in pilot)/50,pilot_true_stages_mean=sum(r['reachable_dag_stages'] for r in pilot)/50,
    all_nodes_reachable=True,all_stage_amounts_updated_simultaneously=True,all_nodes_computational=True,known_eval_or_old_train_normalized_questions=len(evals),
    exact_normalized_question_overlap=0,generator_sha256=sha(Path(__file__)),seed=SEED,
    pool_sha256=sha(B/'candidate-pool.jsonl'),pilot_sha256=sha(B/'pilot-tasks.jsonl'),oracle_sha256=sha(B/'oracle-source.jsonl'),
    limitations=['New synthetic distribution; it is not evidence of broader mathematical generalization.','Exact normalized contamination screening does not prove absence of semantic resemblance.','Teacher may choose fewer/more rounds; measure actual traces, do not substitute oracle stages for executed trace rounds.'])
(B/'pool-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
