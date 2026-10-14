"""CPU exact visibility/GQA proof; no CUDA allocation or FlashAttention speed claim."""
from pathlib import Path
import importlib.util,json,sys,time
import torch
from torch.nn import functional as F
R=Path('${PROJECT_ROOT}');O=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013'
S=Path(json.loads((O/'cloud-submission.json').read_text())['current_run_root']);P=O/'candidate-flash-varlen-decode'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
a=load('old_dag',S/'src/dag_backend.py');b=load('new_dag',P/'src/dag_backend.py')
torch.manual_seed(42);torch.set_num_threads(1);maximum=0.;cases=0
for width in [1,2,3,4,6,8,16,32]:
 for variant in range(3):
  lengths=[3+(i*17+variant*11)%97 for i in range(width)];rows=[];nextslot=1
  for i,n in enumerate(lengths):
   # Shared prefixes across rows, independent append writes; slot0 is padding.
   reads=tuple(range(nextslot,nextslot+n));nextslot+=n
   write=(nextslot,);nextslot+=1
   rows.append((reads,write,torch.ones(1,n+1,dtype=torch.bool),i,i+1))
  old=a.DAGMetadata(tuple(a.DAGRow(*x) for x in rows),width).prepare('cpu')
  new=b.DAGMetadata(tuple(b.DAGRow(*x) for x in rows),width).prepare('cpu');assert new.decode_only
  store=torch.randn(2,nextslot,2,8,dtype=torch.float64);store[:,0]=0
  q=torch.randn(width,8,8,dtype=torch.float64)
  dense=F.scaled_dot_product_attention(q[:,None].transpose(1,2),store[0][old.physical_indices].transpose(1,2),store[1][old.physical_indices].transpose(1,2),attn_mask=old.allowed_mask,dropout_p=0.,is_causal=False,enable_gqa=True).transpose(1,2)[:,0]
  packedk=store[0].index_select(0,new.flat_physical_indices);packedv=store[1].index_select(0,new.flat_physical_indices);result=[]
  for i,(start,end) in enumerate(zip(new.cu_seqlens_k.tolist(),new.cu_seqlens_k.tolist()[1:])):
   result.append(F.scaled_dot_product_attention(q[i][None,None].transpose(1,2),packedk[start:end][None].transpose(1,2),packedv[start:end][None].transpose(1,2),dropout_p=0.,is_causal=False,enable_gqa=True).reshape(8,8))
  delta=float((dense-torch.stack(result)).abs().max());maximum=max(maximum,delta);assert delta<1e-12;cases+=1
  assert new.flat_physical_indices.tolist()==[x for row in rows for x in row[0]+row[1]]
  # Any inaccessible sibling key forces the unchanged mask-aware path.
  masked=rows.copy();r=masked[0];mask=r[2].clone();mask[0,0]=False;masked[0]=(*r[:2],mask,*r[3:])
  fallback=b.DAGMetadata(tuple(b.DAGRow(*x) for x in masked),width).prepare('cpu');reference=a.DAGMetadata(tuple(a.DAGRow(*x) for x in masked),width).prepare('cpu')
  assert not fallback.decode_only and torch.equal(fallback.allowed_mask,reference.allowed_mask) and torch.equal(fallback.physical_indices,reference.physical_indices)
d=dict(passed=True,CPU_only=True,cases=cases,widths=[1,2,3,4,6,8,16,32],ragged_GQA_max_abs=maximum,exact_read_slot_order=True,masked_sibling_fallback_exact=True,CUDA_or_flash_kernel_NOT_tested=True,no_speed_claim=True,time=time.time())
(P/'CPU-VISIBILITY-PROOF.json').write_text(json.dumps(d,indent=2));print(json.dumps(d))
