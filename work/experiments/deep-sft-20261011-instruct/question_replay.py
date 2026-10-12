"""Secondary exact replay parsed from source question prose, without oracle-source."""
from pathlib import Path
import collections,hashlib,json,re
b=Path('work/experiments/deep-sft-20261011-instruct/production-v3')
rows=[json.loads(s)['row'] for s in (b/'journal.jsonl').read_text().splitlines() if json.loads(s)['decision']=='accepted']
rule=re.compile(r'Stage (\d+), ([A-Za-z]+): take (\d+) times the previous-stage amount of ([A-Za-z]+), add the previous-stage amount of ([A-Za-z]+), then (add|subtract) (\d+)\.')
failures=[];receipts=[];relations=0
for row in rows:
    try:
        question=row['problem'];intro=question.split('Stage 1,',1)[0]
        values={name:int(value) for name,value in re.findall(r'([A-Za-z]+) has (\d+)',intro)};assert len(values) in (3,4,5)
        initial=values.copy();rules=collections.defaultdict(list)
        for stage,name,coefficient,a,c,op,offset in rule.findall(question):rules[int(stage)].append((name,int(coefficient),a,c,op,int(offset)))
        assert sorted(rules)==list(range(1,len(rules)+1)) and len(rules) in (3,4,5)
        expected={f'{name}_0':value for name,value in initial.items()}
        for stage,layer in sorted(rules.items()):
            assert len(layer)==len(values) and {x[0] for x in layer}==set(values)
            next_values={name:coefficient*values[a]+values[c]+(offset if op=='add' else -offset) for name,coefficient,a,c,op,offset in layer}
            expected.update({f'{name}_{stage}':value for name,value in next_values.items()});values=next_values;relations+=len(layer)
        query=question.split('After the final stage, what is ',1)[1]
        terms=re.findall(r'the amount of ([A-Za-z]+)|(\d+) times the amount of ([A-Za-z]+)',query)
        assert len(terms)==len(values)
        answer=sum(values[name] if name else int(weight)*values[other] for name,weight,other in terms)
        assert answer==int(row['answer'])
        proved=row['verification']['source_relations']['receipts']
        assert all(expected[r['label']]==r['result'] for r in proved)
        assert {r['label'] for r in proved}=={k for k in expected if not k.endswith('_0')}
        receipts.append(dict(id=row['id'],question_sha256=hashlib.sha256(question.encode()).hexdigest(),source_nodes=sum(map(len,rules.values())),answer=answer,raw_response_sha256=hashlib.sha256(row['raw_response'].encode()).hexdigest()))
    except (AssertionError,KeyError,ValueError,IndexError) as e:failures.append(dict(id=row['id'],error=repr(e)))
report=dict(checked_rows=len(rows),passed=len(receipts),failures=failures,source_relations_recomputed=relations,oracle_source_used=False,
            method='Exact integer stage simulation from the original question sentences; matched to saved relation receipts and final reference.',
            limitations='Secondary artifact audit, not independent reviewer narrative admission; source prose grammar is restricted to this synthetic generator.')
(b/'question-replay-report.json').write_text(json.dumps(report,indent=2)+'\n')
(b/'question-replay-receipts.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in receipts))
print(json.dumps(report,indent=2))
