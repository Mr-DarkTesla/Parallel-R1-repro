"""CPU preflight: import actual fresh evaluator class; no model or CUDA allocations."""
import asyncio,json,os,sys,ast,hashlib,random
from pathlib import Path
from types import SimpleNamespace
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W/'code'))
os.environ['PARALLEL_R1_TRACE_DIR']=''
import torch
from transformers import AutoTokenizer
from omegaconf import OmegaConf
from verl.parallel_thinking_generation_v3.parallel_thinking_loop_v3 import ParallelThinkingAgentLoopV3 as Loop
from verl.workers.rollout.vllm_rollout.structured_worker import validate_sampling
torch.set_num_threads(1)
manifest=json.loads((W/'manifest.json').read_text())
tok=AutoTokenizer.from_pretrained(manifest['checkpoint'],local_files_only=True)
think=tok.encode('<think>\n',add_special_tokens=False)
assert think==[151667,198],think
class Server:
    def __init__(self,width=2,rounds=0):self.width=width;self.rounds=rounds;self.main=0;self.calls=[]
    async def generate(self,**kw):
        self.calls.append(kw);sp=kw['sampling_params'];stop=sp['stop_token_ids'][0]
        if stop==151671:
            self.main+=1
            out=[151671] if self.main<=self.rounds else tok.encode('</think>\nFinal Answer: \\boxed{7}',add_special_tokens=False)+[tok.eos_token_id]
        elif stop==198:out=tok.encode(str(self.width)+'\n',add_special_tokens=False)
        else:out=tok.encode('Computed term.',add_special_tokens=False)+[stop]
        return out[:sp['max_tokens']]
def config(budget=30720,explicit=True):
    agent=dict(min_paths=2,max_paths=8,max_iterations_for_parallel_thinking=0,max_path_response_length=8192)
    if explicit:agent['force_think_prefix']=True
    return OmegaConf.create(dict(actor_rollout_ref=dict(rollout=dict(prompt_length=2048,response_length=budget,structured_unseen=True,agent=agent))))
async def run(budget=30720,width=2,rounds=0,tokenizer=tok,explicit=True):
    Loop._class_initialized=False;s=Server(width,rounds)
    a=Loop(SimpleNamespace(config=config(budget,explicit)),s,tokenizer)
    a.trajectory={'sample_index':0,'unique_id':'cpu-preflight'}
    out=await a.run([{'role':'user','content':'Compute seven.'}],dict(temperature=.6,top_p=.95,top_k=20,repetition_penalty=1.))
    return a,s,out
a,s,out=asyncio.run(run())
assert out.response_ids[:2]==think and out.response_mask[:2]==[0,0]
assert out.rollout_calls[0]['response_start']==2
assert s.calls[0]['prompt_ids']==out.prompt_ids+think==out.rollout_calls[0]['prompt_ids']
assert s.calls[0]['sampling_params']['_structure_start']==len(out.prompt_ids)
assert s.calls[0]['sampling_params']['max_tokens']==30718
assert a.trace.record['forced_think_prefix_tokens']==2
assert sum(out.response_mask)==out.repro_stats['generated_tokens']
for budget in [1,2]:
    a,s,o=asyncio.run(run(budget))
    assert o.response_ids==think[:budget] and o.response_mask==[0]*budget and not s.calls
a,s,o=asyncio.run(run(explicit=False))
assert o.response_ids[:2]==think and o.response_mask[:2]==[0,0]
class TemplateThink:
    def __getattr__(self,name):return getattr(tok,name)
    def apply_chat_template(self,*args,**kwargs):return tok.apply_chat_template(*args,**kwargs)+think
a,s,o=asyncio.run(run(tokenizer=TemplateThink()))
assert a.trace.record['forced_think_prefix_tokens']==0
assert s.calls[0]['prompt_ids']==o.prompt_ids
assert o.prompt_ids[-2:]==think and o.response_mask[0]==1
fork_results=[]
for width in [2,8]:
    a,s,o=asyncio.run(run(width=width,rounds=2))
    assert o.repro_stats['forks']==2 and o.response_mask[:2]==[0,0]
    assert all(c['sampling_params']['_structure_start']==len(o.prompt_ids) for c in s.calls)
    assert all(c['prompt_ids'][len(o.prompt_ids):len(o.prompt_ids)+2]==think for c in s.calls)
    assert len(o.response_ids)<=30720 and sum(o.response_mask)==sum(len(c['generated_ids']) for c in a.trace.record['calls'])
    fork_results.append(dict(width=width,forks=o.repro_stats['forks'],sampled_tokens=sum(o.response_mask)))
validate_sampling(dict(temperature=.6,top_p=.95,top_k=20),evaluation_only=True)
rejected=0
for x in [dict(top_p=.95),dict(top_k=20)]:
    try:validate_sampling(x)
    except ValueError:rejected+=1
assert rejected==2
questions=list(map(json.loads,(W/'questions.jsonl').read_text().splitlines()))
lengths=[len(tok.apply_chat_template([dict(role='system',content=manifest['system_prompt']),dict(role='user',content=q['problem'])],add_generation_prompt=True,tokenize=True)) for q in questions]
assert len(questions)==500 and len({q['id'] for q in questions})==500
assert max(lengths)<=2048
assert hashlib.sha256((W/'questions.jsonl').read_bytes()).hexdigest()==manifest['questions_sha256']
for p in list(W.glob('*.py'))+list((W/'code').rglob('*.py')):ast.parse(p.read_text(),filename=str(p))
assert not torch.cuda.is_initialized()
result=dict(status='passed',actual_loop_import='passed',force_think_prefix_ids=think,forced_response_mask=[0,0],default_prefix='passed',already_open_template_no_duplicate='passed',tiny_budgets='passed',repeated_forks=fork_results,prompt_tokens_min=min(lengths),prompt_tokens_max=max(lengths),prompt_over_2048=0,strict_ppo_sampling_guard='passed',evaluation_top_k_top_p_guard='passed',cuda_initialized=False,checkpoint_sha256=manifest['checkpoint_sha256'])
(W/'preflight-loop.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
