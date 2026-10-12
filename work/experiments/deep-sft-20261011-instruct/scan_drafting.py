"""Whole durable candidate inventory scan; findings never rewrite/admit traces."""
from pathlib import Path
import hashlib,json,re
b=Path('work/experiments/deep-sft-20261011-instruct/production-v2')
rows=[json.loads(s) for s in (b/'journal.jsonl').read_text().splitlines()]
patterns=[r'Return only',r'[Ll]et.s final',r'[Ww]e won.t',r'[Ww]e.ll output only',r'[Nn]eed ["“]',r'^\s*\.\s*["”]']
findings=[]
for r in rows:
    if r['decision']!='accepted':continue
    text=r['row']['raw_response'];prefix=text.split('Plan:',1)[0]
    hits=[p for p in patterns if re.search(p,prefix)]
    if hits:findings.append(dict(id=r['id'],raw_response_sha256=hashlib.sha256(text.encode()).hexdigest(),patterns=hits,prefix=prefix))
report=dict(scanned_accepted=sum(r['decision']=='accepted' for r in rows),findings=findings,
            automatic_admission=False,limitations='Known drafting markers only; no proof of all unflagged prose semantics.')
(b/'drafting-prefix-findings.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(scanned_accepted=report['scanned_accepted'],flagged=len(findings),ids=[r['id'] for r in findings]),indent=2))
