"""Report both full pilot denominators and the accepted subset."""
import collections,json,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
rows=[json.loads(l) for l in ((ROOT/'reviewed-pilot-results.jsonl') if (ROOT/'reviewed-pilot-results.jsonl').exists() else (ROOT/'pilot-results.jsonl')).read_text().splitlines()] if (ROOT/'pilot-results.jsonl').exists() else []
tasks={r['id']:r for r in map(json.loads,(ROOT/'pilot-tasks.jsonl').read_text().splitlines())}
def stats(rs):
 widths=[w for r in rs for w in r.get('metrics',{}).get('widths',[])];out={'rows':len(rs),'forks':len(widths),'mean_width_per_fork':float(np.mean(widths)) if widths else None,'width_histogram':dict(collections.Counter(widths)),'round_histogram':dict(collections.Counter(r.get('metrics',{}).get('rounds') for r in rs)),'op_histogram':dict(collections.Counter(str(tasks[r['id']].get('op')) for r in rs))}
 for key in ['total_tokens','sequential_tokens','critical_path_tokens_proxy','parallel_path_tokens']:
  values=[r['metrics'][key] for r in rs if r.get('metrics')]
  out[key]={k:float(v) for k,v in zip(['mean','p50','p90','p95','max'],[np.mean(values),*np.percentile(values,[50,90,95]),max(values)])} if values else None
 values=[r['student_tokens'] for r in rs if 'student_tokens' in r];out['student_tokens']={k:float(v) for k,v in zip(['mean','p50','p90','p95','max'],[np.mean(values),*np.percentile(values,[50,90,95]),max(values)])} if values else None
 byop={}
 for op in out['op_histogram']:
  ws=[w for r in rs if str(tasks[r['id']].get('op'))==op for w in r.get('metrics',{}).get('widths',[])]
  byop[op]={'forks':len(ws),'mean_width':float(np.mean(ws)) if ws else None}
 verification=[v for r in rs for v in r.get('judge',{}).get('verification_paths',[])]
 out['verification_paths']=len(verification)
 out['rows_with_verification']=sum(bool(r.get('judge',{}).get('verification_paths')) for r in rs)
 judged=[r for r in rs if r.get('judge')]
 judged_forks=sum(r.get('metrics',{}).get('rounds',0) for r in judged)
 out['mean_distinct_work_width_proxy_judged']=(sum(sum(r['metrics']['widths']) for r in judged)-len(verification))/judged_forks if judged_forks else None
 ratios=[r['metrics']['critical_path_tokens_proxy']/r['metrics']['total_tokens'] for r in rs if r.get('metrics',{}).get('total_tokens')]
 out['mean_critical_to_total_ratio']=float(np.mean(ratios)) if ratios else None
 out['width_by_op']=byop
 return out
accepted=[r for r in rows if r.get('accepted')]
report={'at':time.time(),'pilot_state':json.loads((ROOT/'pilot-status.json').read_text()),'completed':len(rows),'target':60,'final_correct':sum(r.get('grade',{}).get('correct') is True for r in rows),'final_checked':sum('grade' in r for r in rows),'structure_valid':sum(r.get('structure',{}).get('valid') is True for r in rows),'accepted':len(accepted),'errors':dict(collections.Counter(r.get('error','semantic_judge_reject') for r in rows if not r.get('accepted'))),'judge_issues':[{'id':r['id'],'issues':r['judge'].get('issues')} for r in rows if r.get('judge',{}).get('issues')],'all':stats(rows),'accepted_subset':stats(accepted),'limitations':['Teacher answer correctness is measured against source references; acceptance also uses the same model as semantic critic.','Critical-path tokens are a tokenizer-based proxy, not measured runtime forwards or small-student accuracy.','Mean width is weighted per fork; examples with no forks do not enter this mean.']}
(ROOT/'pilot-statistics.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report,indent=2,ensure_ascii=False))
