import json
from pathlib import Path
from rollout import execute,TAGS
from train import instruct_prefix,format_flags
class Tok:
 pad_token_id=0
 tags={t:1000+i for i,t in enumerate(TAGS+['</think>'])}
 def encode(self,text,add_special_tokens=False):return [self.tags[text]] if text in self.tags else [ord(c)+1 for c in text]
 def decode(self,ids,skip_special_tokens=False):
  rev={v:k for k,v in self.tags.items()};return ''.join(rev[x] if x in rev else chr(x-1) for x in ids)
 def apply_chat_template(self,messages,**kw):
  assert kw==dict(tokenize=False,add_generation_prompt=True,enable_thinking=True);return 'USER\n<think>'
t=Tok();assert t.decode(instruct_prefix(t,[])).endswith('<think>\n');records=[]
for width in [2,3,4,6,8]:
 plan='Plan:\n'+''.join(f'{i}: compute\n' for i in range(1,width+1));script=[('main',t.encode(plan)+t.encode('<Parallel>')),('width',t.encode(str(width)+'\n'))]
 script += [('path',t.encode('X')+[999])]*width
 script += [('summary',t.encode('Merged.')+t.encode('</Summary>')),('main',t.encode('</think>')),('main',t.encode('\nFinal Answer: 2')+[999])]
 def dec(call,budget,stops):
  phase,raw=script.pop(0);assert phase==call['phase'];assert not set(raw)&set(call['blocked_token_ids'])
  if phase=='main' and len(script)==0:assert call['blocked_token_ids']==[t.tags[x] for x in TAGS]
  return raw,[-1.]*len(raw),len(raw)
 trace=execute(t,instruct_prefix(t,[]),dec,[999]);assert not script
 assert format_flags(trace['output'],trace['stats'])==(True,True)
 for c in trace['policy_calls']:
  start=c['response_start'];assert all(trace['response_mask'][start:start+len(c['generated_ids'])])
  if c['phase']=='path':assert c['generated_ids'][-1]==999 and trace['response_ids'][start+len(c['generated_ids'])-1]==t.tags['</Path>']
 assert trace['stats']['forced_tokens']>0 and sum(trace['response_mask'])==sum(len(c['generated_ids']) for c in trace['policy_calls'])
 records.append(dict(width=width,raw_replaced_stop_preserved=True,forced_headers_mask0=True,thinking_close_sampled=True,postthink_guard=True,physical_forwards=trace['stats']['actual_model_forward_calls']))
Path(__file__).with_name('cpu-contract-proof.json').write_text(json.dumps(dict(passed=True,cases=records),indent=2)+'\n');print(json.dumps(dict(passed=True,cases=len(records))))
