from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
from compiler import build_sample
import pandas as pd
import torch
class InstructDataset(torch.utils.data.Dataset):
 def __init__(self,parquet_files,tokenizer,config):
  paths=[parquet_files] if isinstance(parquet_files,str) else list(parquet_files)
  self.rows=pd.concat([pd.read_parquet(p) for p in paths]).to_dict('records');self.tokenizer=tokenizer;self.max_length=config.max_length
  self.system=(Path(__file__).parent/'system.txt').read_text()
  self.tags=tuple(tokenizer.encode(t,add_special_tokens=False)[0] for t in ('<Parallel>','</Parallel>','<Path>','</Path>'))
 def __len__(self):return len(self.rows)
 def __getitem__(self,i):
  s=build_sample(self.rows[i],self.tokenizer,self.system,self.max_length);n=len(s['input_ids']);pad=self.max_length-n
  # Trainer mask is indexed at logits: logit j predicts target j+1.
  loss=s['target_mask'][1:]+[0]+[0]*pad
  return dict(input_ids=torch.tensor(s['input_ids']+[self.tokenizer.pad_token_id]*pad),position_ids=torch.tensor(s['position_ids']+[0]*pad),attention_mask=torch.tensor([1]*n+[0]*pad),loss_mask=torch.tensor(loss),prompt_length=torch.tensor(s['prompt_length']))
 def generate_parallel_thinking_reasponse_mask(self,ids,start=0):
  from verl.utils.parallel_structure import attention
  return attention(ids,start,self.tags,self.tokenizer.pad_token_id)
