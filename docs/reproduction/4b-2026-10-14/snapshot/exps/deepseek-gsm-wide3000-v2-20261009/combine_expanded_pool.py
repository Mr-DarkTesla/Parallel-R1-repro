import json,hashlib,random,time,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent.parent
old=BASE/'exps/deepseek-gsm-only-20261009'
processed={r['id'] for r in map(json.loads,(old/'production/journal.jsonl').read_text().splitlines())}
existing=[json.loads(l) for l in (ROOT/'candidate-pool.jsonl').read_text().splitlines()];existing_ids={r['id'] for r in existing}
expanded=[json.loads(l) for l in (ROOT/'expanded-original-candidate-pool.jsonl').read_text().splitlines()]
conventions='GSM-Infinite dataset conventions: For this self-contained problem, an unmentioned category at a location contributes zero. A total includes all relevant categories mentioned at that location. Total nominations or newborn children are sums of (number of films or adult animals) times (average nominations or children per member); totals of schools or adult animals sum the category counts.\n\n'
norm=lambda s:' '.join(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',s).lower()))
seen={norm(r['core_problem']) for r in existing}
seen.update(norm(r['core_problem']) for r in map(json.loads,(old/'candidate-pool.jsonl').read_text().splitlines()) if r['id'] in processed)
extras=[]
for candidate in expanded:
 key=norm(candidate['core_problem'])
 if candidate['id'] in existing_ids|processed or key in seen:continue
 seen.add(key);extras.append(candidate)
for r in extras:
 r['question']=conventions+r['question'];r['question_conventions_version']='explicit-gsm-rules-v1'
 eligible=int(hashlib.sha256(r['id'].encode()).hexdigest()[:8],16)%5==0
 r['verification_eligible']=eligible
 r['verification_policy']=('For this example, if useful, include at most one explicitly planned independent recomputation of a substantive intermediate quantity or candidate answer. It may repeat the same subproblem and even the same method. Work it out independently in full and compare both results in Summary. This is intentional verification; do not copy a sibling result. Omit it if it provides no real checking value.' if eligible else 'For this example prefer distinct useful computed outputs. You may perform necessary consistency checks, but do not add a duplicated assignment merely to increase width.')
random.Random(2026100902).shuffle(extras);rows=existing+extras
assert len({r['id'] for r in rows})==len(rows) and not ({r['id'] for r in rows}&processed)
print({'old_remaining':len(existing),'expanded':len(expanded),'extra':len(extras),'total':len(rows)},flush=True)
assert all(r['source']=='GSM_Infinite' for r in rows) and len(rows)>=8000
(ROOT/'candidate-pool.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
manifest=json.loads((ROOT/'pool-manifest.json').read_text());manifest.update(at=time.time(),expanded_candidates=len(rows),new_pool_sha256=hashlib.sha256((ROOT/'candidate-pool.jsonl').read_bytes()).hexdigest(),source_expansion_manifest=str(ROOT/'expanded-source-manifest.json'),mean_width_acceptance_target=None,narrow_valid_candidates_retained=True)
(ROOT/'pool-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print({'candidates':len(rows),'extra':len(extras),'mean_width_target':None})
