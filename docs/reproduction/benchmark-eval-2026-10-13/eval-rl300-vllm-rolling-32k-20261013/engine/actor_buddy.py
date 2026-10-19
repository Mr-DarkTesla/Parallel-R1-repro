"""TP1 actor subprocess, CUDA-IPC FP32 master leases, no CPU/disk weights.
Synchronous fresh-batch mode: refresh -> immutable whole episodes -> release ->
one learner update. q, p0 and current stay distinct. No async lag in this gate.
"""
import os,time,json,traceback,threading
from pathlib import Path
import torch
import torch.multiprocessing as mp

def packed_view(parameters,name,source,source_shapes):
 """TP1 Qwen3 HF names -> exact physical packed target slice."""
 for packed,names in [('qkv_proj',['q_proj','k_proj','v_proj']),('gate_up_proj',['gate_proj','up_proj'])]:
  for i,part in enumerate(names):
   if '.'+part+'.' in name:
    target=name.replace('.'+part+'.','.'+packed+'.');offset=sum(source_shapes[name.replace('.'+part+'.','.'+prior+'.')][0] for prior in names[:i])
    return parameters[target].narrow(0,offset,source.shape[0]),target
 return parameters[name],name

def _actor_main(commands,answers,cfg,rank,local_rank):
 for key in ['RANK','WORLD_SIZE','LOCAL_RANK','LOCAL_WORLD_SIZE','MASTER_ADDR','MASTER_PORT','GROUP_RANK','TORCHELASTIC_RUN_ID']:os.environ.pop(key,None)
 os.environ.update(STRUCTURED_GPU_AUTHORIZED='1',VLLM_USE_V1='0',TORCHELASTIC_USE_AGENT_STORE='False',OMP_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false')
 torch.cuda.set_device(local_rank);torch.set_num_threads(1);torch.backends.cuda.matmul.allow_tf32=False
 import subprocess,socket
 gpu_uuids={int(line.split(',')[0]):line.split(',')[1].strip() for line in subprocess.check_output(['nvidia-smi','--query-gpu=index,uuid','--format=csv,noheader'],text=True).splitlines()};gpu_uuid=gpu_uuids[local_rank]
 from engine_patch import load_patched_worker
 from structured_adapter import Ledger
 from slot_decoder import VLLMSlotDecoder
 from cohort_decoder import CohortDecoder
 from rollout import execute
 from audited_backend import enable_same_actor_audit
 worker=backend=decoder=None;version=None
 out=Path(cfg['output']);out.mkdir(parents=True,exist_ok=True)
 (out/f'actor-rank-{rank}-launch.json').write_text(json.dumps(dict(pid=os.getpid(),start_ticks=Path(f'/proc/{os.getpid()}/stat').read_text().split()[21],parent_pid=os.getppid(),rank=rank,local_rank=local_rank,host=socket.gethostname(),gpu_uuid=gpu_uuid,TP=1,learner_world=cfg['expected_world_size'],CUDA_VISIBLE_DEVICES=os.environ.get('CUDA_VISIBLE_DEVICES'),time=time.time()))+'\n')
 try:
  ledger=Ledger();worker,backend=load_patched_worker(cfg['model'],ledger,'bfloat16',cfg['max_context'],cfg['slot_capacity'],cfg['actor_port_base']+rank,local_rank=local_rank)
  enable_same_actor_audit(backend)
  from transformers import AutoTokenizer
  tok=AutoTokenizer.from_pretrained(cfg['model'],local_files_only=True)
  answers.put(dict(kind='ready',pid=os.getpid(),model_type=type(worker.model_runner.model).__name__,runner=type(worker.model_runner).__name__))
  while True:
   cmd=commands.get();kind=cmd['kind']
   if kind=='stop':break
   if kind=='refresh':
    started=time.perf_counter();new=cmd['version'];assert version is None or new==version+1
    if decoder is not None:decoder.clear();assert not backend.allocator.refs
    weights=cmd['weights'];assert weights and all(t.device.type=='cuda' and t.device.index==local_rank and t.dtype==torch.float32 for _,t in weights)
    shapes={name:tuple(t.shape) for name,t in weights};model=worker.model_runner.model;parameters=dict(model.named_parameters(remove_duplicate=False))
    # Official Qwen3 AutoWeightsLoader delegates packed QKV/gate/up to installed
    # TP1 weight_loaders. CUDA IPC views remain alive until loader+verification ACK.
    with torch.inference_mode():
     loaded=model.load_weights(iter(weights));expected=set();checked=0
     for name,tensor in weights:
      target,key=packed_view(parameters,name,tensor,shapes);expected.add(key);assert target.shape==tensor.shape
      assert torch.isfinite(tensor).all(),name;assert torch.equal(target,tensor.to(torch.bfloat16)),name;checked+=tensor.numel()
    assert set(loaded)==expected,(set(loaded)-expected,expected-set(loaded))
    assert checked==4_022_468_096 and all(t.dtype==torch.bfloat16 for t in parameters.values())
    torch.cuda.synchronize(local_rank);version=new;backend.actor_version=None;decoder=VLLMSlotDecoder(backend,f'learner-v{version}/vllm-bf16');backend.reset_audit()
    del weights,cmd,tensor,target;torch.cuda.ipc_collect()
    receipt=dict(kind='refreshed',version=version,parameters=checked,host=socket.gethostname(),gpu_uuid=gpu_uuid,local_rank=local_rank,loaded_parameters=len(loaded),cuda_ipc=True,cpu_weight_bytes=0,packed_weights_exact=True,all_master_elements_finite=True,seconds=time.perf_counter()-started,pid=os.getpid(),rank=rank,peak_allocated=torch.cuda.max_memory_allocated(local_rank),peak_reserved=torch.cuda.max_memory_reserved(local_rank))
    with (out/f'actor-refresh-rank-{rank}.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
    answers.put(receipt)
   elif kind=='rollout':
    assert cmd['version']==version;server=CohortDecoder(decoder,max_rows=32);lock=threading.Lock();jobs=[]
    for request in cmd['requests']:
     def job(client,request=request):
      trace=execute(tok,request['prefix'],client,cmd['eos'],4096,768,16384,request['seed']);trace.update(purpose=cmd.get('purpose','train'),actor_version=version,behavior_version=version,behavior_precision='vllm_whole_bf16',behavior_policy='q',prompt_index=request['prompt_index'],sample=request['sample'],seed=request['seed'],id=request['id'],answer=request['answer'])
      with lock,(out/f'raw-{cmd.get("purpose","train")}-step-{cmd["step"]}-rank-{rank}.jsonl').open('a') as f:f.write(json.dumps(trace)+'\n');f.flush();os.fsync(f.fileno())
      return trace
     jobs.append(job)
    torch.cuda.synchronize(local_rank);started=time.perf_counter();F=backend.actual_model_forwards;T=backend.total_model_forwards;traces=server.run(jobs);torch.cuda.synchronize(local_rank);wall=time.perf_counter()-started
    assert backend.actual_model_forwards-F==sum(x['physical_forward_calls'] for x in server.server_batches)
    assert int(backend.device_forward_counter.item())==backend.actual_model_forwards and int(backend.device_total_counter.item())==backend.total_model_forwards
    guard=backend.audit_stats();assert guard['actions']>0
    receipt=dict(kind='rollout',version=version,traces=traces,wall=wall,host=socket.gethostname(),gpu_uuid=gpu_uuid,rank=rank,local_rank=local_rank,generation_F=backend.actual_model_forwards-F,total_F=backend.total_model_forwards-T,technical_F=backend.total_model_forwards-T-(backend.actual_model_forwards-F),guard=guard,peak_allocated=torch.cuda.max_memory_allocated(local_rank),peak_reserved=torch.cuda.max_memory_reserved(local_rank),backend_batches=server.server_batches,pid=os.getpid())
    answers.put(receipt);decoder.clear();backend.reset_audit();del cmd,traces,receipt,jobs;torch.cuda.empty_cache()
   else:raise ValueError(kind)
  if decoder is not None:decoder.clear()
  if backend is not None:backend.close()
  import torch.distributed as dist
  if dist.is_initialized():dist.destroy_process_group()
  answers.put(dict(kind='stopped',pid=os.getpid(),version=version))
 except BaseException as error:
  answers.put(dict(kind='error',error=repr(error),traceback=traceback.format_exc()));raise

class ActorBuddy:
 def __init__(self,model,cfg,rank,local_rank):
  self.model,self.cfg,self.rank,self.local_rank=model,cfg,rank,local_rank;context=mp.get_context('spawn');self.commands=context.Queue(maxsize=1);self.answers=context.Queue(maxsize=1)
  self.process=context.Process(target=_actor_main,args=(self.commands,self.answers,cfg,rank,local_rank),daemon=False);self.process.start();self.receive('ready');self.version=None;self.refresh_actor(cfg['initial_step'])
 def receive(self,kind):
  import queue
  while True:
   try:result=self.answers.get(timeout=5)
   except queue.Empty:
    if not self.process.is_alive():raise RuntimeError(f'Actor buddy exited{self.process.exitcode}')
    continue
   if result['kind']=='error':raise RuntimeError(result['traceback'])
   assert result['kind']==kind,result;return result
 def refresh_actor(self,version):
  if self.version==version:return
  # named_parameters creates unique detached CUDA views; Queue's torch reducer transfers IPC
  # handles. Master storage never mutates until rollout reply and learner phase.
  weights=[(name,parameter.detach()) for name,parameter in self.model.named_parameters(remove_duplicate=True)];torch.cuda.synchronize(self.local_rank);self.commands.put(dict(kind='refresh',version=version,weights=weights));self.last_refresh=self.receive('refreshed');assert self.last_refresh['version']==version;self.version=version;del weights
 def collect(self,requests,eos,step,purpose="train"):
  assert self.version is not None;self.commands.put(dict(kind='rollout',version=self.version,requests=requests,eos=eos,step=step,purpose=purpose));self.last_rollout=self.receive('rollout');assert self.last_rollout['version']==self.version;return self.last_rollout['traces']
 def close(self):
  self.commands.put(dict(kind='stop'));self.receive('stopped');self.process.join(timeout=120);assert self.process.exitcode==0;self.commands.close();self.answers.close();torch.cuda.ipc_collect()
