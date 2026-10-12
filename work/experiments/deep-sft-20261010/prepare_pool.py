"""Build a fresh GSM-only pool, screen every existing local eval input."""
from pathlib import Path
import collections, hashlib, json, random, re, unicodedata
import pandas as pd

P = Path.cwd()
B = P/'work/experiments/deep-sft-20261010'
OLD = P/'exps/deepseek-gsm-wide3000-v2-20261009'
CONVENTIONS = ('GSM-Infinite dataset conventions: For this self-contained problem, an unmentioned category at a location contributes zero. A total includes all relevant categories mentioned at that location. Total nominations or newborn children are sums of (number of films or adult animals) times (average nominations or children per member); totals of schools or adult animals sum the category counts.\n\n')
def norm(s): return ' '.join(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',s).lower()))
def family(s): return re.sub(r'\d+', 'NUM', norm(s))
def grams(s):
    w=family(s).split();return set(zip(w,w[1:],w[2:]))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

excluded_ids=set();excluded_questions=set();files={}
for manifest in sorted((P/'work/experiments').glob('*/evaluations/*/manifest.json')):
    m=json.loads(manifest.read_text()); f=Path(m.get('fixed_questions',''))
    if not f.is_file() or str(f) in files:continue
    files[str(f)]=sha(f)
    for line in f.open():
        r=json.loads(line);excluded_ids.add(r['id']);excluded_questions.add(r.get('problem',r.get('question','')))
for d in [P/'exps/rl-dataset-screen-20261007', P/'cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots']:
    for f in sorted(d.glob('*.parquet') if 'rl-dataset' in str(d) else d.glob('*/*/test-*.parquet')):
        files[str(f)]=sha(f)
        for r in pd.read_parquet(f).to_dict('records'):
            q=r.get('problem')
            if q is None:
                pr=r.get('prompt',[])
                q='\n'.join(x['content'] for x in pr if isinstance(x,dict))
            if q:excluded_questions.add(str(q))
old_ids=set();old_exact=set()
for f in [OLD/'production/accepted.jsonl',P/'exps/deepseek-gsm-only-20261009/production/accepted-at-user-stop.jsonl']:
    if not f.exists():continue
    files[str(f)]=sha(f)
    for line in f.open():
        r=json.loads(line);old_ids.add(r['id']);old_exact.add(norm(r['problem']))
exact={norm(q) for q in excluded_questions};index=collections.defaultdict(list);gs=[]
for i,q in enumerate(sorted(excluded_questions)):
    g=grams(q);gs.append(g)
    for v in g:index[v].append(i)
def overlap(q):
    if norm(q) in exact:return True
    g=grams(q);hits=collections.Counter(i for v in g for i in index.get(v,()))
    return any(n/len(g|gs[i])>=.65 for i,n in hits.most_common(10)) if g else True

audit=collections.Counter();accepted=[];seen=set();source=OLD/'candidate-pool.jsonl';files[str(source)]=sha(source)
for line in source.open():
    r=json.loads(line); assert r['source']=='GSM_Infinite'
    if int(r['op'])<21:audit['ops_below_21']+=1;continue
    if r['id'] in excluded_ids or r['id'] in old_ids:audit['prior_id']+=1;continue
    q=r['question'];key=norm(r['core_problem'])
    if norm(q) in old_exact or key in seen:audit['prior_or_duplicate_problem']+=1;continue
    if overlap(r['core_problem']):audit['eval_text_overlap']+=1;continue
    if not re.fullmatch(r'-?\d+(?:\.\d+)?',r['reference'].strip()):audit['reference_non_scalar']+=1;continue
    if not q.startswith('GSM-Infinite dataset conventions:'):q=CONVENTIONS+q
    r['question']=q;r['question_sha256']=hashlib.sha256(q.encode()).hexdigest()
    r['split_group']=hashlib.sha256(family(r['core_problem']).encode()).hexdigest()
    seen.add(key);accepted.append(r)
# Prioritize harder source tasks while randomizing within difficulty strata.
random.Random(20261010).shuffle(accepted)
accepted.sort(key=lambda r:int(r['op'])<25)
assert len(accepted)>=3500, len(accepted)
B.mkdir(exist_ok=True)
for name,rows in [('candidate-pool.jsonl',accepted),('pilot-tasks.jsonl',accepted[:50])]:
    f=B/name;assert not f.exists();f.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
report=dict(candidates=len(accepted),pilot=50,source='GSM-Infinite ONLY, prior pinned source revisions retained',
    op_histogram=dict(collections.Counter(int(r['op']) for r in accepted)),
    pilot_op_histogram=dict(collections.Counter(int(r['op']) for r in accepted[:50])),
    excluded_eval_ids=len(excluded_ids),excluded_eval_questions=len(excluded_questions),old_train_ids=len(old_ids),
    disjoint_ids=True,disjoint_normalized_problems=True,exclusions=dict(audit),
    source_hashes=files,pool_sha256=sha(B/'candidate-pool.jsonl'),pilot_sha256=sha(B/'pilot-tasks.jsonl'),
    limitation='Text and number-masked trigram screening is not proof against semantic paraphrases.')
(B/'pool-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='source_hashes'},indent=2))
