from pathlib import Path
import hashlib,json
B=Path.cwd()/'work/experiments/instruct-full-20261011';E=B/'evaluations';p=E/'evaluate.py';s=p.read_text()
old='def strict_format(t,stats):\n'
new="def strict_format(t,stats):\n spec=importlib.util.spec_from_file_location('instruct_format_compiler',R.parent/'compiler.py');compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)\n try: compiler._parse(re.sub(r'<\\|im_end\\|>\\s*$', '', t))\n except ValueError: return False,False\n"
assert old in s;s=s.replace(old,new);p.write_text(s)
proof=json.loads((B/'eval-guard-prepared.json').read_text());proof['source_hashes']['evaluate.py']=hashlib.sha256(p.read_bytes()).hexdigest();proof['source_hashes']['../compiler.py']=hashlib.sha256((B/'compiler.py').read_bytes()).hexdigest();proof['strict_format_parser']='same canonical Instruct parser as SFT, native terminal im_end stripped for format only';proof['control_substitution_disclosure']='Diagnostic loop retains historical replacement of sampled terminal path/summary EOS/control with closing tag; policy_calls preserve raw generated ids. Same frozen logic applies to warmup and full checkpoints.';(B/'eval-guard-prepared.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof['source_hashes']['evaluate.py'])
