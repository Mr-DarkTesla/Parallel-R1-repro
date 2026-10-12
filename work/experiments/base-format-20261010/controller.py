"""Dedicated Sirius Base SFT pipeline; no mutation of Instruct or Cloud workers."""
import datetime
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

B = Path(__file__).resolve().parent
P = B.parents[2]
C = P / 'work/experiments/format-loss-20261010'

def read(p):
    return json.loads(p.read_text())

def sha(p):
    digest = hashlib.sha256()
    with p.open('rb') as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def save(p, obj):
    t = p.with_suffix('.tmp')
    t.write_text(json.dumps(obj, indent=2) + '\n')
    t.replace(p)

def smoke_check():
    out = B / 'runs/smoke'
    result = read(out / 'result.json')
    init = read(out / 'initialization-proof.json')
    metrics = [json.loads(line) for line in (out / 'metrics.jsonl').open()]
    assert result['state'] == 'complete' and result['steps'] == 2 and result['full_model']
    assert math.isfinite(result['val_loss'])
    assert init['all_parameters_trainable'] and init['trainable_parameters'] == init['total_parameters'] > 3e9
    assert len(metrics) == 2 and [m['step'] for m in metrics] == [1, 2]
    assert all(m['transformer_update_l2'] > 0 and all(math.isfinite(m[k]) for k in ['loss', 'grad_norm', 'transformer_update_l2']) for m in metrics)
    assert (out / 'final/config.json').exists()
    return {str(p): sha(p) for p in [out / 'result.json', out / 'initialization-proof.json', out / 'metrics.jsonl']}

def main():
    lock = (B / 'controller.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert not (B / 'controller-started.json').exists()
    ready = read(B / 'launch-ready.json')
    assert ready['passed'] and read(B / 'independent-source-review.json')['passed']
    def validate():
        for file, digest in ready['sha256'].items():
            assert sha(P / file) == digest, ('Source drift', file)
    validate()
    (B / 'runs').mkdir(exist_ok=False)
    logs = B / 'logs'
    logs.mkdir(exist_ok=False)
    status = dict(pid=os.getpid(), state='waiting_for_sirius', full_model=True, think_wrapped=False,
                  epochs=3, steps=126, lr=1e-5, eval_questions=128, host='sirius', gpus=8)
    def update(**kw):
        status.update(at=datetime.datetime.now(datetime.timezone.utc).isoformat(), **kw)
        save(B / 'status.json', status)
    save(B / 'controller-started.json', status)
    def run(label, argv):
        validate()
        env = os.environ.copy()
        env.update(PARALLEL_R1_PYTHON=sys.executable, PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1')
        with (logs / (label + '.log')).open('x') as log:
            proc = subprocess.Popen(argv, cwd=P, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            update(state='running', active=label, active_pid=proc.pid)
            code = proc.wait()
        update(active_pid=None)
        assert code == 0, (label, code)
        validate()
    try:
        while True:
            prior = read(C / 'sft-status.json')
            assert prior['state'] != 'failed', prior
            if prior['state'] == 'complete' and not subprocess.check_output(['nvidia-smi', '--query-compute-apps=pid', '--format=csv,noheader'], text=True).strip():
                break
            update(prior_active=prior.get('active'))
            time.sleep(10)
        run('smoke', ['bash', str(B / 'run_train.sh'), 'smoke'])
        artifacts = smoke_check()
        update(state='awaiting_smoke_review', active=None, smoke_artifacts_sha256=artifacts)
        approval_file = B / 'root-smoke-approved.json'
        while not approval_file.exists():
            assert smoke_check() == artifacts
            validate()
            time.sleep(5)
        approval = read(approval_file)
        assert approval['passed'] and approval['artifacts_sha256'] == artifacts
        review = B / 'independent-smoke-review.json'
        assert read(review)['passed'] and sha(review) == approval['independent_review_sha256']
        run('production', ['bash', str(B / 'run_train.sh'), 'production'])
        result = read(B / 'runs/production/result.json')
        assert result['state'] == 'complete' and result['steps'] == 126 and result['full_model']
        run('base-unconstrained-128', ['bash', str(B / 'evaluations/run_eval.sh'), '--model', str(B / 'runs/production/final'),
             '--mode', 'structured', '--name', 'base-no-think-unconstrained-128', '--suite', '128', '--system-file', str(B / 'system.txt')])
        out = B / 'evaluations/base-no-think-unconstrained-128'
        summary = read(out / 'summary.json')
        assert summary['planned'] == summary['completed'] == 128 and not summary['think_wrapped']
        assert read(out / 'worker-exits.json') == [0] * 8
        update(state='complete', active=None, training=result, summary_path=str(out / 'summary.json'))
    except BaseException as exc:
        update(state='failed', error=repr(exc))
        raise

if __name__ == '__main__':
    main()
