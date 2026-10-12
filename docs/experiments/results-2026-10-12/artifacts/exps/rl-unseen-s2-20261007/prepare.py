import shutil,json,hashlib,subprocess,os
from pathlib import Path
import pyarrow.parquet as pq
ROOT=Path('${PROJECT_ROOT}');RUN=Path(__file__).resolve().parent;OLD=ROOT/'exps/rl-unseen-s1-20261007-seq128'
assert RUN.is_relative_to(ROOT)
assert not (RUN/'code').exists(), 'Never overwrite a frozen snapshot'
shutil.copytree(OLD/'code',RUN/'code',symlinks=True)
for f in ['verl/verl/workers/fsdp_workers.py','verl/verl/workers/actor/dp_actor.py','verl/verl/workers/rollout/vllm_rollout/decode_graph.py','verl/verl/trainer/config/rl_qwen3_06b.yaml']:
 shutil.copyfile(RUN/'overlay'/f,RUN/'code'/f)
m=json.loads((RUN/'manifest.json').read_text())
for f,h in {**m['changed_file_sha256'],**m['data_sha256']}.items():assert hashlib.sha256((RUN/'code'/f).read_bytes()).hexdigest()==h,f
base=RUN/'code/verl/data_preprocess_scripts/data/dapo/adaptive_parallel_thinking_final_with_prompt_v3'
a=pq.read_table(base/'rl_all_accuracy_reward/train.parquet').to_pylist();b=pq.read_table(base/'rl_all_accuracy_parallel_interv_reward/train.parquet').to_pylist()
assert len(a)==len(b)==17917
for x,y in zip(a,b):
 assert x['extra_info'].pop('reward_method')=='accuracy_reward'
 assert y['extra_info'].pop('reward_method')=='accuracy_parallel_interv_reward'
 assert x==y,'S2 must not change questions, order, labels, prompts or other metadata'
(RUN/'data-check.json').write_text(json.dumps(dict(rows=len(a),same_except_reward=True,validation='unchanged accuracy-only'),indent=2))
env=dict(os.environ,TMPDIR=str(ROOT/'t'),HF_HOME=str(ROOT/'cache/huggingface'))
with (RUN/'preflight.log').open('w') as log:
 p=subprocess.run([str(ROOT/'.venv/bin/python'),str(RUN/'run.py'),'--preflight'],cwd=RUN,env=env,stdout=log,stderr=subprocess.STDOUT)
print((RUN/'preflight.log').read_text()[-2500:]);assert p.returncode==0
(RUN/'READY').write_text(m['commit'])
