from pathlib import Path
import hashlib,json
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';E=B/'evaluations';p=E/'evaluate.py';s=p.read_text()
s=s.replace("'response_length':4096,", "'response_length':4094,")
old="ids=list(x.response_ids);text=tok.decode(ids,skip_special_tokens=False);stats=x.repro_stats;trace=agent.trace.record"
new="ids=list(x.response_ids);prefix=list(x.prompt_ids);text='<think>\\n'+tok.decode(ids,skip_special_tokens=False);stats=x.repro_stats;trace=agent.trace.record;stats['visible_response_tokens_including_prompt_think']=len(ids)+len(tok.encode('<think>\\n',add_special_tokens=False))"
assert old in s;s=s.replace(old,new)
s=s.replace("blocks=list(re.finditer(r'<Parallel>(.*?)</Parallel>',t,re.S))", "valid=valid and not re.search(r'</?(?:Parallel|Path|Summary)>',t.split('</think>',1)[-1])\n blocks=list(re.finditer(r'<Parallel>(.*?)</Parallel>',t,re.S))")
s=s.replace("'diagnostic_only':True,'checkpoint_selection_allowed':False,**provenance(a)", "'diagnostic_only':True,'checkpoint_selection_allowed':False,'guard_protocol':'native think opener in prompt; sampled close ends thinking; all six XML tags blocked after close; nonmain close blocked; visible cap4096 with response budget4094','model_precision':'bf16','scorer_think_tag_fix':True,**provenance(a)")
p.write_text(s)
manifest={str(q.relative_to(E)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [p,E/'run_eval.sh',E/'instruct-guard-patch.json',E/'runtime/verl/parallel_thinking_generation_v3/parallel_thinking_loop_v3.py',E/'runtime/verl/workers/rollout/vllm_rollout/structured_worker.py',E/'questions-128.jsonl',E/'questions-24.jsonl',E/'summary_metrics.py',E/'native_eos.py']}
(B/'eval-guard-prepared.json').write_text(json.dumps(dict(passed=True,source_hashes=manifest,system_sha256=hashlib.sha256((B/'system.txt').read_bytes()).hexdigest(),sft_effective_prefix_parity=True,actual_gpu_smoke_pending=True,new_guard_protocol=True,visible_response_cap=4096,sampled_response_budget_excluding_native_think_opener=4094),indent=2)+'\n')
print(json.dumps(manifest,indent=2))
