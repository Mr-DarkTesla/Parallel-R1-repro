"""Seal independently audited data, full-model launcher and learned-format evaluation."""
from pathlib import Path
import ast
import hashlib
import json
import subprocess
import sys

P = Path.cwd()
B = P / 'work/experiments/base-format-20261010'
assert json.loads((B / 'prepare-proof.json').read_text())['passed']
review = json.loads((B / 'independent-source-review.json').read_text())
assert review['passed']
p = B / 'evaluations/summary_metrics.py'
s = p.read_text().replace("['format_schema_version']=2", "['format_schema_version']=3")
s = s.replace("format_schema_version=2", "format_schema_version=3")
p.write_text(s)
for p in (B / 'evaluations').glob('*.py'):
    compile(p.read_text(), str(p), 'exec')
for p in [B / 'controller.py', B / 'code/verl/trainer/fsdp_parallel_sft_trainer.py']:
    compile(p.read_text(), str(p), 'exec')
subprocess.run(['bash', '-n', str(B / 'run_train.sh')], check=True)
sys.path.insert(0, str(B / 'evaluations'))
from summary_metrics import canonical_format_flags, executed_widths
sample = 'Plan:\n1: Compute twice three.\n2: Verify by addition.\n<Parallel>2\n<Path>1\n2*3=6\n</Path><Path>2\n3+3=6\n</Path></Parallel><Summary>Both results are 6.</Summary>\nFinal Answer: \\boxed{6}'
assert canonical_format_flags(sample)['format'] == 1
assert canonical_format_flags('<think>' + sample + '</think>')['format'] == 0
assert canonical_format_flags(sample.replace('2: Verify', '3: Verify'))['format'] == 0
assert canonical_format_flags(sample.replace('</Path><Path>2', 'Final Answer: 6\n</Path><Path>2'))['format'] == 0
row = dict(mode='structured', stats=dict(forks=2), trace=dict(policy_calls=[dict(phase=x) for x in ['planner','path','path','summary','planner','path','path','path','summary']]))
assert executed_widths(row) == [2, 3]
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()
paths = []
for root in [B / 'code', B / 'data', B / 'model', B / 'evaluations/runtime']:
    paths.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.startswith('._'))
paths.extend(p for p in (B / 'evaluations').iterdir() if p.is_file())
paths.extend(B / name for name in ['controller.py','run_train.sh','prepare-proof.json','source-pin.json','system.txt'])
ready = dict(passed=True, full_model=True, think_wrapped=False, source=review['source'] if 'source' in review else json.loads((B / 'source-pin.json').read_text()),
             protocol=dict(train=2700, validation=300, lr=1e-5, epochs=3, steps=126, batch_size=64,
                           eval=128, forced_parallel_opener=False, forced_width=False,
                           loss='all response tokens, including runtime synchronization and Path headers'),
             sha256={str(p.relative_to(P)):sha(p) for p in sorted(set(paths))},
             independent_source_review_sha256=sha(B / 'independent-source-review.json'),
             cpu_runtime_checks='no-think validator, Plan IDs, Final outside blocks, actual fork widths passed')
(B / 'launch-ready.json').write_text(json.dumps(ready, indent=2) + '\n')
print('SEALED', len(paths), 'files: full Base SFT smoke2/production126 -> autonomous128')
