"""Prepare exact ragged FlashAttention decode; do not mutate or stop live jobs."""
from pathlib import Path
import ast,hashlib,json,os,shutil,time
R=Path('${PROJECT_ROOT}');os.chdir(R)
O=R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013'
S=Path(json.loads((O/'cloud-submission.json').read_text())['current_run_root']);P=O/'candidate-flash-varlen-decode'
assert not P.exists(),'Never overwrite an existing candidate/submission'
P.mkdir();shutil.copytree(S/'src',P/'src',ignore=shutil.ignore_patterns('__pycache__','*.pyc'));shutil.copy(S/'reward.py',P/'reward.py')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
f=P/'src/dag_backend.py';s=f.read_text()
needle=' qmax: int = 0\n'
assert s.count(needle)==1
s=s.replace(needle,needle+' decode_only: bool = False\n flat_physical_indices: object = None\n cu_seqlens_q: object = None\n cu_seqlens_k: object = None\n max_seqlen_k: int = 0\n')
needle=' def prepare(self,device):\n'
assert s.count(needle)==1
s=s.replace(needle,needle+'''  # One real query and exactly its permitted keys. No padding/mask is sent
  # to the fused decode kernel. Any masked/multiquery DAG stays on old SDPA.
  if all(row.query_end-row.query_begin==1 and len(row.write_slots)==1
         and row.allowed.device.type=='cpu'
         and row.allowed.shape==(1,len(row.read_slots)+1)
         and bool(row.allowed.all()) for row in self.rows):
   flat=[];cumulative=[0];writes=[]
   for row in self.rows:
    flat.extend(row.read_slots);flat.extend(row.write_slots)
    cumulative.append(len(flat));writes.extend(row.write_slots)
   if len(writes)!=len(set(writes)) or 0 in writes:raise ValueError('Duplicate/reserved physical writes')
   self.decode_only=True;self.qmax=1
   self.write_indices=torch.tensor(writes,dtype=torch.long,device=device)
   self.flat_physical_indices=torch.tensor(flat,dtype=torch.long,device=device)
   self.cu_seqlens_q=torch.arange(len(self.rows)+1,dtype=torch.int32,device=device)
   self.cu_seqlens_k=torch.tensor(cumulative,dtype=torch.int32,device=device)
   self.max_seqlen_k=max(b-a for a,b in zip(cumulative,cumulative[1:]))
   return self
''')
needle='  batch=len(rows);qmax=metadata.qmax\n'
assert s.count(needle)==1
s=s.replace(needle,'''  if metadata.decode_only:
   from vllm.vllm_flash_attn import flash_attn_varlen_func
   # GQA stays native: no repeating KV heads and no dense padded attention.
   keys=store[0].index_select(0,metadata.flat_physical_indices)
   values=store[1].index_select(0,metadata.flat_physical_indices)
   result=flash_attn_varlen_func(q.contiguous(),keys,values,
       max_seqlen_q=1,cu_seqlens_q=metadata.cu_seqlens_q,
       max_seqlen_k=metadata.max_seqlen_k,cu_seqlens_k=metadata.cu_seqlens_k,
       dropout_p=0.,softmax_scale=self.scale,causal=False,fa_version=2)
   self.calls+=1
   if output is not None:output.copy_(result.reshape_as(output));return output
   return result.reshape(query.shape)
'''+needle)
f.write_text(s)
(P/'node_entry.py').write_text((S/'node_entry.py').read_text().replace(str(S),str(P)))
c=json.loads((S/'production-config.json').read_text().replace(str(S),str(P)));c['actor_decode_attention']='flash_attn2_varlen_one_query_exact_visible_keys';save(P/'production-config.json',c)
for f in [P/'node_entry.py',P/'reward.py',*(P/'src').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
assert c['expected_world_size']==16 and c['global_batch']['responses_per_step']==64
assert c['response_budget']==32000 and c['path_budget']==4000 and c['max_context']==40960
assert sha(P/'reward.py')==sha(S/'reward.py')
save(P/'PREPARED-NOT-LAUNCHED.json',dict(prepared=True,source_AST_pass=True,no_GPU_test=True,no_measured_speedup=True,no_live_source_changes=True,no_signals=True,no_submit=True,source=str(S),changes=['exact ragged key lists for fully visible one-query decode','native FlashAttention2 GQA','original masked/multiquery SDPA retained unchanged'],remaining_bottlenecks=['KV still gathered per layer','actor rebuild still required','cohort phase scheduler not continuous'],caps_batch_reward_data_loss_unchanged=True,sha256={str(f):sha(f) for f in [P/'node_entry.py',P/'production-config.json',P/'reward.py',*(P/'src').rglob('*.py')]},time=time.time()))
print(json.dumps(dict(prepared=True,root=str(P),config_sha256=sha(P/'production-config.json'),not_launched=True)))
