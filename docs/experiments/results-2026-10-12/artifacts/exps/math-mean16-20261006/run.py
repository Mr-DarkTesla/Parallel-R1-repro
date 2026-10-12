import hashlib
import json
import os
import re
import subprocess
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

root = Path('${PROJECT_ROOT}')
q = Path(__file__).resolve().parent
code = q / 'code/verl'
state = {}
lock = threading.Lock()
names = ['seen-sync', 'seen-async', 'unseen-sync', 'unseen-async']
def now(): return datetime.now(timezone.utc).isoformat()
def write(path, value): path.write_text(json.dumps(value, indent=2) + '\n')
def update(name, **fields):
    with lock:
        state[name] = dict(updated=now(), **fields)
        write(q / 'status.json', state)
        print(now(), name, fields, flush=True)

source = root / 'verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet'
data = pd.read_parquet(source)
data = data[data.data_source == 'APO_MATH300'].reset_index(drop=True)
assert len(data) == 316
# Explicitly repeat each question 16 times; keep generation n=1.
data = data.loc[data.index.repeat(16)].reset_index(drop=True)
data.to_parquet(q / 'math16.parquet', index=False)
write(q / 'protocol.json', dict(questions=316, samples_per_question=16, answers_per_run=5056, names=names, batch=1024, temperature=1.0, response_tokens=3000, eager=True, checkpoint_epoch=5, code_sha256=hashlib.sha256((q / 'code.tar.gz').read_bytes()).hexdigest(), data_sha256=hashlib.sha256((q / 'math16.parquet').read_bytes()).hexdigest(), ci='Paired question-cluster percentile bootstrap, 50000 draws, seed 20261006. 95% marginal CIs; Bonferroni 99.1667% pair CIs for six comparisons.'))
(q / 'started').write_text(now())

def evaluate(slot, name):
    result = q / 'results/eval' / name
    result.mkdir(parents=True, exist_ok=True)
    variant, mode = name.split('-')
    checkpoint = root / f'exps/fixes-20261005/results/train/Parallel-SFT-{variant.title()}-Qwen3-0.6B-fixed-mb4-20261005/final'
    assert (checkpoint / 'model.safetensors').is_file()
    env = os.environ.copy()
    env.update(PATH=str(root / '.venv/bin') + ':' + env['PATH'], CUDA_VISIBLE_DEVICES=f'{2*slot},{2*slot+1}', NPROC_PER_NODE='2', OMP_NUM_THREADS='1', RAY_TMPDIR=f'${TMPDIR}/parallel_r1_m16_{slot}', PARALLEL_R1_OUTPUT_ROOT=str(q / 'results'), PARALLEL_R1_SCRATCH_ROOT='${SHM_ROOT}/parallel_r1_math16', HF_HOME='${MODEL_ROOT}/huggingface', PARALLEL_R1_EVAL_NAME=name)
    cmd = ['bash', 'training_scripts/eval_qwen3_06b.sh', str(checkpoint), f'actor_rollout_ref.rollout.mode={mode}', 'actor_rollout_ref.rollout.enforce_eager=true', 'actor_rollout_ref.rollout.val_kwargs.n=1', 'data.val_batch_size=1024', f'data.val_files={q / "math16.parquet"}', 'ray_init.num_cpus=16']
    write(result / 'command.json', cmd)
    update(name, status='running', gpus=[2*slot, 2*slot+1])
    started = time.monotonic()
    with (result / 'driver.log').open('w') as log:
        rc = subprocess.run(cmd, cwd=code, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    (result / 'exit_code').write_text(str(rc))
    (result / 'finished').write_text(now())
    assert rc == 0, f'{name}: exit {rc}'
    groups = defaultdict(list)
    for line in (result / '0.jsonl').open():
        row = json.loads(line)
        assert row['data_source'] == 'APO_MATH300' and row['acc'] in (0, 1)
        groups[row['input']].append(row)
    assert len(groups) == 316 and all(len(rows) == 16 for rows in groups.values())
    means = {prompt: sum(r['acc'] for r in rows)/16 for prompt, rows in groups.items()}
    mean = sum(means.values())/316
    logged = re.findall(r'val-core/APO_MATH300/acc/mean@16:([0-9.e+-]+)', (result / 'driver.log').read_text())
    assert logged and abs(float(logged[-1])-mean) < 1e-7
    write(result / 'summary.json', dict(complete=True, answers=5056, correct=round(mean*5056), mean=mean, seconds=time.monotonic()-started, mean_unique_outputs=np.mean([len({r['output'] for r in rows}) for rows in groups.values()])))
    update(name, status='complete', answers=5056, mean=mean)
    return means

try:
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {name: pool.submit(evaluate, slot, name) for slot, name in enumerate(names)}
        results = {}
        for name, future in futures.items():
            try: results[name] = future.result()
            except Exception as error: update(name, status='failed', error=str(error))
    assert len(results) == 4, 'Not all evaluations completed'
    prompts = sorted(results[names[0]])
    assert all(set(r) == set(prompts) for r in results.values())
    values = np.array([[results[name][p] for name in names] for p in prompts])
    rng = np.random.default_rng(20261006)
    boot = np.concatenate([values[rng.integers(0, len(prompts), size=(1000, len(prompts)))].mean(axis=1) for _ in range(50)])
    summary = dict(complete=True, questions=316, answers_per_model=5056, finished=now(), estimates={}, comparisons=[])
    for index, name in enumerate(names):
        summary['estimates'][name] = dict(mean=float(values[:,index].mean()), ci95=np.quantile(boot[:,index], [.025,.975]).tolist())
    for a in range(4):
        for b in range(a+1,4):
            delta = boot[:,a] - boot[:,b]
            summary['comparisons'].append(dict(a=names[a], b=names[b], difference=float((values[:,a]-values[:,b]).mean()), ci95=np.quantile(delta,[.025,.975]).tolist(), ci_family95=np.quantile(delta,[.05/12,1-.05/12]).tolist()))
    write(q / 'summary.json', summary)
    write(q / 'per-question.json', dict(names=names, prompts=prompts, mean_correct=values.tolist()))
    (q / 'exit_code').write_text('0')
except Exception:
    (q / 'exit_code').write_text('1')
    raise
finally:
    (q / 'finished').write_text(now())
