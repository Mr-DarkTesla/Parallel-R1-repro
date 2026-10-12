"""Actual tiny Qwen: four per-prompt groups accumulated equals combined gradient/update."""
import copy,json
from pathlib import Path
import torch
from transformers import Qwen3Config,Qwen3ForCausalLM
torch.set_num_threads(1);torch.manual_seed(731)
c=Qwen3Config(vocab_size=128,hidden_size=32,intermediate_size=64,num_hidden_layers=2,num_attention_heads=2,num_key_value_heads=1,head_dim=16,attention_dropout=0.,pad_token_id=0);c._attn_implementation='sdpa'
a=Qwen3ForCausalLM(c);b=copy.deepcopy(a);oa=torch.optim.AdamW(a.parameters(),lr=1e-5,foreach=False);ob=torch.optim.AdamW(b.parameters(),lr=1e-5,foreach=False)
x=torch.randint(1,128,(16,7));rewards=torch.tensor([[0.,1.,.2,.3],[.9,.9,.9,.9],[1.,0.,1.,0.],[.2,.7,.8,.1]])
adv=(rewards-rewards.mean(dim=1,keepdim=True)).flatten();assert torch.allclose(adv.reshape(4,4).sum(1),torch.zeros(4),atol=1e-6)
max_gradient=0.;max_update=0.
for step in range(2):
 oa.zero_grad();ob.zero_grad()
 for slot in range(4):
  q=a(x[slot*4:(slot+1)*4]).logits[:,:-1];lp=q.log_softmax(-1).gather(-1,x[slot*4:(slot+1)*4,1:,None]).squeeze(-1)
  (-lp*adv[slot*4:(slot+1)*4,None]).sum().div(7*4*4).backward()
 q=b(x).logits[:,:-1];lp=q.log_softmax(-1).gather(-1,x[:,1:,None]).squeeze(-1);(-lp*adv[:,None]).sum().div(7*16).backward()
 delta=max(float((p.grad-r.grad).abs().max()) for p,r in zip(a.parameters(),b.parameters()));max_gradient=max(max_gradient,delta);assert delta<1e-6
 oa.step();ob.step();delta=max(float((p-r).abs().max()) for p,r in zip(a.parameters(),b.parameters()));max_update=max(max_update,delta);assert delta<1e-6
report=dict(passed=True,steps=2,model='actual tiny Qwen3 CPU',prompts_per_rank=4,rollouts_per_prompt=4,global_prompt_batch_at8ranks=32,global_response_batch_at8ranks=128,historical_response_batch=256,within_prompt_centering=True,zero_advantage_prompt_preserved=True,optimizer_updates=2,max_gradient_delta=max_gradient,max_parameter_delta=max_update,actual_8GPU_memory_proof_pending=True)
Path(__file__).with_name('cpu-accumulation-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
