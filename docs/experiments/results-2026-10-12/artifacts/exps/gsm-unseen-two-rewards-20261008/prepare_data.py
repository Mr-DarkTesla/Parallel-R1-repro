"""Prepare full GSM-Infinite ops2..6; retain the original screening split."""
from pathlib import Path
import json,hashlib,random,re,collections
RUN=Path(__file__).resolve().parent
screen=RUN.parent/'rl-dataset-screen-20261007'
# Reuse the already audited MATH/SFT exclusion and original RL prompt template.
namespace={'__file__':str(screen/'prepare.py')}
exec(compile((screen/'prepare.py').read_text().split('\ngsm=[]')[0],'screen_prepare','exec'),namespace)
pd=namespace['pd'];fetch=namespace['fetch'];norm=namespace['norm'];overlap=namespace['overlap']
prefix=namespace['prefix'];tokenizer=namespace['tokenizer'];DATA=namespace['DATA']
held=pd.read_parquet(screen/'gsm_infinite.parquet').to_dict('records')
held_ids={x['index'] for x in held};held_questions=set()
source=[]
for op in range(2,7):
    path=fetch('InfiniAILab/gsm_infinite_medium_0',f'data/ops_{op}-00000-of-00001.parquet','c6c5ab433565ddfe3e38e22be165b5c40e6bd576')
    for i,row in pd.read_parquet(path).iterrows():
        ident=f'gsm_infinite_ops{op}/ops{op}/{i}'
        q=row.problem+'\n'+row.question
        if ident in held_ids:held_questions.add(norm(q))
        source.append((ident,op,q,row))
assert len(held_ids)==256 and len(held_questions)==256
train=[];reject=[];seen=set()
for ident,op,q,row in source:
    key=norm(q)
    if key in held_questions:reject.append((ident,'screening_holdout'));continue
    if key in seen:reject.append((ident,'duplicate'));continue
    match=overlap(q)
    if match:reject.append((ident,match));continue
    answer=re.findall(r'Answer:\s*(-?\d+(?:\.\d+)?)',row.solution)
    assert len(answer)==1,(ident,row.solution)
    rules=row.messages[1]['content'].replace("'Answer: xxx'","'Final Answer: xxx'")
    prompt=[dict(role='user',content=prefix+rules+'\n\n'+q)]
    n=len(tokenizer.apply_chat_template(prompt,add_generation_prompt=True))
    if n>2000:reject.append((ident,'overlong_prompt'));continue
    train.append(dict(data_source='gsm_infinite_train',prompt=prompt,ability='math',index=ident,
                      reward_model={'ground_truth':answer[0],'style':'rule'},
                      extra_info={'index':ident,'op':op,'reward_method':'accuracy_parallel_interv_reward'}))
    seen.add(key)
assert not seen.intersection(held_questions)
random.Random(20261008).shuffle(train)
for row in held:
    row['data_source']='gsm_infinite_heldout'
    row['extra_info']={'index':row['index'],'op':row['extra_info']['op'],'reward_method':'accuracy_reward'}
apo=pd.read_parquet(DATA/'APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet')
mathrows=apo[apo.data_source=='APO_MATH300'].to_dict('records')
assert len(mathrows)==316,len(mathrows)
for i,row in enumerate(mathrows):
    row['index']=f'MATH316/{i}';row['extra_info']={'index':row['index'],'op':-1,'reward_method':'accuracy_reward'}
val=held+mathrows
fields=['data_source','prompt','ability','index','reward_model','extra_info']
for name,rows in [('train',train),('validation',val)]:
    pd.DataFrame([{k:r[k] for k in fields} for r in rows]).to_parquet(RUN/f'{name}.parquet',index=False)
pd.DataFrame([{k:r[k] for k in fields} for r in held[:8]]).to_parquet(RUN/'smoke-validation.parquet',index=False)
audit={'train_rows':len(train),'train_by_op':dict(collections.Counter(r['extra_info']['op'] for r in train)),
       'heldout_gsm_rows':256,'math_validation_only_rows':316,'source_revision':'c6c5ab433565ddfe3e38e22be165b5c40e6bd576',
       'excluded_math_rows':12500,'excluded_sft_rows':5910,'rejections':reject,
       'split':'Normalized exact question disjoint; shared generator templates remain. Original 256 screening questions held out.',
       'decontamination':'Normalized exact and number-masked trigram Jaccard>=0.65 against all MATH and SFT; not semantic proof.',
       'gold_histogram':dict(collections.Counter(r['reward_model']['ground_truth'] for r in train)),
       'data_sha256':{name:hashlib.sha256((RUN/name).read_bytes()).hexdigest() for name in ['train.parquet','validation.parquet','smoke-validation.parquet']}}
(RUN/'data-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps({k:v for k,v in audit.items() if k not in ['rejections','gold_histogram']},indent=2))
