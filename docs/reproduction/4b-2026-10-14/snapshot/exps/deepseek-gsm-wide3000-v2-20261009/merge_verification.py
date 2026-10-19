import json,hashlib,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
assert json.loads((ROOT/'pilot-status.json').read_text())['state']=='complete'
assert json.loads((ROOT/'verification-pilot-status.json').read_text())['state']=='complete'
base=[json.loads(l) for l in (ROOT/'pilot-results.jsonl').read_text().splitlines()]
replacement={r['id']:r for r in map(json.loads,(ROOT/'verification-pilot-results.jsonl').read_text().splitlines())}
assert len(base)==60 and len(replacement)==8
combined=[{**replacement[r['id']],'review_origin':'verification-prompt-correction'} if r['id'] in replacement else {**r,'review_origin':'wide-cut-pilot'} for r in base]
assert len({r['id'] for r in combined})==60
(ROOT/'reviewed-pilot-results.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in combined))
report={'at':time.time(),'unique_questions':60,'verification_cases_regenerated':8,'original_responses_preserved':True,'production_prompt_sha256':hashlib.sha256((ROOT/'prompt-wide-explicit.txt').read_bytes()).hexdigest(),'note':'Verification wording was aligned with student and judge; non-verification cases retain the initial wide-cut pilot outputs.'}
(ROOT/'pilot-correction-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
