from pathlib import Path
import json
P=Path.cwd();B=P/'work/experiments/instruct-full-20261011';exec((B/'check_eval128_admission.py').read_text())
Q=P/'work/experiments/night-20261010/cloud-continued/tmp2/queue/304-instruct-full-matched-guard128.json'
item=dict(argv=['bash',str(B/'run_eval128.sh')],cwd=str(P),timeout_seconds=18000)
with Q.open('x') as f:json.dump(item,f,indent=2)
print(Q)
