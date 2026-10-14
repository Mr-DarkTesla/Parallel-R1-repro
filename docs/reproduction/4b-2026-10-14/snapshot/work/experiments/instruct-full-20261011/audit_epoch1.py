from pathlib import Path
import hashlib,json,math
from safetensors import safe_open
import torch
torch.set_num_threads(4)
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';init=P/'work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final';out=B/'runs/epoch1/final'
result=json.loads((B/'runs/epoch1/result.json').read_text());assert result['state']=='complete' and result['steps']==42 and result['full_model'] and result['think_wrapped']
metrics=[json.loads(s) for s in (B/'runs/epoch1/metrics.jsonl').read_text().splitlines()];assert len(metrics)==42 and all(math.isfinite(r['loss']) and math.isfinite(r['grad_norm']) and math.isfinite(r['transformer_update_l2']) for r in metrics);assert sum(r['transformer_update_l2']>0 for r in metrics)>=38
old=json.loads((init/'model.safetensors.index.json').read_text())['weight_map'];new=json.loads((out/'model.safetensors.index.json').read_text())['weight_map'];changed=[]
for k in new:
 with safe_open(str(out/new[k]),framework='pt') as f:a=f.get_tensor(k)
 assert torch.isfinite(a).all(),k
 with safe_open(str(init/old[k]),framework='pt') as f:b=f.get_tensor(k)
 if not torch.equal(a,b):changed.append(k)
assert any('layers.' in k for k in changed)
paths=list(out.glob('*.json'))+list(out.glob('*.jinja'))+list(out.glob('*.safetensors'))+[B/'runs/epoch1/result.json',B/'runs/epoch1/metrics.jsonl',B/'root-epoch1-approved.json',B/'production-launch-proof.json',Path(__file__)]
manifest={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
proof=dict(passed=True,init_checkpoint=str(init),checkpoint=str(out),tensor_count=len(new),changed_tensor_count=len(changed),changed_tensors=changed,steps=42,validation_loss=result['val_loss'],trainable_parameters=4022468096,positive_update_steps=sum(r['transformer_update_l2']>0 for r in metrics),sample_exposures=2688,source_train_rows=2700,drop_last=True,manifest=manifest)
(B/'epoch1-export-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items() if k not in ('manifest','changed_tensors')},indent=2))
