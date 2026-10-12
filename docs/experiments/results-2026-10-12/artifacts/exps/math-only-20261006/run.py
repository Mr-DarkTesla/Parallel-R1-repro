import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

root = Path('${PROJECT_ROOT}')
q = Path(__file__).resolve().parent
name = 'unseen-sync'
result = q / 'results/eval' / name
result.mkdir(parents=True, exist_ok=True)
source = root / 'verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet'
data = pd.read_parquet(source)
data = data[data.data_source == 'APO_MATH300']
assert len(data) == 316
data.to_parquet(q / 'math.parquet', index=False)
checkpoint = root / 'exps/fixes-20261005/results/train/Parallel-SFT-Unseen-Qwen3-0.6B-fixed-mb4-20261005/final'
env = os.environ.copy()
env.update(PATH=str(root / '.venv/bin') + ':' + env['PATH'], CUDA_VISIBLE_DEVICES='0,1', NPROC_PER_NODE='2', OMP_NUM_THREADS='1', RAY_TMPDIR='${TMPDIR}/pr1math', PARALLEL_R1_OUTPUT_ROOT=str(q / 'results'), PARALLEL_R1_EVAL_NAME=name)
cmd = ['bash', 'training_scripts/eval_qwen3_06b.sh', str(checkpoint), 'actor_rollout_ref.rollout.mode=sync', 'actor_rollout_ref.rollout.enforce_eager=true', 'data.val_batch_size=256', f'data.val_files={q / "math.parquet"}', 'ray_init.num_cpus=16']
(q / 'command.json').write_text(json.dumps(cmd, indent=2))
(q / 'started').write_text(datetime.now(timezone.utc).isoformat())
with (result / 'driver.log').open('w') as log:
    rc = subprocess.run(cmd, cwd=root / 'verl', env=env, stdout=log, stderr=subprocess.STDOUT).returncode
(q / 'exit_code').write_text(str(rc))
if rc == 0:
    rows = [json.loads(line) for line in (result / '0.jsonl').open()]
    assert len(rows) == 316 and len({r['input'] for r in rows}) == 316
    assert all(r['data_source'] == 'APO_MATH300' for r in rows)
    summary = dict(complete=True, answers=len(rows), correct=sum(r['acc'] for r in rows), mean=sum(r['acc'] for r in rows) / len(rows), checkpoint=str(checkpoint), mode='sync', batch=256, eager=True)
    (q / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
(q / 'finished').write_text(datetime.now(timezone.utc).isoformat())
raise SystemExit(rc)
