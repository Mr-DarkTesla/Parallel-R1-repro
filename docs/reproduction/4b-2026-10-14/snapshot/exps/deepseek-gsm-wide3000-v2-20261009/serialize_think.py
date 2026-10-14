"""Publish checked SFT with all solution work inside think; preserve raw journal."""
import argparse,collections,hashlib,json,time
from pathlib import Path
import pandas as pd
from transformers import AutoTokenizer
from validate import validate
from layout import split_solution

ROOT=Path(__file__).resolve().parent
RAW=ROOT/'production'
OUT=RAW/'sft-think'
BASE=ROOT.parent.parent

def save(path,value):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)

def export(preview=False):
    OUT.mkdir(exist_ok=True)
    system=(ROOT/'student-system.txt').read_text()
    (OUT/'student-system.txt').write_text(system)
    tok=AutoTokenizer.from_pretrained(BASE/'exps/sft-unseen-three-datasets-20261008/runs/01_gsm_infinite/final',local_files_only=True)
    data=(RAW/'journal.jsonl').read_text()
    lines=data.splitlines()
    if not data.endswith('\n'):lines=lines[:-1]
    raw=[r['row'] for r in map(json.loads,lines) if r['decision']=='accepted']
    assert len({r['id'] for r in raw})==len(raw)
    rows=[]
    for original in raw:
        assert original['source']=='GSM_Infinite'
        trace=original['response'].strip();shape=validate(trace)
        assert shape['valid'],(original['id'],shape['errors'])
        body,answer=split_solution(trace)
        assert answer.splitlines()[-1].startswith('Final Answer: ') and body.strip()
        assert '<think>' not in trace and '</think>' not in trace
        wrapped='<think>\n'+body.rstrip()+'\n</think>\n\n'+answer
        messages=[{'role':'system','content':system},{'role':'user','content':original['problem']},{'role':'assistant','content':wrapped}]
        rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=False)
        assistant=rendered.rsplit('<|im_start|>assistant',1)[1]
        assert assistant.count('<think>')==1 and assistant.count('</think>')==1
        thinking=assistant.split('<think>',1)[1].split('</think>',1)[0]
        final=assistant.split('</think>',1)[1].strip().removesuffix('<|im_end|>').strip()
        assert thinking.strip()==body.strip() and final==answer,(original['id'],'template altered trace')
        assert thinking.count('<Parallel>')==original['fork_count']
        prefix=tok.apply_chat_template(messages[:-1],tokenize=False,add_generation_prompt=True)
        completion=body.rstrip()+'\n</think>\n\n'+answer if prefix.rstrip().endswith('<think>') else wrapped
        loader_rendered=prefix+completion+tok.eos_token
        loader_assistant=loader_rendered.rsplit('<|im_start|>assistant',1)[1]
        assert loader_assistant.count('<think>')==1 and loader_assistant.count('</think>')==1
        assert loader_assistant.split('<think>',1)[1].split('</think>',1)[0].strip()==body.strip()
        tokens=len(tok.encode(prefix,add_special_tokens=False))+len(tok.encode(completion+tok.eos_token,add_special_tokens=False))
        assert tokens<=16384,(original['id'],tokens)
        row={**original,'response':completion,'assistant_content':wrapped,'messages':messages,'prompt_messages':json.dumps(messages[:-1],ensure_ascii=False),'student_tokens':tokens,'student_system_sha256':hashlib.sha256(system.encode()).hexdigest(),'serialization_version':'counted-forks-think-tail-final-v4','raw_journal_reference':str(RAW/'journal.jsonl')}
        rows.append(row)
    if preview:
        (OUT/'preview.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
        save(OUT/'preview-validation.json',dict(at=time.time(),rows=len(rows),all_rendered_single_think=True,all_parallel_blocks_inside_think=True,final_answers_outside_think=True,max_student_tokens=max((r['student_tokens'] for r in rows),default=0)))
        return
    assert (RAW/'COMPLETED').exists() and len(rows)==3000
    original_splits={s:{r['id'] for r in map(json.loads,(RAW/f'{s}.jsonl').read_text().splitlines())} for s in ['train','val']}
    assert original_splits['train'].isdisjoint(original_splits['val'])
    assert len(original_splits['train'])==2700 and len(original_splits['val'])==300
    for split,ids in original_splits.items():
        selected=[r for r in rows if r['id'] in ids];assert len(selected)==len(ids)
        (OUT/f'{split}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in selected))
        pd.DataFrame([{k:r[k] for k in ['id','problem','answer','response','prompt_messages','source','fork_count','branch_schedule','student_tokens']} for r in selected]).to_parquet(OUT/f'{split}.parquet',index=False)
    report=dict(complete=True,accepted=3000,train=2700,val=300,serialization_version='counted-forks-think-tail-final-v4',all_rendered_single_think=True,all_parallel_blocks_inside_think=True,final_answers_outside_think=True,sources={'GSM_Infinite':3000},sha256={f:hashlib.sha256((OUT/f).read_bytes()).hexdigest() for f in ['train.jsonl','val.jsonl','train.parquet','val.parquet','student-system.txt']})
    save(OUT/'summary.json',report);(OUT/'READY').write_text(str(time.time())+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--watch',action='store_true');parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    try:
        if args.watch:
            while not (RAW/'COMPLETED').exists():
                if (RAW/'fatal-error.json').exists():raise RuntimeError('Raw generation failed')
                s=json.loads((RAW/'status.json').read_text())
                if s['state']=='pool_exhausted':raise RuntimeError('GSM pool exhausted before target')
                save(ROOT/'think-export-status.json',dict(state='waiting_for_raw_completion',at=time.time(),accepted=s['accepted']))
                time.sleep(30)
        export(preview=args.preview)
        save(ROOT/'think-export-status.json',dict(state='preview_checked' if args.preview else 'complete',at=time.time(),output=str(OUT)))
    except BaseException as error:
        save(ROOT/'think-export-error.json',dict(error=repr(error),at=time.time()));raise
