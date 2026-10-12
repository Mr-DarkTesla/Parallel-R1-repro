"""Original arithmetic probes for engineering readiness, never curriculum data."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent/'technical-probes.jsonl';rows=[]
for i in range(16):
 a=17+3*i;b=9+2*i;c=4+i
 rows.append(dict(id=f'instruct-engineering-synthetic-{i}',problem=f'A store receives {a} boxes, each containing {b} pencils, and gives away {c} pencils. How many pencils remain?',answer=str(a*b-c),source='Original generated engineering probe, arithmetic only',curriculum_allowed=False,benchmark=False))
p.write_text(''.join(json.dumps(x)+'\n' for x in rows));print(p)
