"""CPU-only, final hash-bound deep data admission and native full-response CE preparation."""
from pathlib import Path
import hashlib,json,shutil,sys
P=Path.cwd();B=P/'work/experiments/instruct-deep-full-20261011'
cfg=json.loads((B/'plan.json').read_text());old=Path(cfg['source_namespace']);init=Path(cfg['init_checkpoint'])
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for x in iter(lambda:f.read(8*1024*1024),b''):h.update(x)
 return h.hexdigest()
admission=json.loads(Path(cfg['data_admission']).read_text())
assert admission['passed'] and admission['manifest_sha256']==sha(cfg['data_manifest'])
assert admission['train_sha256']==sha(cfg['train_jsonl']) and admission['val_sha256']==sha(cfg['val_jsonl'])
assert admission['train_count']==2700 and admission['val_count']==300 and admission['group_disjoint']
model=json.loads((init/'config.json').read_text());assert model['hidden_size']==2560 and model['num_hidden_layers']==36 and model['model_type']=='qwen3'
assert not (B/'prepare-proof.json').exists()
shutil.copytree(old/'code',B/'code',ignore=shutil.ignore_patterns('__pycache__','*.pyc','._*'))
for name in ['compiler.py','system.txt']:shutil.copy2(old/name,B/name)
shutil.copy2(B/'sft_qwen3_4b_instruct_deep.yaml',B/'code/verl/trainer/config/sft_qwen3_4b_instruct_deep.yaml')
sys.path.insert(0,str(B));from compiler import build_sample
import pandas as pd
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained(init,local_files_only=True);assert tok.eos_token=='<|im_end|>'
system=(B/'system.txt').read_text();data=B/'data';data.mkdir();splits={};ids={}
for split,count in [('train',2700),('val',300)]:
 rows=[]
 for line in Path(cfg[split+'_jsonl']).open():
  raw=json.loads(line);assert raw['assistant_content'].startswith('<think>')
  assert raw.get('response',raw['assistant_content'])==raw['assistant_content']
  messages=json.loads(raw['prompt_messages']) if isinstance(raw['prompt_messages'],str) else raw['prompt_messages']
  assert messages[0]==dict(role='system',content=system)
  sample=build_sample(raw,tok,system,cfg['max_length']);n=len(sample['input_ids']);start=sample['prompt_length']
  assert not any(sample['target_mask'][:start]) and all(sample['target_mask'][start:])
  rows.append(dict(id=raw['id'],problem=raw['problem'],answer=str(raw['answer']),assistant_content=raw['assistant_content'],total_tokens=n,source_record_json=json.dumps(raw,ensure_ascii=False)))
 assert len(rows)==count and len({r['id'] for r in rows})==count
 frame=pd.DataFrame(rows);frame.to_parquet(data/(split+'.parquet'),index=False)
 frame.nlargest(16,'total_tokens').to_parquet(data/('smoke-'+split+'.parquet'),index=False)
 ids[split]={r['id'] for r in rows};splits[split]=dict(count=count,max_compiled_tokens=max(r['total_tokens'] for r in rows),min_compiled_tokens=min(r['total_tokens'] for r in rows))
assert ids['train'].isdisjoint(ids['val'])
sys.path.insert(0,str(B/'code'))
from verl.utils.parallel_structure import layout
import torch
tags=tuple(tok.encode(v,add_special_tokens=False)[0] for v in ['<Parallel>','</Parallel>','<Path>','</Path>'])
eligible=False
for raw in pd.read_parquet(data/'smoke-train.parquet').to_dict('records'):
 sample=build_sample(raw,tok,system,cfg['max_length']);_,blocks=layout(torch.tensor(sample['input_ids']),sample['prompt_length'],tags,tok.pad_token_id)
 eligible=eligible or any(len(block)>=3 for block in blocks)
assert eligible,'Longest16 smoke train lacks >=3 sibling isolation fixture'
# Native compiler and proven shifted loss mask remain byte-for-byte inherited.
# Add epoch validation observations; optimizer/scheduler remain uninterrupted.
trainer=B/'code/verl/trainer/fsdp_parallel_sft_trainer.py';text=trainer.read_text()
needle='            # save checkpoint\n            self.save_checkpoint(step=global_step)'
replacement='''            if rank == 0:
                import json
                with open(os.path.join(self.config.trainer.default_local_dir, 'epoch-validation.jsonl'), 'a') as f:
                    f.write(json.dumps(dict(epoch=epoch+1, step=global_step, clean_validation_ce=val_loss, selection_source='teacher-holdout300-fullresponseCE'))+'\\n')
            # save checkpoint
            self.save_checkpoint(step=global_step)'''
assert text.count(needle)==1;trainer.write_text(text.replace(needle,replacement))
paths=list((B/'code').rglob('*.py'))+list((B/'code').rglob('*.yaml'))+[Path(cfg[k]) for k in ['data_manifest','data_admission','train_jsonl','val_jsonl']]+list(data.glob('*.parquet'))+[B/'compiler.py',B/'dataset.py',B/'system.txt',trainer]+list(init.glob('*.json'))+list(init.glob('*.jinja'))+list(init.glob('*.safetensors'))
proof=dict(passed=True,init_checkpoint=str(init),init_rationale=cfg['init_rationale'],splits=splits,full_response_CE=True,native_eos=tok.eos_token,mask_prompt_pad_zero=True,structured_attention=True,repeated_positions=True,manifest={str(p):sha(p) for p in paths})
(B/'prepare-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items() if k!='manifest'},indent=2))
