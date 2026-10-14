"""CPU tests and full immutable 2700/300 audit: python test_data.py --audit."""
import os
os.environ.setdefault('CUDA_VISIBLE_DEVICES', '')
os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
import argparse,collections,hashlib,json,re,sys,types,unittest
from pathlib import Path
import torch
from transformers import AutoTokenizer
from data import build_sample,build_attention,can_attend,XML,OPENER
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
TOK=AutoTokenizer.from_pretrained(D/'tokenizer',local_files_only=True)
SYSTEM=(D/'system.txt').read_text()

def content(width=3,rounds=1):
 text='<think>\n'
 for r in range(rounds):
  text+='Plan:\n'+''.join(f'{i}: Compute local term {i}.\n' for i in range(1,width+1))
  text+=f'<Parallel>{width}\n'+''.join(f'<Path>{i}\n{r+i}+1={r+i+1}.\n</Path>\n\n' for i in range(1,width+1))
  text+='</Parallel>\n<Summary>\nCombine local terms.\n</Summary>\n'
 return text+'</think>\n\nFinal Answer: \\boxed{10}'

def row(text):return {'problem':'Compute ten.','answer':'10','assistant_content':text}

def invariant(sample):
 ids=sample['input_ids'];p=sample['position_ids'];m=sample['target_mask'];prefix=sample['prompt_length']
 assert len(ids)==len(p)==len(m) and all(x==0 for x in m[:prefix]) and m[-1]==1 and ids[-1]==151645
 for block in sample['spans']:
  first=block[0][0];base=p[first]
  for j,(s,e) in enumerate(block):
   assert p[s:e]==list(range(base,base+e-s)) and ids[s]==TOK.convert_tokens_to_ids('<Path>') and m[s]==0
   assert not any(can_attend(q,k,sample['spans']) for q in [s,e-1] for k in range(first,s))
   # Closure proof: a branch key is common prefix (<first) or own path.
   # Prefix keys are causal and precede every sibling, including whitespace;
   # own-path keys obey the same invariant. Thus any number of layers is safe.
   if j:assert all(not can_attend(s,k,sample['spans']) for k in range(first,s))
  merge=block[-1][1];assert p[merge]==base+max(e-s for s,e in block)
  assert all(can_attend(merge,k,sample['spans']) for k in range(first,merge))

class DataTests(unittest.TestCase):
 def test_all_widths_two_rounds(self):
  for width in range(2,9):
   s=build_sample(row(content(width,2)),TOK,'Solve.',8192);invariant(s);self.assertEqual(s['widths'],[width,width])
 def test_native_source_bytes_and_im_end(self):
  text=content();s=build_sample(row(text),TOK,'Solve.');decoded=TOK.decode(s['input_ids'],skip_special_tokens=False,clean_up_tokenization_spaces=False)
  self.assertTrue(decoded.endswith(text+'<|im_end|>'));self.assertEqual(s['input_ids'][-1],151645)
 def test_target_slots_and_forced_headers(self):
  s=build_sample(row(content()),TOK,'Solve.');ids=s['input_ids'];mask=s['target_mask'];p=s['prompt_length']
  for tag in ['<Parallel>','</Path>','</Summary>']:
   self.assertTrue(all(mask[i]==1 for i in range(p,len(ids)) if ids[i]==TOK.convert_tokens_to_ids(tag)))
  for tag in ['<Path>','</Parallel>','<Summary>']:
   self.assertTrue(all(mask[i]==0 for i in range(p,len(ids)) if ids[i]==TOK.convert_tokens_to_ids(tag)))
  for block in s['spans']:
   for start,end in block:
    self.assertEqual(mask[start:start+3],[0,0,0])
 def test_whitespace_attached_previous_and_attention(self):
  s=build_sample(row(content(3)),TOK,'Solve.');a=build_attention(s,'cpu')
  for q in range(len(s['input_ids'])):
   for k in range(len(s['input_ids'])):self.assertEqual(bool(a[q,k]),can_attend(q,k,s['spans']))
  for block in s['spans']:
   for (_,end),(nextstart,_) in zip(block,block[1:]):self.assertEqual(end,nextstart)
 def test_indirect_multilayer_isolation(self):
  s=build_sample(row(content(3)),TOK,'S.');a=build_attention(s,'cpu');n=len(s['input_ids']);reachable=[{i} for i in range(n)]
  for _ in range(3):
   reachable=[set().union(*(reachable[k] for k in range(q+1) if a[q,k])) for q in range(n)]
   for block in s['spans']:
    first=block[0][0]
    for start,end in block[1:]:self.assertFalse(reachable[end-1]&set(range(first,start)))
 def test_frozen_layout_equivalence(self):
  path=ROOT/'work/experiments/night-20261010/rl-code/verl/verl/utils/parallel_structure.py';m=types.ModuleType('frozen_layout');exec(compile(path.read_text(),str(path),'exec'),m.__dict__)
  for width in range(2,9):
   s=build_sample(row(content(width,2)),TOK,'Solve.');tags=[TOK.convert_tokens_to_ids(x) for x in XML[:4]];tags=[TOK.convert_tokens_to_ids(x) for x in ['<Parallel>','</Parallel>','<Path>','</Path>']];pos,spans=m.layout(torch.tensor(s['input_ids']),s['prompt_length'],tags,TOK.pad_token_id);self.assertEqual(pos.tolist(),s['position_ids']);self.assertEqual(spans,s['spans']);self.assertTrue(torch.equal(m.attention(torch.tensor(s['input_ids']),s['prompt_length'],tags,TOK.pad_token_id),build_attention(s)))
 def test_reject_malformed_and_wrong_gold(self):
  good=content(3)
  for bad in [good.replace('<Parallel>3','<Parallel>9'),good.replace('<Path>2','<Path>1'),good.replace('</Summary>',''),good.replace('Final Answer: \\boxed{10}','Final Answer: \\boxed{11}'),good.replace('1+1=2.','Final Answer: 2'),good.replace('Plan:','Assignments:')]:
   with self.assertRaises(ValueError):build_sample(row(bad),TOK,'Solve.')
 def test_valid_sequential_source(self):
  s=build_sample(row('<think>\n5+5=10.\n</think>\nFinal Answer: \\boxed{10}'),TOK,'Solve.');invariant(s);self.assertEqual(s['spans'],[]);self.assertEqual(s['position_ids'],list(range(len(s['input_ids']))))
 def test_no_truncation(self):
  with self.assertRaises(ValueError):build_sample(row(content()),TOK,'Solve.',max_length=10)

def audit():
 source=ROOT/'exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think';report={'passed':False,'source_sha256':{},'splits':{},'tokenizer_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (D/'tokenizer').iterdir() if p.is_file()},'data_module_sha256':hashlib.sha256((D/'data.py').read_bytes()).hexdigest(),'system_sha256':hashlib.sha256(SYSTEM.encode()).hexdigest(),'torch_GPU_launches':False,'response_transformations':'Only separate native initialthink into prompt and append native im_end; all source assistant bytes preserved; sibling whitespace retained on preceding path.'};sets={}
 for split,count in [('train',2700),('val',300)]:
  p=source/(split+'.jsonl');report['source_sha256'][str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();rows=[json.loads(l) for l in p.read_text().splitlines()];assert len(rows)==count;sets[split]={r['problem'] for r in rows};lengths=[];widths=collections.Counter();telemetry=[];targets=0
  for r in rows:
   s=build_sample(r,TOK,SYSTEM,8192);invariant(s);lengths.append(len(s['input_ids']));widths.update(s['widths']);targets+=sum(s['target_mask'])
   if s['boundary_telemetry']:telemetry.append({'id':r['id'],'tokens':s['boundary_telemetry']})
  sorted_l=sorted(lengths);report['splits'][split]={'rows':count,'unique_questions':len(sets[split]),'min_length':min(lengths),'max_length':max(lengths),'mean_length':sum(lengths)/count,'p50_length':sorted_l[int(.5*(count-1))],'p95_length':sorted_l[int(.95*(count-1))],'width_histogram':dict(widths),'total_supervised_targets':targets,'boundary_telemetry':telemetry,'all_direct_and_indirect_isolation_invariants':True,'no_truncation':True};print(split,report['splits'][split]['max_length'],dict(widths),flush=True)
 assert not sets['train']&sets['val'];report['train_val_question_overlap']=0;report['passed']=True;(D/'data-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('FULL3000AUDIT PASS',flush=True)

if __name__=='__main__':
 runaudit='--audit' in sys.argv
 if runaudit:sys.argv.remove('--audit')
 result=unittest.main(exit=False)
 if not result.result.wasSuccessful():raise SystemExit(1)
 if runaudit:audit()
