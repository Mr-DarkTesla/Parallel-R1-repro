"""Compile A100 BF16 kernel without initializing CUDA or executing GPU work."""
from pathlib import Path
import os,sys,json,time,hashlib,importlib.util
R=Path('${PROJECT_ROOT}');P=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013/candidate-direct-paged-decode'
for kind in ['triton','tmp']:(P/'cache/offline'/kind).mkdir(parents=True,exist_ok=True)
os.environ['TRITON_CACHE_DIR']=str(P/'cache/offline/triton');os.environ['TMPDIR']=str(P/'cache/offline/tmp');sys.dont_write_bytecode=True
import torch,triton
from triton.compiler import ASTSource
from triton.backends.compiler import GPUTarget
assert not torch.cuda.is_initialized()
spec=importlib.util.spec_from_file_location('paged_offline',P/'src/paged_decode_triton.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
source=ASTSource(m._decode,signature={'Q':'*bf16','K':'*bf16','V':'*bf16','Slots':'*i64','Cu':'*i32','O':'*bf16'},constants=dict(H=32,HK=8,D=128,GROUP=4,SCALE=128**-.5,BQ=16,BN=64))
kernel=triton.compile(source,target=GPUTarget('cuda',80,32),options=dict(num_warps=4,num_stages=2))
assert not torch.cuda.is_initialized()
d=dict(passed=True,target='A100 sm80',dtype='BF16',heads32_kvheads8_headsize128=True,compiled_cubin_sha256=hashlib.sha256(kernel.asm['cubin']).hexdigest(),shared_bytes=kernel.metadata.shared,CUDA_context_initialized=False,GPU_execution=False,numerical_GPU_parity_and_speed_NOT_proven=True,time=time.time())
(P/'CPU-OFFLINE-COMPILE-PROOF.json').write_text(json.dumps(d,indent=2));print(json.dumps(d))
