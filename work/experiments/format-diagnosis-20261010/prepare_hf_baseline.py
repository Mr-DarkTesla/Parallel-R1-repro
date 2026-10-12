from pathlib import Path
import shutil,hashlib,json,ast
P=Path.cwd();D=P/'work/experiments/instruct-token-warmup-20261010';F=P/'work/experiments/format-diagnosis-20261010';E=F/'evaluations';E.mkdir(exist_ok=False)
for p in (D/'evaluations').glob('*.py'):shutil.copy2(p,E/p.name)
for name in ['questions-24.jsonl','questions-128.jsonl']:shutil.copy2(D/'evaluations'/name,E/name)
shutil.copytree(D/'evaluations/runtime',E/'runtime',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
p=E/'evaluate.py';s=p.read_text();old="x=llm.generate(prompt_token_ids=[prefix],sampling_params=SamplingParams(temperature=.6,top_p=.95,top_k=20,max_tokens=4096-len(think),seed=seed,stop_token_ids=eos_ids),use_tqdm=False)[0];ids=think+list(x.outputs[0].token_ids);text=tok.decode(ids,skip_special_tokens=False);stats={'critical_depth':len(x.outputs[0].token_ids),'sampled_tokens':len(x.outputs[0].token_ids),'forced_tokens':len(think),'generated_tokens':len(x.outputs[0].token_ids),'generation_calls':1,'forks':0,'truncated':len(ids)>=4096,'invalid_width':False}"
new="generated=llm.llm_engine.collective_rpc('structured_generate',args=(prefix,dict(temperature=.6,top_p=.95,top_k=20,max_tokens=4096-len(think),seed=random.randrange(2**31),stop_token_ids=eos_ids,_evaluation_only=True),len(prefix),[-11,-12,-13,-14],tok.pad_token_id))[0];ids=think+list(generated);text=tok.decode(ids,skip_special_tokens=False);stats={'critical_depth':len(generated),'sampled_tokens':len(generated),'forced_tokens':len(think),'generated_tokens':len(generated),'generation_calls':1,'forks':0,'truncated':len(ids)>=4096,'invalid_width':False};trace={'backend':'native_thinking_HF_serial_SDPA','calls':[{'phase':'native_thinking','generated_ids':generated}], 'no_parallel_control_or_constraints':True}"
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("(out/'scores.jsonl').write_text", "summary['baseline_backend']='native_thinking_HF_serial_SDPA';summary['backend_labels']=['native_thinking_HF_serial_SDPA'];summary['constrained_decoding']=False\n (out/'scores.jsonl').write_text")
ast.parse(s);p.write_text(s)
shutil.copy2(D/'math-system.txt',F/'math-system.txt')
run=(D/'evaluations/run_eval.sh').read_text().replace('instruct-token-warmup-20261010/evaluations','format-diagnosis-20261010/evaluations').replace('warm4beval','warm4bcleanbaseline');(E/'run_eval.sh').write_text(run)
proof={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in E.rglob('*') if p.is_file()};(F/'hf-baseline-source-proof.json').write_text(json.dumps(dict(passed=True,base_evaluator_sha256=hashlib.sha256((D/'evaluations/evaluate.py').read_bytes()).hexdigest(),changes='Only native branch generation backend to frozen HF worker; no parallel controls, original weights/tokenizer; summary labels explicit',sha256=proof),indent=2)+'\n')
print('PREPARED',len(proof))
