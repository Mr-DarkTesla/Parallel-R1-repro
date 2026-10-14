"""GSM-Infinite only: original user dataset, then pinned official GSM reserve."""
import collections, concurrent.futures, hashlib, json, random, re, unicodedata
from pathlib import Path
import pandas as pd
from huggingface_hub import hf_hub_download, HfApi

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
OLD=BASE/'exps/deepseek-sft-counted-20261009'
CACHE=BASE/'cache/screen-hf'
REV='49b0c72bca4c257a378d07da41561fe081ec5ad5'
def norm(s):return ' '.join(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',s).lower()))
def family(s):return re.sub(r'\d+','NUM',norm(s))
def grams(s):
    w=family(s).split();return set(zip(w,w[1:],w[2:]))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    excluded=[];files={}
    for f in sorted((CACHE/'datasets--EleutherAI--hendrycks_math/snapshots').glob('*/*/test-*.parquet')):
        files[str(f)]=sha(f);excluded.extend(pd.read_parquet(f).problem.astype(str))
    for f in OLD.glob('pilot*-tasks.jsonl'):
        files[str(f)]=sha(f);excluded.extend(r['question'] for r in map(json.loads,f.read_text().splitlines()))
    for f in (BASE/'exps/rl-dataset-screen-20261007').glob('*.parquet'):
        files[str(f)]=sha(f)
        excluded.extend(r['prompt'][0]['content'].split('\n\nProblem: ',1)[-1] for r in pd.read_parquet(f).to_dict('records'))
    exact={norm(q) for q in excluded};index=collections.defaultdict(list);gs=[]
    for i,q in enumerate(excluded):
        g=grams(q);gs.append(g)
        for v in g:index[v].append(i)
    def overlap(q):
        if norm(q) in exact:return True
        g=grams(q);hits=collections.Counter(i for v in g for i in index.get(v,()))
        return any(n/len(g|gs[i])>=.65 for i,n in hits.most_common(10)) if g else True
    audit=collections.Counter();seen=set();accepted=[]
    def add(r):
        q=r['question'];key=norm(r['core_problem'])
        if key in seen:audit['duplicate']+=1;return
        if not 30<=len(q)<=14000:audit['question_length']+=1;return
        if overlap(q):audit['eval_or_pilot_overlap']+=1;return
        if not re.fullmatch(r'-?\d+(?:\.\d+)?',r['reference'].strip()):audit['non_numeric_reference']+=1;return
        seen.add(key);r.update(question_sha256=hashlib.sha256(q.encode()).hexdigest(),split_group=hashlib.sha256(family(r['core_problem']).encode()).hexdigest());accepted.append(r)
    f=BASE/'exps/sft-unseen-three-datasets-20261008/input/gsm_infinite_adaptive_parallel_5k.jsonl'
    files[str(f)]=sha(f);original=list(enumerate(map(json.loads,f.read_text().splitlines())));random.Random(20261009).shuffle(original)
    for i,r in original:
        add(dict(id=f'gsm_infinite/{i}',source='GSM_Infinite',source_file=str(f),source_row_index=i,question=r['messages'][1]['content'],core_problem=r['problem']+'\n'+r['question'],reference=str(r['answer']),source_dataset=r['source_dataset'],original_source_file=r['source_file'],original_source_row_index=r['source_row_index'],old_branch_schedule=r['branch_schedule'],**{k:r[k] for k in ['op','length','mode','template','d']}))
    original_count=len(accepted)
    print('original_eligible',original_count,'exclusions',dict(audit),flush=True)
    medium_repo='InfiniAILab/gsm_infinite_medium_0'
    snapshots=sorted((CACHE/'datasets--InfiniAILab--gsm_infinite_medium_0/snapshots').glob('*'))
    medium_revision=snapshots[-1].name if snapshots else HfApi().dataset_info(medium_repo).sha
    assert re.fullmatch('[0-9a-f]{40}',medium_revision)
    configs=[('InfiniAILab/gsm_infinite_hard_0',REV,op) for op in range(15,31)]+[(medium_repo,medium_revision,op) for op in range(15,31)]
    def fetch(config):
        repo,revision,op=config
        return repo,revision,Path(hf_hub_download(repo,f'data/ops_{op}-00000-of-00001.parquet',repo_type='dataset',revision=revision,cache_dir=CACHE))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:paths=list(pool.map(fetch,configs))
    reserve=[]
    for repo,revision,f in paths:
        files[str(f)]=sha(f)
        for i,r in enumerate(pd.read_parquet(f).to_dict('records')):
            if r['mode']!='normalforward':continue
            answer=re.findall(r'Answer:\s*(-?\d+(?:\.\d+)?)',r['solution'])
            if len(answer)!=1:audit['missing_reserve_answer']+=1;continue
            msgs=r['messages'];rules=next(m['content'] for m in msgs if m['role']=='user').split('Explain your calculation',1)[0].rstrip()
            core=r['problem']+'\n'+r['question'];q=rules+'\n\n'+core
            assert r['problem'] in q and r['question'] in q
            reserve.append(dict(id=f'{repo.split("/")[-1]}/{f.stem}/{i}',source='GSM_Infinite',source_file=str(f),source_row_index=i,question=q,core_problem=core,reference=answer[0],source_dataset=repo,source_revision=revision,**{k:str(r[k]) for k in ['op','length','mode','template','d']}))
    random.Random(20261010).shuffle(reserve)
    for r in reserve:
        add(r)
        if len(accepted)>=24000:break
    print('candidate_count',len(accepted),'original',original_count,'reserve_rows_examined',len(reserve),'exclusions',dict(audit),flush=True)
    assert len(accepted)>=6500,len(accepted)
    (ROOT/'expanded-original-candidate-pool.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in accepted))
    manifest=dict(source='GSM_Infinite ONLY',target=3000,original_eligible=original_count,reserve=len(accepted)-original_count,candidates=len(accepted),official_reserve_revision=REV,exclusions=dict(audit),sources_sha256=files,seed=20261009,decontamination='Normalized exact and number-masked trigram Jaccard >=0.65 against MATH test, previous RL evaluation and pilot tasks. Not semantic proof of decontamination.',max_question_characters=14000)
    (ROOT/'expanded-source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest),flush=True)

if __name__=='__main__':main()
