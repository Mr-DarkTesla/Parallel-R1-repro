import json,time
from pathlib import Path
from validate import validate
ROOT=Path(__file__).resolve().parent
p=ROOT/'reviewed-pilot-results.jsonl';rows=[json.loads(l) for l in p.read_text().splitlines()]
changes=[]
for r in rows:
 shape=validate(r.get('output',''));shape.pop('blocks');r['structure']=shape
 if r.get('error','').startswith('deterministic_path_audit/') and shape['valid']:
  r['accepted']=True;r.pop('error',None)
 if r.get('accepted') and not shape['valid']:
  r.update(accepted=False,error='deterministic_path_audit/'+','.join(shape['errors']))
  changes.append({'id':r['id'],'errors':shape['errors']})
p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
(ROOT/'deterministic-path-audit.json').write_text(json.dumps({'at':time.time(),'rows':len(rows),'rejected_previously_accepted':changes,'note':'Every GSM path must display a numeric computation, as required by the explicit teaching prompt; numeric aliases alone are insufficient.'},indent=2)+'\n');print(changes)
