"""Gold-blind teacher corroboration; source evidence and raw responses retained."""
from pathlib import Path
import concurrent.futures as cf
import collections, hashlib, importlib.util, json, os, random, re, requests, signal, subprocess, time

R=Path.cwd();B=R/'work/experiments/rl-r2-24gpu-20261012';D=B/'data'
load=lambda p:list(map(json.loads,p.read_text().splitlines()))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    t=p.with_suffix('.tmp');t.write_text(json.dumps(x,indent=2));os.replace(t,p)
while not (D/'candidates.jsonl').exists():time.sleep(5)
while True:
    try:
        x=requests.get('http://127.0.0.1:8005/v1/models',timeout=5);x.raise_for_status();break
    except requests.RequestException:time.sleep(10)
spec=importlib.util.spec_from_file_location('scorer',R/'work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py')
scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer)
assert scorer.check()==13
raw=D/'teacher-raw';raw.mkdir(exist_ok=True)
reviewed=load(D/'reviewed.jsonl');candidates=load(D/'candidates.jsonl')
accepted={r['id']:r for r in reviewed};verdicts=[]
counts=collections.Counter(r['source'] for r in accepted.values())
def verify(row):
    ident=row['id'];path=raw/(ident.replace('/','_')+'.json')
    body=dict(model='deepseek-v4.1-flash',messages=[dict(role='system',content='Solve the supplied mathematics problem independently. Check all constraints and whether the answer is uniquely determined. Give a concise derivation followed by <status>OK</status><final>your exact mathematical answer</final>. If the problem is ambiguous or incomplete, use <status>AMBIGUOUS</status>. Do not guess. The final field must contain only the answer, with no explanation.'),dict(role='user',content=row['problem'])],temperature=0,max_tokens=4096,chat_template_kwargs={'thinking':False})
    if path.exists():response=json.loads(path.read_text())
    else:
        response=None
        for retry in range(3):
            try:
                request=requests.post('http://127.0.0.1:8005/v1/chat/completions',json=body,timeout=600);request.raise_for_status();response=request.json();break
            except requests.RequestException:
                if retry==2:raise
                time.sleep(3)
        save(path,response)
    choice=response['choices'][0];text=choice['message'].get('content') or ''
    finals=re.findall(r'<final>(.*?)</final>',text,re.S)
    good=choice.get('finish_reason')=='stop' and '<status>OK</status>' in text and len(finals)==1
    verdict=dict(id=ident,problem_sha256=hashlib.sha256(row['problem'].encode()).hexdigest(),raw_sha256=sha(path),finish_reason=choice.get('finish_reason'),teacher_answer=finals[0].strip() if len(finals)==1 else None,status='rejected',gold_blind=True)
    if good:
        grade=scorer.grade('Final Answer: \\boxed{'+finals[0].strip()+'}',row['answer'])
        verdict['comparison']=grade
        if grade.get('error'):verdict['status']='unknown_parser'
        elif grade['correct'] and grade['valid']:verdict['status']='corroborated'
    return row,verdict
with (D/'teacher-verdicts.jsonl').open('a',buffering=1) as ledger,cf.ThreadPoolExecutor(max_workers=96) as pool:
    pending={};cursor=0
    while min(counts.get(s,0) for s in ['cn_k12','orca_math'])<512:
        while len(pending)<96 and cursor<len(candidates):
            row=candidates[cursor];cursor+=1
            if counts[row['source']]<512:pending[pool.submit(verify,row)]=row
        if not pending:raise RuntimeError('Not enough independently corroborated public examples: '+str(counts))
        done,_=cf.wait(pending,return_when=cf.FIRST_COMPLETED)
        for future in done:
            del pending[future]
            row,verdict=future.result();verdicts.append(verdict);ledger.write(json.dumps(verdict)+'\n')
            if verdict['status']=='corroborated' and counts[row['source']]<512:
                accepted[row['id']]={**row,'reference_review':'source_gold_blind_teacher_agreement','teacher_verdict_sha256':hashlib.sha256(json.dumps(verdict,sort_keys=True).encode()).hexdigest()};counts[row['source']]+=1
        save(D/'status.json',dict(state='verifying',accepted=dict(counts),completed=len(verdicts),running=len(pending),target=1024))
    # Drain only already dispatched requests; their raw evidence remains useful.
    for future in cf.as_completed(pending):
        row,verdict=future.result();verdicts.append(verdict);ledger.write(json.dumps(verdict)+'\n')
train=list(accepted.values());assert len(train)==1024 and counts=={'cn_k12':512,'orca_math':512}
random.Random(20261012).shuffle(train)
val=load(D/'val.jsonl');pilot=load(D/'pilot.jsonl')
groups=[{r['split_group'] for r in rows} for rows in [train,val,pilot]]
assert all(not(groups[i]&groups[j]) for i in range(3) for j in range(i))
assert len(groups[0])==1024 and len({r['id'] for r in train})==1024
assert {r['id'] for r in load(R/'work/experiments/rl-instruct-20261011/data/revision2/train.jsonl')}<={r['id'] for r in train}
for row in train+val+pilot:
    grade=scorer.grade('Final Answer: \\boxed{'+row['answer']+'}',row['answer'])
    if grade.get('error') or not grade['correct'] or not grade['valid']:raise ValueError('Reference parser incompatible: '+row['id'])
(D/'train.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in train))
manifest=dict(passed=True,train=1024,val=len(val),pilot=len(pilot),sources=dict(counts),previous128_preserved=True,group_disjoint=True,benchmark_selection=False,preparation_sha256=sha(D/'preparation.json'),train_sha256=sha(D/'train.jsonl'),val_sha256=sha(D/'val.jsonl'),teacher_verdicts_sha256=sha(D/'teacher-verdicts.jsonl'),new_gold_blind_teacher_corroborated=sum(r.get('reference_review')=='source_gold_blind_teacher_agreement' for r in train),prior_reviewed=sum(r.get('reference_review')!='source_gold_blind_teacher_agreement' for r in train),rejected_or_unknown=sum(v['status']!='corroborated' for v in verdicts),limitations=['Teacher agreement corroborates references; it is not an exact oracle or proof that every semantic paraphrase of benchmarks is absent.','Published original per-item source URLs unavailable; only pinned CNK12/Orca whitelisted.'],scorer_sha256=sha(R/'work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py'))
save(D/'manifest.json',manifest);save(D/'status.json',dict(state='complete',train=1024))
# The known teacher process and its process group belong to this isolated audit.
teacher=json.loads((B/'teacher-launch.json').read_text());pid=teacher['pid']
cmd=Path(f'/proc/{pid}/cmdline').read_bytes().decode(errors='replace')
assert 'vllm.entrypoints.openai.api_server' in cmd and 'deepseek-v4.1-flash' in cmd
os.killpg(pid,signal.SIGTERM)
for _ in range(120):
    if not subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True).strip():break
    time.sleep(5)
else:raise RuntimeError('Teacher GPU processes did not drain')
save(B/'teacher-drained.json',dict(passed=True,pid=pid,empty_gpu=True,time=time.time()))
print(json.dumps(manifest),flush=True)
