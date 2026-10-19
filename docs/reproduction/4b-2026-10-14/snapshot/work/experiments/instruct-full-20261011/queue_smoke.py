from pathlib import Path
import json
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';Q=P/'work/experiments/night-20261010/cloud-continued/tmp2/queue/300-instruct-full-smoke.json'
assert (B/'prepare-proof.json').exists()
item=dict(argv=['bash',str(B/'run_train.sh'),'smoke'],cwd=str(P),timeout_seconds=10800)
with Q.open('x') as f:json.dump(item,f,indent=2)
print(Q)
