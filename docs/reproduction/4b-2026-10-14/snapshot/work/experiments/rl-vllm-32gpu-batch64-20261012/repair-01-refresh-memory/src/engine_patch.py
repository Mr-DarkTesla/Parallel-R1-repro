"""Isolated vLLM0.8.5.post1 worker/ModelRunner patch. GPU load is explicit."""
import os
from dag_backend import PagedSlotBackend

def load_patched_worker(model_path,ledger,actor_dtype='bfloat16',max_context=16384,capacity=65536,port=29791,local_rank=0):
 """CPU import/API proof may inspect this; calling it requires assigned free GPU.
 Uses the installed vLLM loader, CUDA Qwen3 linear/RMS/RoPE implementations;
 replaces only this worker's instantiated attention and cache tensors.
 """
 if os.environ.get('STRUCTURED_GPU_AUTHORIZED')!='1':raise RuntimeError('GPU launch requires explicit assigned-lane environment')
 for key in ['RANK','WORLD_SIZE','LOCAL_RANK','LOCAL_WORLD_SIZE','GROUP_RANK','MASTER_ADDR','MASTER_PORT','TORCHELASTIC_RUN_ID'] :os.environ.pop(key,None)
 os.environ['TORCHELASTIC_USE_AGENT_STORE']='False'
 import vllm
 if vllm.__version__!='0.8.5.post1':raise RuntimeError('Installed vLLM version changed; new source proof required')
 from vllm.engine.arg_utils import EngineArgs
 from vllm.worker.worker import Worker
 from vllm.attention.layer import Attention
 from structured_runner import patch_model_runner
 args=EngineArgs(model=model_path,tokenizer=model_path,dtype=actor_dtype,tensor_parallel_size=1,pipeline_parallel_size=1,max_model_len=max_context,max_num_seqs=32,max_num_batched_tokens=max_context,enforce_eager=True,enable_prefix_caching=False,enable_chunked_prefill=False,trust_remote_code=False)
 config=args.create_engine_config()
 config.compilation_config.level=0
 worker=Worker(config,local_rank=local_rank,rank=0,distributed_init_method=f'tcp://127.0.0.1:{port}',is_driver_worker=True,model_runner_cls=patch_model_runner)
 worker.init_device();worker.load_model()
 model=worker.model_runner.model
 layers=[layer for layer in model.modules() if isinstance(layer,Attention)]
 if not layers:raise ValueError('Actual vLLM Attention layers not found')
 backend=PagedSlotBackend(model,config,layers,ledger,capacity=capacity,runner=worker.model_runner)
 return worker,backend
