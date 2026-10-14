"""CPU-only incremental/final analysis. Import isolated scorer before other packages."""
import score
import argparse,ast,collections,datetime as dt,hashlib,json,math,re,statistics
from pathlib import Path
WORK=Path(__file__).resolve().parent

def stats(values):
    a=sorted(values)
    if not a:return {'n':0}
    def q(p):
        x=(len(a)-1)*p;i=int(x);return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(x-i)
    return dict(n=len(a),sum=sum(a),mean=statistics.mean(a),median=statistics.median(a),p90=q(.9),p95=q(.95),max=max(a),min=min(a))
def tally(values):return dict(sorted(collections.Counter(str(x) for x in values).items()))
def rate(rows):
    n=len(rows);k=sum(r['grade']['correct'] for r in rows)
    return dict(n=n,correct=k,pass_at_1=k/n if n else None,ci95=score.wilson(k,n) if n else None,final_answer_only_correct=sum(r['grade']['final_answer_only']['correct'] for r in rows),final_answer_only_pass_at_1=sum(r['grade']['final_answer_only']['correct'] for r in rows)/n if n else None)

def think_format(text):
    tags=list(re.finditer(r'</?think>',text))
    good=len(tags)==2 and tags[0].group()=='<think>' and tags[1].group()=='</think>'
    forks=list(re.finditer(r'</?(?:Parallel|Path|Summary)>',text))
    within=good and all(tags[0].end()<=m.start()<tags[1].start() for m in forks)
    finals=list(re.finditer(r'(?i)Final\s+Answer\s*:',text))
    after=good and bool(finals) and finals[-1].start()>=tags[1].end()
    return dict(exactly_one_balanced_think=good,all_forks_inside_think=within,final_after_think=after,fully_valid=good and within and after)

def answer_format(text):
    headers=list(re.finditer(r'(?i)Final\s+Answer\s*:',text))
    lines=list(re.finditer(r'(?im)^\s*(?:\*\*)?Final\s+Answer(?:\*\*)?\s*:',text))
    tail=text[headers[-1].end():] if headers else ''
    paths=re.findall(r'<Path>\d+\n(.*?)</Path>',text,re.S)
    return dict(explicit_final_header=bool(headers),standalone_final_header=bool(lines),multiple_final_headers=len(headers)>1,boxed_after_final_header=bool(headers) and bool(re.search(r'\\(?:boxed|fbox)\s*\{',tail)),final_header_inside_path=any(re.search(r'(?i)Final\s+Answer\s*:',p) for p in paths),explicit_unresolved=bool(re.match(r'\s*unresolved\b',tail,re.I)))

def load():
    records=[]
    for f in sorted(WORK.glob('traces-*.jsonl')):
        for line in f.read_text().splitlines():
            try:records.append(json.loads(line))
            except json.JSONDecodeError:continue # Last line can be in flight.
    records.sort(key=lambda r:r['index'])
    assert len({r['id'] for r in records})==len(records),'Duplicate answers'
    return records

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--final',action='store_true');args=parser.parse_args()
    questions={q['id']:q for q in map(json.loads,(WORK/'questions.jsonl').read_text().splitlines())}
    manifest=json.loads((WORK/'manifest.json').read_text());force_prefix=manifest.get('force_think_prefix',False)
    rows=load()
    if args.final:assert len(rows)==500 and {r['id'] for r in rows}==set(questions)
    # Use exact production format checker without importing VERL/ANTLR dependencies.
    source=(WORK/'code/verl/utils/reward_score/counted_parallel.py').read_text();tree=ast.parse(source)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='check_format')
    scope={'re':re,'TAG':re.compile(r'</?Parallel>|</?Path>|</?Summary>')}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'<production-format-check>','exec'),scope)
    cachepath=WORK/'scores.jsonl';cache={}
    if cachepath.exists():cache={r['id']:r for r in map(json.loads,cachepath.read_text().splitlines())}
    derived=[];paths=[];widths=[];phases=collections.defaultdict(list);groups=[];errors=[];closures=collections.Counter();capped=collections.Counter()
    for r in rows:
        text=r['output'];digest=hashlib.sha256(text.encode()).hexdigest();cached=cache.get(r['id'])
        if cached and cached['output_sha256']==digest:g=cached
        else:
            primary=score.grade(text,questions[r['id']]['answer'])
            # Diagnostic removes think markup only, still uses reference-blind last-final extraction.
            diagnostic=score.grade(re.sub(r'</?think>','',text),questions[r['id']]['answer'])
            g=dict(id=r['id'],index=r['index'],output_sha256=digest,**primary,final_answer_only=diagnostic)
        r['grade']=g
        fmt,ws=scope['check_format'](text);widths.extend(ws)
        tc=r['trace']['calls'];pc=r['trace']['policy_calls'];assert len(tc)==len(pc)
        audit=[];forkpaths=[];prefix_failures=0;label_differences=0
        if force_prefix:
            ids=r['trace']['response_ids'];mask=r['trace']['response_mask']
            if ids[:2]!=[151667,198] or mask[:2]!=[0,0]:audit.append('missing_exogenous_initial_think')
            if r['trace'].get('forced_think_prefix_tokens')!=2:audit.append('forced_think_telemetry_mismatch')
            if pc and (pc[0]['response_start']!=2 or pc[0]['prompt_ids']!=r['trace']['prompt_ids']+[151667,198]):audit.append('first_context_missing_forced_think')

        for call,policy in zip(tc,pc):
            phase=call['phase'];raw=call['generated_ids'];phases[phase].append(len(raw))
            if len(raw)==call['sampling_params']['max_tokens']:capped[phase]+=1
            if raw and raw[-1]==151643:closures[phase+'_sampled_eos']+=1
            offset=policy['response_start'];actual=r['trace']['response_ids'][offset:offset+len(raw)]
            expected=list(raw)
            if phase=='path' and expected and expected[-1] in [151643,151669,151671,151672,151673,151674]:expected[-1]=151670
            if phase=='summary' and expected and expected[-1] in [151643,151671,151672,151669,151670,151673]:expected[-1]=151674
            if actual!=expected:audit.append('assembled_labels_mismatch')
            if raw!=policy['generated_ids']:audit.append('sampled_labels_mutated')
            label_differences+=sum(a!=b for a,b in zip(actual,raw))
            if not all(r['trace']['response_mask'][offset:offset+len(raw)]):audit.append('sampled_token_masked_out')
            if phase=='path':forkpaths.append(policy)
            elif forkpaths:
                bases=[p['prompt_ids'][:-3] for p in forkpaths]
                if any(b!=bases[0] for b in bases):prefix_failures+=1
                if [p['prompt_ids'][-3] for p in forkpaths]!=[151669]*len(forkpaths):audit.append('path_opening_not_expected')
                groups.append(dict(id=r['id'],width=len(forkpaths),prefixes_identical=all(b==bases[0] for b in bases)));forkpaths=[]
        if forkpaths:
            bases=[p['prompt_ids'][:-3] for p in forkpaths]
            if any(b!=bases[0] for b in bases):prefix_failures+=1
            groups.append(dict(id=r['id'],width=len(forkpaths),prefixes_identical=all(b==bases[0] for b in bases)))
            if not r['repro_stats']['truncated']:audit.append('paths_without_summary_call_before_budget_exhaustion')
        if prefix_failures:audit.append('sibling_prefix_mismatch')
        assert sum(r['trace']['response_mask'])==r['sampled_tokens']
        assert sum(len(c['generated_ids']) for c in tc)==r['sampled_tokens']
        if audit:errors.append(dict(id=r['id'],issues=audit))
        found=re.findall(r'<Path>(\d+)\n(.*?)</Path>',text,re.S)
        norms=[re.sub(r'\s+',' ',s).strip() for _,s in found]
        duplicates=sum(n-1 for n in collections.Counter(norms).values() if n>1)
        for branch,body in found:
            words=re.findall(r'\w+',body.lower());grams=[tuple(words[i:i+5]) for i in range(max(0,len(words)-4))]
            paths.append(dict(id=r['id'],branch=int(branch),chars=len(body),repeat_5gram_fraction=1-len(set(grams))/len(grams) if grams else 0))
        d=dict(id=r['id'],index=r['index'],subject=r['subject'],level=r['level'],grade=g,response_tokens=r['response_tokens'],sampled_tokens=r['sampled_tokens'],forced_tokens=r['response_tokens']-r['sampled_tokens'],forks=r['repro_stats']['forks'],widths=ws,format_errors=fmt,invalid_width=r['repro_stats']['invalid_width'],budget_exhausted=r['repro_stats']['truncated'],critical_depth=r['repro_stats']['critical_depth'],sampled_work_over_critical_depth=r['sampled_tokens']/max(1,r['repro_stats']['critical_depth']),elapsed_seconds=r['elapsed_seconds'],generation_calls=len(tc),closure_label_replacements=label_differences,exact_duplicate_paths_within_trace=duplicates,think_open_count=text.count('<think>'),think_close_count=text.count('</think>'),think_structure=think_format(text),answer_format=answer_format(text))
        derived.append(d)
    cachepath.write_text(''.join(json.dumps(r['grade'],ensure_ascii=False)+'\n' for r in rows))
    (WORK/'trace-statistics.jsonl').write_text(''.join(json.dumps(d,ensure_ascii=False)+'\n' for d in derived))
    n=len(rows);k=sum(r['grade']['correct'] for r in rows);errorrows=[r['grade'] for r in rows if r['grade']['error']]
    out=dict(force_think_prefix=force_prefix,forced_initial_prefix_action_mask=0,state='complete' if args.final and not errorrows and not errors else 'partial',updated_at=dt.datetime.now(dt.timezone.utc).isoformat(),questions=n,total_questions=500,samples_per_question=1,correct=k,pass_at_1=k/n if n else None,ci95=score.wilson(k,n) if n else None,invalid_answers=sum(not r['grade']['valid'] for r in rows),extraction=tally(r['grade']['extraction'] for r in rows),scorer_errors=errorrows,
        final_answer_only_diagnostic=dict(correct=sum(r['grade']['final_answer_only']['correct'] for r in rows),pass_at_1=sum(r['grade']['final_answer_only']['correct'] for r in rows)/n if n else None,ci95=score.wilson(sum(r['grade']['final_answer_only']['correct'] for r in rows),n) if n else None,invalid_answers=sum(not r['grade']['final_answer_only']['valid'] for r in rows),description='Primary answer-equivalence metric: remove think tags before the same reference-blind extraction. Historical think-gated scoring and format compliance are retained separately; this legacy field name is kept for compatibility.'),
        by_subject={v:rate([r for r in rows if r['subject']==v]) for v in sorted({r['subject'] for r in rows})},by_level={str(v):rate([r for r in rows if r['level']==v]) for v in sorted({r['level'] for r in rows})},
        by_parallel={str(v):rate([r for r in rows if bool(r['repro_stats']['forks'])==v]) for v in [False,True]},
        forks=tally(d['forks'] for d in derived),widths=tally(widths),parallel_questions=sum(d['forks']>0 for d in derived),multi_round_questions=sum(d['forks']>1 for d in derived),format_invalid_questions=sum(bool(d['format_errors']) for d in derived),invalid_width_questions=sum(d['invalid_width'] for d in derived),budget_exhausted_questions=sum(d['budget_exhausted'] for d in derived),
        response_tokens=stats([d['response_tokens'] for d in derived]),sampled_tokens=stats([d['sampled_tokens'] for d in derived]),forced_tokens=stats([d['forced_tokens'] for d in derived]),phase_tokens={p:stats(v) for p,v in phases.items()},critical_depth=stats([d['critical_depth'] for d in derived]),sampled_work_over_critical_depth=stats([d['sampled_work_over_critical_depth'] for d in derived]),elapsed_seconds_per_question=stats([d['elapsed_seconds'] for d in derived]),generation_calls=stats([d['generation_calls'] for d in derived]),
        call_budget_reached=dict(capped),sampled_eos_by_phase=dict(closures),runtime_closure_label_replacements=sum(d['closure_label_replacements'] for d in derived),
        exact_duplicate_paths_within_trace=sum(d['exact_duplicate_paths_within_trace'] for d in derived),path_repeated_5gram_fraction=stats([p['repeat_5gram_fraction'] for p in paths]),paths_with_repeated_5gram_fraction_over_half=sum(p['repeat_5gram_fraction']>.5 for p in paths),think_markup=tally(f"open={d['think_open_count']},close={d['think_close_count']}" for d in derived),think_structure={key:sum(d['think_structure'][key] for d in derived) for key in ['exactly_one_balanced_think','all_forks_inside_think','final_after_think','fully_valid']},
        answer_format={key:sum(d['answer_format'][key] for d in derived) for key in ['explicit_final_header','standalone_final_header','multiple_final_headers','boxed_after_final_header','final_header_inside_path','explicit_unresolved']},
        by_max_width={str(v):rate([r for r,d in zip(rows,derived) if max(d['widths'],default=0)==v]) for v in sorted({max(d['widths'],default=0) for d in derived})},
        context_audit=dict(forks_checked=len(groups),sibling_prefix_mismatches=sum(not g['prefixes_identical'] for g in groups),policy_label_or_mask_errors=errors),
        theoretical_ratio_note='Sampled work / serial critical token depth. Branches execute sequentially per GPU in this evaluator; this ratio is not measured speedup.',extraction_tests=score.check())
    out.update(primary_metric='Math-Verify final-answer equivalence, independent of think-tag validity',primary_correct=out['final_answer_only_diagnostic']['correct'],primary_pass_at_1=out['final_answer_only_diagnostic']['pass_at_1'],primary_ci95=out['final_answer_only_diagnostic']['ci95'],historical_extraction_pass_at_1=out['pass_at_1'])
    (WORK/'summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (WORK/'review-index.json').write_text(json.dumps(sorted(derived,key=lambda d:d['index']),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False))
    if args.final:assert not errorrows and not errors,(errorrows,errors)
if __name__=='__main__':main()
