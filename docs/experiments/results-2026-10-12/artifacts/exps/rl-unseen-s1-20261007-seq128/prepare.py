import shutil,json,hashlib,subprocess,os
from pathlib import Path
ROOT=Path('${PROJECT_ROOT}');RUN=Path(__file__).resolve().parent
assert RUN.is_relative_to(ROOT)
old=ROOT/'exps/rl-unseen-s1-20261006'
if not (RUN/'code').exists():shutil.copytree(old/'code',RUN/'code',symlinks=True)
shutil.copyfile(RUN/'dp_actor.py',RUN/'code/verl/verl/workers/actor/dp_actor.py')
m=json.loads((RUN/'manifest.json').read_text())
for name,digest in {**m['changed_file_sha256'],**m['data_sha256']}.items():assert hashlib.sha256((RUN/'code'/name).read_bytes()).hexdigest()==digest,name
env=dict(os.environ,TMPDIR=str(ROOT/'t'),HF_HOME=str(ROOT/'cache/huggingface'))
with (RUN/'preflight.log').open('w') as log:
 p=subprocess.run([str(ROOT/'.venv/bin/python'),str(RUN/'run.py'),'--preflight'],cwd=RUN,env=env,stdout=log,stderr=subprocess.STDOUT)
print('preflight_exit',p.returncode);print((RUN/'preflight.log').read_text()[-2500:])
raise SystemExit(p.returncode)
