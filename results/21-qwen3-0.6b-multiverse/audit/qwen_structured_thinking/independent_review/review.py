"""CPU-only independent audit; source inputs are read-only."""
import json
import pathlib
import re
import sys
ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts/exp21'))
from mv_format import parse, ANY_TAG
BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(__file__).resolve().parent
GOLD = {r['id']: r for r in map(json.loads, (BASE / 'candidates149_with_gold.jsonl').read_text().splitlines())}
NOTES = {
'gsm8k-train/5368': ('30/6+60/6+42/6=5+10+7=22', 'Independent allocations from common prepared quantities. Prefix already solves entire task; low incremental parallel value. Source mistakenly says no independent parts.'),
'gsm8k-train/5148': ('20+2*25+20/2+2*28=136', 'Independent class groups; first path also recalls fourth class from common prefix. Could tag second/third and fifth/sixth totals only.'),
'math-train/1132': ('(5*(3/2)**2-13*(3/2)+4)*(2*(3/2)-3)=(-17/4)*0=0', 'Independent factors. Source calls trinomial 5a²-13a+4 a binomial and suggests FOIL; terminology false although six distributed products and all arithmetic correct. Source says both methods give 0 before expanded evaluation occurs, then substantiates it.'),
'math-train/2553': ('sqrt(30*15*10*5)=150; heights=300/15,300/20,300/25=20,15,12', 'Independent altitude cases from shared area. Prefix setup allowed by actual decoder context; if literal problem-only rule applies, area 150 must be derived within each path.'),
'gsm8k-train/531': ('3*2+2*2=10', 'Independent species totals. Standard gold interpretation is cumulative recovery hours; concurrent recovery duration unspecified.'),
'gsm8k-train/5086': ('10*.2+10*.5=7', 'Independent discount savings. Later source parts regular cost/savings are less natural grouping but arithmetic sound.'),
'gsm8k-train/396': ('7*(2+3+2*3)=77', 'Three independent weekly quantities from shared setup. Third path uses prepared 6, not another path result.'),
'gsm8k-train/5661': ('60*4+90*2=420', 'Independent revenues. Price per bacon slice inferred from intended gold reading; wording says add bacon for $2 without explicit serving size.'),
'math-train/1290': ('50*10=500;20*25=500;500/(500+500)*100=50', 'Independent coin values. Dime/quarter denomination uses standard background knowledge. Later final Part 3/4 depend on earlier parts, but tagged paths independent.'),
'math-train/7395': ('det=2*k*k-7*k+6; +15 roots 9/2,-1; -15 discriminant -119', 'Independent sign cases from prepared determinant. All cross-product and quadratic calculations correct. Source calls absolute determinant scalar triple product; signed scalar triple product is determinant, absolute value is volume.'),
'gsm8k-train/6828': ('38*2.5=95;56*3.5=196;95+196=291', 'Independent item costs. Source incorrectly claims no independent quantities later; contradicted by own valid decomposition.'),
'gsm8k-train/5177': ('50-50/5=40;50-4=46;46-40=6', 'Independent student correct-answer counts. Sylvia wording interpreted as one-fifth of 50 incorrect, matching gold.'),
'gsm8k-train/1320': ('8*12=96;5*25=125;96+125=221', 'Independent service incomes; every intermediate calculation correct.'),
'math-train/1173': ('log3(27)+log3(sqrt(3))=3+1/2=7/2', 'Independent logarithm terms after product identity. Opening recalls properties vaguely as log(a)*log(b), but gives no false equality; correct product law follows. Scope log3(27sqrt3) matches gold.'),
'math-train/1128': ('(7/12)*(1/12)=7/144; x=1/3,y=1/4;1/9-1/16=7/144', 'Paths are independent alternative proofs of same quantity. Current MV prompt excludes independent checks; early prompt includes them. Source says solving x,y necessary although identity suffices; redundant, not arithmetic error.'),
'math-train/1961': ('5!/2=60;choose(5,2)*3!=10*6=60', 'Paths are independent alternative proofs of same count. Current MV prompt excludes independent checks; early prompt includes them. Position argument needs explicit 1 in earlier chosen slot, 2 in later slot, logically implied by condition. Final source lacks requested Final Answer: line.')}
rows=[]
for agent in 'abc':
    originals={r['id']:r for r in map(json.loads,(BASE/f'agent_{agent}/input.jsonl').read_text().splitlines())}
    for r in map(json.loads,(BASE/f'agent_{agent}/tagged.jsonl').read_text().splitlines()):
        t=r['response']; original=originals[r['id']]['response']; structure=parse(t)
        recovered=re.sub(r'<Goal>.*?</Goal>|<Conclusion>.*?</Conclusion>','',t,flags=re.S)
        recovered=re.sub(r'<Path>\d+: ','',recovered); recovered=ANY_TAG.sub('',recovered)
        inside=all(t.index('<think>')<b['start']<b['end']<=t.index('</think>') for b in structure['blocks'])
        independent_checks=r['id'] in ('math-train/1128','math-train/1961')
        calc,note=NOTES[r['id']]
        issues=['Conclusion contains instruction, not combined results; actual combination remains outside Parallel.']
        if independent_checks:issues.append('Alternative verification methods outside narrower current prompt scope.')
        if r['id']=='math-train/1132':issues.append('False intermediate terminology: trinomial called binomial/FOIL.')
        if r['id']=='math-train/7395':issues.append('Signed scalar triple product conflated with its absolute value.')
        rows.append(dict(id=r['id'],agent=agent,gold=GOLD[r['id']]['answer'],question_matches_gold=r['question']==GOLD[r['id']]['question'],answer_correct=True,calculation=calc,intermediate_math_valid=r['id'] not in ('math-train/1132','math-train/7395'),paths_independent=True,path_scope_current_prompt=not independent_checks,path_scope_early_prompt=True,strict_grammar=structure['valid'] and all(b['numbered'] for b in structure['blocks']),tags_inside_think=inside,source_text_verbatim_and_order_preserved=recovered==original,conclusion_semantically_complete=False,verdict='needs_correction',notes=note,issues=issues,recommendation='Move existing following result-combination text into Conclusion, preserving source text/order. Replace procedural placeholder. '+('Exclude from narrow quantity/case dataset or explicitly adopt early independent-check scope. ' if independent_checks else '')+('For strict fully correct traces reject source; do not silently rewrite mathematics.' if r['id'] in ('math-train/1132','math-train/7395') else '')))
(OUT/'verdicts.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
summary=dict(reviewed=len(rows),answer_correct=sum(r['answer_correct'] for r in rows),strict_grammar=sum(r['strict_grammar'] for r in rows),tags_inside_think=sum(r['tags_inside_think'] for r in rows),source_preserved=sum(r['source_text_verbatim_and_order_preserved'] for r in rows),paths_independent=sum(r['paths_independent'] for r in rows),current_prompt_scope=sum(r['path_scope_current_prompt'] for r in rows),semantically_complete_conclusion=0,strict_accept=0,needs_correction=16)
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
