"""MATH-500 only; official Qwen sampling, native template, one trial per item."""
import argparse
import fcntl
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = WORK.parent.parent
MODEL = Path('${MODEL_ROOT}/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca')
SOURCE = ROOT / 'exps/branch-diversity-20261006/math500.parquet'
PROFILES = {
    'instant': dict(temperature=0.7, top_p=0.8, top_k=20, min_p=0.0, presence_penalty=1.5),
    'reasoning': dict(temperature=0.6, top_p=0.95, top_k=20, min_p=0.0, presence_penalty=0.0),
}
INSTRUCTION = r'Please reason step by step, and put your final answer within \boxed{}.'


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def sha(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def status(value, **fields):
    write(WORK / 'status.json', dict(status=value, updated=now(), controller_pid=os.getpid(), **fields))
    print(now(), value, fields, flush=True)


def prepare():
    import pandas as pd
    from transformers import AutoTokenizer
    data = pd.read_parquet(SOURCE)
    assert len(data) == 500
    questions = []
    for row in data.itertuples():
        old = row.prompt[0]['content']
        assert '\n\nProblem: ' in old
        problem = old.split('\n\nProblem: ', 1)[1]
        questions.append(dict(id=row.extra_info['unique_id'], problem=problem,
                              answer=str(row.reward_model['ground_truth']),
                              prompt=problem + '\n\n' + INSTRUCTION))
    assert len({r['id'] for r in questions}) == 500
    assert all(not any(tag in r['prompt'] for tag in ('<Parallel>', '<Path>', '<Summary>')) for r in questions)
    (WORK / 'questions.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in questions))
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    checks = {}
    for mode in PROFILES:
        prompts = [tokenizer.apply_chat_template([dict(role='user', content=r['prompt'])], tokenize=False, add_generation_prompt=True, enable_thinking=mode == 'reasoning') for r in questions]
        lengths = [len(tokenizer.encode(p, add_special_tokens=False)) for p in prompts]
        assert max(lengths) + 32768 <= 40960
        checks[mode] = dict(enable_thinking=mode == 'reasoning', example=prompts[0], max_prompt_tokens=max(lengths))
    write(WORK / 'prompt-check.json', checks)
    audit = subprocess.run([sys.executable, str(WORK / 'score.py'), '--check'], check=True, capture_output=True, text=True)
    write(WORK / 'scoring-check.json', json.loads(audit.stdout.splitlines()[-1]))
    original = json.loads((ROOT / 'exps/qwen3-06b-plain-20261006/manifest.json').read_text())
    weight_hash = sha(MODEL / 'model.safetensors')
    assert weight_hash == original['weights_sha256']['model.safetensors']
    write(WORK / 'manifest.json', dict(created=now(), model='Qwen/Qwen3-0.6B', revision=MODEL.name,
          weights_sha256=weight_hash, source_dataset='HuggingFaceH4/MATH-500', questions=500,
          profiles=PROFILES, samples_per_question=1, max_output_tokens=32768, max_model_len=40960,
          prompt_instruction=INSTRUCTION, native_chat_template=True, parallel_r1=False,
          seed=42, dtype='bfloat16', tensor_parallel_size=1, gpus_per_run=1, sequential_modes=True,
          engine=dict(max_num_seqs=32, max_num_batched_tokens=8192, enable_chunked_prefill=True, gpu_memory_utilization=0.85),
          scoring='Math-Verify 0.8.0 symbolic equivalence, reference-blind final answer extraction',
          source_sha256=sha(SOURCE), dataset_sha256=sha(WORK / 'questions.jsonl'),
          code_sha256={p.name: sha(p) for p in (WORK / 'run.py', WORK / 'score.py')},
          versions={p: importlib.metadata.version(p) for p in ('vllm', 'transformers')},
          references=['https://arxiv.org/html/2505.09388v1#S4.SS4', 'https://huggingface.co/Qwen/Qwen3-0.6B#best-practices'],
          note='Reproduces published decoding settings and recommended prompt. The technical report does not specify its complete MATH-500 grading implementation; Math-Verify is explicitly identified here.'))


def free_gpu():
    snapshot = subprocess.check_output(['nvidia-smi', '--query-gpu=index,uuid,memory.used,utilization.gpu', '--format=csv,noheader,nounits'], text=True)
    processes = subprocess.check_output(['nvidia-smi', '--query-compute-apps=gpu_uuid', '--format=csv,noheader,nounits'], text=True)
    occupied = set(processes.splitlines())
    for line in snapshot.splitlines():
        index, uuid, memory, utilization = [x.strip() for x in line.split(',')]
        if uuid not in occupied and int(memory) < 1024 and int(utilization) == 0:
            return index
    return None


def worker(mode):
    from transformers import AutoTokenizer
    from vllm import LLM, SamplingParams
    directory = WORK / mode
    directory.mkdir(exist_ok=True)
    data = [json.loads(line) for line in (WORK / 'questions.jsonl').read_text().splitlines()]
    trace = directory / 'traces.jsonl'
    done = {json.loads(line)['id'] for line in trace.read_text().splitlines()} if trace.exists() else set()
    data = [r for r in data if r['id'] not in done]
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    sampling = SamplingParams(n=1, max_tokens=32768, seed=42, skip_special_tokens=False, **PROFILES[mode])
    write(directory / 'sampling.json', dict(repr=repr(sampling), **PROFILES[mode], n=1, seed=42, max_tokens=32768, skip_special_tokens=False))
    if not data:
        return
    model = LLM(model=str(MODEL), tokenizer=str(MODEL), dtype='bfloat16', tensor_parallel_size=1,
                max_model_len=40960, max_num_seqs=32, max_num_batched_tokens=8192,
                enable_chunked_prefill=True, gpu_memory_utilization=0.85, seed=42,
                generation_config='vllm')
    with trace.open('a') as stream:
        for start in range(0, len(data), 32):
            batch = data[start:start+32]
            prompts = [tokenizer.apply_chat_template([dict(role='user', content=r['prompt'])], tokenize=False, add_generation_prompt=True, enable_thinking=mode == 'reasoning') for r in batch]
            outputs = model.generate(prompts, sampling, use_tqdm=False)
            assert len(outputs) == len(batch)
            for row, result in zip(batch, outputs):
                assert len(result.outputs) == 1
                output = result.outputs[0]
                stream.write(json.dumps(dict(id=row['id'], output=output.text, output_tokens=len(output.token_ids),
                    prompt_tokens=len(result.prompt_token_ids), finish_reason=output.finish_reason, stop_reason=output.stop_reason)) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
            write(directory / 'progress.json', dict(updated=now(), answers=len(done)+min(start+32,len(data)), expected=500))
            print(now(), mode, 'answers', len(done)+min(start+32,len(data)), flush=True)


def controller():
    status('preparing')
    prepare()
    for mode in PROFILES:
        summary = WORK / mode / 'summary.json'
        if summary.exists() and json.loads(summary.read_text())['complete']:
            continue
        status('waiting_for_free_gpu', next_mode=mode, queued_modes=list(PROFILES), condition='No compute process, <1 GiB memory and zero utilization; three consecutive checks')
        stable_gpu, stable_count = None, 0
        while True:
            gpu = free_gpu()
            stable_count = stable_count+1 if gpu is not None and gpu == stable_gpu else int(gpu is not None)
            stable_gpu = gpu
            if stable_count >= 3:
                break
            time.sleep(20)
        directory = WORK / mode
        directory.mkdir(exist_ok=True)
        env = os.environ.copy()
        env.update(CUDA_VISIBLE_DEVICES=gpu, OMP_NUM_THREADS='4', TOKENIZERS_PARALLELISM='false')
        with (directory / 'driver.log').open('a') as log:
            child = subprocess.Popen([sys.executable, '-u', str(WORK / 'run.py'), '--worker', mode], env=env, stdout=log, stderr=subprocess.STDOUT)
            status('running', mode=mode, gpu=gpu, worker_pid=child.pid)
            rc = child.wait()
        (directory / 'exit_code').write_text(str(rc))
        if rc:
            raise RuntimeError(f'{mode} inference exited {rc}; inspect driver.log')
        status('scoring', mode=mode)
        with (directory / 'scoring.log').open('w') as log:
            subprocess.run([sys.executable, str(WORK / 'score.py'), '--mode', mode], stdout=log, stderr=subprocess.STDOUT, check=True)
    write(WORK / 'summary.json', dict(complete=True, finished=now(), profiles={m: json.loads((WORK / m / 'summary.json').read_text()) for m in PROFILES}))
    status('complete', summary=str(WORK / 'summary.json'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--worker', choices=list(PROFILES))
    args = parser.parse_args()
    if args.worker:
        worker(args.worker)
    elif args.prepare_only:
        prepare()
    else:
        with (WORK / 'controller.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            try:
                controller()
                (WORK / 'exit_code').write_text('0')
            except Exception as error:
                status('failed', error=f'{type(error).__name__}: {error}')
                (WORK / 'exit_code').write_text('1')
                traceback.print_exc()
                raise
