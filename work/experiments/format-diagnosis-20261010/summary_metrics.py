"""Shared CPU-only evaluation reporting and explicit non-mandatory-fork gate."""
import math,re,statistics,collections

def distribution(values):
 values=sorted(float(v) for v in values if v is not None and math.isfinite(float(v)))
 if not values:return {'n':0,'sum':0.,'mean':None,'median':None,'p95':None,'min':None,'max':None}
 x=.95*(len(values)-1);lo=int(x);hi=min(lo+1,len(values)-1)
 return {'n':len(values),'sum':sum(values),'mean':statistics.mean(values),'median':statistics.median(values),'p95':values[lo]+(values[hi]-values[lo])*(x-lo),'min':values[0],'max':values[-1]}

def normalize_row(r):
 s=dict(r.get('stats') or {});trace=r.get('trace') or {};assembled=int(r.get('response_tokens',len(r.get('response_ids',[]))));native=r.get('mode')=='native'
 if native:
  forced=int(s.get('forced_tokens',2));sampled=int(s.get('sampled_tokens',max(0,assembled-forced)));s.update(critical_depth=sampled,sampled_tokens=sampled,forced_tokens=forced,generation_calls=1,generated_tokens=sampled,forks=0,invalid_width=False,truncated=bool(s.get('truncated',assembled>=4096)))
 else:
  s.setdefault('critical_depth',trace.get('critical_depth'));s.setdefault('generation_calls',trace.get('generation_calls',len(trace.get('calls',[]))));s.setdefault('generated_tokens',trace.get('generated_tokens_total'));s.setdefault('sampled_tokens',sum(trace.get('response_mask',[])) if trace.get('response_mask') is not None else None);s.setdefault('forced_tokens',assembled-s['sampled_tokens'] if s.get('sampled_tokens') is not None else None);s.setdefault('forks',trace.get('executed_fork_count',0));s.setdefault('invalid_width',trace.get('invalid_width',False));s.setdefault('truncated',trace.get('truncated',assembled>=4096))
 r['stats']=s;r['cost']={'F':s.get('critical_depth'),'T_sampled':s.get('sampled_tokens'),'T_forced':s.get('forced_tokens'),'T_assembled':assembled,'actual_generated_tokens':s.get('generated_tokens'),'generation_calls':s.get('generation_calls'),'wall_seconds':r.get('seconds'),'forks':s.get('forks',0),'rounds':s.get('forks',0),'generation_turns':s.get('forks',0)+1,'widths':[int(x) for x in re.findall(r'<Parallel>\s*([2-8])(?:\s|<Path>)',r.get('output',''))],'truncated':bool(s.get('truncated'))}
 inferred={'model_forward_calls_inferred':None,'prefill_calls_inferred':None,'decode_calls_inferred':None}
 if native:r['work_inference']={'status':'unavailable_native_backend_not_measured','trace_verified':False}
 else:
  actual_calls=trace.get('calls');generated=s.get('generated_tokens');count=s.get('generation_calls');verified=False;agreement=None
  if actual_calls is not None:
   lengths=[len(c['generated_ids']) for c in actual_calls];generated=sum(lengths);count=sum(n>0 for n in lengths);verified=True;agreement=(generated==s.get('generated_tokens') and len(actual_calls)==s.get('generation_calls') and generated==trace.get('generated_tokens_total',generated))
  if generated is not None and count is not None and 0<=count<=generated:
   inferred={'model_forward_calls_inferred':generated,'prefill_calls_inferred':count,'decode_calls_inferred':generated-count}
  r['work_inference']={'status':'inferred_from_serial_hf_source_not_measured','trace_verified':verified,'trace_and_reported_stats_agree':agreement,'inference_uses_all_actual_calls_including_discarded_outputs':True,'zero_output_calls':sum(not c['generated_ids'] for c in actual_calls) if actual_calls is not None else None}
 r['cost'].update(inferred)
 return r

def aggregate(rows):
 numeric=['F','T_sampled','T_forced','T_assembled','actual_generated_tokens','generation_calls','wall_seconds','forks','rounds','generation_turns','model_forward_calls_inferred','prefill_calls_inferred','decode_calls_inferred'];result={k:distribution([r['cost'].get(k) for r in rows]) for k in numeric};result['widths']=distribution([w for r in rows for w in r['cost']['widths']]);result['width_histogram']=dict(sorted(collections.Counter(str(w) for r in rows for w in r['cost']['widths']).items()));result['truncated_samples']=sum(r['cost']['truncated'] for r in rows);result['truncated_fraction']=result['truncated_samples']/len(rows) if rows else None;result['invalid_width_samples']=sum(bool(r['stats'].get('invalid_width')) for r in rows);result['forked_samples']=sum(r['cost']['forks']>0 for r in rows);return result

def enrich_summary(summary,rows,planned_rows):
 for r in rows:
  r['legacy_format_valid']=r.get('legacy_format_valid',r['format_valid']);r['legacy_parallel_protocol_valid']=r.get('legacy_parallel_protocol_valid',r['parallel_protocol_valid'])
  flags=canonical_format_flags(r['output']);r['format_flags_v2']=flags;r['format_valid']=bool(flags['format']);r['parallel_syntax_valid']=bool(flags['parallel_format_valid']);r['format_schema_version']=2
  selected,method=extract_primary(r['output'])
  if 'answer' in r['grade'] and (selected!=r['grade'].get('answer') or method!=r['grade'].get('extraction')):
   import importlib.util
   from pathlib import Path
   scorer_path=Path(__file__).resolve().parents[2]/'unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py'
   spec=importlib.util.spec_from_file_location('canonical_grade',scorer_path);scorer=importlib.util.module_from_spec(spec);spec.loader.exec_module(scorer)
   r['legacy_primary_grade']=r['grade']
   if selected is None:r['grade']=dict(correct=False,answer=None,extraction=method,valid=False,error=None)
   else:
    try:
     gold,pred=scorer.parsed(str(r['answer'])),scorer.parsed(selected)
     if not gold:raise ValueError('unparseable reference')
     r['grade']=dict(correct=bool(pred and scorer.verify(gold,pred,timeout_seconds=5)),answer=selected,extraction=method,valid=bool(pred),error=None)
    except Exception as error:r['grade']=dict(correct=False,answer=selected,extraction=method,valid=False,error=f'{type(error).__name__}: {error}')
  r['accuracy_schema_version']=2;normalize_row(r)
  actual_forks=int(r['stats'].get('forks',0));textual_forks=r['output'].count('<Parallel>');widths=canonical_check_format(r['output'])[1];r['parallel_rounds_textual']=textual_forks;r['parallel_rounds_parsed']=len(widths);r['parallel_execution_matches_text']=actual_forks==textual_forks==len(widths);r['parallel_protocol_valid']=bool(r['format_valid'] and r['parallel_syntax_valid'] and actual_forks>0 and r['parallel_execution_matches_text'] and not any(r['stats'].get(k,False) for k in ['invalid_main_control','invalid_width','invalid_text_protocol']))
 n=len(rows);forked=[r for r in rows if r['stats'].get('forks',0)>0];valid_parallel=sum(r['parallel_protocol_valid'] for r in forked);invalid=sum(bool(r['stats'].get('invalid_width')) for r in rows);basic=sum(r['format_valid'] for r in rows);correct=sum(r['grade']['correct'] for r in rows)
 criteria={'all_planned_completed':n==summary['planned'],'basic_strict_format_at_least_0_8':n>0 and basic/n>=.8,'fork_coverage_at_least_0_2':n>0 and len(forked)/n>=.2,'valid_parallel_among_executed_fork_samples_at_least_0_9':bool(forked) and valid_parallel/len(forked)>=.9,'invalid_width_fraction_at_most_0_05':n>0 and invalid/n<=.05,'at_least_one_correct':correct>0}
 summary.update(parallel_syntax_valid=sum(r['parallel_syntax_valid'] for r in rows),parallel_execution_mismatch_samples=sum(not r['parallel_execution_matches_text'] for r in rows),parallel_valid_definition='Canonical strict format AND syntax AND actual executed forks>0 AND parsed/textual rounds equal executed forks AND no invalid runtime control',format_schema_version=2,accuracy_schema_version=2,legacy_format_valid=sum(r['legacy_format_valid'] for r in rows),legacy_format_fraction_completed_only=sum(r['legacy_format_valid'] for r in rows)/n if n else None,legacy_parallel_protocol_valid=sum(r['legacy_parallel_protocol_valid'] for r in rows),format_valid=basic,format_fraction_completed_only=basic/n if n else None,parallel_protocol_valid=sum(r['parallel_protocol_valid'] for r in rows),parallel_protocol_fraction_completed_only=sum(r['parallel_protocol_valid'] for r in rows)/n if n else None,correct=correct,pass_at_1_completed_only=correct/n if n else None,primary_extraction_changed_samples=sum('legacy_primary_grade' in r for r in rows),gate_passed=all(criteria.values()),gate_criteria=criteria,gate_thresholds={'basic_strict_format':.8,'fork_coverage':.2,'valid_parallel_among_executed_forks':.9,'max_invalid_width':.05,'min_correct':1},gate_raw_counts={'completed':n,'basic_valid':basic,'executed_fork_samples':len(forked),'valid_parallel_among_fork_samples':valid_parallel,'invalid_width_samples':invalid,'correct':correct},fork_coverage=len(forked)/n if n else None,valid_parallel_among_executed_forks=valid_parallel/len(forked) if forked else None,invalid_width_fraction=invalid/n if n else None,correct_and_basic_valid=sum(r['grade']['correct'] and r['format_valid'] for r in rows),correct_and_parallel_valid=sum(r['grade']['correct'] and r['parallel_protocol_valid'] for r in rows),metrics_all=aggregate(rows),metrics_correct=aggregate([r for r in rows if r['grade']['correct']]))
 def dataset(r):
  d=r.get('dataset','unknown');return 'math' if d in ['math','math500'] else d
 by={}
 for d in sorted(set(dataset(r) for r in planned_rows)|set(dataset(r) for r in rows)):
  rr=[r for r in rows if dataset(r)==d];nn=len(rr);cc=sum(r['grade']['correct'] for r in rr);ff=sum(r['format_valid'] for r in rr);pp=sum(r['parallel_protocol_valid'] for r in rr);by[d]={'planned':sum(dataset(r)==d for r in planned_rows),'completed':nn,'correct':cc,'pass_at_1':cc/nn if nn else None,'basic_valid':ff,'basic_valid_fraction':ff/nn if nn else None,'parallel_valid':pp,'parallel_syntax_valid':sum(r['parallel_syntax_valid'] for r in rr),'parallel_execution_mismatch_samples':sum(not r['parallel_execution_matches_text'] for r in rr),'correct_and_basic_valid':sum(r['grade']['correct'] and r['format_valid'] for r in rr),'correct_and_parallel_valid':sum(r['grade']['correct'] and r['parallel_protocol_valid'] for r in rr),'metrics_all':aggregate(rr),'metrics_correct':aggregate([r for r in rr if r['grade']['correct']])}
 historical=sum(r.get('historical_grade',r['grade'])['correct'] for r in rows)
 summary['historical_correct']=historical;summary['historical_pass_at_1_completed_only']=historical/n if n else None;summary['primary_metric']='Math-Verify final answer equivalence after removing only think markup; independent of think-format validity'
 for d,v in by.items():
  rr=[r for r in rows if dataset(r)==d];v['historical_correct']=sum(r.get('historical_grade',r['grade'])['correct'] for r in rr);v['historical_pass_at_1']=v['historical_correct']/len(rr) if rr else None
 summary['work_inference']={'measurement_status':'INFERRED from structured serial HF source; not measured GPU telemetry','structured_trace_verified_samples':sum(r.get('mode')!='native' and r['work_inference']['trace_verified'] for r in rows),'structured_trace_stat_mismatch_samples':sum(r.get('mode')!='native' and r['work_inference'].get('trace_and_reported_stats_agree') is False for r in rows),'native_forward_counts_available':False}
 summary['by_dataset']=by;summary['cost_definitions']={'model_forward_calls_inferred':'INFERRED, not measured: serial HF structured_generate runs one initial model forward and one for each additional sampled output, hence sum raw generated_ids lengths across ALL calls. Native unavailable.', 'prefill_calls_inferred':'INFERRED, not measured: one initial HF prefill per positive-output generation call. Native unavailable.', 'decode_calls_inferred':'INFERRED, not measured: all raw generated tokens minus positive-output generation calls; no speculation in this backend. Native unavailable.', 'rounds':'Executed parallel fork rounds; native=0','generation_turns':'Parallel rounds+1; native=1','F':'Logical critical sequential sampled-token depth; native F=sampled length. Not measured GPU model-forward invocations.','T_sampled':'Retained sampled response tokens','T_forced':'Forced response tokens including think prefix/protocol bridges','T_assembled':'Total assembled response tokens','actual_generated_tokens':'All generated token outputs across actual generation calls, including discarded outputs if any','wall_seconds':'Per-question generation elapsed, excludes engine startup; backend confounded','backend_confound':'Structured uses HF structured serial backend through vLLM worker RPC; native uses fast vLLM generation. Wall comparisons are descriptive and cannot establish parallel execution speedup.'};summary['backend_labels']=sorted({'native_vllm_fast' if r.get('mode')=='native' else 'hf_structured_serial_backend' for r in rows});summary['matching_protocol']={'prompt_policy':'native generic math prompt; structured counted protocol prompt; these are complete configuration comparisons','question_seed':'42+sample_index','response_budget':4096,'path_budget':2048,'temperature':.6,'top_p':.95,'top_k':20};return summary


# Canonical format v2 copied from RL pure validators; no RL/parser imports.
TAG=re.compile(r"</?Parallel>|</?Path>|</?Summary>")
def canonical_check_format(text):
    state='main';width=0;count=0;widths=[];errors=[];previous_end=0
    for match in TAG.finditer(text):
        tag=match.group();between=text[previous_end:match.start()]
        if tag=='<Parallel>' and state=='main':state='header';count=0
        elif tag=='<Path>' and state in ['header','between']:
            if state=='header':
                try:width=int(between.strip())
                except ValueError:width=0
                if re.fullmatch(r'[2-8]\n',between) is None:errors.append('Invalid width header')
            elif between.strip():errors.append('Unexpected content between sibling paths')
            tail=text[match.end():]
            branch=re.match(r'(\d+)\n',tail)
            count+=1
            if branch is None or int(branch.group(1))!=count:errors.append('Incorrect path ID')
            state='path'
        elif tag=='</Path>' and state=='path':state='between'
        elif tag=='</Parallel>' and state=='between':
            if between.strip():errors.append('Unexpected content after last path')
            if count!=width:errors.append('Declared width differs from path count')
            widths.append(width);state='need_summary'
        elif tag=='<Summary>' and state=='need_summary':
            if between.strip():errors.append('Unexpected content before summary')
            state='summary'
        elif tag=='</Summary>' and state=='summary':state='main'
        else:errors.append('Misnested control tag '+tag)
        previous_end=match.end()
    if state!='main':errors.append('Unclosed fork/path/summary')
    return errors,widths

def canonical_format_flags(text):
    errors,widths=canonical_check_format(text)
    parallel_valid=not errors
    think_valid=text.count("<think>")==1 and text.count("</think>")==1 and text.find("<think>")<text.find("</think>")
    strict=False
    if think_valid:
        opening=text.index("<think>")+len("<think>");closing=text.index("</think>")
        inside=all(opening<=m.start()<closing for m in re.finditer(r"</?(?:Parallel|Path|Summary)>",text))
        final_pattern=r"(?i)(?:\*\*)?Final\s+Answer(?:\*\*)?\s*:"
        final_outside=bool(re.search(final_pattern,text[closing+len("</think>"):]))
        final_in_path=any(re.search(final_pattern,m.group()) for m in re.finditer(r"<Path>.*?</Path>",text,re.DOTALL))
        strict=parallel_valid and inside and final_outside and not final_in_path
    return dict(format=float(strict),parallel_format_valid=float(parallel_valid),think_valid=float(think_valid),
                format_schema_version=2,max_width=max(widths,default=0))

def extract_visible(text):
    headers=list(re.finditer(r"(?i)(?:\*\*)?Final\s+Answer(?:\*\*)?\s*:",text))
    if headers:text=text[headers[-1].end():]
    boxes=list(re.finditer(r"\\(?:boxed|fbox)\s*\{",text))
    if boxes:
        start=boxes[-1].end();depth=1
        for i in range(start,len(text)):
            if text[i]=="{":depth+=1
            elif text[i]=="}":depth-=1
            if depth==0:return text[start:i],"boxed"
        return None,"unclosed_box"
    if headers:
        for line in text.splitlines():
            line=re.sub(r"<\|[^>]*\|>|</?(?:Parallel|Path|Summary)>","",line).strip().strip("*").strip()
            if line and line not in ("$$","$",r"\[",r"\]"):return line.strip("$"),"final_answer_line"
    return None,"missing_final_answer"

def extract_primary(raw_text):
    return extract_visible(re.sub(r"</?think>","",raw_text))
