from pathlib import Path
import json,hashlib
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011'
receipt=json.loads((B/'root-epoch1-approved.json').read_text());assert receipt['passed'] and receipt['scope']=='Instruct-4B-full-SFT-epoch1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for rel,expected in receipt['hashes'].items():assert sha(B/rel)==expected,rel
assert json.loads((B/'smoke-export-proof.json').read_text())['passed']
assert json.loads((B/'runs/isolation/isolation-proof.json').read_text())['passed']
assert json.loads((B/receipt['independent_report']).read_text())['passed']
Q=P/'work/experiments/night-20261010/cloud-continued/tmp2/queue/302-instruct-full-epoch1.json'
assert not (B/'runs/epoch1').exists()
item=dict(argv=['bash',str(B/'run_train.sh'),'epoch1'],cwd=str(P),timeout_seconds=21600)
with Q.open('x') as f:json.dump(item,f,indent=2)
(B/'production-launch-proof.json').write_text(json.dumps(dict(root_receipt_sha256=sha(B/'root-epoch1-approved.json'),queue_path=str(Q),item=item),indent=2)+'\n');print(Q)
