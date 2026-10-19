from pathlib import Path
import json,hashlib
B=Path.cwd()/'work/experiments/instruct-full-20261011'
receipt=json.loads((B/'root-eval128-approved.json').read_text());assert receipt['passed'] and receipt['scope']=='Instruct-full-epoch1-matched-guard-eval128'
for rel,expected in receipt['hashes'].items():assert hashlib.sha256((B/rel).read_bytes()).hexdigest()==expected,rel
smoke=json.loads((B/'evaluations/epoch1-guard-structured-24/summary.json').read_text());assert smoke['completed']==24 and smoke['missing']==0
assert json.loads((B/'evaluations/epoch1-guard-structured-24/worker-exits.json').read_text())==[0]*8
exec((B/'check_eval_smoke_admission.py').read_text())
print('actual smoke and matched guarded128 root admission PASS')
