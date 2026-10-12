from pathlib import Path
import json,hashlib,math,argparse
parser=argparse.ArgumentParser();parser.add_argument('--result',required=True);parser.add_argument('--output',required=True);args=parser.parse_args()
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';D=P/'work/experiments/rl-instruct-20261011'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for a in iter(lambda:f.read(8*1024*1024),b''):h.update(a)
 return h.hexdigest()
L=D/'long-run';result=Path(args.result);assert result.resolve()==(P/'work/experiments/night-20261010/cloud-continued/tmp2/results/307-instruct-rl-bs32-technical-step-resume.json').resolve();assert json.loads(result.read_text())['returncode']==0
technical=L/'actual-batch32-proof.json';proof=json.loads(technical.read_text());assert proof['passed'] and proof['state']=='passed' and proof['actual_8GPU_memory_pass'] and proof['clean_exits']
seal=L/'batch-proof-source-seal.json';sealed=json.loads(seal.read_text());assert all(sha(P/k)==v for k,v in sealed['sha256'].items())
evidence=[result,technical,seal,L/'batch-proof-root-approved.json',B/'independent-batch32-source-review.json',Path(__file__)]
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained(B/'runs/epoch1/final',local_files_only=True);system=(B/'system.txt').read_text();tags={tok.convert_tokens_to_ids(t) for t in ['<Parallel>','</Parallel>','<Path>','</Path>','<Summary>','</Summary>']};close=tok.encode('</think>',add_special_tokens=False)[0]
steps={}
for name,step in [('step1',1),('resume-step2',2)]:
 run=L/'batch-proof'/name;terminal=json.loads((run/'result.json').read_text());assert terminal['completed'] and terminal['world_size']==8 and terminal['steps']==step
 records=[json.loads(l) for l in (run/'metrics.jsonl').read_text().splitlines() if l.strip()];assert len(records)==1 and records[0]['step']==step;metrics=records[0]['ranks'];assert len(metrics)==8 and {m['rank'] for m in metrics}==set(range(8))
 peaks=[];update=[];drifts=[]
 for m in metrics:
  assert m['global_prompt_batch']==32 and m['global_rollouts']==128 and m['prompts_per_rank']==4 and m['within_prompt_group']==4
  assert len(m['prompt_advantages'])==4 and all(len(a)==4 and abs(sum(a))<1e-9 and all(math.isfinite(v) for v in a) for a in m['prompt_advantages'])
  assert m['step']==step and m['trainable']==4022468096 and m['optimizer_step'] and m['backbone_update_l2']>0 and m['optimizer_state_sharded']
  assert all(math.isfinite(m[k]) for k in ['loss','grad_norm','backbone_update_l2','max_replay_logp_drift','mean_replay_logp_drift','p95_replay_logp_drift'])
  assert m['max_replay_logp_drift']<=.01 and m['mean_replay_logp_drift']<=.002 and m['p95_replay_logp_drift']<=.005
  total=m['memory_stages'][0]['total'];assert 0<m['peak_gpu_bytes']<total;assert all(0<=s['allocated']<=s['reserved']<=s['total'] for s in m['memory_stages'])
  if step==2:
   rp=m['resume_proof'];assert rp['world_size']==8 and all(rp[k] for k in ['exact_local_adam_state','exact_cpu_rng','exact_cuda_rng','exact_python_rng']);assert 'Before validate' in rp['rng_identity_boundary']
  peaks.append(m['peak_gpu_bytes']);update.append(m['backbone_update_l2']);drifts.append(m['max_replay_logp_drift'])
 cfg=json.loads((run/'config.json').read_text());problems={r['id']:r['problem'] for r in [json.loads(l) for l in Path(cfg['train']).read_text().splitlines() if l.strip()]};trajectory_count=action_count=forced_count=call_count=postthink_count=0
 for rank in range(8):
  ts=[json.loads(l) for l in (run/f'traces-rank-{rank}.jsonl').read_text().splitlines() if l.strip()];assert len(ts)==16 and {(t['prompt_slot'],t['sample']) for t in ts}=={(i,j) for i in range(4) for j in range(4)} and all(t['rank']==rank and t['step']==step for t in ts)
  metric=next(m for m in metrics if m['rank']==rank)
  for slot in range(4):
   group=sorted([t for t in ts if t['prompt_slot']==slot],key=lambda t:t['sample']);rewards=[t['reward']['score'] for t in group];mean=sum(rewards)/4
   assert all(abs((v-mean)-a)<1e-10 for v,a in zip(rewards,metric['prompt_advantages'][slot]))
  evidence.append(run/f'traces-rank-{rank}.jsonl')
  for t in ts:
   text=tok.apply_chat_template([dict(role='system',content=system),dict(role='user',content=problems[t['id']])],tokenize=False,add_generation_prompt=True,enable_thinking=True)
   if text.endswith('<think>'):text+='\n'
   elif not text.endswith('<think>\n'):text+='<think>\n'
   assert t['prompt_ids']==tok.encode(text,add_special_tokens=False)
   mask=t['response_mask'];assert len(mask)==len(t['response_ids']) and all(x in (0,1) for x in mask);occupied=[0]*len(mask)
   for call in t['policy_calls']:
    raw=call['generated_ids'];start=call['response_start'];assert t['response_ids'][start:start+len(raw)]==raw;assert call['structure_start']==len(t['prompt_ids']);assert len(raw)==len(call['old_logprobs']) and all(math.isfinite(v) for v in call['old_logprobs'])
    blocked=set(call.get('blocked_token_ids',[]));assert not any(x in blocked for x in raw)
    if call['phase']!='main':assert close in blocked
    if close in call['prompt_ids'][len(t['prompt_ids']):]:assert tags<=blocked and call['phase']=='main';postthink_count+=1
    for index in range(start,start+len(raw)):
     assert 0<=index<len(mask) and mask[index]==1 and occupied[index]==0;occupied[index]=1
    call_count+=1;action_count+=len(raw)
   assert occupied==mask;trajectory_count+=1;forced_count+=len(mask)-sum(mask)
 checkpoint=run/f'checkpoint-{step:04}';complete=json.loads((checkpoint/'complete.json').read_text());assert complete['step']==step and complete['world_size']==8 and all(complete[k] for k in ['model','optimizer','rng'])
 for rank in range(8):
  assert (checkpoint/f'optimizer-rank-{rank}.pt').stat().st_size>0 and (checkpoint/f'rng-{rank}.pt').stat().st_size>0
 steps[str(step)]=dict(all8_finite_actual_updates=True,update_l2_per_rank=update,max_replay_drift_per_rank=drifts,peak_gpu_bytes_per_rank=peaks,exact_all8_adam_cpu_cuda_python_rng_resume=(step==2),trajectory_count=trajectory_count,raw_policy_calls_checked=call_count,sampled_actions_checked=action_count,forced_tokens_excluded=forced_count,actual_postthink_guard_calls=postthink_count,prefix_and_raw_action_mask_exact=True)
 evidence.extend([run/'result.json',run/'metrics.jsonl',checkpoint/'complete.json',run/'config.json'])
assert proof['source_seal_sha256']==sha(seal)
review=json.loads((B/'independent-batch32-source-review.json').read_text());assert review['passed'] and review['batch_proof_source_seal_sha256']==sha(seal)
report=dict(passed=True,scope='Actual retained8GPU32prompt128response engineering save/resume admission; not quality result',actual_8GPU_memory_pass=True,actual_batch32_proof_sha256=sha(technical),predecessor_result_sha256=sha(result),source_seal_sha256=sha(seal),world_size=8,steps=steps,clean_launcher_and_nccl_exit=True,gpus_empty_after_each_launcher='Asserted by hashed technical launcher before emitting passed; next production launcher rechecks fresh empty inventory',rng_boundary='Exact saved state restored before validation; per-call actions use explicit seeds',evidence_sha256={str(p.relative_to(P)):sha(p) for p in evidence})
out=Path(args.output);assert out.resolve().is_relative_to(P.resolve());tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(report,indent=2)+'\n');tmp.replace(out);print(json.dumps({k:v for k,v in report.items() if k!='evidence_sha256'},indent=2))
