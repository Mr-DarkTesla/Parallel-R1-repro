from pathlib import Path
import shutil,json,ast
P=Path.cwd();B=P/'work/experiments/base-format-20261010';D=P/'work/experiments/instruct-token-warmup-20261010';E=B/'evaluations';E.mkdir(exist_ok=False)
for p in (D/'evaluations').glob('*.py'):shutil.copy2(p,E/p.name)
for n in ['questions-24.jsonl','questions-128.jsonl']:shutil.copy2(D/'evaluations'/n,E/n)
shutil.copytree(D/'evaluations/runtime',E/'runtime',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
p=E/'evaluate.py';s=p.read_text().replace("'force_think_prefix':True","'force_think_prefix':False")
s=s.replace("think=tok.encode('<think>\\n',add_special_tokens=False)","think=[]")
# Native optional mode must not accidentally append native think when empty.
s=s.replace("if prefix[-len(think):]!=think:","if think and prefix[-len(think):]!=think:")
s=s.replace("summary['system_file']=manifest.get('system_file')", "summary.update(think_wrapped=False,constrained_decoding=False,base_format_schema_version=1,prompt_mode='plain Instruction/Problem/Solution',learned_parallel_measurement='autonomous sampled Parallel opener and width; runtime injects Path headers and synchronization bridges');summary['system_file']=manifest.get('system_file')")
ast.parse(s);p.write_text(s)
p=E/'summary_metrics.py';s=p.read_text();begin=s.index('def canonical_format_flags(text):');end=s.index('\ndef extract_visible',begin)
replacement='''def canonical_format_flags(text):
    errors,widths=canonical_check_format(text)
    no_think='<think>' not in text and '</think>' not in text
    finals=list(re.finditer(r'(?im)^Final Answer:\\s*',text))
    blocks=list(re.finditer(r'<Parallel>.*?</Parallel>\\s*<Summary>.*?</Summary>',text,re.S))
    final_outside=len(finals)==1 and not any(m.start()<=finals[0].start()<m.end() for m in blocks)
    plan_valid=True;previous=0
    for block in blocks:
        leading=text[previous:block.start()];plan=leading.rsplit('Plan:',1)[-1] if 'Plan:' in leading else ''
        header=re.match(r'<Parallel>([2-8])\\n',block.group())
        assigned=[int(x) for x in re.findall(r'^\\s*([1-8]):',plan,re.M)]
        plan_valid=plan_valid and header is not None and assigned==list(range(1,int(header.group(1))+1))
        previous=block.end()
    strict=no_think and not errors and final_outside and plan_valid
    return dict(format=float(strict),parallel_format_valid=float(not errors),think_valid=float(no_think),format_schema_version=3,max_width=max(widths,default=0))
'''
s=s[:begin]+replacement+s[end:]
old="'widths':[int(x) for x in re.findall(r'<Parallel>\\s*([2-8])(?:\\s|<Path>)',r.get('output',''))]"
new="'widths':executed_widths(r)"
assert old in s;s=s.replace(old,new)
helper='''def executed_widths(r):
 if r.get('mode')=='native':return []
 groups=[];current=0
 for call in r.get('trace',{}).get('policy_calls',[]):
  if call.get('phase')=='path':current+=1
  elif current:groups.append(current);current=0
 if current:groups.append(current)
 assert len(groups)==int(r.get('stats',{}).get('forks',0))
 return groups

'''
s=s.replace('def normalize_row',helper+'def normalize_row') if 'def normalize_row' in s else helper+s
ast.parse(s);p.write_text(s)
run=(D/'evaluations/run_eval.sh').read_text().replace('instruct-token-warmup-20261010/evaluations','base-format-20261010/evaluations').replace('warm4beval','base4beval');(E/'run_eval.sh').write_text(run)
print('PREPARED BASE no-think unconstrained runtime/scorer; actual executedwidths')
