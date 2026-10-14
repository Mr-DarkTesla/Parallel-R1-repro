import json
from pathlib import Path
from transformers import AutoTokenizer
from layout import split_solution
r=Path(__file__).resolve().parent;b=r.parent.parent
x=next(x for x in map(json.loads,(r/'reviewed-pilot-results.jsonl').read_text().splitlines()) if x['id']=='gsm_infinite/2881')
t=next(t for t in map(json.loads,(r/'pilot-tasks.jsonl').read_text().splitlines()) if t['id']==x['id'])
tok=AutoTokenizer.from_pretrained(b/'exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final',local_files_only=True)
reason,final=split_solution(x['output']);prompt=[{'role':'system','content':(r/'student-system.txt').read_text()},{'role':'user','content':t['question']}]
prefix=tok.apply_chat_template(prompt,tokenize=False,add_generation_prompt=True);full='<think>\n'+reason+'\n</think>\n\n'+final
for label,seq in [('merged',prefix+(reason+'\n</think>\n\n'+final if prefix.rstrip().endswith('<think>') else full)+tok.eos_token),('full',tok.apply_chat_template(prompt+[{'role':'assistant','content':full}],tokenize=False,add_generation_prompt=False))]:
 a=seq.rsplit('<|im_start|>assistant',1)[1];inside=a.split('<think>',1)[1].split('</think>',1)[0];outside=a.split('</think>',1)[1].strip().removesuffix(tok.eos_token).strip()
 print('prefix-end',repr(prefix[-100:]))
 print(label,'reason equal',inside.strip()==reason,'final equal',outside==final)
 print('reason',repr(reason[:100]),repr(reason[-100:]),'inside',repr(inside[:100]),repr(inside[-100:]))
 print('final',repr(final[:100]),repr(final[-100:]),'outside',repr(outside[:100]),repr(outside[-100:]))
