import json
from pathlib import Path
import torch
from verl.trainer import fsdp_parallel_sft_trainer as trainer
def audit(self):
 self.fsdp_model.eval()
 ds=self.train_dataset
 from verl.utils.parallel_structure import layout
 for chosen in range(len(ds.rows)):
  sample=ds[chosen];valid=sample['attention_mask'].bool();n=int(valid.sum());ids=sample['input_ids'][:n];pos=sample['position_ids'][:n];start=int(sample['prompt_length'])
  _,blocks=layout(ids,start,ds.tags,ds.tokenizer.pad_token_id)
  eligible=[b for b in blocks if len(b)>=3]
  if eligible:spans=eligible[0];break
 else:raise ValueError('No >=3 sibling isolation fixture in compiled smoke set')
 first=spans[0];third=spans[2];changed=ids.clone();perturb=first[0]+3
 assert perturb<first[1] and ids[perturb] not in ds.tags
 replacement=ds.tokenizer.encode('different',add_special_tokens=False)[0]
 assert replacement!=ids[perturb];changed[perturb]=replacement
 allowed=ds.generate_parallel_thinking_reasponse_mask(ids,start)
 mask=torch.zeros(allowed.shape,dtype=torch.float32).masked_fill_(~allowed,-torch.inf)[None,None].cuda()
 device_pos=pos[None].cuda()
 def forward(tokens):
  with torch.no_grad(),torch.autocast('cuda',dtype=torch.bfloat16):
   output=self.fsdp_model(input_ids=tokens[None].cuda(),attention_mask=mask,position_ids=device_pos,use_cache=False)
  isolated=output.logits[0,third[0]:third[1]].float().cpu();suffix=output.logits[0,spans[-1][1]].float().cpu();del output
  return isolated,suffix
 a,sa=forward(ids);b,sb=forward(changed)
 diff=float((a-b).abs().max());suffix=float((sa-sb).abs().max())
 assert diff<=1e-5,('Sibling leak',diff)
 assert suffix>0,('Perturbation ineffective',suffix)
 proof=dict(passed=True,sibling_logits_max_abs_diff=diff,merged_suffix_max_abs_diff=suffix,perturbed_index=perturb,compared_third_span=third,source_id=ds.rows[chosen]['id'],actual_full_fsdp_model=True,rank=torch.distributed.get_rank())
 if torch.distributed.get_rank()==0:(Path(self.config.trainer.default_local_dir)/'isolation-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
 torch.distributed.barrier()
trainer.FSDPParallelThinkingSFTTrainer.fit=audit
if __name__=='__main__':trainer.main()
