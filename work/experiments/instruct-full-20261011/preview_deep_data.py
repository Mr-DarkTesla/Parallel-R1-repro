from pathlib import Path
import json,hashlib,sys
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';sys.path.insert(0,str(B));from compiler import build_sample
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained(B/'runs/epoch1/final',local_files_only=True);system=(B/'system.txt').read_text()
D=P/'work/experiments/deep-sft-20261011-instruct/production-v2';files=[D/'seed-accepted.jsonl',D/'accepted-so-far.jsonl'];rows=[];hashes={}
for p in files:
 raw=p.read_bytes();hashes[str(p)]=hashlib.sha256(raw).hexdigest();rows.extend(json.loads(line) for line in raw.decode().splitlines() if line.strip())
raw_count=len(rows);unique={}
for r in rows:
 if r['id'] in unique:assert r['assistant_content']==unique[r['id']]['assistant_content'],r['id']
 unique[r['id']]=r
rows=list(unique.values());lengths=[];reported_matches=0;prompt_system_matches=0;deltas={}
for r in rows:
 s=build_sample(r,tok,system,8192);assert all(s['target_mask'][s['prompt_length']:]);lengths.append(len(s['input_ids']))
 if r.get('student_tokens')==len(s['input_ids']):reported_matches+=1
 if r.get('student_tokens') is not None:
  delta=str(int(r['student_tokens'])-len(s['input_ids']));deltas[delta]=deltas.get(delta,0)+1
 messages=r.get('prompt_messages')
 if isinstance(messages,str):messages=json.loads(messages)
 if messages and messages[0]['role']=='system' and messages[0]['content']==system:prompt_system_matches+=1
proof=dict(passed=True,scope='Preview serialization only; not substantive dataset or training admission',count=len(rows),raw_snapshot_records=raw_count,duplicates_deduplicated=raw_count-len(rows),max_tokens=max(lengths),min_tokens=min(lengths),all_response_tokens_supervised=True,native_think_inside_parallel_contract=True,reported_token_count_matches=reported_matches,reported_minus_compiled_token_deltas=deltas,exact_prompt_system_matches=prompt_system_matches,source_snapshot_hashes=hashes,quarantined=True,training_authorized=False)
(B/'deep-data-preview-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
