"""Rescore all prior outputs under identical historical and think-agnostic extraction."""
import score
import json,re
from pathlib import Path
WORK=Path(__file__).resolve().parent
OLD=WORK.parents[3]/'exps/math500-new-sft-20261008/runs'
questions={q['index']:q for q in map(json.loads,(WORK/'questions.jsonl').read_text().splitlines())}
results={}
for name in ['gsm_infinite_ep5','sft_messages_ep5','mixed_ep1']:
    run=OLD/name;files=list((run/'results').rglob('0.jsonl'));assert len(files)==1
    records=list(map(json.loads,files[0].read_text().splitlines()));assert len(records)==500
    assert set(r['sample_index'] for r in records)==set(questions)
    detailed=[]
    for r in records:
        q=questions[r['sample_index']];historical=score.grade(r['output'],q['answer']);final_only=score.grade(re.sub(r'</?think>','',r['output']),q['answer'])
        detailed.append(dict(index=q['index'],id=q['id'],historical=historical,final_answer_only=final_only))
    oldsummary=json.loads((run/'summary.json').read_text())
    historical_correct=sum(d['historical']['correct'] for d in detailed)
    final_correct=sum(d['final_answer_only']['correct'] for d in detailed)
    errors=[d for d in detailed if d['historical']['error'] or d['final_answer_only']['error']]
    (WORK/f'previous-{name}-scores.jsonl').write_text(''.join(json.dumps(d,ensure_ascii=False)+'\n' for d in detailed))
    results[name]=dict(n=500,historical_correct=historical_correct,historical_pass_at_1=historical_correct/500,final_answer_only_correct=final_correct,final_answer_only_pass_at_1=final_correct/500,old_summary_correct=oldsummary.get('correct'),errors=errors)
    assert not errors
    assert historical_correct==oldsummary['correct'],(name,historical_correct,oldsummary['correct'])
(WORK/'previous-comparison.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results))
