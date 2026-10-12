"""Grouped difficulty diagnostic on admitted16 pilot; no updates or selection."""
import argparse,json,sys,time,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rank',type=int,required=True);p.add_argument('--world',type=int,default=8);p.add_argument('--model',required=True);p.add_argument('--output',required=True);a=p.parse_args();base=Path(__file__).resolve().parent.parent;root=next(x for x in base.parents if (x/'verl').is_dir() and (x/'exps').is_dir());sys.path.insert(0,str(base/'production-runner'))
import torch
from transformers import AutoModelForCausalLM,AutoTokenizer
from train import instruct_prefix,format_flags,load_module
from rollout import execute,native_eos_ids
import structured_replay as replay
from microbatch_decoder import MicrobatchedHFDecoder
pilot=base/'data/revision2/pilot.jsonl';assert hashlib.sha256(pilot.read_bytes()).hexdigest()=='0782fce946cf81f9a23706631e703a8ddd38bd3422ace756dd01ac3ad0d0d25d';manifest=json.loads((base/'data/revision2/manifest.json').read_text());assert manifest['passed'] and manifest['reserved_aime_excluded'] and manifest['math_all_train_test_excluded'];rows=[json.loads(l) for l in pilot.read_text().splitlines()];assert len(rows)==16
out=Path(a.output);assert out.resolve().is_relative_to(base);out.mkdir(parents=True,exist_ok=True);assert not (out/f'rank-{a.rank}.jsonl').exists();torch.set_num_threads(1);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.set_float32_matmul_precision('highest');tok=AutoTokenizer.from_pretrained(a.model,local_files_only=True);model=AutoModelForCausalLM.from_pretrained(a.model,local_files_only=True,torch_dtype=torch.float32,attn_implementation='sdpa').to('cuda').eval();decoder=MicrobatchedHFDecoder(model,replay,'cuda',max_paths=2);system=(root/'work/experiments/instruct-full-20261011/system.txt').read_text();eos=native_eos_ids(a.model,tok);scorer=load_module('frozen_scorer',root/'work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py')
with (out/f'rank-{a.rank}.jsonl').open('w',buffering=1) as f:
 for index in range(a.rank,len(rows),a.world):
  row=rows[index];prefix=instruct_prefix(tok,[dict(role='system',content=system),dict(role='user',content=row['problem'])])
  for sample in range(4):
   started=time.time();trace=execute(tok,prefix,decoder,eos,4096,768,16384,33161011+index*1000+sample*100);grade=scorer.grade(trace['output'],str(row['answer']));valid,parallel=format_flags(trace['output'],trace['stats']);trace.update(id=row['id'],source=row['source'],sample=sample,rank=a.rank,grade=grade,format_valid=valid,parallel_valid=parallel,seconds=time.time()-started,diagnostic_only=True,optimizer_updates=0,selection_allowed=False);f.write(json.dumps(trace,ensure_ascii=False)+'\n')
print(json.dumps(dict(rank=a.rank,completed=True,optimizer_updates=0,peak_gpu_bytes=torch.cuda.max_memory_allocated())))
