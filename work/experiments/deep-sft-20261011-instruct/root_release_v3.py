from pathlib import Path
import hashlib, json, time

B = Path('work/experiments/deep-sft-20261011-instruct')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
reports = {
    'independent-review/v3-source-style-review.json': '2499e9495d4755b1c2092bdc329e70b7736ce526f375f9261b9ba1a34f0c8573',
    'independent-review/v3-seed-admission-review.json': '5583cd44c8e03e634a99128de54ecddbed95d15573376fdbe43b756c966f4870',
    'independent-review/v3-seed-reviewed-coverage.json': 'cb39caf26974057966721983f6f863284c8e894c2651a31eb32506433ec56ead',
}
for name, expected in reports.items():
    assert sha(B/name) == expected
    report = json.loads((B/name).read_text())
    assert report['passed']
    for group in ['hashes', 'bound_hashes']:
        for path, digest in report.get(group, {}).items():
            assert sha(Path(path)) == digest, path
seed_path = B/'production-v3/seed-manifest.json'
assert sha(seed_path) == 'd9ed27a11ae3f03bc60834ddbaabfd928e87390ba51ba6745a559dba4095cf83'
seed = json.loads(seed_path.read_text())
assert seed['seed_accepted'] == 554 and seed['seed_rejected'] == 17
coverage = json.loads((B/'independent-review/v3-seed-reviewed-coverage.json').read_text())
assert coverage['exact_substantive_reviewed_passes_preserved'] == 147
for path, digest in seed['hashes'].items(): assert sha(Path(path)) == digest, path
receipt = json.loads((B/'root-production-v3-approved.template.json').read_text())
receipt.update(approved=True, approved_at=time.time(), independent_reports=reports,
               seed_manifest_sha256=sha(seed_path), exact_reviewed_pass_traces=147,
               scope='Generation continuation to3000; final training release pending')
def save(p, data):
    q=p.with_suffix('.tmp'); q.write_text(json.dumps(data,indent=2)+'\n');q.replace(p)
p=B/'root-production-v3-approved.json'
assert not p.exists()
save(p,receipt)
save(B/'production-v3/FIRST128-REVIEWED',dict(passed=True,root_receipt_sha256=sha(p),
    exact_reviewed_pass_traces=147,seed_manifest_sha256=sha(seed_path)))
print(json.dumps(dict(approved=True,receipt_sha256=sha(p))))
