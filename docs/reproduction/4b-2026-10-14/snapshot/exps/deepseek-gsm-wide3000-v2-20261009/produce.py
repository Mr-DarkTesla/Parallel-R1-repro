"""Configurable generate -> verify -> judge pipeline with durable acceptance journal."""
import asyncio, collections, fcntl, hashlib, importlib.util, json, os, re, sys, time, traceback
from pathlib import Path
import aiohttp
from transformers import AutoTokenizer
from layout import split_solution
from validate import validate

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
OUT=ROOT/'production'
CONCURRENCY=int(os.environ.get('SFT_CONCURRENCY','64'))
assert 1 <= CONCURRENCY <= 256
WORKERS=256
TARGETS={'GSM_Infinite':3000}
spec=importlib.util.spec_from_file_location('scorer',BASE/'exps/math500-new-sft-20261008/score.py')
score=importlib.util.module_from_spec(spec);spec.loader.exec_module(score)
FIELDS=['mathematically_correct','complete','independent_paths','plan_faithful','summary_faithful','useful_parallelism','scheduling_faithful','all_branch_outputs_used','no_given_only_paths','sufficient_explanation','verification_paths_valid']

def append(path,row):
    with path.open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
def save(path,row):
    t=path.with_suffix('.tmp');t.write_text(json.dumps(row,indent=2,ensure_ascii=False)+'\n');t.replace(path)

async def main():
    OUT.mkdir(exist_ok=True)
    lock=(OUT/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    approval=json.loads((ROOT/'pilot-review.json').read_text())
    assert approval['production_ready'], 'Pilot has not passed review'
    prompt=(ROOT/approval['production_prompt']).read_text()
    assert hashlib.sha256(prompt.encode()).hexdigest()==approval['production_prompt_sha256']
    judge_prompt=(ROOT/'judge-prompt.txt').read_text()
    student=(ROOT/'student-system.txt').read_text()
    (OUT/'student-system.txt').write_text(student)
    tokenizer=AutoTokenizer.from_pretrained(BASE/'exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final',local_files_only=True)
    candidates=[json.loads(l) for l in (ROOT/'candidate-pool.jsonl').read_text().splitlines()]
    assert candidates and all(r['source']=='GSM_Infinite' for r in candidates)
    journals=[json.loads(l) for l in (OUT/'journal.jsonl').read_text().splitlines()] if (OUT/'journal.jsonl').exists() else []
    assert all(r['source']=='GSM_Infinite' for r in journals)
    processed={r['id'] for r in journals};counts=collections.Counter(r['source'] for r in journals if r['decision']=='accepted')
    round_counts=collections.Counter(r['row']['fork_count'] for r in journals if r['decision']=='accepted')
    width_counts=collections.Counter(w for r in journals if r['decision']=='accepted' for w in r['row']['branch_schedule'])
    pending={s:[r for r in candidates if r['source']==s and r['id'] not in processed] for s in TARGETS}
    positions=collections.Counter();inflight=collections.Counter()
    errors=collections.Counter(r.get('error','unknown').split('/')[0] for r in journals if r['decision']=='rejected')
    previous=json.loads((OUT/'status.json').read_text()) if (OUT/'status.json').exists() else {}
    state=dict(state='running',started_at=previous.get('started_at',time.time()),resumed_at=time.time(),pid=os.getpid(),concurrency=CONCURRENCY,reasoning_effort=50,
        targets=TARGETS,accepted=dict(counts),processed=len(processed),active_requests=0,max_active_requests=0)
    last_limit_read=0.0
    def concurrency_limit():
        nonlocal last_limit_read
        if time.monotonic()-last_limit_read>=1:
            config=OUT/'concurrency.json'
            if config.exists():
                limit=json.loads(config.read_text())['concurrency']
                assert isinstance(limit,int) and 1<=limit<=WORKERS
                state['concurrency']=limit
            last_limit_read=time.monotonic()
        return state['concurrency']
    def status():
        state.update(accepted=dict(counts),processed=len(processed),inflight=dict(inflight),errors=dict(errors),
            accepted_round_histogram=dict(round_counts),accepted_width_histogram=dict(width_counts),updated_at=time.time())
        save(OUT/'status.json',state)
    status()
    def pick():
        eligible=[s for s in TARGETS if counts[s]+inflight[s]<TARGETS[s] and positions[s]<len(pending[s])]
        if not eligible:return None
        s=min(eligible,key=lambda s:(counts[s]+inflight[s])/TARGETS[s])
        r=pending[s][positions[s]];positions[s]+=1;inflight[s]+=1;return r
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2400,connect=30),connector=aiohttp.TCPConnector(limit=WORKERS)) as session:
        async def request(payload):
            for attempt in range(3):
                while state['active_requests']>=concurrency_limit():await asyncio.sleep(.2)
                state['active_requests']+=1;state['max_active_requests']=max(state['max_active_requests'],state['active_requests'])
                try:
                    async with session.post('http://127.0.0.1:8005/v1/chat/completions',json=payload) as res:
                        b=await res.json()
                        if res.status!=200:raise RuntimeError(f'HTTP {res.status}: {str(b)[:350]}')
                    return b
                except Exception:
                    if attempt==2:raise
                    await asyncio.sleep(3*(attempt+1))
                finally:state['active_requests']-=1
        async def worker():
            while not (OUT/'STOP').exists():
                item=pick()
                if item is None:
                    if any(inflight.values()):await asyncio.sleep(2);continue
                    return
                start=time.time();ident=item['id'];source=item['source']
                record=dict(id=ident,source=source,started_at=start)
                try:
                    payload=dict(model='deepseek-v4.1-flash',messages=[{'role':'user','content':prompt.replace('{{INSERT_PROBLEM_HERE}}',item['question']).replace('{{VERIFICATION_POLICY}}',item['verification_policy'])}],
                        temperature=.6,top_p=.95,max_tokens=32768,seed=int(hashlib.sha256(ident.encode()).hexdigest()[:8],16)%2147483647,
                        chat_template_kwargs={'enable_thinking':True,'reasoning_effort':50})
                    response=await request(payload)
                    choice=response['choices'][0];text=choice['message'].get('content') or ''
                    append(OUT/'teacher-responses.jsonl',dict(id=ident,response=response,request={k:v for k,v in payload.items() if k!='messages'}))
                    shape=validate(text);shape.pop('blocks')
                    record.update(structure=shape,teacher_usage=response.get('usage'),finish_reason=choice.get('finish_reason'))
                    if choice.get('finish_reason')!='stop':raise ValueError('generation_not_finished')
                    if not shape['valid']:raise ValueError('structure/'+','.join(shape['errors']))
                    grade=score.grade(text,item['reference']);record['grade']=grade
                    if not grade['correct'] or grade['error']:raise ValueError('answer_verification')
                    messages=[{'role':'system','content':student},{'role':'user','content':item['question']},{'role':'assistant','content':text}]
                    body,answer_line=split_solution(text)
                    prefix=tokenizer.apply_chat_template(messages[:-1],tokenize=False,add_generation_prompt=True)
                    tail=body+'\n</think>\n\n'+answer_line if prefix.rstrip().endswith('<think>') else '<think>\n'+body+'\n</think>\n\n'+answer_line
                    token_count=len(tokenizer.encode(prefix,add_special_tokens=False))+len(tokenizer.encode(tail+tokenizer.eos_token,add_special_tokens=False))
                    record['student_tokens']=token_count
                    if token_count>16384:raise ValueError('student_context_over_16384')
                    payload=dict(model='deepseek-v4.1-flash',temperature=0,top_p=1,max_tokens=16384,
                        response_format={'type':'json_object'},
                        chat_template_kwargs={'enable_thinking':True,'reasoning_effort':50},
                        messages=[{'role':'system','content':judge_prompt},{'role':'user','content':json.dumps({'problem':item['question'],'reference_answer':item['reference'],'candidate_solution':text},ensure_ascii=False)}])
                    judge_response=await request(payload)
                    append(OUT/'judge-responses.jsonl',dict(id=ident,response=judge_response))
                    choice=judge_response['choices'][0]
                    if choice.get('finish_reason')!='stop':raise ValueError('judge_not_finished')
                    verdict=json.loads(choice['message']['content']);record['judge']=verdict
                    if verdict.get('accept') is not True or any(verdict.get(k) is not True for k in FIELDS) or verdict.get('reference_suspect') is not False or verdict.get('issues')!=[]:
                        raise ValueError('semantic_judge_reject')
                    row=dict(id=ident,source=source,source_file=item['source_file'],source_row_index=item['source_row_index'],
                        source_metadata={k:item[k] for k in ['source_dataset','source_revision','original_source_file','original_source_row_index','old_branch_schedule','op','length','mode','template','d'] if k in item},
                        problem=item['question'],answer=item['reference'],response=text,messages=messages,
                        prompt_messages=json.dumps(messages[:-1],ensure_ascii=False),split_group=item['split_group'],
                        fork_count=shape['rounds'],branch_schedule=shape['widths'],student_tokens=token_count,
                        teacher_model='deepseek-v4.1-flash',reasoning_effort=50,prompt_sha256=approval['production_prompt_sha256'],
                        student_system_sha256=hashlib.sha256(student.encode()).hexdigest(),serialization_version='counted-forks-v1',
                        verification={'final_answer':'Math-Verify 0.8.0','structure':True,'semantic_judge':verdict})
                    record.update(decision='accepted',row=row)
                    counts[source]+=1
                    round_counts[shape['rounds']]+=1;width_counts.update(shape['widths'])
                except Exception as error:
                    message=str(error);errors[message.split('/')[0]]+=1
                    record.update(decision='rejected',error=message)
                record['finished_at']=time.time();append(OUT/'journal.jsonl',record)
                processed.add(ident);inflight[source]-=1;status()
                print(ident,record['decision'],dict(counts),record.get('error',''),flush=True)
        async def heartbeat():
            while True:
                concurrency_limit();status();await asyncio.sleep(15)
        ticker=asyncio.create_task(heartbeat())
        try:await asyncio.gather(*(worker() for _ in range(WORKERS)))
        finally:
            ticker.cancel()
            await asyncio.gather(ticker,return_exceptions=True)
    accepted=[r['row'] for r in map(json.loads,(OUT/'journal.jsonl').read_text().splitlines()) if r['decision']=='accepted']
    assert len({r['id'] for r in accepted})==len(accepted)
    (OUT/'accepted.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in accepted))
    complete=all(counts[s]==n for s,n in TARGETS.items())
    state.update(state='complete' if complete else 'stopped' if (OUT/'STOP').exists() else 'pool_exhausted',finished_at=time.time());status()
    if complete:
        import pandas as pd
        groups=collections.defaultdict(list)
        for r in accepted:groups[r['split_group']].append(r)
        val=[];train=[]
        for key in sorted(groups):
            (val if len(val)+len(groups[key])<=300 else train).extend(groups[key])
        assert len(val)==300 and len(train)==2700
        for split,rows in [('train',train),('val',val)]:
            (OUT/f'{split}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
            pd.DataFrame([{k:r[k] for k in ['id','problem','answer','response','prompt_messages','source','fork_count','branch_schedule','student_tokens']} for r in rows]).to_parquet(OUT/f'{split}.parquet',index=False)
        report=dict(complete=True,accepted=len(accepted),sources=dict(counts),train=2700,val=300,
            rounds=dict(collections.Counter(r['fork_count'] for r in accepted)),widths=dict(collections.Counter(w for r in accepted for w in r['branch_schedule'])),
            total_requests_max_concurrency=state['max_active_requests'],rejections=dict(errors),
            mean_width_target=None,mean_width_actual=sum(sum(r['branch_schedule']) for r in accepted)/sum(r['fork_count'] for r in accepted),valid_narrow_traces_preserved=str(OUT/'valid-narrow-deferred.jsonl'),limitations=['Semantic judge uses the same teacher model and is not a formal proof checker.','Decontamination is textual, not a guarantee against semantic paraphrases.','Serving inference was teacher serialization, not separate isolated worker generation.','Requires counted-fork-aware SFT loader and rollout runtime.'],
            sha256={f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in ['train.jsonl','val.jsonl','train.parquet','val.parquet']})
        save(OUT/'summary.json',report);(OUT/'COMPLETED').write_text(str(time.time())+'\n')

if __name__=='__main__':
    try:asyncio.run(main())
    except BaseException as error:
        if OUT.exists():save(OUT/'fatal-error.json',dict(error=repr(error),traceback=traceback.format_exc(),time=time.time()))
        raise
