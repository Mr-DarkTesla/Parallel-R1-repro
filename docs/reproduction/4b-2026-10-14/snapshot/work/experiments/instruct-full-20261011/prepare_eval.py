from pathlib import Path
import shutil,json,hashlib
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';old=P/'work/experiments/instruct-token-warmup-20261010/evaluations';E=B/'evaluations';E.mkdir(exist_ok=True)
for name in ['evaluate.py','native_eos.py','summary_metrics.py','questions-128.jsonl','questions-24.jsonl','run_eval.sh']:
 shutil.copy2(old/name,E/name)
shutil.copytree(old/'runtime',E/'runtime',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc','._*'))
launcher=E/'run_eval.sh';text=launcher.read_text().replace('instruct-token-warmup-20261010/evaluations','instruct-full-20261011/evaluations').replace('$ROOT/t/warm4beval','$ROOT/work/experiments/instruct-full-20261011/eval-tmp');launcher.write_text(text)
proof=dict(source_namespace=str(old),isolated_output=str(E),corrected_scorer='grade(re.sub(think tags), gold)',response_cap=4096,path_cap=2048,suite=128,seed_policy='42+sample_index; per-call RNG from seed',generation=dict(temperature=.6,top_p=.95,top_k=20,repetition_penalty=1.0),native_im_end=True,parallel_guard_status='pending integration',system_file=str(B/'system.txt'),precision='HF exported bf16; vLLM bf16')
proof['source_hashes']={str(p.relative_to(E)):hashlib.sha256(p.read_bytes()).hexdigest() for p in E.rglob('*') if p.is_file()}
(B/'eval-preparation-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
