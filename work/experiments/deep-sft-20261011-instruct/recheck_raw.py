"""CPU-only new checker receipts; frozen journals and raw responses stay intact."""
from pathlib import Path
import collections,hashlib,importlib.util,json,re
from arithmetic_check_v2 import check as arithmetic
from oracle_check_v4 import check as oracle_check
from relation_check_v2 import check as relation_check
b=Path('work/experiments/deep-sft-20261011-instruct');source=Path('work/experiments/deep-sft-20261010')
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
v=module('v','exps/deepseek-gsm-wide3000-v2-20261009/validate.py')
scorer=module('scorer','exps/math500-new-sft-20261008/score.py')
oracles={r['id']:r for r in map(json.loads,(source/'oracle-source.jsonl').read_text().splitlines())}
tasks={r['id']:r for r in map(json.loads,(source/'candidate-pool.jsonl').read_text().splitlines())}
rows=[];selected={}
for r in map(json.loads,(b/'production/teacher-responses.jsonl').read_text().splitlines()):
    choice=r['response']['choices'][0];text=choice['message'].get('content') or ''
    shape=v.validate(text);blocks=shape.pop('blocks');matches=list(v.BLOCK.finditer(text))
    blocks=[dict(x,start=m.start(),end=m.end()) for x,m in zip(blocks,matches)]
    o=oracle_check(text,oracles[r['id']],blocks);a=relation_check(text,oracles[r['id']],blocks);ar=arithmetic(text);grade=scorer.grade(text,tasks[r['id']]['reference'])
    exact=all(text.count('<'+tag+'>')==text.count('</'+tag+'>')==count for tag,count in [('Parallel',shape['rounds']),('Summary',shape['rounds']),('Path',sum(shape['widths']))])
    passed=bool(shape['valid'] and exact and choice['finish_reason']=='stop' and '<think>' not in text and '</think>' not in text and grade['correct'] and not grade['error'] and not ar['mismatches'] and not o['failures'] and not a['failures'])
    receipt=dict(id=r['id'],attempt=r['attempt'],passed=passed,raw_response_sha256=hashlib.sha256(text.encode()).hexdigest(),shape=shape,oracle=o,relations=a,arithmetic=ar,grade=grade,exact_xml=exact)
    rows.append(receipt)
    if passed:selected.setdefault(r['id'],receipt)
out=b/'first128-rechecked';out.mkdir(exist_ok=True)
(out/'receipts.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
errors=collections.Counter(f['type'] for x in rows for f in x['oracle']['failures'])
errors.update(f[0] for x in rows for f in x['relations']['failures'])
report=dict(raw_responses=len(rows),unique_tasks=len({x['id'] for x in rows}),accepted_math_canonical=len(selected),accepted_attempts=sum(x['passed'] for x in rows),first_attempt_passed=sum(x['passed'] and x['attempt']==1 for x in rows),failures=dict(errors),selected_attempts={k:v['attempt'] for k,v in selected.items()},excluded_ids=['synthetic-layered-dag-v1/2026104114'],new_teacher_calls=0,release_status='HOLD independent substantive review required')
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='selected_attempts'},indent=2))
