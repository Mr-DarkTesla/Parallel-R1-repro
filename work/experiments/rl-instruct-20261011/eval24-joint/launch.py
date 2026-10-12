import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

R = Path.cwd()
B = R / 'work/experiments/rl-instruct-20261011/eval24-joint'
lane = sys.argv[1]
L = B / lane

def read(p):
    return json.loads(Path(p).read_text())

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def write(p, value):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    t = p.with_suffix('.tmp')
    t.write_text(json.dumps(value, indent=2) + '\n')
    t.replace(p)

assert sha(L / 'plan.json') == sys.argv[2]
plan = read(L / 'plan.json')
assert os.uname().nodename == plan['hostname']
assert all(sha(k) == v for k, v in plan['sources'].items())
assert sha(__file__) == plan['launcher_sha256']
fd = os.open(L / 'controller.lock', os.O_CREAT | os.O_EXCL | os.O_WRONLY)
os.write(fd, str(os.getpid()).encode())
os.close(fd)

def status(state, **kw):
    write(L / 'status.json', dict(state=state, pid=os.getpid(), at=time.time(), **kw))

try:
    while True:
        blocker = Path(plan['after_result'])
        if blocker.exists():
            x = read(blocker)
            assert x['passed'] and x['completed'] == 500 and x['missing'] == 0
            assert x.get('exit_codes', [0] * 8) == [0] * 8
            break
        status('waiting_current_evaluation')
        time.sleep(10)
    while subprocess.check_output(['nvidia-smi', '--query-compute-apps=pid', '--format=csv,noheader'], text=True).strip():
        status('waiting_empty8')
        time.sleep(10)
    assert len(subprocess.check_output(['nvidia-smi', '--query-gpu=uuid', '--format=csv,noheader'], text=True).splitlines()) == 8
    proof = Path(plan['width8_proof'])
    assert sha(proof) == plan['width8_proof_sha256'] and read(proof)['passed']
    model = Path(plan['model']).resolve()
    assert model.is_relative_to(R.resolve())
    complete = Path(plan['complete']).resolve()
    assert complete.parent / 'hf' == model
    assert read(complete) == dict(step=32, world_size=8, model=True, optimizer=True, rng=True)
    for p in model.iterdir():
        if p.is_file():
            assert p.resolve().is_relative_to(model)
    manifest = {str(p): sha(p) for p in model.iterdir() if p.is_file()}
    baseline_index = read(Path(plan['baseline']) / 'model.safetensors.index.json')
    assert set(read(model / 'model.safetensors.index.json')['weight_map']) == set(baseline_index['weight_map'])
    questions = [json.loads(l) for l in Path(plan['questions']).read_text().splitlines()]
    assert len(questions) == 500 and len({q['id'] for q in questions}) == 500
    release = L / 'release.json'
    output = L / 'traces'
    write(release, dict(model=str(model), questions=plan['questions'], system=plan['system'], scorer=plan['scorer'], output=str(output), protocol=plan['protocol'], model_manifest=manifest, selection_allowed=False))
    children = []
    handles = []
    for local in range(8):
        rank = plan['rank_offset'] + local
        env = os.environ.copy()
        env.update(CUDA_VISIBLE_DEVICES=str(local), HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', OMP_NUM_THREADS='1', TOKENIZERS_PARALLELISM='false', NVIDIA_TF32_OVERRIDE='0')
        h = (L / f'rank-{rank}.log').open('a')
        handles.append(h)
        children.append(subprocess.Popen([sys.executable, str(B / 'worker.py'), '--job', str(release), '--rank', str(rank), '--shards', '24'], cwd=R, env=env, stdin=subprocess.DEVNULL, stdout=h, stderr=subprocess.STDOUT))
    while any(c.poll() is None for c in children):
        status('evaluating', worker_pids=[c.pid for c in children])
        time.sleep(10)
    codes = [c.wait() for c in children]
    for h in handles:
        h.close()
    assert codes == [0] * 8, codes
    rows = [json.loads(l) for f in output.glob('rank-*.jsonl') for l in f.read_text().splitlines()]
    expected = {i for i in range(500) if plan['rank_offset'] <= i % 24 < plan['rank_offset'] + 8}
    assert len(rows) == len(expected) and {r['index'] for r in rows} == expected
    assert all(r['id'] == questions[r['index']]['id'] and not r['grade'].get('error') for r in rows)
    assert all(r['instrumented_forward_calls'] == r['stats']['actual_model_forward_calls'] for r in rows)
    assert all(x['microbatch_max_paths'] == 8 and x['sequential_subgroup_count'] == 1 for r in rows for x in r['fork_batch_ledger'])
    assert all(sha(k) == v for k, v in manifest.items())
    write(L / 'result.json', dict(passed=True, lane=lane, completed=len(rows), expected_indices=sorted(expected), exit_codes=codes, model_manifest=manifest, protocol=plan['protocol'], traces={str(f): sha(f) for f in output.glob('rank-*.jsonl')}, source_manifest=plan['sources'], selection_allowed=False))
    status('completed', completed=len(rows))
except Exception as e:
    status('failed', error=repr(e))
    raise
