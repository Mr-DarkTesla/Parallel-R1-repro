"""Two-rank CPU actual Qwen Adam parity with moment sharding and state reload."""
import os,json,copy
from pathlib import Path
import torch,torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed.optim import ZeroRedundancyOptimizer
from transformers import Qwen3Config,Qwen3ForCausalLM
rank=int(os.environ['RANK']);dist.init_process_group('gloo');torch.set_num_threads(1);torch.manual_seed(87)
cfg=Qwen3Config(vocab_size=128,hidden_size=32,intermediate_size=64,num_hidden_layers=2,num_attention_heads=2,num_key_value_heads=1,head_dim=16,attention_dropout=0.,pad_token_id=0);cfg._attn_implementation='sdpa'
model=Qwen3ForCausalLM(cfg);reference=copy.deepcopy(model);ddp=DDP(model,gradient_as_bucket_view=True)
opts=dict(lr=1e-5,foreach=False,weight_decay=0.);shard=ZeroRedundancyOptimizer(model.parameters(),optimizer_class=torch.optim.AdamW,**opts);full=torch.optim.AdamW(reference.parameters(),**opts)
for step in range(2):
 x=torch.tensor([[20,21,22+step,23]]);shard.zero_grad(set_to_none=False);full.zero_grad(set_to_none=False)
 ddp(input_ids=x,labels=x).loss.backward();reference(input_ids=x,labels=x).loss.backward();shard.step();full.step()
 delta=max(float((a-b).abs().max()) for a,b in zip(model.parameters(),reference.parameters()));assert delta<1e-7
state=copy.deepcopy(shard.optim.state_dict())
for entry in shard.optim.state.values():
 for value in entry.values():
  if isinstance(value,torch.Tensor):value.zero_()
shard.optim.load_state_dict(state)
x=torch.tensor([[20,21,24,23]]);shard.zero_grad(set_to_none=False);full.zero_grad(set_to_none=False)
ddp(input_ids=x,labels=x).loss.backward();reference(input_ids=x,labels=x).loss.backward();shard.step();full.step()
resume_delta=max(float((a-b).abs().max()) for a,b in zip(model.parameters(),reference.parameters()));assert resume_delta<1e-7
local=sum(v.numel() for entry in shard.optim.state.values() for v in entry.values() if isinstance(v,torch.Tensor));global_states=[None]*dist.get_world_size();dist.all_gather_object(global_states,local)
report=dict(passed=True,rank=rank,steps=2,max_parameter_delta=delta,local_optimizer_state_elements=local,per_rank_state_elements=global_states,full_optimizer_state_elements=sum(v.numel() for entry in full.state.values() for v in entry.values() if isinstance(v,torch.Tensor)),reload_local_state_pass=True,resumed_next_update_delta=resume_delta)
assert local<report['full_optimizer_state_elements'];Path(__file__).with_name(f'cpu-zero1-rank{rank}.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));dist.destroy_process_group()
