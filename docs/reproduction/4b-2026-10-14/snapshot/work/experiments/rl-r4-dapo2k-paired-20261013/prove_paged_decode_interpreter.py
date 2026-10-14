"""Run the actual Triton program in CPU interpreter mode, never on CUDA."""
import os
os.environ['TRITON_INTERPRET']='1'
from pathlib import Path
import importlib.util,json,sys,time
import torch
R=Path('${PROJECT_ROOT}');P=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013/candidate-direct-paged-decode'
spec=importlib.util.spec_from_file_location('paged_cpu_interpreter',P/'src/paged_decode_triton.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
torch.set_num_threads(1);torch.manual_seed(23);maximum=0.;cases=0
for rows in [1,2,4,8,32]:
 lengths=[1+(i*31+63)%193 for i in range(rows)];cu=[0];slots=[]
 for n in lengths:slots.extend(torch.randperm(1024)[:n].tolist());cu.append(len(slots))
 q=torch.randn(rows,8,128,dtype=torch.float16);k=torch.randn(1024,2,128,dtype=torch.float16);v=torch.randn_like(k);o=torch.empty_like(q)
 slots=torch.tensor(slots,dtype=torch.long);cu=torch.tensor(cu,dtype=torch.int32)
 m._decode[(rows,2)](q,k,v,slots,cu,o,H=8,HK=2,D=128,GROUP=4,SCALE=128**-.5,BQ=16,BN=64,num_warps=4,num_stages=2)
 reference=[]
 for i,n in enumerate(lengths):
  ix=slots[cu[i]:cu[i+1]];keys=k[ix].repeat_interleave(4,dim=1).float();values=v[ix].repeat_interleave(4,dim=1).float()
  prob=torch.softmax(torch.einsum('hd,nhd->hn',q[i].float(),keys)*128**-.5,dim=-1)
  reference.append(torch.einsum('hn,nhd->hd',prob,values))
 delta=float((o.float()-torch.stack(reference)).abs().max());assert delta<.005,(rows,delta);maximum=max(maximum,delta);cases+=1
d=dict(passed=True,CPU_interpreter_actual_Triton_program=True,cases=cases,widths=[1,2,4,8,32],sparse_physical_slots=True,ragged_lengths_and_64_tile_tails=True,head_size128_GQA4=True,FP16_interpreter_max_abs=maximum,BF16_CUDA_compilation_numerics_performance_NOT_proven=True,no_GPU_test=True,time=time.time());(P/'CPU-KERNEL-INTERPRETER-PROOF.json').write_text(json.dumps(d,indent=2));print(json.dumps(d))
