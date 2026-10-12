"""Root engineering release; run from the authorized Sirius project root."""
from pathlib import Path
import hashlib
import json
import time

B = Path('work/experiments/deep-sft-20261011-instruct')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

review_path = B / 'independent-review/continuation-v2-source-review.json'
assert sha(review_path) == '3abf6394b22d6aea10e0578f5f6d15bf28cc54acb0a7492e451757d4848c5856'
review = json.loads(review_path.read_text())
assert review['passed'] and review['exact_reviewed_seed_traces'] == 97
for name, expected in review['source_hashes'].items():
    assert sha(B / name) == expected, name
aggregate_path = B / 'independent-review/first128-substantive-aggregate.json'
aggregate = json.loads(aggregate_path.read_text())
assert aggregate['passed'] and aggregate['reviewed_actual_traces'] >= 96
assert aggregate['substantive_pass'] == 97
for name, expected in aggregate['hashes'].items():
    assert sha(B / name) == expected, name
seed = json.loads((B / 'production-v2/seed-manifest.json').read_text())
assert seed['seed_accepted'] == 124 and seed['seed_rejected'] == 4
assert 'synthetic-layered-dag-v1/2026104114' in seed['exclusions']
for name, expected in seed['hashes'].items():
    assert sha(Path(name)) == expected, name
receipt = json.loads((B / 'root-production-v2-approved.template.json').read_text())
receipt.update(approved=True, approved_at=time.time(),
               scope='Instruct deep-data generation continuation only; final training release pending',
               independent_source_review_sha256=sha(review_path),
               seed_manifest_sha256=sha(B / 'production-v2/seed-manifest.json'),
               aggregate_review_sha256=sha(aggregate_path),
               exact_reviewed_pass_traces=97, recovered_quarantined_traces=27,
               excluded=aggregate['excluded'])
def save(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)

destination = B / 'root-production-v2-approved.json'
assert not destination.exists(), 'Do not replace an existing release'
save(destination, receipt)
save(B / 'production-v2/FIRST128-REVIEWED', {
    'passed': True, 'root_receipt_sha256': sha(destination),
    'aggregate_review_sha256': sha(aggregate_path),
    'reviewed_actual_traces': 98, 'substantive_pass': 97,
    'excluded': aggregate['excluded'], 'approved_at': time.time(),
})
print(json.dumps({'approved': True, 'receipt_sha256': sha(destination)}))
