"""Two sequential pairs: original sampling, then Qwen report sampling."""
import argparse
import hashlib
import json
import os
import subprocess
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import pandas as pd

from rescore import PREVIOUS, ROOT, WORK, check_extractor, rescore

state = {}
lock = threading.Lock()
PROFILES = {
    'baseline-instant': dict(mode='instant', temperature=1.0, top_p=1.0, top_k=-1, presence_penalty=0.0),
    'baseline-reasoning': dict(mode='reasoning', temperature=1.0, top_p=1.0, top_k=-1, presence_penalty=0.0),
    'author-instant': dict(mode='instant', temperature=0.7, top_p=0.8, top_k=20, presence_penalty=1.5),
    'author-reasoning': dict(mode='reasoning', temperature=0.6, top_p=0.95, top_k=20, presence_penalty=0.0),
}

def now():
    return datetime.now(timezone.utc).isoformat()

def write(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)

def update(name, **fields):
    with lock:
        state[name] = dict(updated=now(), **fields)
        write(WORK / 'status.json', state)
        print(now(), name, fields, flush=True)

def prepare(include_math316):
    data = pd.read_parquet(PREVIOUS / 'plain.parquet')
    keep = data[data.data_source.isin(['APO_AIME24', 'APO_AIME25', 'APO_AMC23'])]
    math500 = data[data.data_source == 'APO_MATH500']
    assert len(math500) == 500
    frames = [keep, math500.loc[math500.index.repeat(16)]]
    if include_math316:
        frames.append(data[data.data_source == 'APO_MATH300'])
    data = pd.concat(frames, ignore_index=True)
    expected = 14656 if include_math316 else 9600
    assert len(data) == expected
    assert all(not any(tag in r[0]['content'] for tag in ['<Parallel>', '<Path>', '<Summary>']) for r in data['prompt'])
    data.to_parquet(WORK / 'plain.parquet', index=False)
    code = WORK / 'code/verl/verl/workers/rollout/vllm_rollout/vllm_rollout_spmd.py'
    text = code.read_text()
    anchor = '            outputs = self.inference_engine.generate('
    assert text.count(anchor) == 1
    text = text.replace(anchor, '            print("R1_EVAL_SAMPLING", self.sampling_params, flush=True)\n' + anchor)
    code.write_text(text)
    trainer = WORK / 'code/verl/verl/trainer/ppo/ray_trainer.py'
    text = trainer.read_text()
    anchor = '            sample_outputs.extend(output_texts)'
    assert text.count(anchor) == 1
    text = text.replace(anchor, anchor + '\n            print(f"R1_EVAL_PROGRESS answers={len(sample_outputs)}", flush=True)')
    trainer.write_text(text)
    old = json.loads((PREVIOUS / 'manifest.json').read_text())
    manifest = dict(started=now(), model=old['model'], revision=old['revision'], weights_sha256=old['weights_sha256'], max_response_tokens=32768, samples_per_question=16, primary_math='MATH-500', includes_math316=include_math316, answers_per_run=expected, total_answers=4*expected, data_sha256=hashlib.sha256((WORK/'plain.parquet').read_bytes()).hexdigest(), profiles=PROFILES, decoder='ordinary autoregressive sync, TP=1', gpus_per_run=4, val_batch_size=128, max_num_batched_tokens=34816, code_origin_sha256=old['code_sha256'], logging_patch_sha256={str(p.relative_to(WORK)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [code,trainer]}, scorer_sha256=hashlib.sha256((WORK/'rescore.py').read_bytes()).hexdigest(), author_reference='https://arxiv.org/html/2505.09388v1#S4.SS6', note='Authors use 38912 tokens and 64 samples for AIME. Here all four runs use the requested 32768 tokens and 16 samples. Prompts and non-symbolic verifier differ from the public protocol; only author sampling parameters are reproduced. Original and corrected extraction metrics are both retained.')
    write(WORK / 'manifest.json', manifest)
    for name in PROFILES:
        update(name, status='queued')

def evaluate(name, gpus):
    p = PROFILES[name]
    result = WORK / 'results/eval' / name
    result.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(PATH=str(ROOT/'.venv/bin')+':'+env['PATH'], CUDA_VISIBLE_DEVICES=gpus, NPROC_PER_NODE='4', OMP_NUM_THREADS='1', RAY_TMPDIR='${TMPDIR}/pr1suite_'+name, PARALLEL_R1_OUTPUT_ROOT=str(WORK/'results'), PARALLEL_R1_SCRATCH_ROOT='${SHM_ROOT}/pr1suite', HF_HOME='${MODEL_ROOT}/huggingface', PARALLEL_R1_EVAL_NAME=name)
    command = ['bash','training_scripts/eval_qwen3_06b.sh',str(PREVIOUS/'models'/p['mode']), 'actor_rollout_ref.rollout.mode=sync', 'actor_rollout_ref.rollout.enforce_eager=true', 'actor_rollout_ref.rollout.val_kwargs.n=1', 'data.max_response_length=32768', 'data.val_batch_size=128', 'actor_rollout_ref.rollout.max_num_batched_tokens=34816', 'actor_rollout_ref.rollout.gpu_memory_utilization=0.8', f'data.val_files={WORK/"plain.parquet"}', f'data.train_files={WORK/"plain.parquet"}', 'ray_init.num_cpus=24', f'actor_rollout_ref.rollout.val_kwargs.temperature={p["temperature"]}', f'actor_rollout_ref.rollout.val_kwargs.top_p={p["top_p"]}', f'actor_rollout_ref.rollout.val_kwargs.top_k={p["top_k"]}', f'+actor_rollout_ref.rollout.presence_penalty={p["presence_penalty"]}']
    write(result/'command.json',command)
    (result/'started').write_text(now())
    update(name,status='running',gpus=gpus)
    with (result/'driver.log').open('w') as log:
        rc=subprocess.run(command,cwd=WORK/'code/verl',env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (result/'exit_code').write_text(str(rc))
    if rc:
        raise RuntimeError(f'{name}: inference exited {rc}')
    report=rescore(name,result,p['mode'])
    write(result/'summary.json',report)
    (result/'finished').write_text(now())
    update(name,status='complete',answers=report['answers'])

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--include-math316',action='store_true')
    args=parser.parse_args()
    (WORK/'started').write_text(now())
    try:
        check_extractor()
        prepare(args.include_math316)
        failed=[]
        for phase in ['baseline','author']:
            with ThreadPoolExecutor(max_workers=2) as pool:
                pending={f'{phase}-{mode}':pool.submit(evaluate,f'{phase}-{mode}',gpus) for mode,gpus in [('instant','0,1,2,3'),('reasoning','4,5,6,7')]}
                for name,future in pending.items():
                    try:
                        future.result()
                    except Exception as error:
                        failed.append(name)
                        update(name,status='failed',error=str(error))
                        traceback.print_exc()
            if failed:
                raise RuntimeError(f'Not starting the next phase after failures: {failed}')
        (WORK/'exit_code').write_text('0')
    except Exception:
        (WORK/'exit_code').write_text('1')
        raise
    finally:
        (WORK/'finished').write_text(now())
