"""Unified HF weights only, preserve parameter aliases, atomically seal export.
No optimizer or RNG state. Full CPU copies exist only for scheduled export,
never for actor refresh (which exclusively uses CUDA IPC).
"""
from pathlib import Path
import json,os,hashlib,gc

def file_sha(path):
 digest=hashlib.sha256()
 with Path(path).open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''):digest.update(chunk)
 return digest.hexdigest()

def due(step):return step>0 and step%50==0

def export_weights_only(model,tokenizer,output,logical_step,optimizer_update_id,world,*,probe=False):
 import torch
 root=Path(output);name=f'checkpoint-{logical_step:04}' if not probe else f'export-probe-{logical_step:04}';target=root/name;staging=root/(name+'.inprogress')
 assert not target.exists() and not staging.exists();staging.mkdir();hf=staging/'hf';hf.mkdir()
 # Alias-aware CPU state: tied embedding/lm_head must share CPU storage so HF
 # safe serialization emits the canonical unique tensor exactly once.
 canonical={id(p):name for name,p in model.named_parameters(remove_duplicate=True)}
 unique={name:p.detach().cpu().contiguous() for name,p in model.named_parameters(remove_duplicate=True)}
 assert sum(t.numel() for t in unique.values())==4_022_468_096
 assert all(t.dtype==torch.float32 and torch.isfinite(t).all() for t in unique.values())
 state={name:unique[canonical[id(p)]] for name,p in model.named_parameters(remove_duplicate=False)}
 for name,value in model.state_dict().items():
  if name not in state:state[name]=value.detach().cpu().contiguous()
 model.save_pretrained(hf,state_dict=state,safe_serialization=True,max_shard_size='100GB');tokenizer.save_pretrained(hf)
 del state,unique;gc.collect()
 assert (hf/'model.safetensors').exists() and not (hf/'model.safetensors.index.json').exists()
 assert not any('optimizer' in p.name or 'rng' in p.name for p in staging.rglob('*'))
 manifest={str(p.relative_to(staging)):dict(bytes=p.stat().st_size,sha256=file_sha(p)) for p in hf.iterdir() if p.is_file()}
 receipt=dict(step=logical_step,optimizer_update_id=optimizer_update_id,world_size=world,model=True,optimizer=False,rng=False,unsharded=True,weights_only=True,probe=probe,all_master_finite=True,trainable=4_022_468_096,files=manifest)
 (staging/'complete.json').write_text(json.dumps(receipt,indent=2)+'\n');os.replace(staging,target);return receipt

def verify_reload(path):
 """CPU streaming safetensor reload, all unique keys/shapes/dtypes/finite values.
 Reads one tensor at a time; no actor weight refresh and no CPU full model copy.
 """
 import torch
 from safetensors import safe_open
 from transformers import AutoConfig,AutoModelForCausalLM,AutoTokenizer
 from accelerate import init_empty_weights
 path=Path(path);receipt=json.loads((path/'complete.json').read_text());hf=path/'hf';config=AutoConfig.from_pretrained(hf,local_files_only=True)
 with init_empty_weights():model=AutoModelForCausalLM.from_config(config,torch_dtype=torch.float32)
 model.tie_weights();expected={k:tuple(p.shape) for k,p in model.named_parameters(remove_duplicate=True)}
 with safe_open(hf/'model.safetensors',framework='pt',device='cpu') as reader:
  assert set(reader.keys())==set(expected),(set(reader.keys())-set(expected),set(expected)-set(reader.keys()))
  count=0
  for name,shape in expected.items():
   tensor=reader.get_tensor(name);assert tuple(tensor.shape)==shape and tensor.dtype==torch.float32 and torch.isfinite(tensor).all();count+=tensor.numel();del tensor
 assert count==receipt['trainable']==4_022_468_096
 assert file_sha(hf/'model.safetensors')==receipt['files']['hf/model.safetensors']['sha256']
 tokenizer=AutoTokenizer.from_pretrained(hf,local_files_only=True);assert tokenizer.apply_chat_template([dict(role='user',content='test')],tokenize=False,add_generation_prompt=True,enable_thinking=True)
 return dict(passed=True,weights_only=True,unique_parameters=len(expected),elements=count,tensors_reloaded=True,all_finite=True,unified_single_safetensors=True,tokenizer_template_loaded=True,optimizer=False,rng=False)
