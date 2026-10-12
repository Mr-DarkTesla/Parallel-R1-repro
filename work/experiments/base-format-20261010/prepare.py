from pathlib import Path
import os,json,hashlib,shutil,datetime,re
P=Path.cwd();B=P/'work/experiments/base-format-20261010';D=P/'work/experiments/instruct-token-warmup-20261010';OLD=P/'work/experiments/night-20261010/sft'
os.environ.update(HF_HOME=str(B/'cache'),HF_HUB_DISABLE_XET='1',TOKENIZERS_PARALLELISM='false')
from huggingface_hub import snapshot_download
pin=json.loads((B/'source-pin.json').read_text());raw=B/'raw'
snapshot_download(pin['model'],revision=pin['revision'],local_dir=raw,allow_patterns=['*.json','*.safetensors','*.txt','*.jinja','README.md'],max_workers=4)
import torch,pandas as pd
from transformers import AutoTokenizer
from safetensors.torch import load_file,save_file
from safetensors import safe_open
torch.set_num_threads(4);model=B/'model';model.mkdir(exist_ok=False);tok=AutoTokenizer.from_pretrained(raw,local_files_only=True)
xml=['<Path>','</Path>','<Parallel>','</Parallel>','<Summary>','</Summary>'];native_len=len(tok);pieces={t:tok.encode(t,add_special_tokens=False) for t in xml};assert tok.add_special_tokens({'additional_special_tokens':xml})==6
cfg=json.loads((raw/'config.json').read_text());assert cfg['model_type']=='qwen3' and cfg['hidden_size']==2560 and cfg['num_hidden_layers']==36 and cfg['tie_word_embeddings'];assert len(tok)<=cfg['vocab_size']
tagids=[tok.convert_tokens_to_ids(t) for t in xml];assert len(set(tagids))==6
changed={};n_tensors=0
for p in raw.glob('model*.safetensors'):
 with safe_open(str(p),framework='pt') as f:keys=list(f.keys());meta=f.metadata()
 n_tensors+=len(keys)
 relevant=[k for k in keys if k.endswith('embed_tokens.weight') or k.endswith('lm_head.weight')]
 if not relevant:shutil.copy2(p,model/p.name);continue
 state=load_file(str(p))
 for k in relevant:
  w=state[k];initial=[]
  for token in xml:initial.append(w[pieces[token]].float().mean(0).to(w.dtype))
  for ix,row in zip(tagids,initial):w[ix]=row
  changed[k]=dict(tag_ids=tagids,rows_sha256=hashlib.sha256(w[tagids].contiguous().view(torch.uint8).numpy().tobytes()).hexdigest(),shape=list(w.shape))
 save_file(state,str(model/p.name),metadata=meta);del state
for p in raw.glob('*.json'):
 if not p.name.startswith('tokenizer'):shutil.copy2(p,model/p.name)
template="{% for message in messages %}{% if message['role'] == 'system' %}Instruction: {{ message['content'] }}\n\n{% elif message['role'] == 'user' %}Problem: {{ message['content'] }}\n\n{% endif %}{% endfor %}{% if add_generation_prompt %}Solution:\n{% endif %}"
tok.chat_template=template;tok.save_pretrained(model);(model/'chat_template.jinja').write_text(template)
# Native Base EOS is kept, no forced think or chat role token injection.
system='''Solve the problem accurately. Organize useful independent calculations with a multiline Plan: using numbered assignments. Then write <Parallel>N with N from 2 through 8 and a newline. Use exactly N numbered paths: <Path>ID followed by a newline, the actual calculation, and </Path>. Paths cannot read siblings. Close with </Parallel><Summary>, combine the computed results and close </Summary>. Continue reasoning or start another useful round if needed. End with Final Answer: \\boxed{the exact result}. Never use <think> or </think>. Do not invent duplicate or empty branches.'''
(B/'system.txt').write_text(system+'\n');data=B/'data';data.mkdir();lengths={};source_sha={}
for split,n in [('train',2700),('val',300)]:
 src=P/'exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think'/f'{split}.jsonl';source_sha[split]=hashlib.sha256(src.read_bytes()).hexdigest();rows=[]
 for l in src.open():
  r=json.loads(l);content=r['assistant_content'];assert content.startswith('<think>\n') and content.count('</think>')==1
  body,final=content[len('<think>\n'):].split('</think>');response=body.rstrip()+'\n\n'+final.strip();assert '<think>' not in response and '</think>' not in response
  # Remove only separators outside sibling path bodies, matching proven isolation compiler.
  def compact(m):
   body=m.group(1);ix=body.index('<Path>');paths=re.findall(r'<Path>.*?</Path>',body,re.S);assert not re.sub(r'<Path>.*?</Path>','',body[ix:],flags=re.S).strip();return '<Parallel>'+body[:ix]+''.join(paths)+'</Parallel>'
  response=re.sub(r'<Parallel>(.*?)</Parallel>',compact,response,flags=re.S)
  messages=[dict(role='system',content=system+'\n'),dict(role='user',content=r['problem'])];prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True);ids=tok.encode(prompt,add_special_tokens=False)+tok.encode(response+tok.eos_token,add_special_tokens=False)
  assert len(ids)<=8192,(r['id'],len(ids));rows.append(dict(id=r['id'],problem=r['problem'],answer=r['answer'],response=response,prompt_messages=json.dumps(messages,ensure_ascii=False),total_tokens=len(ids)))
 assert len(rows)==n;pd.DataFrame(rows).to_parquet(data/f'{split}.parquet',index=False);(data/f'{split}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));pd.DataFrame(rows).nlargest(16,'total_tokens').to_parquet(data/f'smoke-{split}.parquet',index=False);lengths[split]=dict(n=n,max=max(r['total_tokens'] for r in rows),min=min(r['total_tokens'] for r in rows))
assert {r['id'] for r in pd.read_parquet(data/'train.parquet').to_dict('records')}.isdisjoint({r['id'] for r in pd.read_parquet(data/'val.parquet').to_dict('records')})
shutil.copytree(OLD/'code',B/'code',ignore=shutil.ignore_patterns('__pycache__','*.pyc','._*','.git'))
# Retain proven full-model FSDP/Unseen recipe in isolated code; no live sources modified.
report=dict(passed=True,source=pin,old_recipe='Full model FULL_SHARD SFT, not token-row warmup',native_vocab_len=native_len,new_vocab_len=len(tok),model_vocab_size=cfg['vocab_size'],added_tags=dict(zip(xml,tagids)),changed_initial_rows=changed,source_tensor_count=n_tensors,full_model_training=True,no_think=True,prompt_mode='plain Instruction/Problem/Solution, explicit training/inference template',data_lengths=lengths,source_data_sha256=source_sha)
(B/'prepare-proof.json').write_text(json.dumps(report,indent=2)+'\n');print('PREPARED',json.dumps(report),flush=True)
