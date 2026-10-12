import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone
import traceback

RUN = Path(__file__).resolve().parent
ROOT = Path('${PROJECT_ROOT}')
manifest = json.loads((RUN / 'manifest.json').read_text())

def status(state, **extra):
    data = dict(state=state, observed_utc=datetime.now(timezone.utc).isoformat(), **extra)
    (RUN / 'status.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data), flush=True)

try:
    assert hashlib.sha256((RUN / 'code.tar.gz').read_bytes()).hexdigest() == manifest['archive_sha256']
    code = RUN / 'code'
    for name, digest in manifest['data_sha256'].items():
        assert hashlib.sha256((code / name).read_bytes()).hexdigest() == digest
    from transformers import AutoTokenizer, AutoConfig
    from safetensors import safe_open
    model = Path(manifest['checkpoint'])
    config = AutoConfig.from_pretrained(model, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(model, local_files_only=True)
    tags = ['<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>']
    ids = [tokenizer.encode(t, add_special_tokens=False) for t in tags]
    assert all(len(x) == 1 for x in ids) and len({x[0] for x in ids}) == 6
    assert config.model_type == 'qwen3' and config.hidden_size == 1024
    assert max(x[0] for x in ids) < config.vocab_size
    with safe_open(model / 'model.safetensors', framework='pt', device='cpu') as f:
        assert f.get_slice('model.embed_tokens.weight').get_shape() == [config.vocab_size, config.hidden_size]
    (RUN / 'model-sha256.txt').write_text(hashlib.sha256((model / 'model.safetensors').read_bytes()).hexdigest() + '\n')
    env = os.environ.copy()
    env.update(PATH=str(ROOT / '.venv/bin') + ':' + env['PATH'], CUDA_VISIBLE_DEVICES=','.join(map(str, manifest['gpus'])),
               NPROC_PER_NODE=str(len(manifest['gpus'])), PARALLEL_R1_RL_NAME=manifest['run'], PARALLEL_R1_RL_DIR=str(RUN / 'results'),
               PARALLEL_R1_SCRATCH_ROOT='${MODEL_ROOT}', HF_HOME='${MODEL_ROOT}/huggingface',
               RAY_TMPDIR='${TMPDIR}/r1s1_20261006_flashinfer8gpu', WANDB_MODE='offline', PYTHONUNBUFFERED='1')
    env.update(manifest['extra_env'])
    env.pop('RAY_ADDRESS', None)
    cmd = ['bash', str(code / 'scripts/qwen3.sh'), 'rl', 's1', str(model), *manifest['overrides']]
    (RUN / 'command.json').write_text(json.dumps(cmd, indent=2) + '\n')
    with (RUN / 'resolved-config.yaml').open('w') as log:
        subprocess.run([*cmd, '--cfg', 'job', '--resolve'], cwd=code, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
    status('starting', commit=manifest['commit'], checkpoint=str(model), gpus=manifest['gpus'], steps=300)
    with (RUN / 'driver.log').open('w') as log:
        process = subprocess.Popen(cmd, cwd=code, env=env, stdout=log, stderr=subprocess.STDOUT)
        status('running', pid=process.pid, gpus=manifest['gpus'], steps=300)
        (RUN / 'started').write_text(datetime.now(timezone.utc).isoformat() + '\n')
        result = process.wait()
    (RUN / 'exit_code').write_text(str(result) + '\n')
    status('complete' if result == 0 else 'failed', exit_code=result)
except Exception as exc:
    status('failed', error=repr(exc))
    traceback.print_exc()
    raise
