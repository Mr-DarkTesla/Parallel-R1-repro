"""60 unseen questions with the explicit, wider scheduling prompt."""
import asyncio,hashlib,importlib.util,json,os,re,time
from pathlib import Path
import aiohttp
from transformers import AutoTokenizer
from layout import split_solution
from validate import validate,BLOCK

ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent.parent
OLD=BASE/'exps/deepseek-gsm-only-20261009'
CONVENTIONS='GSM-Infinite dataset conventions: For this self-contained problem, an unmentioned category at a location contributes zero. A total includes all relevant categories mentioned at that location. Total nominations or newborn children are sums of (number of films or adult animals) times (average nominations or children per member); totals of schools or adult animals sum the category counts.\n\n'
spec=importlib.util.spec_from_file_location('score',BASE/'exps/math500-new-sft-20261008/score.py');score=importlib.util.module_from_spec(spec);spec.loader.exec_module(score)
tok=AutoTokenizer.from_pretrained(BASE/'exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final',local_files_only=True)
FIELDS=['mathematically_correct','complete','independent_paths','plan_faithful','summary_faithful','useful_parallelism','scheduling_faithful','all_branch_outputs_used','no_given_only_paths','sufficient_explanation','verification_paths_valid']
def save(path,data):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');tmp.replace(path)
def append(path,data):
    with path.open('a') as f:f.write(json.dumps(data,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
def metrics(text):
    token=lambda s:len(tok.encode(s,add_special_tokens=False))
    cursor=0;serial=0;critical=0;path_totals=0;maxima=[];widths=[]
    for m in BLOCK.finditer(text):
        serial+=token(text[cursor:m.start()])+token('<Parallel>'+m[1]+'\n')+token('</Parallel>\n<Summary>'+m[3]+'</Summary>')
        paths=re.findall(r'<Path>[1-8]\n[\s\S]*?</Path>',m[2]);lengths=[token(b) for b in paths]
        maxima.append(max(lengths));path_totals+=sum(lengths);widths.append(int(m[1]));cursor=m.end()
    serial+=token(text[cursor:]);critical=serial+sum(maxima)
    return dict(total_tokens=token(text),sequential_tokens=serial,critical_path_tokens_proxy=critical,parallel_path_tokens=path_totals,path_max_tokens=maxima,rounds=len(widths),widths=widths)

def prepare():
    tasks=[json.loads(l) for l in (ROOT/'candidate-pool.jsonl').read_text().splitlines()][:60]
    assert len(tasks)==60 and len({r['id'] for r in tasks})==60
    old_records=[json.loads(l) for l in (OLD/'production/journal.jsonl').read_text().splitlines()]
    assert not ({r['id'] for r in tasks}&{r['id'] for r in old_records})
    (ROOT/'verification-pilot-tasks.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in tasks))
    return tasks

async def main():
    assert not (ROOT/'verification-pilot-results.jsonl').exists()
    tasks=[r for r in prepare() if r['verification_eligible']];save(ROOT/'verification-pilot-status.json',dict(state='waiting_for_capacity',total=len(tasks),completed=0,pilot_concurrency=8))
    sem=asyncio.Semaphore(8);status=dict(state='running',started_at=time.time(),total=len(tasks),completed=0,errors=0)
    timeout=aiohttp.ClientTimeout(total=2400,connect=30)
    async with aiohttp.ClientSession(timeout=timeout,connector=aiohttp.TCPConnector(limit=8)) as session:
        while json.loads((ROOT/'pilot-status.json').read_text())['completed']<4:
            await asyncio.sleep(5)
        save(ROOT/'verification-pilot-status.json',status)
        async def request(payload):
            for attempt in range(3):
                try:
                    async with session.post('http://127.0.0.1:8005/v1/chat/completions',json=payload) as r:
                        value=await r.json()
                        if r.status!=200:raise RuntimeError(f'HTTP {r.status}: {str(value)[:200]}')
                        return value
                except Exception:
                    if attempt==2:raise
                    await asyncio.sleep(3*(attempt+1))
        async def one(style,item):
            async with sem:
                row=dict(style=style,id=item['id'],started_at=time.time())
                try:
                    prompt=(ROOT/f'prompt-wide-{style}.txt').read_text()
                    response=await request(dict(model='deepseek-v4.1-flash',temperature=.6,top_p=.95,max_tokens=32768,seed=int(hashlib.sha256(item['id'].encode()).hexdigest()[:8],16)%2147483647,chat_template_kwargs={'enable_thinking':True,'reasoning_effort':50},messages=[{'role':'user','content':prompt.replace('{{INSERT_PROBLEM_HERE}}',item['question']).replace('{{VERIFICATION_POLICY}}',item['verification_policy'])}]))
                    append(ROOT/'verification-pilot-teacher-raw.jsonl',dict(style=style,id=item['id'],response=response,prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
                    choice=response['choices'][0];text=choice['message'].get('content') or '';shape=validate(text);shape.pop('blocks');grade=score.grade(text,item['reference']);row.update(output=text,structure=shape,grade=grade,metrics=metrics(text),finish_reason=choice['finish_reason'])
                    assert choice['finish_reason']=='stop' and shape['valid'] and grade['correct'] and not grade['error'], 'structural_or_answer_check'
                    system=(ROOT/'student-system.txt').read_text()
                    body,answer_line=split_solution(text)
                    prefix=tok.apply_chat_template([{'role':'system','content':system},{'role':'user','content':item['question']}],tokenize=False,add_generation_prompt=True)
                    tail=body+'\n</think>\n\n'+answer_line if prefix.rstrip().endswith('<think>') else '<think>\n'+body+'\n</think>\n\n'+answer_line
                    row['student_tokens']=len(tok.encode(prefix,add_special_tokens=False))+len(tok.encode(tail+tok.eos_token,add_special_tokens=False))
                    assert row['student_tokens']<=16384,'student_context_over_16384'
                    response=await request(dict(model='deepseek-v4.1-flash',temperature=0,top_p=1,max_tokens=16384,response_format={'type':'json_object'},chat_template_kwargs={'enable_thinking':True,'reasoning_effort':50},messages=[{'role':'system','content':(ROOT/'judge-prompt.txt').read_text()},{'role':'user','content':json.dumps(dict(problem=item['question'],reference_answer=item['reference'],candidate_solution=text),ensure_ascii=False)}]))
                    append(ROOT/'verification-pilot-judge-raw.jsonl',dict(style=style,id=item['id'],response=response));choice=response['choices'][0];assert choice['finish_reason']=='stop','judge_not_finished';verdict=json.loads(choice['message']['content']);row['judge']=verdict
                    row['accepted']=verdict.get('accept') is True and all(verdict.get(k) is True for k in FIELDS) and verdict.get('reference_suspect') is False and verdict.get('issues')==[]
                except Exception as e:row.update(accepted=False,error=repr(e));status['errors']+=1
                row['finished_at']=time.time();append(ROOT/'verification-pilot-results.jsonl',row);status['completed']+=1;save(ROOT/'verification-pilot-status.json',status);print(style,item['id'],row['accepted'],row.get('metrics'),row.get('error',''),flush=True)
        await asyncio.gather(*(one(style,item) for style in ['explicit'] for item in tasks))
    status.update(state='complete',finished_at=time.time());save(ROOT/'verification-pilot-status.json',status)

if __name__=='__main__':asyncio.run(main())
