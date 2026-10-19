"""Strict counted-fork grammar, ownership IDs and final-line checks."""
import json,re
from pathlib import Path

TAG=re.compile(r'</?(?:Parallel|Path|Summary)>')
BLOCK=re.compile(r'<Parallel>([2-8])\n((?:<Path>[1-8]\n[\s\S]*?</Path>\s*)+)</Parallel>\s*<Summary>([\s\S]*?)</Summary>')

def has_explicit_arithmetic(body):
    # GSM paths must show a derived computation; numeric aliases aren't work.
    numeric=r'-?\d+(?:\.\d+)?'
    if re.search(r'\\frac\s*\{\s*'+numeric+r'\s*\}\s*\{\s*'+numeric+r'\s*\}',body):return True
    flat=body.replace('{','').replace('}','')
    if re.search(numeric+r'(?:\s+[A-Za-z]+){0,6}\s*(?:\+|×|−|\\times|\\cdot|\bplus\b|\bminus\b|\btimes\b)\s*'+numeric,flat):return True
    op=r'(?:\+|−|-|\*|×|÷|/|\^|\\times|\\cdot|\\div|\bplus\b|\bminus\b|\btimes\b)'
    return bool(re.search(numeric+r'\s*'+op+r'\s*'+numeric,flat) or re.search(numeric+r'\s*\(\s*'+numeric+r'\s*\)',flat))

def validate(text):
    errors=[]; widths=[]; blocks=[]; cursor=0; duplicate_paths=0
    for m in BLOCK.finditer(text):
        before=text[cursor:m.start()]
        if TAG.search(before):errors.append('unexpected_tags_between_blocks')
        if 'Plan:' not in before:errors.append('missing_plan');plan='';intro=''
        else:intro,plan=before.rsplit('Plan:',1)
        if not intro.strip():errors.append('missing_prefork_explanation')
        assignments=re.findall(r'^([1-8]):\s*(\S.*)$',plan,re.M)
        n=int(m[1]);widths.append(n)
        expected=[str(i) for i in range(1,n+1)]
        if [i for i,_ in assignments]!=expected:errors.append('plan_ids_or_count')
        paths=re.findall(r'<Path>([1-8])\n([\s\S]*?)</Path>',m[2])
        if [i for i,_ in paths]!=expected:errors.append('path_ids_or_count')
        for i,body in paths:
            if not body.strip():errors.append('empty_path')
            if not has_explicit_arithmetic(body):errors.append('path_without_explicit_computation')
            if TAG.search(body):errors.append('nested_or_stray_path_tags')
            if re.search(r'(?im)^Final Answer:',body):errors.append('branch_final_answer')
        if not m[3].strip():errors.append('empty_summary')
        if TAG.search(m[3]):errors.append('tags_inside_summary')
        normalized=[' '.join(b.split()) for _,b in paths]
        duplicate_paths+=len(normalized)-len(set(normalized))
        blocks.append({'width':n,'assignments':assignments,'paths':paths,'summary':m[3],'intro':intro})
        cursor=m.end()
    if TAG.search(text[cursor:]):errors.append('unparsed_structural_tags')
    final=re.findall(r'^Final Answer:\s*(.+)$',text,re.M)
    if len(final)!=1:errors.append('final_answer_count')
    elif not text.rstrip().endswith('Final Answer: '+final[0]):errors.append('final_answer_not_last')
    elif 'unresolved' in final[0].lower():errors.append('unresolved')
    if '```' in text:errors.append('code_fence')
    if '\nFinal solution:\n' not in text:errors.append('missing_final_solution')
    else:
        final_solution=text.split('\nFinal solution:\n',1)[1]
        if TAG.search(final_solution):errors.append('tags_in_final_solution')
    return dict(exact_duplicate_paths=duplicate_paths,valid=not errors,errors=sorted(set(errors)),rounds=len(widths),widths=widths,final=final[0] if len(final)==1 else None,blocks=blocks)

if __name__=='__main__':
    import sys
    p=Path(sys.argv[1]);rows=[]
    for r in map(json.loads,p.read_text().splitlines()):
        v=validate(r['output']);v.pop('blocks');rows.append({'id':r['id'],'finish_reason':r['finish_reason'],**v})
    p.with_name('structure.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows,indent=2))
