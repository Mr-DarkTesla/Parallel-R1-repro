"""Resume drained v2 without new forwards, keeping every original trace intact."""
from pathlib import Path
import hashlib,importlib.util,json
from style_check import check
b=Path('work/experiments/deep-sft-20261011-instruct');old=b/'production-v2';out=b/'production-v3'
state=json.loads((old/'status.json').read_text());assert state['inflight']==0 and state['state']=='stopped',state
spec=importlib.util.spec_from_file_location('v','exps/deepseek-gsm-wide3000-v2-20261009/validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[];accepted=[];exclusions=[]
for r in map(json.loads,(old/'journal.jsonl').read_text().splitlines()):
    if r['decision']=='accepted':
        row=r['row'];text=row['raw_response'];s=v.validate(text);matches=list(v.BLOCK.finditer(text));blocks=[dict(x,start=m.start(),end=m.end()) for x,m in zip(s['blocks'],matches)]
        style=check(text,blocks)
        if style['failures']:
            exclusions.append(dict(id=r['id'],raw_response_sha256=hashlib.sha256(text.encode()).hexdigest(),findings=style['failures']))
            r=dict(r,decision='rejected',error='drafting_or_serial_prefork_quarantine',quarantined_row=row,style_check=style);r.pop('row')
        else:
            row=dict(row,verification=dict(row['verification'],style_check=style),student_tokens_native_fulltemplate=row['student_tokens'],release_status='quarantine pending final whole-dataset admission')
            r=dict(r,row=row);accepted.append(row)
    records.append(r)
out.mkdir(exist_ok=True)
(out/'journal.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
(out/'seed-accepted.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in accepted))
(out/'seed-style-exclusions.json').write_text(json.dumps(exclusions,indent=2)+'\n')
manifest=dict(original_tasks=len(records),seed_accepted=len(accepted),seed_rejected=len(records)-len(accepted),new_teacher_calls=0,style_exclusions=exclusions,hashes={str(p):sha(p) for p in [old/'journal.jsonl',old/'teacher-responses.jsonl',out/'journal.jsonl',out/'seed-accepted.jsonl',out/'seed-style-exclusions.json']},status='staged root release pending; original immutable')
(out/'seed-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
