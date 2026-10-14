from pathlib import Path
import json,shutil,hashlib,sys
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';D=P/'work/experiments/instruct-token-warmup-20261010'
B.mkdir(exist_ok=True)
init=D/'variants/lr-1e-3/runs/production/final'
cfg=json.loads((init/'config.json').read_text());assert cfg['hidden_size']==2560 and cfg['num_hidden_layers']==36 and cfg['model_type']=='qwen3'
shutil.copytree(P/'work/experiments/base-format-20261010/code',B/'code',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc','._*'))
shutil.copy2(D/'system.txt',B/'system.txt')
compiler=(D/'data.py').read_text().replace('target_mask[start + index] = 0','target_mask[start + index] = 1 # FULL SFT: learn every response token')
(B/'compiler.py').write_text(compiler)
sys.path.insert(0,str(B));from compiler import build_sample
import pandas as pd
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained(init,local_files_only=True);system=(B/'system.txt').read_text()
assert tok.eos_token=='<|im_end|>'
data=B/'data';data.mkdir(exist_ok=True);proof={}
for split,n in [('train',2700),('val',300)]:
 src=P/'exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think'/f'{split}.jsonl';rows=[]
 for line in src.open():
  raw=json.loads(line);s=build_sample(raw,tok,system);assert all(s['target_mask'][s['prompt_length']:]);r={k:raw[k] for k in ('id','problem','answer','assistant_content')};r['answer']=str(r['answer']);r['source_record_json']=json.dumps(raw,ensure_ascii=False);r['total_tokens']=len(s['input_ids']);rows.append(r)
 assert len(rows)==n
 df=pd.DataFrame(rows);df.to_parquet(data/f'{split}.parquet',index=False);df.nlargest(16,'total_tokens').to_parquet(data/f'smoke-{split}.parquet',index=False)
 proof[split]=dict(count=n,min_tokens=int(df.total_tokens.min()),max_tokens=int(df.total_tokens.max()),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest())
assert set(pd.read_parquet(data/'train.parquet').id).isdisjoint(set(pd.read_parquet(data/'val.parquet').id))
trainer=B/'code/verl/trainer/fsdp_parallel_sft_trainer.py';text=trainer.read_text().replace('think_wrapped=False','think_wrapped=True').replace('base_full_proof','instruct_full_proof').replace('base_metrics_step','instruct_metrics_step')
trainer.write_text(text)
proof.update(init_checkpoint=str(init),model_config=cfg,tokenizer_eos=tok.eos_token,full_response_ce=True,think_wrapped=True,structured_attention=True,max_length=8192)
(B/'prepare-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
