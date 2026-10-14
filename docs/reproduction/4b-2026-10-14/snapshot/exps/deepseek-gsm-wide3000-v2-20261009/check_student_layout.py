"""Validate the exact Unseen loader prefix/response concatenation and whole chats."""
import hashlib,json
from pathlib import Path
from transformers import AutoTokenizer
from layout import split_solution
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent.parent
student=(ROOT/'student-system.txt').read_text()
tok=AutoTokenizer.from_pretrained(BASE/'exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final',local_files_only=True)
tasks={r['id']:r for r in map(json.loads,(ROOT/'pilot-tasks.jsonl').read_text().splitlines())}
results=[json.loads(l) for l in ((ROOT/'reviewed-pilot-results.jsonl') if (ROOT/'reviewed-pilot-results.jsonl').exists() else (ROOT/'pilot-results.jsonl')).read_text().splitlines()]
checked=[]
for row in results:
 if not row.get('accepted'):continue
 reason,final=split_solution(row['output']);prompt=[{'role':'system','content':student},{'role':'user','content':tasks[row['id']]['question']}]
 full='<think>\n'+reason+'\n</think>\n\n'+final
 prefix=tok.apply_chat_template(prompt,tokenize=False,add_generation_prompt=True)
 response=reason+'\n</think>\n\n'+final if prefix.rstrip().endswith('<think>') else full
 merged=prefix+response+tok.eos_token
 rendered=tok.apply_chat_template(prompt+[{'role':'assistant','content':full}],tokenize=False,add_generation_prompt=False)
 for sequence in [merged,rendered]:
  assistant=sequence.rsplit('<|im_start|>assistant',1)[1]
  assert assistant.count('<think>')==1 and assistant.count('</think>')==1,row['id']
  inside=assistant.split('<think>',1)[1].split('</think>',1)[0];outside=assistant.split('</think>',1)[1].strip().removesuffix(tok.eos_token).removesuffix('<|im_end|>').strip()
  assert inside.strip()==reason and outside==final,row['id']
  assert inside.count('<Parallel>')==row['structure']['rounds']
  assert not any(t in outside for t in ['<Parallel>','<Path>','<Summary>'])
 sequence_length=len(tok.encode(prefix,add_special_tokens=False))+len(tok.encode(response+tok.eos_token,add_special_tokens=False))
 assert sequence_length==row['student_tokens'] and sequence_length<=16384
 checked.append({'id':row['id'],'tokens':sequence_length})
report={'actual_tokenizer_prompt_opens_think':prefix.rstrip().endswith('<think>'),'checked':len(checked),'actual_loader_concatenation_single_think':True,'whole_chat_single_think':True,'all_work_inside_think':True,'final_solution_outside_think':True,'max_student_tokens':max(r['tokens'] for r in checked) if checked else None,'student_system_sha256':hashlib.sha256(student.encode()).hexdigest(),'serialization_version':'counted-forks-think-tail-final-v4'}
(ROOT/'student-layout-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
assert checked,'No accepted pilot examples to validate'
