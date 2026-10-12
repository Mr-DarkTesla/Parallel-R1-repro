"""Plain autoregressive Qwen3-0.6B baselines on the existing test questions."""
import hashlib
import json
import os
import subprocess
import threading
import traceback
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

ROOT = Path('${PROJECT_ROOT}')
WORK = Path(__file__).resolve().parent
MODEL = Path('${MODEL_ROOT}/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca')
TAGS = ['<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>']
state = {}
lock = threading.Lock()

def now():
    return datetime.now(timezone.utc).isoformat()

def write(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2) + '\n')
    temp.replace(path)

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def update(name, **fields):
    with lock:
        state[name] = dict(updated=now(), **fields)
        write(WORK / 'status.json', state)
        print(now(), name, fields, flush=True)

def prepare():
    source = ROOT / 'verl/data_preprocess_scripts/data/APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_reward/test.parquet'
    math500 = ROOT / 'exps/branch-diversity-20261006/math500.parquet'
    original = pd.read_parquet(source)
    assert original.groupby('data_source').size().to_dict() == {'APO_AIME24': 480, 'APO_AIME25': 480, 'APO_AMC23': 640, 'APO_MATH300': 316}
    math = original[original.data_source == 'APO_MATH300']
    math = math.loc[math.index.repeat(16)]
    extra = pd.read_parquet(math500)
    assert len(extra) == 500
    extra['data_source'] = 'APO_MATH500'
    data = pd.concat([original[original.data_source != 'APO_MATH300'], math, extra], ignore_index=True)
    instruction = 'Solve the following problem step by step.\nEnd your response with a line starting with Final Answer: followed by the final result.\n\nProblem: '
    prompts = []
    for prompt in data['prompt']:
        assert len(prompt) == 1 and prompt[0]['role'] == 'user'
        old = prompt[0]['content']
        assert '\n\nProblem: ' in old
        problem = old.split('\n\nProblem: ', 1)[1]
        clean = instruction + problem
        assert not any(tag in clean for tag in TAGS)
        prompts.append([dict(role='user', content=clean)])
    data['prompt'] = prompts
    assert len(data) == 7156
    data.to_parquet(WORK / 'plain.parquet', index=False)
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    assert all(tag not in tokenizer.get_added_vocab() for tag in TAGS)
    checks = {}
    for name, thinking in [('instant', False), ('reasoning', True)]:
        dest = WORK / 'models' / name
        dest.mkdir(parents=True)
        for file in MODEL.iterdir():
            if file.name.startswith('model') or file.name in ('config.json', 'generation_config.json'):
                (dest / file.name).symlink_to(file.resolve())
        tok = AutoTokenizer.from_pretrained(MODEL)
        expected = tok.apply_chat_template(prompts[0], tokenize=False, add_generation_prompt=True, enable_thinking=thinking)
        tok.chat_template = '{% set enable_thinking = ' + str(thinking).lower() + ' %}' + tok.chat_template
        tok.save_pretrained(dest)
        actual = AutoTokenizer.from_pretrained(dest).apply_chat_template(prompts[0], tokenize=False, add_generation_prompt=True)
        assert actual == expected and not any(tag in actual for tag in TAGS)
        checks[name] = dict(enable_thinking=thinking, prompt=actual, matches_native_template=True, tokenizer_length=len(tok))
    write(WORK / 'prompt-check.json', checks)
    write(WORK / 'manifest.json', dict(model='Qwen/Qwen3-0.6B', revision=MODEL.name, started=now(), decoding='ordinary autoregressive, rollout.mode=sync', parallel_tokens_added=False, parallel_instructions=False, temperature=1.0, max_response_tokens=3000, samples={'APO_AIME24': 16, 'APO_AIME25': 16, 'APO_AMC23': 16, 'APO_MATH300': 16, 'APO_MATH500': 1}, answers_per_mode=len(data), source_sha256={str(p): sha(p) for p in [source, math500]}, data_sha256=sha(WORK / 'plain.parquet'), code_sha256=sha(WORK / 'code.tar.gz'), weights_sha256={p.name: sha(p) for p in MODEL.glob('*.safetensors')}))

def evaluate(name, gpus):
    result = WORK / 'results/eval' / name
    result.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(PATH=str(ROOT / '.venv/bin') + ':' + env['PATH'], CUDA_VISIBLE_DEVICES=gpus, NPROC_PER_NODE='4', OMP_NUM_THREADS='1', RAY_TMPDIR='${TMPDIR}/pr1plain_' + name, PARALLEL_R1_OUTPUT_ROOT=str(WORK / 'results'), PARALLEL_R1_SCRATCH_ROOT='${SHM_ROOT}/pr1plain', HF_HOME='${MODEL_ROOT}/huggingface', PARALLEL_R1_EVAL_NAME=name)
    cmd = ['bash', 'training_scripts/eval_qwen3_06b.sh', str(WORK / 'models' / name), 'actor_rollout_ref.rollout.mode=sync', 'actor_rollout_ref.rollout.enforce_eager=true', 'actor_rollout_ref.rollout.val_kwargs.n=1', 'data.val_batch_size=1024', f'data.val_files={WORK / "plain.parquet"}', f'data.train_files={WORK / "plain.parquet"}', 'ray_init.num_cpus=24']
    write(result / 'command.json', cmd)
    update(name, status='running', gpus=gpus, pid=os.getpid())
    with (result / 'driver.log').open('w') as log:
        rc = subprocess.run(cmd, cwd=WORK / 'code/verl', env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    (result / 'exit_code').write_text(str(rc))
    (result / 'finished').write_text(now())
    if rc:
        raise RuntimeError(f'{name} exited {rc}; see {result / "driver.log"}')
    groups = defaultdict(lambda: defaultdict(list))
    with (result / '0.jsonl').open() as f:
        for line in f:
            row = json.loads(line)
            assert row['acc'] in (0, 1)
            groups[row['data_source']][row['input']].append(row)
    expected = {'APO_AIME24': (30,16), 'APO_AIME25': (30,16), 'APO_AMC23': (40,16), 'APO_MATH300': (316,16), 'APO_MATH500': (500,1)}
    assert set(groups) == set(expected)
    summary = {}
    for dataset, (questions, n) in expected.items():
        bucket = groups[dataset]
        assert len(bucket) == questions and all(len(rows) == n for rows in bucket.values())
        rows = [r for samples in bucket.values() for r in samples]
        summary[dataset] = dict(questions=questions, samples_per_question=n, answers=len(rows), correct=sum(int(r['acc']) for r in rows), accuracy=sum(r['acc'] for r in rows)/len(rows), observed_pass_at_n=sum(any(r['acc'] for r in samples) for samples in bucket.values())/questions, invalid_answer=sum(r.get('pred') == '[INVALID]' for r in rows)/len(rows), parallel_tag_responses=sum(any(tag in r['output'] for tag in TAGS) for r in rows))
    write(result / 'summary.json', dict(complete=True, finished=now(), answers=7156, benchmarks=summary, traces_sha256=sha(result / '0.jsonl')))
    update(name, status='complete', answers=7156, summary=str(result / 'summary.json'))

if __name__ == '__main__':
    (WORK / 'started').write_text(now())
    try:
        prepare()
        failed = False
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {name: pool.submit(evaluate, name, gpus) for name, gpus in [('instant', '0,1,2,3'), ('reasoning', '4,5,6,7')]}
            for name, future in futures.items():
                try:
                    future.result()
                except Exception as error:
                    failed = True
                    update(name, status='failed', error=str(error))
                    traceback.print_exc()
        if failed:
            raise RuntimeError('At least one evaluation failed')
        (WORK / 'exit_code').write_text('0')
    except Exception:
        (WORK / 'exit_code').write_text('1')
        raise
    finally:
        (WORK / 'finished').write_text(now())
