from pathlib import Path
import hashlib,json,random,re,urllib.request,os
import pyarrow.parquet as pq
R=Path('${PROJECT_ROOT}');os.chdir(R)
P=R/'work/experiments/rl-r4-dapo2k-paired-20261013';D=P/'data';D.mkdir(parents=True,exist_ok=True)
revision='61829aa9fe754403c5559e46423772deac5a329b'
url=f'https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k/resolve/{revision}/data/dapo-math-17k.parquet'
raw=D/'dapo-math-17k.parquet'
if not raw.exists():
 urllib.request.urlretrieve(url,raw.with_suffix('.download'));os.replace(raw.with_suffix('.download'),raw)
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8388608),b''):h.update(b)
 return h.hexdigest()
def norm(s):return re.sub(r'[^a-z0-9]', '',str(s).lower())
holdout_paths=[R/'work/experiments/rl-r2-32gpu-batch32-20261012/eval-questions-500.jsonl',R/'work/experiments/paperbench-rl50-20261012/data/aime24-25-amc23.jsonl',R/'work/experiments/paperbench-rl50-20261012/data/aime26.jsonl',R/'work/experiments/rl-r2-24gpu-20261012/data/val.jsonl']
holdouts=set()
for p in holdout_paths:
 assert p.exists(),p
 for l in p.read_text().splitlines():
  r=json.loads(l);text=r.get('problem',r.get('question',r.get('prompt')));assert isinstance(text,str),(p,list(r));holdouts.add(norm(text))
rows=[]
for b in pq.ParquetFile(raw).iter_batches(batch_size=1000):
 rows.extend(b.to_pylist())
 if len(rows)>=10000:break
rows=rows[:10000];assert len(rows)==10000
prefix='Solve the following math problem step by step. The last line of your response should be of the form Answer: $Answer (without quotes) where $Answer is the answer to the problem.\n\n'
suffix='\n\nRemember to put your answer on its own line after "Answer:".'
pool=[];seen={};duplicates=[];excluded=[];conflicts=set()
rawsha=sha(raw)
for i,row in enumerate(rows):
 content=row['prompt'][0]['content'];assert content.startswith(prefix),(i,content[:100])
 problem=content[len(prefix):]
 if problem.endswith(suffix):problem=problem[:-len(suffix)]
 answer=str(row['reward_model']['ground_truth']);key=re.sub(r'\s+','',problem)
 if key in seen:
  if seen[key]!=answer:conflicts.add(key)
  duplicates.append(i);continue
 seen[key]=answer
 if norm(problem) in holdouts:excluded.append(i);continue
 pool.append(dict(id='dapo/'+str(row['extra_info']['index']),problem=problem,answer=answer,source='DAPO-Math-17k',source_repository='BytedTsinghua-SIA/DAPO-Math-17k',source_revision=revision,source_row_index=i,source_file_sha256=rawsha))
pool=[r for r in pool if re.sub(r'\s+','',r['problem']) not in conflicts]
assert len(pool)>=2000,len(pool)
selected=random.Random(20261013).sample(pool,2000)
assert len({re.sub(r'\s+','',r['problem']) for r in selected})==2000
(D/'train.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in selected))
manifest=dict(passed=True,source_url=url,revision=revision,source_file_sha256=rawsha,first_rows=10000,pool_unique_nonholdout=len(pool),duplicate_rows=duplicates,conflicting_problem_count=len(conflicts),excluded_holdout_rows=excluded,n=2000,seed=20261013,selection='random.sample without replacement from eligible unique problems in ORIGINAL first10000 rows',selected_source_indices=[r['source_row_index'] for r in selected],train_sha256=sha(D/'train.jsonl'),holdouts={str(p):sha(p) for p in holdout_paths},decontamination='exact normalized alphanumeric problem equality; no claim of semantic paraphrase detection',prompt_processing='remove exact source instruction prefix and exact terminal Answer instruction only; preserve all problem paragraphs')
(D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k in ['passed','first_rows','pool_unique_nonholdout','n','train_sha256']}),flush=True)
