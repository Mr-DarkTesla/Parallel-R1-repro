from pathlib import Path
import os,json,shutil,hashlib,ast,time
R=Path('${PROJECT_ROOT}');os.chdir(R)
E=R/'work/experiments/eval-rl300-random2-8gpu-20261014'
B=R/'work/experiments/rl-r4-posteval-20261013'
assert (E/'USER-AUTHORIZATION.json').exists() and json.loads((E/'source-deleted.json').read_text())['passed']
assert not (E/'job.json').exists(), 'Prepared once; reconcile before retry'
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8388608),b''):h.update(b)
 return h.hexdigest()
shutil.copytree(B/'engine',E/'engine',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
selector='''import hashlib,random
def choose_branches(question_seed,fork_index,requested_width):
    assert 2 <= requested_width <= 8
    selection_seed=int.from_bytes(hashlib.sha256(f"rl300-random2-v1:{question_seed}:{fork_index}".encode()).digest()[:8],"big")
    selected=sorted(random.Random(selection_seed).sample(range(1,requested_width+1),2)) if requested_width>2 else [1,2]
    return selected,selection_seed
'''
(E/'engine/branch_selection.py').write_text(selector)
namespace={};exec(selector,namespace)
for width in range(2,9):
 for seed in range(100):
  a,s=namespace['choose_branches'](seed,0,width)
  assert len(a)==2 and len(set(a))==2 and a==sorted(a) and all(1<=i<=width for i in a)
  assert namespace['choose_branches'](seed,0,width)==(a,s)
assert len({tuple(namespace['choose_branches'](s,0,4)[0]) for s in range(100)})==6
p=E/'engine/rollout.py';s=p.read_text()
s=s.replace('import copy\n','import copy\nfrom branch_selection import choose_branches\n')
s=s.replace('fork_batch_ledger = []','fork_batch_ledger = []\n    branch_selection_ledger = []\n    requested_widths = []')
old="""        prefixes = [[bo] + tokenizer.encode(str(i)+'\\n', add_special_tokens=False)
                    for i in range(1, width+1)]
        suffix = [pc] + newline + [so]
        overhead = sum(len(p)+1 for p in prefixes) + len(suffix) + 1
        budget = min(path_budget, (left()-overhead)//width)
"""
new="""        requested_width = width
        selected_ids, selection_seed = choose_branches(seed, len(widths), requested_width)
        all_prefixes = [[bo] + tokenizer.encode(str(i)+'\\n', add_special_tokens=False)
                       for i in range(1, requested_width+1)]
        prefixes = [all_prefixes[i-1] for i in selected_ids]
        suffix = [pc] + newline + [so]
        # Keep the original per-path budget calculation: pruning must not enlarge it.
        overhead = sum(len(p)+1 for p in all_prefixes) + len(suffix) + 1
        budget = min(path_budget, (left()-overhead)//requested_width)
        width = len(selected_ids)
"""
assert old in s;s=s.replace(old,new)
s=s.replace('seed=seed+(len(calls)+i)*1009) for i,prefix in enumerate(prefixes)]','seed=seed+(len(calls)+original_id-1)*1009) for original_id,prefix in zip(selected_ids,prefixes)]')
s=s.replace('fork_batch_ledger.append(batch_stats)',"""batch_stats.update(requested_width=requested_width, executed_width=width,
                               selected_original_path_ids=selected_ids, selection_seed=selection_seed)
            fork_batch_ledger.append(batch_stats)""")
s=s.replace('        widths.append(width)','''        widths.append(width)
        requested_widths.append(requested_width)
        branch_selection_ledger.append(dict(fork_index=len(widths)-1, requested_width=requested_width,
            executed_width=width, selected_original_path_ids=selected_ids,
            selection_seed=selection_seed, per_path_budget=budget, original_numeric_header_retained=True))''')
s=s.replace('fork_batch_ledger=fork_batch_ledger,','fork_batch_ledger=fork_batch_ledger, requested_widths=requested_widths,\n                branch_selection_ledger=branch_selection_ledger,')
p.write_text(s)
worker=(B/'worker.py').read_text()
worker=worker.replace("1<=x['requested_rows']<=8","x['requested_rows']==2")
needle="  trace.update(id=row['id']"
assert needle in worker
worker=worker.replace(needle,"""  assert trace['widths']==[2]*len(trace['branch_selection_ledger'])
  assert all(len(x['selected_original_path_ids'])==2 and len(set(x['selected_original_path_ids']))==2 for x in trace['branch_selection_ledger'])
  trace['intervention']='uniform_random_two_original_branches_without_replacement'
  trace.update(id=row['id']""")
worker=worker.replace("trace.update(grade=grade,technical_unknown=unknown,format_valid=valid,parallel_valid=parallel,finished_at=time.time())","trace.update(grade=grade,technical_unknown=unknown,format_valid=valid,parallel_valid=parallel,strict_format_may_fail_due_to_deliberate_missing_branches=True,finished_at=time.time())")
(E/'worker.py').write_text(worker)
controller=(B/'controller.py').read_text()
controller=controller.replace("['mpimaster-0','mpiworker-0']","['mpimaster-0']").replace('0<=node<2','0<=node<1').replace('range(2)','range(1)').replace('all16exit0','all8exit0')
(E/'controller.py').write_text(controller)
questions=[json.loads(l) for l in (B/'questions.jsonl').read_text().splitlines() if l.strip()]
assert len(questions)==590 and len({(x['dataset'],x['id']) for x in questions})==590
(E/'questions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in questions))
cp=R/'work/experiments/rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory/production/checkpoint-0300'
complete=json.loads((cp/'complete.json').read_text());assert complete['step']==300 and complete['weights_only'] and complete['all_master_finite']
for relative,d in complete['files'].items():assert sha(cp/relative)==d['sha256'],relative
modelsha=complete['files']['hf/model.safetensors']['sha256']
assert modelsha=='8b4921297d797c4a58c851abdb98ea6dd75eeb4c5af958e5292caa9e2681aa39'
job=json.loads((B/'job-template.json').read_text())
job.update(root=str(E),world_size=8,checkpoint=300,model=str(cp/'hf'),model_sha256=modelsha,
 questions=str(E/'questions.jsonl'),engine_runtime=str(E/'engine'),precision='BF16',
 branch_policy='uniform random two original branch IDs without replacement; preserve requested numeric header and original selected IDs; retain original per-path budget calculation',
 backend='vLLM structured DAG BF16 rolling4 random2',created_at=time.time())
save(E/'job.json',job)
(E/'control').mkdir();save(E/'control/queue.json',dict(next=0,leases={},completed=0))
shared=[Path(job[k]) for k in ['system','scorer']]
shared+=list(Path(job['runtime']).rglob('*.py'))
files=[*E.glob('*.py'),*E.joinpath('engine').rglob('*.py'),E/'job.json',E/'questions.jsonl',*shared]
for f in files:
 if f.suffix=='.py':ast.parse(f.read_text(),filename=str(f))
save(E/'source-seal.json',dict(passed=True,sha256={str(f):sha(f) for f in files},fresh_GPU_tests=False,CPU_selection_cases=700,full_checkpoint_manifest_verified=True))
save(E/'PREPARED.json',dict(passed=True,world_size=8,tasks=590,model_sha256=modelsha,selection_test_passed=True,no_new_GPU_tests=True,time=time.time()))
print(json.dumps(dict(prepared=True,gpus=8,tasks=590,model_sha256=modelsha)))
