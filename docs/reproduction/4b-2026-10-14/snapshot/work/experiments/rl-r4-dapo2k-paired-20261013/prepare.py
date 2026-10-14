from pathlib import Path
import os,json,shutil,ast,hashlib,time
R=Path('${PROJECT_ROOT}');os.chdir(R)
P=R/'work/experiments/rl-r4-posteval-20261013';P.mkdir(exist_ok=True)
S=R/'work/experiments/eval-intermediates-vllm-rolling-32k-20261013/templates';base=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013'
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
engine=P/'engine';shutil.copytree(base/'engine',engine,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
worker=(S/'worker.py').read_text().replace('0<=a.rank<32',"0<=a.rank<job['world_size']").replace('32768','32000')
worker=worker.replace('client,eos,32000,768,40960',"client,eos,32000,job['path_budget'],40960").replace('path_budget=768',"path_budget=job['path_budget']")
(P/'worker.py').write_text(worker)
final=(S/'finalize.py').read_text().replace("E=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013'","E=Path(__import__('sys').argv[1])")
final=final.replace('range(32)',"range(job['world_size'])").replace('checkpoint=300',"checkpoint=job['checkpoint']").replace('all32exit0=True','all16exit0=True').replace('32768','32000')
final=final.replace("response_budget=32000,max_context=40960","response_budget=32000,path_budget=4000,max_context=40960")
(P/'finalize.py').write_text(final)
controller=(S/'controller.py').read_text().replace("E=R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013'","E=Path(os.sys.argv[os.sys.argv.index('--root')+1])")
controller=controller.replace("parser.add_argument('--node',required=True,type=int)","parser.add_argument('--root',required=True);parser.add_argument('--node',required=True,type=int)")
controller=controller.replace("['mpimaster-0','mpiworker-0','mpiworker-1','mpiworker-2']","['mpimaster-0','mpiworker-0']").replace('0<=node<4','0<=node<2').replace('range(4)','range(2)').replace('all32exit0=True','all16exit0=True')
controller=controller.replace("str(E/'finalize.py')],cwd=R","str(E/'finalize.py'),str(E)],cwd=R").replace('checkpoint=300',"checkpoint=json.loads((E/'job.json').read_text())['checkpoint']")
(P/'controller.py').write_text(controller)
questions=[json.loads(l) for l in (base/'questions.jsonl').read_text().splitlines()]
assert len(questions)==590
for row in questions:row.update(response_budget=32000,max_context=40960,path_budget=4000)
(P/'questions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in questions))
job=json.loads((base/'job.json').read_text());job.update(world_size=16,precision='BF16',response_budget=32000,path_budget=4000,max_context=40960,engine_runtime=str(engine),questions_per_gpu=4,aggregate_rows=16,slot_capacity=196608,backend='vLLM structured DAG BF16 rolling4',protocol='ALL590 n1 temperature1 top_p1 response32000 path4000 context40960; identical original question seeds, all BF16, full traces',selection_allowed=False,full_traces=True)
job.pop('job_id',None);save(P/'job-template.json',job)
for label,outer,target,steps in [('sft',R/'work/experiments/rl-r4-dapo2k-sft-16gpu-20261013',200,[50,100,150,200]),('rl300',R/'work/experiments/rl-r4-dapo2k-rl300-16gpu-scheduled-20261013',400,[350,400])]:
 Q=P/label;Q.mkdir();save(Q/'config.json',dict(lane=label,root=str(Q),training_outer=str(outer),training_target=target,checkpoints=steps,world_size=16,nodes=2,eval_template=str(P),new_allocation_only_after_own_training_complete=True,must_not_touch_other_lane=True,counts={'MATH500':500,'AIME2024':30,'AIME2025':30,'AIME2026':30},user_authorization='Automatically eval allsavedcheckpoints aftereachRLcompletes',created_at=time.time()))
for f in [P/'worker.py',P/'finalize.py',P/'controller.py',*(P/'engine').rglob('*.py')]:ast.parse(f.read_text(),filename=str(f))
files=[P/'worker.py',P/'finalize.py',P/'controller.py',P/'questions.jsonl',P/'job-template.json',*(P/'engine').rglob('*.py')]
save(P/'source-seal.json',dict(passed=True,sha256={str(f):sha(f) for f in files},fresh_GPU_test=False,existing_rolling_engine=True,time=time.time()))
print(json.dumps(dict(prepared=True,lanes=['sft','rl300'],checkpoints=[50,100,150,200,350,400],tasks_per_checkpoint=590)))
