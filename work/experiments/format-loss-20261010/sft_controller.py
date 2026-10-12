"""Owned Sirius eight-GPU format SFT: smoke, reviewed production, byte audit, guarded128."""
import datetime
import fcntl
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

C = Path(__file__).resolve().parent
P = C.parents[2]
D = P / 'work/experiments/instruct-token-warmup-20261010'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(path, obj):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2) + '\n')
    tmp.replace(path)


def smoke_artifacts():
    out = C / 'runs/smoke'
    result = read(out / 'result.json')
    init = read(out / 'initialization-proof.json')
    rows = [json.loads(l) for l in (out / 'metrics.jsonl').open()]
    baseline = read(D / 'runs/smoke/initialization-proof.json')
    assert result['state'] == 'complete' and result['steps'] == 2 and result['only_six_rows_updated']
    assert init['trainable_parameters'] == 15360 and init['ddp_frozen_bytes_equal']
    assert init['all_base_parameters_frozen'] and init['native_embeddings_and_lm_head_tied']
    for key in ['initial_rows_sha256', 'tag_ids', 'frozen_bytehash_before_DDP', 'frozen_bytehash_after_DDP']:
        assert init[key] == baseline[key]
    assert init['rank0_gpu_isolation']['width'] == 3 and init['rank0_gpu_isolation']['third_sibling_max_logit_difference'] == 0
    assert len(rows) == 2 and [r['step'] for r in rows] == [1, 2]
    assert [r['loss_phase'] for r in rows] == ['format_only', 'format_x5']
    assert all(r['row_update_l2'] > 0 and r['frozen_parameter_versions_unchanged'] and
               all(math.isfinite(r[k]) for k in ['loss', 'row_grad_norm', 'row_update_l2']) for r in rows)
    return {str(p): sha(p) for p in [out / 'result.json', out / 'initialization-proof.json', out / 'metrics.jsonl']}


def main():
    lock = (C / 'sft-controller.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert not (C / 'sft-controller-started.json').exists(), 'No duplicate/restart/overwrite'
    assert not (C / 'runs').exists()
    assert not (C / 'evaluations/weighted-format-constrained-128').exists()
    ready = C / 'sft-launch-ready.json'
    config = read(ready)
    assert config['passed'] and config['trainable_parameters'] == 15360
    def validate():
        for path, digest in config['sha256'].items():
            assert sha(P / path) == digest, ('Source/artifact drift', path)
    validate()
    assert not subprocess.check_output(['nvidia-smi', '--query-compute-apps=pid', '--format=csv,noheader'], text=True).strip(), 'GPU occupied'
    assert read(C / 'independent-source-mask-review.json')['passed']
    (C / 'runs').mkdir(exist_ok=False)
    logs = C / 'sft-pipeline-logs'
    logs.mkdir(exist_ok=False)
    status = dict(state='starting', at=now(), pid=os.getpid(), only_six_rows=True,
                  epochs=3, target_steps=129, base_lr=.0005, constrained_eval_planned=128)
    save(C / 'sft-controller-started.json', {**status, 'ready_sha256': sha(ready), 'source_sha256': sha(Path(__file__))})
    def update(**kwargs):
        status.update(at=now(), **kwargs)
        save(C / 'sft-status.json', status)
    def run(label, argv):
        validate()
        update(state='running', active=label, argv=argv)
        env = os.environ.copy()
        env.update(PARALLEL_R1_PYTHON=sys.executable, PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1')
        with (logs / (label + '.log')).open('x') as log:
            child = subprocess.Popen(argv, cwd=P, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            update(active_pid=child.pid)
            rc = child.wait()
        update(active_pid=None)
        assert rc == 0, (label, rc)
        validate()
    try:
        run('smoke', ['bash', str(C / 'run_train.sh'), 'smoke'])
        artifacts = smoke_artifacts()
        update(state='awaiting_root_smoke_review', active=None, approval_request=dict(artifacts_sha256=artifacts, ready_sha256=sha(ready)))
        approval_file = C / 'root-sft-smoke-approved.json'
        while not approval_file.exists():
            validate()
            assert smoke_artifacts() == artifacts
            time.sleep(5)
        approval = read(approval_file)
        assert approval['passed'] and approval['ready_sha256'] == sha(ready)
        assert approval['artifacts_sha256'] == artifacts
        independent = Path(approval['independent_review_path']).resolve()
        assert independent.is_relative_to(C) and sha(independent) == approval['independent_review_sha256']
        assert read(independent)['passed']
        run('production', ['bash', str(C / 'run_train.sh'), 'production'])
        result = read(C / 'runs/production/result.json')
        assert result['state'] == 'complete' and result['steps'] == 129 and result['epochs'] == 3 and result['only_six_rows_updated']
        run('export-audit', [sys.executable, '-B', str(C / 'audit_export.py')])
        audit = read(C / 'export-byte-proof.json')
        assert audit['passed'] and audit['only_six_rows_changed'] and len(audit['all_other_tensors_bitwise_identical']) == 398
        assert all(audit['all_other_tensors_bitwise_identical'].values())
        run('constrained-128', ['bash', str(C / 'evaluations/run_eval.sh'), '--model', str(C / 'runs/production/final'),
                              '--mode', 'structured', '--name', 'weighted-format-constrained-128',
                              '--suite', '128', '--system-file', str(D / 'system.txt')])
        folder = C / 'evaluations/weighted-format-constrained-128'
        summary = read(folder / 'summary.json')
        assert summary['planned'] == summary['completed'] == 128 and summary['constrained_decoding']
        assert read(folder / 'worker-exits.json') == [0] * 8
        update(state='complete', active=None, finished_at=now(), training=result,
               evaluation_summary=str(folder / 'summary.json'))
    except BaseException as error:
        update(state='failed', error=repr(error))
        raise


if __name__ == '__main__':
    main()
