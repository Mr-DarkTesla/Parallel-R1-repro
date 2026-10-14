from pathlib import Path
import json
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';Q=P/'work/experiments/night-20261010/cloud-continued/tmp2/queue/303-instruct-full-guard-smoke24.json'
item=dict(argv=['bash',str(B/'run_eval_smoke.sh')],cwd=str(P),wait_for=[str(B/'epoch1-export-proof.json'),str(B/'independent-eval-source-review.json')],timeout_seconds=5400)
with Q.open('x') as f:json.dump(item,f,indent=2)
print(Q)
