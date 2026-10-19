from pathlib import Path
import json,hashlib
B=Path.cwd()/'work/experiments/instruct-full-20261011';E=B/'evaluations'
assert json.loads((B/'epoch1-export-proof.json').read_text())['passed']
review=json.loads((B/'independent-eval-source-review.json').read_text());assert review['passed']
proof=json.loads((B/'eval-guard-prepared.json').read_text());assert proof['passed']
for rel,expected in proof['source_hashes'].items():assert hashlib.sha256((E/rel).read_bytes()).hexdigest()==expected,rel
print('eval source and full model export admission PASS')
