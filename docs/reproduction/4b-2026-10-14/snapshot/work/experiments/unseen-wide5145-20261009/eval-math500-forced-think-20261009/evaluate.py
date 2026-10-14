"""Single-sample MATH-500 evaluation using the production counted Unseen loop."""
from pathlib import Path
import argparse,asyncio,datetime as dt,hashlib,json,os,random,sys,time
from types import SimpleNamespace
WORK=Path(__file__).resolve().parent;PROJECT=WORK.parents[3]
sys.path.insert(0,str(WORK/'code'))
os.environ['VLLM_USE_V1']='1';os.environ['VLLM_ENABLE_V1_MULTIPROCESSING']='0'
def timestamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def worker(rank,limit=0):
    import torch
    from transformers import AutoTokenizer
    from omegaconf import OmegaConf
    from vllm import LLM
    from verl.parallel_thinking_generation_v3.parallel_thinking_loop_v3 import ParallelThinkingAgentLoopV3
    torch.set_num_threads(1);torch.manual_seed(42+rank)
    manifest=json.loads((WORK/'manifest.json').read_text());model=manifest['checkpoint']
    assert torch.cuda.mem_get_info()[0]>60*1024**3,'GPU occupied; do not disturb other work'
    tok=AutoTokenizer.from_pretrained(model,local_files_only=True)
    tags=[tok.convert_tokens_to_ids(t) for t in ['<Parallel>','</Parallel>','<Path>','</Path>']]
    llm=LLM(model=model,dtype='bfloat16',tensor_parallel_size=1,gpu_memory_utilization=.2,max_model_len=32768,max_num_seqs=1,
        max_num_batched_tokens=32768,enforce_eager=True,enable_prefix_caching=False,enable_chunked_prefill=False,
        worker_extension_cls='verl.workers.rollout.vllm_rollout.structured_worker.StructuredWorkerExtension',compilation_config={'level':0},disable_log_stats=True,seed=42)
    class Server:
        async def generate(self,request_id,prompt_ids,sampling_params):
            params=dict(sampling_params);boundary=params.pop('_structure_start');params['_evaluation_only']=True
            params['max_tokens']=min(params['max_tokens'],32768-len(prompt_ids))
            if params['max_tokens']<=0:return []
            return llm.llm_engine.collective_rpc('structured_generate',args=(prompt_ids,params,boundary,tags,tok.pad_token_id))[0]
    config=OmegaConf.create({'actor_rollout_ref':{'rollout':{'prompt_length':2048,'response_length':30720,'structured_unseen':True,'agent':{'max_path_response_length':8192,'max_iterations_for_parallel_thinking':0,'min_paths':2,'max_paths':8,'force_think_prefix':True}}}})
    questions=[json.loads(s) for s in (WORK/'questions.jsonl').read_text().splitlines()][rank::8]
    if limit:questions=questions[:limit]
    ParallelThinkingAgentLoopV3._class_initialized=False
    async def run():
        stream=(WORK/f'traces-{rank}.jsonl').open('a',buffering=1)
        completed={json.loads(line)['id'] for line in (WORK/f'traces-{rank}.jsonl').read_text().splitlines() if line.strip()}
        for q in questions:
            if q['id'] in completed:continue
            random.seed(42+q['index']);torch.manual_seed(42+q['index'])
            agent=ParallelThinkingAgentLoopV3(SimpleNamespace(config=config),Server(),tok)
            agent.trajectory={'sample_index':q['index'],'unique_id':q['id']}
            messages=[{'role':'system','content':manifest['system_prompt']},{'role':'user','content':q['problem']}]
            begun=time.time();output=await agent.run(messages,{'temperature':.6,'top_p':.95,'top_k':20,'repetition_penalty':1.})
            record=dict(index=q['index'],id=q['id'],subject=q['subject'],level=q['level'],problem=q['problem'],output=tok.decode(output.response_ids,skip_special_tokens=False),
                response_tokens=len(output.response_ids),sampled_tokens=sum(output.response_mask),repro_stats=output.repro_stats,trace=agent.trace.record,
                worker=rank,seed=42+q['index'],elapsed_seconds=time.time()-begun,finished_at=timestamp())
            stream.write(json.dumps(record,ensure_ascii=False)+'\n');stream.flush()
            print(json.dumps({'event':'question_complete','index':q['index'],'tokens':record['response_tokens'],'seconds':record['elapsed_seconds'],'forks':output.repro_stats['forks']}),flush=True)
        stream.close()
    asyncio.run(run())
    if torch.distributed.is_initialized():torch.distributed.destroy_process_group()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--worker',type=int,required=True);parser.add_argument('--limit',type=int,default=0);args=parser.parse_args();worker(args.worker,args.limit)
