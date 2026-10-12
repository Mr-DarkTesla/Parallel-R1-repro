"""Prepare one checked 5145-row SFT without altering either source corpus."""
from pathlib import Path
import collections,hashlib,json,re,sys
import pandas as pd
from transformers import AutoTokenizer
ROOT=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
BASE=ROOT/'exps/sft-unseen-three-datasets-20261008/base'
tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True)
system=(ROOT/'exps/deepseek-gsm-wide3000-v2-20261009/student-system.txt').read_text()
oldpath=ROOT/'exps/deepseek-gsm-only-20261009/production/accepted-at-user-stop.jsonl'
old=[json.loads(x) for x in oldpath.read_text().splitlines()]
newdir=ROOT/'exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think'
assert (newdir/'READY').exists()
oldval=set(sorted(range(len(old)),key=lambda i:hashlib.sha256(('wide5145-seed1:'+old[i]['problem']).encode()).hexdigest())[:215])
sources=[('old','val' if i in oldval else 'train',r) for i,r in enumerate(old)]
for split in ['train','val']:sources += [('new',split,json.loads(x)) for x in (newdir/f'{split}.jsonl').read_text().splitlines()]
assert len(sources)==5145 and len({r['problem'] for _,_,r in sources})==5145
rows=[];widths=collections.Counter()
for source,split,r in sources:
    if source=='new':content=r['assistant_content']
    else:
        body,sep,final=r['response'].strip().rpartition('\nFinal Answer:')
        assert sep and body.strip(),r['id']
        content='<think>\n'+body.rstrip()+'\n</think>\n\nFinal Answer:'+final
    # Whitespace between siblings is a causal bridge. Preserve every path byte,
    # the sampled width header and branch IDs; remove only external separators.
    def compact(m):
        body=m.group(1);first=body.index('<Path>');head=body[:first]
        paths=re.findall(r'<Path>.*?</Path>',body,re.S)
        assert not re.sub(r'<Path>.*?</Path>','',body[first:],flags=re.S).strip()
        width=int(head.strip());assert width==len(paths) and 2<=width<=8
        assert [int(re.match(r'<Path>(\d+)',p).group(1)) for p in paths]==list(range(1,width+1))
        widths[width]+=1
        return '<Parallel>'+head+''.join(paths)+'</Parallel>'
    content=re.sub(r'<Parallel>(.*?)</Parallel>',compact,content,flags=re.S)
    assert content.count('<think>')==content.count('</think>')==1
    messages=[dict(role='system',content=system),dict(role='user',content=r['problem'])]
    prefix=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    response=content.split('<think>',1)[1].lstrip('\n') if prefix.rstrip().endswith('<think>') else content
    ids=tok.encode(prefix,add_special_tokens=False)+tok.encode(response+tok.eos_token,add_special_tokens=False)
    assert len(ids)<=16384,(r['id'],len(ids))
    rows.append(dict(id=source+':'+r['id'],source_generation=source,split=split,problem=r['problem'],answer=r['answer'],
        response=response,prompt_messages=json.dumps(messages,ensure_ascii=False),total_tokens=len(ids),branch_schedule=r['branch_schedule']))
for split in ['train','val']:
    subset=[r for r in rows if r['split']==split]
    pd.DataFrame(subset).to_parquet(RUN/'data'/f'{split}.parquet',index=False)
    (RUN/'data'/f'{split}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in subset))
assert not set(r['problem'] for r in rows if r['split']=='train')&set(r['problem'] for r in rows if r['split']=='val')
train=pd.DataFrame([r for r in rows if r['split']=='train']);val=pd.DataFrame([r for r in rows if r['split']=='val'])
train.nlargest(8,'total_tokens').to_parquet(RUN/'data/canary-train.parquet',index=False)
val.nlargest(8,'total_tokens').to_parquet(RUN/'data/canary-val.parquet',index=False)
report=dict(rows=len(rows),train=len(train),val=len(val),widths=dict(widths),max_tokens=max(r['total_tokens'] for r in rows),
    quantiles=train.total_tokens.quantile([.5,.9,.99]).to_dict(),base=str(BASE),base_source=json.loads((BASE/'source.json').read_text()),
    source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [oldpath,newdir/'train.jsonl',newdir/'val.jsonl']},
    split_policy='Keep new train/val; deterministic problem hash old 1930/215; no overlap',
    transformations='Common counted-fork system prompt; old reasoning wrapped in think, final outside; remove external sibling whitespace only')
(RUN/'data-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
