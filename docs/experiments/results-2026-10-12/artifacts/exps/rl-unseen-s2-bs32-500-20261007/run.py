"""Task-local controller; all persistent and temporary output stays under r1."""
import hashlib
import json
import os
import sys
from pathlib import Path
import subprocess
import traceback
from datetime import datetime, timezone

RUN = Path(__file__).resolve().parent
ROOT = Path('${PROJECT_ROOT}')
manifest = json.loads((RUN / 'manifest.json').read_text())


def status(state, **extra):
    record = dict(state=state, observed_utc=datetime.now(timezone.utc).isoformat(), **extra)
    (RUN / 'status.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record), flush=True)


try:
    assert RUN.resolve().is_relative_to(ROOT.resolve())
    code = RUN / 'code'
    for name, digest in {**manifest['changed_file_sha256'], **manifest['data_sha256']}.items():
        assert hashlib.sha256((code / name).read_bytes()).hexdigest() == digest, name
    model = Path(manifest['checkpoint'])
    assert model.resolve().is_relative_to(ROOT.resolve()) and (model / 'model.safetensors').is_file()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(model, local_files_only=True)
    ids = [tokenizer.encode(t, add_special_tokens=False) for t in
           ('<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>')]
    assert all(len(x) == 1 for x in ids) and len({x[0] for x in ids}) == 6
    env = os.environ.copy()
    env.update(PATH=str(ROOT / '.venv/bin') + ':' + env['PATH'], CUDA_VISIBLE_DEVICES='0,1,2,3,4,5,6,7',
               NPROC_PER_NODE='8', PARALLEL_R1_RL_NAME=manifest['run'], PARALLEL_R1_RL_DIR=str(RUN / 'results'),
               PARALLEL_R1_SCRATCH_ROOT=str(ROOT / 'cache'), HF_HOME=str(ROOT / 'cache/huggingface'),
               TMPDIR=str(ROOT / 't'), RAY_TMPDIR=str(ROOT), XDG_CACHE_HOME=str(ROOT / 'cache'),
               VLLM_CACHE_ROOT=str(ROOT / 'cache/vllm-aligned'), TRITON_CACHE_DIR=str(ROOT / 'cache/triton'),
               TORCHINDUCTOR_CACHE_DIR=str(ROOT / 'cache/inductor-aligned'),
               TORCH_EXTENSIONS_DIR=str(ROOT / 'cache/torch-extensions'), CUDA_CACHE_PATH=str(ROOT / 'cache/cuda'),
               WANDB_MODE='offline', PYTHONUNBUFFERED='1', TOKENIZERS_PARALLELISM='false')
    env.update(manifest['extra_env'])
    env.pop('RAY_ADDRESS', None)
    cmd = ['bash', str(code / 'scripts/qwen3.sh'), 'rl', manifest['stage'], str(model), *manifest['overrides']]
    (RUN / 'command.json').write_text(json.dumps(cmd, indent=2) + '\n')
    with (RUN / 'resolved-config.yaml').open('w') as log:
        subprocess.run([*cmd, '--cfg', 'job', '--resolve'], cwd=code, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
    if '--preflight' in sys.argv:
        print('Preflight passed: files, tokenizer, resolved config', flush=True)
        sys.exit(0)
    gpu_apps = subprocess.check_output(['nvidia-smi', '--query-compute-apps=pid', '--format=csv,noheader'], text=True).strip()
    assert not gpu_apps, 'GPU processes exist; inspect ownership before allocating GPUs'
    status('starting', commit=manifest['commit'], checkpoint=str(model), steps=manifest.get("steps"), resume_checkpoint=manifest.get('resume_checkpoint'), gpus=list(range(8)))
    with (RUN / 'driver.log').open('w') as log:
        process = subprocess.Popen(cmd, cwd=code, env=env, stdout=log, stderr=subprocess.STDOUT)
        status('running', pid=process.pid, controller_pid=os.getpid(), steps=manifest.get("steps"), resume_checkpoint=manifest.get('resume_checkpoint'), gpus=list(range(8)))
        result = process.wait()
    (RUN / 'exit_code').write_text(str(result) + '\n')
    status('complete' if result == 0 else 'failed', exit_code=result)
except Exception as exc:
    status('failed', error=repr(exc))
    traceback.print_exc()
    raise
