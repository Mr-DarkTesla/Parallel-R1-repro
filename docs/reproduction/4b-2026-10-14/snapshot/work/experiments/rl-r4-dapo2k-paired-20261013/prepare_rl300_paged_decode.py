"""Prepare only; no signals, allocation or GPU test."""
from pathlib import Path
import ast,hashlib,json,os,shutil,time
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013'
S=O/'candidate-flash-varlen-decode';P=O/'candidate-direct-paged-decode'
assert not P.exists();P.mkdir();shutil.copytree(S/'src',P/'src',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));shutil.copy(S/'reward.py',P/'reward.py')
shutil.copy(R/'work/experiments/rl-r4-dapo2k-paired-20261013/paged_decode_triton.py',P/'src/paged_decode_triton.py')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
f=P/'src/dag_backend.py';s=f.read_text();begin=s.index('   from vllm.vllm_flash_attn import flash_attn_varlen_func');end=s.index('   self.calls+=1',begin)
s=s[:begin]+'''   from paged_decode_triton import paged_gqa_decode
   result=paged_gqa_decode(q.contiguous(),store,
       metadata.flat_physical_indices,metadata.cu_seqlens_k,self.scale)
'''+s[end:];f.write_text(s)
(P/'node_entry.py').write_text((S/'node_entry.py').read_text().replace(str(S),str(P)))
c=json.loads((S/'production-config.json').read_text().replace(str(S),str(P)));c['actor_decode_attention']='direct_paged_triton_one_query_exact_visible_keys';save(P/'production-config.json',c)
for f in [P/'node_entry.py',P/'reward.py',*(P/'src').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
assert c['global_batch']['responses_per_step']==64 and c['expected_world_size']==16 and c['response_budget']==32000 and c['path_budget']==4000 and c['max_context']==40960
assert sha(P/'reward.py')==sha(S/'reward.py')
save(P/'PREPARED-NOT-LAUNCHED.json',dict(prepared=True,AST_pass=True,no_GPU_test=True,no_measured_speedup=True,no_live_source_changes=True,no_signals=True,no_submit=True,changes=['direct KV physical-slot reads in fused GQA decode','FP32 online softmax/BF16 attention','exact one-query visibility restriction; original masked prefill unchanged'],caps_reward_batch_data_loss_guards_unchanged=True,remaining_bottlenecks=['CPU metadata construction','actor rebuilding','phase-boundary cohort scheduler'],sha256={str(f):sha(f) for f in [P/'node_entry.py',P/'production-config.json',P/'reward.py',*(P/'src').rglob('*.py')]},time=time.time()))
print(json.dumps(dict(prepared=True,root=str(P),config_sha256=sha(P/'production-config.json'),not_launched=True)))
