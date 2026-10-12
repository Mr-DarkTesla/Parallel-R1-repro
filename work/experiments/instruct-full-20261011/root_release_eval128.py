"""Release matched guarded evaluations after actual full-SFT smoke."""
from pathlib import Path
import hashlib
import json
import time

B = Path('work/experiments/instruct-full-20261011')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

proofs = {
    'independent-eval24-review.json': '8e7859f42cac25587a8f3cd2d858ef7eb29ac4d21ec09946c62c3c629a682793',
    'independent-eval-source-review.json': '507b86d19de55ef75eff2eb066eca9eb1d4cdb40cd4c1b51fbb2ba091fd0e338',
    'independent-review/epoch1-completion.json': '003de117ed1aea8b64b2ae8853dea9ad62999480e7089a2c3b95cce0138562b5',
}
for name, expected in proofs.items():
    assert sha(B / name) == expected, name
summary = json.loads((B / 'evaluations/epoch1-guard-structured-24/summary.json').read_text())
assert summary['completed'] == 24 and summary['missing'] == 0 and summary['gate_passed']
assert summary['correct'] == 18 and summary['format_valid'] == 24
assert summary['parallel_protocol_valid'] == 23
assert json.loads((B / 'evaluations/epoch1-guard-structured-24/worker-exits.json').read_text()) == [0] * 8
assert json.loads((B / 'epoch1-export-proof.json').read_text())['passed']
assert json.loads((B / 'eval-smoke-proof.json').read_text())['passed']
files = list(proofs) + [
    'evaluations/epoch1-guard-structured-24/summary.json',
    'evaluations/epoch1-guard-structured-24/worker-exits.json',
    'eval-guard-prepared.json', 'epoch1-export-proof.json',
    'eval-smoke-proof.json', 'run_eval128.sh', 'check_eval128_admission.py',
]
receipt = dict(passed=True, scope='Instruct-full-epoch1-matched-guard-eval128',
               approved_at=time.time(), hashes={name: sha(B / name) for name in files},
               limitations=['24-task smoke is not a matched accuracy comparison',
                            'Evaluator F is a critical-path proxy, not measured physical forward calls'])
destination = B / 'root-eval128-approved.json'
assert not destination.exists()
temporary = destination.with_suffix('.tmp')
temporary.write_text(json.dumps(receipt, indent=2) + '\n')
temporary.replace(destination)
print(json.dumps({'passed': True, 'receipt_sha256': sha(destination)}))
