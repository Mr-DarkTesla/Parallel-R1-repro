import collections, hashlib, json, random, re, unicodedata
from pathlib import Path
import pandas as pd
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer

ROOT = Path('${PROJECT_ROOT}')
RUN = Path(__file__).resolve().parent
CODE = ROOT/'exps/rl-unseen-s2-bs32-500-20261007/code'
DATA = CODE/'verl/data_preprocess_scripts/data'
MODEL = ROOT/'exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final'
SEED = 20261007
def fetch(repo, name, revision):
    return hf_hub_download(repo, name, repo_type='dataset', revision=revision, cache_dir=ROOT/'cache/screen-hf')
def question(prompt):
    return prompt[0]['content'].split('\n\nProblem: ', 1)[-1]
def norm(s):
    return ' '.join(re.findall(r'[a-z0-9]+', unicodedata.normalize('NFKC', s).lower()))
def grams(s):
    words = re.sub(r'\d+', 'NUM', norm(s)).split()
    return set(zip(words, words[1:], words[2:]))

excluded=[]
for subject in ['algebra','counting_and_probability','geometry','intermediate_algebra','number_theory','prealgebra','precalculus']:
    for split in ['train','test']:
        p=fetch('EleutherAI/hendrycks_math',f'{subject}/{split}-00000-of-00001.parquet','21a5633873b6a120296cce3e2df9d5550074f4a3')
        excluded.extend((f'MATH/{subject}/{split}/{i}',q) for i,q in enumerate(pd.read_parquet(p).problem))
assert len(excluded)==12500
sft=pd.read_parquet(DATA/'gsm8k/adaptive_parallel_thinking_final_with_prompt_v3/sft_all_accuracy_add_parallel_reward/train.parquet')
excluded.extend((f'SFT/{i}',question(p)) for i,p in enumerate(sft.prompt))
exact={norm(q):ident for ident,q in excluded}
index=collections.defaultdict(list); allgrams=[]
for i,(_,q) in enumerate(excluded):
    g=grams(q);allgrams.append(g)
    for word in g:index[word].append(i)
def overlap(q):
    if norm(q) in exact:return {'match':exact[norm(q)],'kind':'normalized_exact'}
    g=grams(q)
    if len(g)<5:return None
    hits=collections.Counter(i for word in g for i in index.get(word,()))
    for i,n in hits.most_common(10):
        similarity=n/len(g|allgrams[i])
        if similarity>=0.65:return {'match':excluded[i][0],'kind':'number_masked_word_trigram_jaccard','similarity':similarity}
    return None
dapo=pd.read_parquet(DATA/'dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/train.parquet')
prefix=dapo.iloc[0].prompt[0]['content'].split('\n\nProblem: ',1)[0]+'\n\nProblem: '
tokenizer=AutoTokenizer.from_pretrained(MODEL,local_files_only=True)
audit={'seed':SEED,'math_rows':12500,'sft_rows':len(sft),'filter':'normalized exact and number-masked word-trigram Jaccard >=0.65; does not establish absence of semantic paraphrases','datasets':{},'blocked':{'bigmath_orca':'HF access required (401)','bigmath_cn_k12':'HF access required (401)'}}
def select(name,candidates,count):
    rows=[];reject=[];seen=set()
    random.Random(SEED).shuffle(candidates)
    for item in candidates:
        q=item['question']; key=norm(q)
        match=overlap(q)
        if key in seen:continue
        if match:reject.append({'id':item['id'],**match});continue
        content=prefix+item.get('semantics','')+q
        prompt=[{'role':'user','content':content}]
        n=len(tokenizer.apply_chat_template(prompt,add_generation_prompt=True))
        if n>2000:reject.append({'id':item['id'],'kind':'prompt_over_2000','tokens':n});continue
        seen.add(key)
        ident=f'{name}/{item["id"]}'
        rows.append(dict(data_source='math_dapo',prompt=prompt,ability='math',reward_model={'ground_truth':item['answer'],'style':'rule'},index=ident,extra_info={'index':ident,'dataset':name,'op':int(item.get('op',-1)),'reward_method':'accuracy_reward','prompt_tokens':n}))
        if len(rows)==count:break
    assert len(rows)==count,(name,len(rows))
    audit['datasets'][name]={'selected':len(rows),'rejected':reject,'max_prompt_tokens':max(r['extra_info']['prompt_tokens'] for r in rows)}
    return rows

gsm=[]
for op in range(2,7):
    p=fetch('InfiniAILab/gsm_infinite_medium_0',f'data/ops_{op}-00000-of-00001.parquet','c6c5ab433565ddfe3e38e22be165b5c40e6bd576')
    candidates=[]
    for i,row in pd.read_parquet(p).iterrows():
        answer=re.findall(r'Answer:\s*(-?\d+(?:\.\d+)?)',row.solution)
        assert len(answer)==1,(op,i,row.solution)
        rules=row.messages[1]['content'].replace("'Answer: xxx'","'Final Answer: xxx'")
        candidates.append({'id':f'ops{op}/{i}','question':row.problem+'\n'+row.question,'answer':answer[0],'op':op,'semantics':rules+'\n\n'})
    gsm.extend(select(f'gsm_infinite_ops{op}',candidates,52 if op==2 else 51))
random.Random(SEED).shuffle(gsm)
candidates=[{'id':str(r['index']),'question':question(r['prompt']),'answer':str(r['reward_model']['ground_truth'])} for r in dapo.to_dict('records')]
dapo_rows=select('dapo',candidates,256)
for name,rows in [('gsm_infinite',gsm),('dapo',dapo_rows)]:
    path=RUN/f'{name}.parquet';pd.DataFrame(rows).to_parquet(path,index=False)
    audit[name]={'rows':len(rows),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
audit['sources']={'gsm':'InfiniAILab/gsm_infinite_medium_0@c6c5ab433565ddfe3e38e22be165b5c40e6bd576','math_exclusion':'EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3','dapo_file':str(DATA/'dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/train.parquet'),'checkpoint':str(MODEL)}
(RUN/'data-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps({k:v for k,v in audit.items() if k!='datasets'},indent=2))
