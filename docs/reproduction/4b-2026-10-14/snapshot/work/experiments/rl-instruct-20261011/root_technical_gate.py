"""Autonomously approve the reviewed technical run after matched eval exits."""
from pathlib import Path
import fcntl
import hashlib
import json
import os
import time

P = Path.cwd()
B = P / 'work/experiments/rl-instruct-20261011'
S = P / 'work/experiments/instruct-full-20261011'
lock = (B / 'root-technical-gate.lock').open('w')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)

status_path = B / 'root-technical-gate-status.json'
status = dict(state='waiting_for_matched_eval', pid=os.getpid(), started_at=time.time())
save(status_path, status)
try:
    result_path = P / 'work/experiments/night-20261010/cloud-continued/tmp2/results/304-instruct-full-matched-guard128.json'
    while not result_path.exists():
        status['updated_at'] = time.time()
        save(status_path, status)
        time.sleep(5)
    result = json.loads(result_path.read_text())
    assert result['returncode'] == 0, result
    seal_path = B / 'technical-config-seal.json'
    assert sha(seal_path) == 'b2f2080ea6b461567d9b7897fb6da1140594d5f12b966d70c453ae6061779f0d'
    review_path = S / 'independent-rl-technical-source-review.json'
    assert sha(review_path) == 'ea37cf31bace7ffc3164d178a380bdee12336d149a9a733f6afad46979670939'
    review = json.loads(review_path.read_text())
    assert review['passed'] and review['seal_sha256'] == sha(seal_path)
    seal = json.loads(seal_path.read_text())
    for name, expected in seal['sha256'].items():
        assert sha(P / name) == expected, name
    for directory in ['epoch1-guard-structured-128', 'warmup-lr1e3-guard-structured-128']:
        folder = S / 'evaluations' / directory
        summary = json.loads((folder / 'summary.json').read_text())
        assert summary['completed'] == 128 and summary['missing'] == 0
        assert json.loads((folder / 'worker-exits.json').read_text()) == [0] * 8
    configs = {name: sha(B / 'technical-configs' / (name + '.json'))
               for name in ['step1', 'resume-step2']}
    receipt = dict(approved=True, lane='tmp2', approved_at=time.time(),
                   scope='Actual eight-GPU engineering step1 and resumed step2 only',
                   technical_config_seal_sha256=sha(seal_path), config_sha256=configs,
                   predecessor_result_sha256=sha(result_path),
                   independent_source_review_sha256=sha(review_path))
    destination = B / 'technical-root-approved.json'
    assert not destination.exists(), 'Existing root receipt must not be replaced'
    save(destination, receipt)
    status.update(state='released', finished_at=time.time(), receipt_sha256=sha(destination))
except BaseException as error:
    status.update(state='failed', error=repr(error), finished_at=time.time())
    raise
finally:
    save(status_path, status)
