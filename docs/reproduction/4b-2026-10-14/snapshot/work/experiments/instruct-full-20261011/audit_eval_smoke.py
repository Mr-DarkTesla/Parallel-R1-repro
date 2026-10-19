from pathlib import Path
import json,hashlib,re
from transformers import AutoTokenizer
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';E=B/'evaluations/epoch1-guard-structured-24';summary=json.loads((E/'summary.json').read_text());assert summary['completed']==24 and summary['missing']==0
assert json.loads((E/'worker-exits.json').read_text())==[0]*8
tok=AutoTokenizer.from_pretrained(B/'runs/epoch1/final',local_files_only=True);system=(B/'system.txt').read_text();tags={tok.convert_tokens_to_ids(t) for t in ('<Parallel>','</Parallel>','<Path>','</Path>','<Summary>','</Summary>')};close=tok.encode('</think>',add_special_tokens=False);assert len(close)==1
rows=[json.loads(l) for p in E.glob('traces-*.jsonl') for l in p.read_text().splitlines() if l.strip()];assert len(rows)==24
checks=0;postthink=0;calls=0
for r in rows:
 prefix=tok.apply_chat_template([dict(role='system',content=system),dict(role='user',content=r['problem'])],tokenize=False,add_generation_prompt=True,enable_thinking=True)
 if prefix.endswith('<think>'):prefix+='\n'
 elif not prefix.endswith('<think>\n'):prefix+='<think>\n'
 assert r['prompt_ids']==tok.encode(prefix,add_special_tokens=False),r['id'];checks+=1
 for call in r['trace']['policy_calls']:
  calls+=1;blocked=set(call.get('blocked_token_ids',[]));after=close[0] in call['prompt_ids'][len(r['prompt_ids']):]
  if after:
   assert call['phase']=='main',call['phase'];assert tags<=blocked,('Postthink tags not all blocked',blocked);postthink+=1
  if call['phase']!='main':assert close[0] in blocked,call['phase']
  assert not any(t in blocked for t in call['generated_ids']),('Blocked token sampled',r['id'],call['phase'])
 outside=r['output'].split('</think>',1)[-1] if '</think>' in r['output'] else ''
 assert not re.search(r'</?(?:Parallel|Path|Summary)>',outside),r['id']
assert postthink>0,'No actual postthink guard coverage'
files=[E/'summary.json',E/'scores.jsonl',E/'worker-exits.json',B/'eval-guard-prepared.json',B/'independent-eval-source-review.json',B/'epoch1-export-proof.json',Path(__file__)]
proof=dict(passed=True,completed=24,prefix_exact_matches=checks,policy_calls_checked=calls,actual_postthink_guard_calls=postthink,all_blocked_tokens_absent_from_raw_sampled_calls=True,xml_after_think_close_absent=True,summary=summary,hashes={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(B/'eval-smoke-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items() if k not in ('summary','hashes')},indent=2))
