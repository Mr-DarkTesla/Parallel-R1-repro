from pathlib import Path
import json,re,collections,statistics,datetime
P=Path.cwd();D=P/'work/experiments/instruct-token-warmup-20261010';C=P/'work/experiments/format-loss-20261010';F=P/'work/experiments/format-diagnosis-20261010'
report={}
for root,name in [(D/'evaluations','structured-runtime-smoke24'),(D/'evaluations','lr-1e-3-trained-structured-24'),(D/'evaluations','lr-1e-3-trained-structured-128'),(D/'evaluations','lr-2e-4-trained-structured-128'),(C/'evaluations','weighted-format-constrained-128')]:
 folder=root/name;rows=[]
 for p in folder.glob('traces-*.jsonl'):rows.extend(json.loads(l) for l in p.open())
 counts=collections.Counter();headers=collections.Counter();widths=[];errors=collections.Counter();samples=[]
 for r in rows:
  t=r['output'];s=r['stats'];trace=r.get('trace',{});calls=trace.get('policy_calls',[]);n=int(s.get('forks',0));counts['tasks']+=1;counts['executed_rounds']+=n;counts['forked_tasks']+=n>0;counts['invalid_width']+=bool(s.get('invalid_width'));counts['truncated']+=bool(s.get('truncated'));attempts=t.count('<Parallel>');counts['tasks_with_text_parallel']+=attempts>0;counts['text_parallel_openings']+=attempts
  close=t.find('</think>');starts=[m.start() for m in re.finditer('<Parallel>',t)];counts['parallel_after_think_tasks']+=any(close>=0 and x>close for x in starts);counts['no_parallel_before_think_close']+=not any(close<0 or x<close for x in starts)
  path_calls=[x for x in calls if x.get('phase')=='path'];main_count=sum(x.get('phase')=='main' for x in calls)
  # Policy path calls occur in contiguous groups between width and summary. Only groups of actual executed paths count.
  groups=[];current=0
  for x in calls:
   if x.get('phase')=='path':current+=1
   elif current:groups.append(current);current=0
  if current:groups.append(current)
  assert len(groups)==n,(name,r['id'],groups,n)
  widths.extend(groups)
  for m in re.finditer(r'<Parallel>([^<]{0,100})',t):headers[m.group(1).split('<')[0][:60]]+=1
  if (s.get('invalid_width') or n>0) and len(samples)<10:
   ix=t.find('<Parallel>');samples.append(dict(id=r['id'],forks=n,actual_widths=groups,invalid_width=s.get('invalid_width'),snippet=t[max(0,ix-220):ix+500],trace_keys=list(trace),call_phases=[x.get('phase') for x in calls],width_calls=[{k:x.get(k) for k in ['generated_ids','phase','response_start']} for x in calls if x.get('phase')=='width']))
 if (folder/'scores.jsonl').exists():
  scored=[json.loads(l) for l in (folder/'scores.jsonl').open()]
  for r in scored:
   for e in r.get('format_diagnostics',{}).get('errors',[]):errors[e]+=1
  counts['correct']=sum(r['grade']['correct'] for r in scored);counts['basic_valid']=sum(r['format_valid'] for r in scored);counts['parallel_valid']=sum(r['parallel_protocol_valid'] for r in scored)
 report[name]=dict(counts=dict(counts),executed_widths=widths,mean_executed_width=statistics.mean(widths) if widths else None,executed_width_histogram=dict(collections.Counter(widths)),common_headers=headers.most_common(8),format_errors=dict(errors),samples=samples,complete=(folder/'summary.json').exists())
(F/'diagnosis.json').write_text(json.dumps(dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runs=report),ensure_ascii=False,indent=2)+'\n')
for name,r in report.items():print(name,json.dumps({k:v for k,v in r.items() if k!='samples'},ensure_ascii=False))
for name in ['lr-1e-3-trained-structured-24','lr-1e-3-trained-structured-128']:
 for r in report[name]['samples'][:3]:print('EXAMPLE',name,json.dumps(r,ensure_ascii=False)[:1400])
