"""Durable new data arm. Pilot is exactly 50; production requires root review."""
from pathlib import Path
import argparse, asyncio, collections, fcntl, hashlib, importlib.util, json, os, re, time, traceback
import aiohttp
from transformers import AutoTokenizer
from arithmetic_check import check as arithmetic_check
from oracle_check import check as oracle_check

P=Path.cwd();B=P/'work/experiments/deep-sft-20261010'
OLD=P/'exps/deepseek-gsm-wide3000-v2-20261009'
spec=importlib.util.spec_from_file_location('old_validator',OLD/'validate.py')
validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)
spec=importlib.util.spec_from_file_location('old_scorer',P/'exps/math500-new-sft-20261008/score.py')
scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer)
FIELDS=['mathematically_correct','complete','independent_paths','plan_faithful','summary_faithful','useful_parallelism','scheduling_faithful','all_branch_outputs_used','no_given_only_paths','sufficient_explanation','verification_paths_valid']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def append(p,r):
    with p.open('a') as f:f.write(json.dumps(r,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
def save(p,r):
    q=p.with_suffix('.tmp');q.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');q.replace(p)

async def main(args):
    out=B/args.phase;out.mkdir(exist_ok=True)
    lock=(out/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if args.phase=='production':
        review=json.loads((B/'root-pilot-approved.json').read_text())
        assert review['approved'] is True and review['pilot_tasks']==50
        assert review['teacher_prompt_sha256']==sha(B/'teacher-prompt.txt')
        assert review['pilot_report_sha256']==sha(B/'pilot/report.json')
        assert review['pool_sha256']==sha(B/'candidate-pool.jsonl')
    model=P/'work/experiments/base-format-20261010/runs/production/final'
    tok=AutoTokenizer.from_pretrained(model,local_files_only=True)
    system=(P/'work/experiments/base-format-20261010/system.txt').read_text()
    prompt=(B/'teacher-prompt.txt').read_text();judge_prompt=(B/'judge-prompt.txt').read_text()
    source=B/('pilot-tasks.jsonl' if args.phase=='pilot' else 'candidate-pool.jsonl')
    tasks=[json.loads(l) for l in source.open()]
    oracle_path=B/'oracle-source.jsonl'
    oracles={r['id']:r for r in map(json.loads,oracle_path.read_text().splitlines())} if oracle_path.exists() else {}
    if args.phase=='pilot':assert len(tasks)==50
    if args.phase=='production':
        pilot=[json.loads(l) for l in (B/'pilot/journal.jsonl').open()]
        pilot_ids={r['id'] for r in pilot};tasks=[r for r in tasks if r['id'] not in pilot_ids]
    records=[json.loads(l) for l in (out/'journal.jsonl').open()] if (out/'journal.jsonl').exists() else []
    processed={r['id'] for r in records};accepted=[r['row'] for r in records if r['decision']=='accepted']
    counts=collections.Counter(r['decision'] for r in records);errors=collections.Counter(r.get('error','') for r in records if r['decision']=='rejected')
    tasks=[r for r in tasks if r['id'] not in processed];position=0;inflight=0
    target=50 if args.phase=='pilot' else args.target
    state=dict(state='waiting_for_teacher',pid=os.getpid(),phase=args.phase,started_at=time.time(),completed=len(records),accepted=len(accepted),target=target,concurrency=args.concurrency)
    def status():
        state.update(completed=sum(counts.values()),accepted=len(accepted),decisions=dict(counts),errors=dict(errors),inflight=inflight,updated_at=time.time())
        save(out/'status.json',state)
    status()
    timeout=aiohttp.ClientTimeout(total=2400,connect=30)
    async with aiohttp.ClientSession(timeout=timeout,connector=aiohttp.TCPConnector(limit=args.concurrency)) as session:
        # Bounded health check, safe to start while the 8 GPU teacher loads.
        deadline=time.monotonic()+2400
        while True:
            try:
                async with session.get(args.endpoint+'/models',timeout=aiohttp.ClientTimeout(total=10)) as response:
                    models=await response.json()
                    assert 'deepseek-v4.1-flash' in [r['id'] for r in models['data']]
                    break
            except Exception:
                if time.monotonic()>deadline:raise RuntimeError('teacher_not_ready_after_2400s')
                await asyncio.sleep(10)
        state['state']='running';status()
        async def request(payload):
            for attempt in range(3):
                try:
                    async with session.post(args.endpoint+'/chat/completions',json=payload) as response:
                        value=await response.json()
                        if response.status!=200:raise RuntimeError('teacher_HTTP_'+str(response.status))
                        return value
                except Exception:
                    if attempt==2:raise
                    await asyncio.sleep(3*(attempt+1))
        def metrics(text,shape):
            token=lambda t:len(tok.encode(t,add_special_tokens=False))
            cursor=0;serial=0;paths=[];maxima=[]
            for m in validator.BLOCK.finditer(text):
                body_paths=re.findall(r'<Path>[1-8]\n([\s\S]*?)</Path>',m[2]);lengths=[token(x) for x in body_paths]
                paths.extend(lengths);maxima.append(max(lengths));serial+=token(text[cursor:m.start()])+token('<Parallel>'+m[1]+'\n')+token('</Parallel><Summary>'+m[3]+'</Summary>');cursor=m.end()
            serial+=token(text[cursor:])
            return dict(rounds=shape['rounds'],widths=shape['widths'],path_tokens=paths,output_tokens=token(text),sequential_tokens=serial,critical_path_tokens_proxy=serial+sum(maxima))
        async def one(item):
            record=dict(id=item['id'],source=item['source'],started_at=time.time(),attempts=[])
            for attempt in range(args.attempts):
                r=dict(attempt=attempt+1)
                try:
                    content=prompt.replace('{{INSERT_PROBLEM_HERE}}',item['question'])
                    payload=dict(model='deepseek-v4.1-flash',messages=[dict(role='user',content=content)],temperature=.6,top_p=.95,max_tokens=32768,
                        seed=(int(hashlib.sha256(item['id'].encode()).hexdigest()[:8],16)+attempt)%2147483647,
                        chat_template_kwargs=dict(enable_thinking=True,reasoning_effort=50))
                    response=await request(payload);append(out/'teacher-responses.jsonl',dict(id=item['id'],attempt=attempt+1,response=response,prompt_sha256=sha(B/'teacher-prompt.txt')))
                    choice=response['choices'][0];text=choice['message'].get('content') or '';shape=validator.validate(text);blocks=shape.pop('blocks')
                    r.update(output=text,structure=shape,finish_reason=choice['finish_reason'],teacher_usage=response.get('usage'),metrics=metrics(text,shape))
                    if '<think>' in text or '</think>' in text:raise ValueError('outer_think')
                    if choice['finish_reason']!='stop':raise ValueError('unfinished')
                    if not shape['valid']:raise ValueError('structure/'+','.join(shape['errors']))
                    grade=scorer.grade(text,item['reference']);r['grade']=grade
                    if not grade['correct'] or grade['error']:raise ValueError('reference_answer')
                    arithmetic=arithmetic_check(text);r['arithmetic_check']=arithmetic
                    if arithmetic['mismatches']:raise ValueError('explicit_arithmetic_mismatch')
                    if item['id'] in oracles:
                        matches=list(validator.BLOCK.finditer(text))
                        assert len(matches)==len(blocks)
                        oracle_blocks=[dict(block,start=m.start(),end=m.end()) for block,m in zip(blocks,matches)]
                        replay=oracle_check(text,oracles[item['id']],oracle_blocks);r['oracle_replay']=replay
                        if replay['failures']:raise ValueError('independent_oracle_replay')
                    messages=[dict(role='system',content=system),dict(role='user',content=item['question'])]
                    prefix=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
                    # Instruction prose quotes forbidden tags; only the assistant wrapper matters.
                    assert prefix.endswith('Solution:\n')
                    # Match proven SFT serialization: sibling separators contain no whitespace.
                    def compact(m):
                        body=m.group(1);ix=body.index('<Path>');ps=re.findall(r'<Path>.*?</Path>',body,re.S)
                        assert not re.sub(r'<Path>.*?</Path>','',body[ix:],flags=re.S).strip()
                        return '<Parallel>'+body[:ix]+''.join(ps)+'</Parallel>'
                    text=re.sub(r'<Parallel>(.*?)</Parallel>',compact,text,flags=re.S)
                    student_tokens=len(tok.encode(prefix,add_special_tokens=False))+len(tok.encode(text+tok.eos_token,add_special_tokens=False));r['student_tokens']=student_tokens
                    if student_tokens>8192:raise ValueError('student_context_over_8192')
                    payload=dict(model='deepseek-v4.1-flash',temperature=0,top_p=1,max_tokens=16384,response_format=dict(type='json_object'),
                        chat_template_kwargs=dict(enable_thinking=True,reasoning_effort=50),messages=[dict(role='system',content=judge_prompt),dict(role='user',content=json.dumps(dict(problem=item['question'],reference_answer=item['reference'],candidate_solution=text),ensure_ascii=False))])
                    judge=await request(payload);append(out/'judge-responses.jsonl',dict(id=item['id'],attempt=attempt+1,response=judge))
                    choice=judge['choices'][0]
                    if choice['finish_reason']!='stop':raise ValueError('judge_unfinished')
                    verdict=json.loads(choice['message']['content']);r['judge']=verdict
                    if verdict.get('accept') is not True or any(verdict.get(k) is not True for k in FIELDS) or verdict.get('reference_suspect') is not False or verdict.get('issues')!=[]:raise ValueError('semantic_judge_reject')
                    deps=verdict.get('round_dependencies',[])
                    if any(not (1<=d['source_round']<d['target_round']<=shape['rounds']) for d in deps):raise ValueError('judge_dependency_schema')
                    # Preserve honest shallow traces. Selection never pretends their depth is 4.
                    selected=3<=shape['rounds']<=6 and 3<=sum(shape['widths'])/shape['rounds']<=5.5
                    if shape['rounds']>1:
                        targets={d['target_round'] for d in deps}
                        if not set(range(2,shape['rounds']+1))<=targets:raise ValueError('missing_meaningful_round_dependency')
                    r['selected_deep']=selected
                    row=dict(id=item['id'],source=item['source'],problem=item['question'],answer=item['reference'],response=text,prompt_messages=json.dumps(messages,ensure_ascii=False),
                        source_file=item['source_file'],source_row_index=item['source_row_index'],source_metadata={k:v for k,v in item.items() if k in ['source_dataset','source_revision','op','length','mode','template','d']},
                        split_group=item['split_group'],fork_count=shape['rounds'],branch_schedule=shape['widths'],student_tokens=student_tokens,metrics=r['metrics'],round_dependencies=deps,
                        verification=dict(final_answer=grade,explicit_arithmetic=arithmetic,semantic_judge=verdict,oracle_replay=r.get('oracle_replay')),teacher_model='deepseek-v4.1-flash',reasoning_effort=50,
                        prompt_sha256=sha(B/'teacher-prompt.txt'),serialization_version='base-no-think-v1')
                    # Pilot measures all valid traces; production target counts selected deep rows.
                    if args.phase=='production' and not selected:
                        append(out/'valid-shallow.jsonl',row);raise ValueError('valid_but_not_deep_distribution')
                    record.update(decision='accepted',row=row);record['attempts'].append(r);return record
                except Exception as error:
                    r['error']=str(error);record['attempts'].append(r)
                    if str(error)=='valid_but_not_deep_distribution':break
            record.update(decision='rejected',error=record['attempts'][-1].get('error','unknown'));return record
        async def worker():
            nonlocal position,inflight
            while position<len(tasks) and not (out/'STOP').exists():
                if args.phase=='production' and len(accepted)+inflight>=target:
                    if len(accepted)>=target:return
                    await asyncio.sleep(1);continue
                item=tasks[position];position+=1;inflight+=1;status()
                result=await one(item);inflight-=1;result['finished_at']=time.time();append(out/'journal.jsonl',result)
                counts[result['decision']]+=1
                if result['decision']=='accepted':accepted.append(result['row'])
                else:errors[result['error']]+=1
                status();print(item['id'],result['decision'],result.get('row',{}).get('branch_schedule'),result.get('error',''),flush=True)
        await asyncio.gather(*(worker() for _ in range(args.concurrency)))
    state.update(state='complete' if (sum(counts.values())==50 if args.phase=='pilot' else len(accepted)==target) else 'stopped' if (out/'STOP').exists() else 'pool_exhausted',finished_at=time.time());status()
    f=out/'accepted.jsonl';f.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in accepted))
    widths=[w for r in accepted for w in r['branch_schedule']];rounds=[r['fork_count'] for r in accepted];path_tokens=[t for r in accepted for t in r['metrics']['path_tokens']]
    import numpy as np
    def stats(xs):return dict(mean=float(np.mean(xs)),median=float(np.median(xs)),p95=float(np.percentile(xs,95)),max=int(max(xs))) if xs else None
    report=dict(phase=args.phase,completed=sum(counts.values()),accepted=len(accepted),rejected=counts['rejected'],errors=dict(errors),selected_deep=sum(3<=r['fork_count']<=6 and 3<=sum(r['branch_schedule'])/r['fork_count']<=5.5 for r in accepted),
        width=stats(widths),rounds=stats(rounds),width_histogram=dict(collections.Counter(widths)),round_histogram=dict(collections.Counter(rounds)),path_tokens=stats(path_tokens),
        output_tokens=stats([r['metrics']['output_tokens'] for r in accepted]),critical_path_tokens_proxy=stats([r['metrics']['critical_path_tokens_proxy'] for r in accepted]),
        explicit_scalar_equalities_checked=sum(r['verification']['explicit_arithmetic']['explicit_scalar_equalities_checked'] for r in accepted),
        mathematically_reference_verified=len(accepted),no_think=True,all_sibling_ids_structurally_consistent=True,
        hashes={str(p.name):sha(p) for p in [B/'teacher-prompt.txt',B/'judge-prompt.txt',B/'pool-manifest.json',B/'pilot-tasks.jsonl',out/'journal.jsonl',f]},
        limitations=['The teacher also acts as semantic judge; not independent proof of every governing relation.','Explicit arithmetic checker covers flat scalar equalities only.','Manual actual-trace review is mandatory before releasing production generation.','F is token critical-path proxy, not measured GPU latency.'])
    save(out/'report.json',report);print(json.dumps(report,indent=2),flush=True)
    if args.phase=='production' and len(accepted)==target:
        import pandas as pd
        groups=collections.defaultdict(list)
        for r in accepted:groups[r['split_group']].append(r)
        train=[];val=[]
        for key in sorted(groups):(val if len(val)+len(groups[key])<=300 else train).extend(groups[key])
        assert len(val)==300 and len(train)==target-300
        for split,rows in [('train',train),('val',val)]:
            (out/f'{split}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
            pd.DataFrame(rows).to_parquet(out/f'{split}.parquet',index=False)
        save(out/'data-manifest.json',dict(train=len(train),val=len(val),split_group_disjoint=True,hashes={f:sha(out/f) for f in ['train.jsonl','val.jsonl','train.parquet','val.parquet']}))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--phase',choices=['pilot','production'],required=True);a.add_argument('--concurrency',type=int,default=32);a.add_argument('--target',type=int,default=3000);a.add_argument('--attempts',type=int,default=2);a.add_argument('--endpoint',default='http://127.0.0.1:8005/v1');args=a.parse_args()
    try:asyncio.run(main(args))
    except BaseException as e:
        (B/args.phase).mkdir(exist_ok=True);save(B/args.phase/'fatal-error.json',dict(error=repr(e),traceback=traceback.format_exc(),at=time.time()));raise
