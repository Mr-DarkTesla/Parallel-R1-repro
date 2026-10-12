import argparse,json,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--job',required=True);p.add_argument('--rank',type=int,required=True);a=p.parse_args()
job=json.loads(Path(a.job).read_text());root=Path.cwd();base=root/'work/experiments/rl-instruct-20261011';sys.path.insert(0,str(base/'production-runner'))
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
from train import instruct_prefix,format_flags,load_module
from rollout import execute,native_eos_ids
import structured_replay as replay
from microbatch_decoder import MicrobatchedHFDecoder
torch.set_num_threads(1);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.set_float32_matmul_precision('highest')
tok=AutoTokenizer.from_pretrained(job['model'],local_files_only=True);model=AutoModelForCausalLM.from_pretrained(job['model'],local_files_only=True,torch_dtype=torch.float32,attn_implementation='sdpa').to('cuda').eval()
decoder=MicrobatchedHFDecoder(model,replay,'cuda',max_paths=2);eos=native_eos_ids(job['model'],tok);system=Path(job['system']).read_text();scorer=load_module('frozen_math_scorer',job['scorer'])
forward_counter=[0];original_forward=model.forward
def counted_forward(*args,**kwargs):
 forward_counter[0]+=1
 return original_forward(*args,**kwargs)
model.forward=counted_forward
out=Path(job['output']);out.mkdir(parents=True,exist_ok=True);fpath=out/f'rank-{a.rank}.jsonl';done={json.loads(l)['id'] for l in fpath.read_text().splitlines()} if fpath.exists() else set()
rows=[json.loads(l) for l in Path(job['questions']).read_text().splitlines()]
with fpath.open('a',buffering=1) as f:
 for index in range(a.rank,len(rows),8):
  row=rows[index]
  if row['id'] in done:continue
  started=time.time();before=forward_counter[0];prefix=instruct_prefix(tok,[dict(role='system',content=system),dict(role='user',content=row['problem'])])
  trace=execute(tok,prefix,decoder,eos,4096,768,16384,42161011+index*1000)
  actual_f=forward_counter[0]-before;assert actual_f==trace['stats']['actual_model_forward_calls']
  valid,parallel=format_flags(trace['output'],trace['stats']);grade=scorer.grade(trace['output'],str(row['answer']))
  trace.update(id=row['id'],index=index,rank=a.rank,grade=grade,format_valid=valid,parallel_valid=parallel,seconds=time.time()-started,instrumented_forward_calls=actual_f,selection_allowed=False)
  f.write(json.dumps(trace,ensure_ascii=False)+'\n')
