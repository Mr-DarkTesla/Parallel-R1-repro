from pathlib import Path
import hashlib,json,math
from safetensors import safe_open
import torch
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';init=P/'work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final';out=B/'runs/smoke/final'
metrics=[json.loads(s) for s in (B/'runs/smoke/metrics.jsonl').read_text().splitlines()];assert len(metrics)==2 and all(math.isfinite(r['loss']) and math.isfinite(r['grad_norm']) and r['transformer_update_l2']>0 for r in metrics)
old=json.loads((init/'model.safetensors.index.json').read_text())['weight_map'];new=json.loads((out/'model.safetensors.index.json').read_text())['weight_map'];changed=[];count=0
for k in new:
 with safe_open(str(out/new[k]),framework='pt') as f:a=f.get_tensor(k)
 assert torch.isfinite(a).all(),k
 with safe_open(str(init/old[k]),framework='pt') as f:b=f.get_tensor(k)
 different=not torch.equal(a,b);count+=1
 if different:changed.append(k)
assert any('layers.' in k for k in changed)
paths=list(B.glob('*.py'))+list(B.glob('*.sh'))+list((B/'data').glob('*.parquet'))+[B/'system.txt',B/'prepare-proof.json',B/'code/verl/trainer/fsdp_parallel_sft_trainer.py',B/'code/verl/utils/parallel_structure.py']
paths+=list(init.glob('*.json'))+list(init.glob('*.jinja'))+list(init.glob('*.safetensors'))+list(out.glob('*.json'))+list(out.glob('*.jinja'))+list(out.glob('*.safetensors'))
manifest={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
proof=dict(passed=True,tensor_count=count,changed_tensor_count=len(changed),changed_tensors=changed,metrics=metrics,manifest=manifest)
(B/'smoke-export-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items() if k!='manifest'},indent=2))
