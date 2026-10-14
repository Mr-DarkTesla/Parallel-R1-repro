"""Preserve pilot provenance and count its accepted new examples toward 3000."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'production';OUT.mkdir(exist_ok=True)
assert json.loads((ROOT/'pilot-status.json').read_text())['state']=='complete'
assert not (OUT/'journal.jsonl').exists()
results=[json.loads(l) for l in ((ROOT/'reviewed-pilot-results.jsonl') if (ROOT/'reviewed-pilot-results.jsonl').exists() else (ROOT/'pilot-results.jsonl')).read_text().splitlines()];assert len(results)==60
tasks={r['id']:r for r in map(json.loads,(ROOT/'pilot-tasks.jsonl').read_text().splitlines())};prompt=(ROOT/'prompt-wide-explicit.txt').read_text();student=(ROOT/'student-system.txt').read_text()
base_hashes={r['id']:r['prompt_sha256'] for r in map(json.loads,(ROOT/'pilot-teacher-raw.jsonl').read_text().splitlines())}
verify_hashes={r['id']:r['prompt_sha256'] for r in map(json.loads,(ROOT/'verification-pilot-teacher-raw.jsonl').read_text().splitlines())}
records=[]
for r in results:
 item=tasks[r['id']];record={'id':r['id'],'source':'GSM_Infinite','started_at':r['started_at'],'finished_at':r['finished_at'],'decision':'accepted' if r['accepted'] else 'rejected','pilot':True,'pilot_result_reference':str(ROOT/'pilot-results.jsonl'),'structure':r.get('structure'),'grade':r.get('grade'),'judge':r.get('judge')}
 if r['accepted']:
  shape=r['structure'];messages=[{'role':'system','content':student},{'role':'user','content':item['question']},{'role':'assistant','content':r['output']}]
  record['row']=dict(id=r['id'],source='GSM_Infinite',source_file=item['source_file'],source_row_index=item['source_row_index'],source_metadata={k:item[k] for k in ['source_dataset','source_revision','original_source_file','original_source_row_index','old_branch_schedule','op','length','mode','template','d','question_conventions_version'] if k in item},problem=item['question'],answer=item['reference'],response=r['output'],messages=messages,prompt_messages=json.dumps(messages[:-1],ensure_ascii=False),split_group=item['split_group'],fork_count=shape['rounds'],branch_schedule=shape['widths'],student_tokens=r['student_tokens'],teacher_model='deepseek-v4.1-flash',reasoning_effort=50,prompt_sha256=(verify_hashes if r.get('review_origin')=='verification-prompt-correction' else base_hashes)[r['id']],production_prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),student_system_sha256=hashlib.sha256(student.encode()).hexdigest(),serialization_version='counted-forks-v1',verification={'final_answer':'Math-Verify 0.8.0','structure':True,'semantic_judge':r['judge']})
 else:record['error']=r.get('error','semantic_judge_reject')
 records.append(record)
assert len({r['id'] for r in records})==60
(OUT/'journal.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
(OUT/'concurrency.json').write_text(json.dumps({'concurrency':256})+'\n')
print({'pilot_accepted_seeded':sum(r['accepted'] for r in results),'new_total_target':3000})
