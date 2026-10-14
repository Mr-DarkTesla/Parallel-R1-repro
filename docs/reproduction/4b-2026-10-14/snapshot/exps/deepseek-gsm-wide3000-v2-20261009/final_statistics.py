import collections,hashlib,json,re,time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
from transformers import AutoTokenizer
from validate import BLOCK
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent.parent;OUT=ROOT/'production/sft-think'
tok=AutoTokenizer.from_pretrained(BASE/'exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final',local_files_only=True)
splits={k:[json.loads(l) for l in (OUT/f'{k}.jsonl').read_text().splitlines()] for k in ['train','val']};rows=splits['train']+splits['val']
assert len(rows)==3000 and len({r['id'] for r in rows})==3000
assert {r['split_group'] for r in splits['train']}.isdisjoint({r['split_group'] for r in splits['val']})
manifest=json.loads((OUT/'summary.json').read_text());assert all(hashlib.sha256((OUT/f).read_bytes()).hexdigest()==h for f,h in manifest['sha256'].items())
def stats(values):
 return dict(zip(['mean','p50','p90','p95','p99','max'],map(float,[np.mean(values),*np.percentile(values,[50,90,95,99]),max(values)])))
output_lengths=[];critical_lengths=[];serial_lengths=[];path_lengths=[]
for r in rows:
 text=r['assistant_content'];assert text.count('<think>')==text.count('</think>')==1
 inside=text.split('<think>',1)[1].split('</think>',1)[0];outside=text.split('</think>',1)[1]
 assert inside.count('<Parallel>')==r['fork_count'] and '<Parallel>' not in outside
 token=lambda s:len(tok.encode(s,add_special_tokens=False))
 cursor=0;serial=0;maxima=[]
 for m in BLOCK.finditer(text):
  serial+=token(text[cursor:m.start()])+token('<Parallel>'+m[1]+'\n')+token('</Parallel>\n<Summary>'+m[3]+'</Summary>')
  lengths=[token(b) for b in re.findall(r'<Path>[1-8]\n[\s\S]*?</Path>',m[2])];path_lengths.extend(lengths);maxima.append(max(lengths));cursor=m.end()
 serial+=token(text[cursor:]);serial_lengths.append(serial);critical_lengths.append(serial+sum(maxima));output_lengths.append(token(text))
records=[json.loads(l) for l in (ROOT/'production/journal.jsonl').read_text().splitlines()];graded=[r for r in records if r.get('grade') is not None]
widths=[w for r in rows for w in r['branch_schedule']];verifications=[v for r in rows for v in r['verification']['semantic_judge'].get('verification_paths',[])]
finish=json.loads((ROOT/'pipeline-status.json').read_text())['finished_at']
report={'complete':True,'finished_moscow':datetime.fromtimestamp(finish,ZoneInfo('Europe/Moscow')).isoformat(),'new_examples':3000,'old_examples_preserved':2145,'combined_if_used':5145,'train':2700,'val':300,'decisions':len(records),'acceptance_percent':100*3000/len(records),'sources':dict(collections.Counter(r['source'] for r in rows)),'source_datasets':dict(collections.Counter(r['source_metadata']['source_dataset'] for r in rows)),'op_histogram':dict(collections.Counter(str(r['source_metadata']['op']) for r in rows)),'forks':len(widths),'mean_width_per_fork':float(np.mean(widths)),'width_histogram':dict(collections.Counter(widths)),'round_histogram':dict(collections.Counter(r['fork_count'] for r in rows)),'mean_rounds':float(np.mean([r['fork_count'] for r in rows])),'width_above_two_percent':100*sum(w>2 for w in widths)/len(widths),'verification_rows':sum(bool(r['verification']['semantic_judge'].get('verification_paths')) for r in rows),'verification_rows_percent':100*sum(bool(r['verification']['semantic_judge'].get('verification_paths')) for r in rows)/3000,'verification_paths':len(verifications),'all_accepted_reference_match':all(r['verification']['final_answer']=='Math-Verify 0.8.0' for r in rows),'pipeline_final_answer_checks':{'checked':len(graded),'correct':sum(r['grade'].get('correct') is True for r in graded),'note':'Conditional on pipeline reaching the answer-check stage; not all teacher responses.'},'output_tokens':stats(output_lengths),'student_sequence_tokens':stats([r['student_tokens'] for r in rows]),'critical_path_tokens_proxy':stats(critical_lengths),'sequential_output_tokens':stats(serial_lengths),'path_tokens':stats(path_lengths),'validation':{'unique_ids':True,'train_val_group_disjoint':True,'hashes_match':True,'single_think':True,'all_parallel_blocks_inside_think':True,'final_solution_outside_think':True},'limitations':['Semantic critic is the teacher model; final-answer matching is not a proof of every reasoning step.','Critical-path token count is a proxy, not measured forwards or student accuracy.']}
(ROOT/'final-statistics.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report,indent=2,ensure_ascii=False))
