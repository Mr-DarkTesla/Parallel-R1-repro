"""Run one isolated constrained128 test after the existing tmp3 pipeline exits.

No resource provisioning or model edits. Source pins and ownership fail closed.
"""
import datetime
import hashlib
import json
import os
import subprocess
from pathlib import Path

C = Path(__file__).resolve().parent
P = C.parents[2]
D = P / 'work/experiments/instruct-token-warmup-20261010'
N = P / 'work/experiments/night-20261010'
E = C / 'evaluations'
NAME = 'baseline-lr-5e-4-constrained-128'


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, value):
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(p)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    status = C / 'guard128-status.json'
    try:
        assert os.uname().nodename == 'lm-mpi-job-984c4577-4afe-42f9-a508-75b70956552e-mpimaster-0'
        prior = read(N / 'cloud-continued/tmp3/results/100-fourb-token-warmup-lr-2e-4.json')
        assert prior['returncode'] == 0, 'Previous evaluation pipeline failed: manual recovery required'
        assert read(D / 'variants/lr-2e-4/pipeline-status.json')['state'] == 'completed'
        proof = read(C / 'guard128-launch-ready.json')
        assert proof['passed'] and proof['constrained_decoding'] and proof['planned'] == 128
        for name, digest in proof['sha256'].items():
            assert sha(P / name) == digest, ('Pinned file changed', name)
        assert read(C / 'independent-guard-review.json')['passed']
        assert not (E / NAME).exists(), 'No duplicate/restart/overwrite'
        assert not (C / 'guard128-started.json').exists()
        model = D / 'runs/production/final'
        args = ['bash', str(E / 'run_eval.sh'), '--model', str(model), '--mode', 'structured',
                '--name', NAME, '--suite', '128', '--system-file', str(D / 'system.txt')]
        receipt = dict(state='running', at=now(), pid=os.getpid(), argv=args,
                       constrained_decoding=True, planned=128, model=str(model),
                       source_sha256=sha(Path(__file__)))
        save(C / 'guard128-started.json', receipt)
        save(status, receipt)
        with (C / 'guard128.log').open('x') as log:
            result = subprocess.run(args, cwd=P, stdout=log, stderr=subprocess.STDOUT)
        assert result.returncode == 0, ('Evaluation failed', result.returncode)
        summary = read(E / NAME / 'summary.json')
        assert summary['planned'] == summary['completed'] == 128
        assert summary['constrained_decoding'] and summary['format_guard_version'] == 1
        assert read(E / NAME / 'worker-exits.json') == [0] * 8
        save(status, dict(state='complete', at=now(), constrained_decoding=True,
                          summary=str(E / NAME / 'summary.json'),
                          metrics={k: summary[k] for k in ['planned', 'completed', 'correct',
                                   'format_valid', 'parallel_protocol_valid', 'executed_fork_samples']}))
    except BaseException as error:
        save(status, dict(state='failed', at=now(), error=repr(error), constrained_decoding=True))
        raise


if __name__ == '__main__':
    main()
