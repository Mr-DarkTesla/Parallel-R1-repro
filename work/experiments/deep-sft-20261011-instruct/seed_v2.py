"""Preserved-raw seed export for new revision; original ledger never modified."""
from pathlib import Path
import collections,hashlib,json,re,time
from transformers import AutoTokenizer
b=Path('work/experiments/deep-sft-20261011-instruct');old=Path('work/experiments/deep-sft-20261010');out=b/'production-v2';out.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tasks={r['id']:r for r in map(json.loads,(old/'candidate-pool.jsonl').read_text().splitlines())}
receipts={(r['id'],r['attempt']):r for r in map(json.loads,(b/'first128-rechecked/receipts.jsonl').read_text().splitlines())}
original={r['id']:r for r in map(json.loads,(b/'production/journal.jsonl').read_text().splitlines())}
excluded={'synthetic-layered-dag-v1/2026104114':'Independent substantive review: stage prose update count off by one.'}
selected={}
for r in map(json.loads,(b/'production/teacher-responses.jsonl').read_text().splitlines()):
    receipt=receipts[r['id'],r['attempt']]
    if receipt['passed'] and r['id'] not in excluded:
        selected.setdefault(r['id'],(r,receipt))
        original_row=original[r['id']].get('row',{})
        if original_row and original_row.get('raw_response')==r['response']['choices'][0]['message']['content']:
            selected[r['id']]=(r,receipt)
p=Path('work/experiments/instruct-token-warmup-20261010')
tok=AutoTokenizer.from_pretrained(p/'variants/lr-1e-3/runs/production/final',local_files_only=True);system=(p/'system.txt').read_text()
records=[];rows=[]
for id,orig in original.items():
    record=dict(id=id,source=tasks[id]['source'],started_at=orig['started_at'],finished_at=orig['finished_at'],seed_from_preserved_raw=True,original_decision=orig['decision'])
    if id not in selected:
        record.update(decision='rejected',error='independent_substantive_quarantine' if id in excluded else 'repaired_checks_no_valid_attempt',attempts=orig['attempts'],quarantine_reason=excluded.get(id));records.append(record);continue
    raw,c=selected[id];text=raw['response']['choices'][0]['message']['content'];item=tasks[id]
    def compact(m):
        body=m[1];ix=body.index('<Path>');ps=re.findall(r'<Path>.*?</Path>',body,re.S)
        assert not re.sub(r'<Path>.*?</Path>','',body[ix:],flags=re.S).strip()
        return '<Parallel>'+body[:ix]+''.join(ps)+'</Parallel>'
    response=re.sub(r'<Parallel>(.*?)</Parallel>',compact,text,flags=re.S)
    reasoning,answer=response.rsplit('Final Answer:',1);content='<think>\n'+reasoning.rstrip()+'\n</think>\nFinal Answer:'+answer
    messages=[dict(role='system',content=system),dict(role='user',content=item['question'])]
    full=tok.apply_chat_template(messages+[dict(role='assistant',content=content)],tokenize=False,enable_thinking=True);tokens=len(tok.encode(full,add_special_tokens=False));assert tokens<=8192
    path_tokens=[len(tok.encode(m[1],add_special_tokens=False)) for m in re.finditer(r'<Path>[1-8]\n([\s\S]*?)</Path>',text)]
    row=dict(id=id,source=item['source'],problem=item['question'],answer=item['reference'],response=content,assistant_content=content,raw_response=text,prompt_messages=json.dumps(messages),split_group=item['split_group'],fork_count=c['shape']['rounds'],branch_schedule=c['shape']['widths'],student_tokens=tokens,source_file=item['source_file'],source_row_index=item['source_row_index'],source_metadata={k:v for k,v in item.items() if k.startswith('source_')},metrics=dict(rounds=c['shape']['rounds'],widths=c['shape']['widths'],path_tokens=path_tokens,output_tokens=len(tok.encode(text,add_special_tokens=False)),sequential_tokens=len(tok.encode(re.sub(r'<Path>[1-8]\n[\s\S]*?</Path>','',text),add_special_tokens=False)),critical_path_tokens_proxy=len(tok.encode(re.sub(r'<Path>[1-8]\n[\s\S]*?</Path>','',text),add_special_tokens=False))+sum(max(path_tokens[sum(c['shape']['widths'][:i]):sum(c['shape']['widths'][:i+1])]) for i in range(c['shape']['rounds']))),round_dependencies=c['relations']['round_dependencies'],verification=dict(final_answer=c['grade'],explicit_arithmetic=c['arithmetic'],oracle_replay=c['oracle'],source_relations=c['relations']),teacher_model='deepseek-v4.1-flash',reasoning_effort=50,prompt_sha256=sha(b/'teacher-prompt.txt'),serialization_version='qwen3-instruct-think-parallel-v2',raw_response_sha256=c['raw_response_sha256'],release_status='quarantine pending final independent review',reviewed_trace_preserved=(orig.get('row',{}).get('raw_response')==text),selected_attempt=raw['attempt'])
    record.update(decision='accepted',row=row,attempts=[dict(attempt=raw['attempt'],output=text,source_relations=c['relations'])]);records.append(record);rows.append(row)
(out/'journal.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
(out/'seed-accepted.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
manifest=dict(original_tasks=len(original),seed_accepted=len(rows),seed_rejected=len(records)-len(rows),exclusions=excluded,teacher_calls=0,hashes={str(p):sha(p) for p in [b/'production/journal.jsonl',b/'production/teacher-responses.jsonl',b/'first128-rechecked/receipts.jsonl',out/'journal.jsonl',out/'seed-accepted.jsonl']},status='staged no new teacher requests')
(out/'seed-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
