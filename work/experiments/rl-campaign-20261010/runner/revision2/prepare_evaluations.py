"""Relocate frozen evaluator without changing its generation or scoring policy."""
from pathlib import Path
import hashlib
import json
import shutil

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'verl').is_dir() and (p/'exps').is_dir())
source=ROOT/'work/experiments/base-format-20261010/evaluations'
destination=HERE/'evaluations'
if destination.exists():
    if (destination/'setup-proof.json').exists():
        raise FileExistsError('Already prepared immutable evaluations')
    destination.rename(HERE/'evaluations-failed-setup-01')
destination.mkdir()
for name in ['evaluate.py','summary_metrics.py','native_eos.py','questions-128.jsonl']:
    shutil.copy2(source/name,destination/name)
path=destination/'evaluate.py'
text=path.read_text()
assert 'R.parents[3]' in text
text=text.replace('P=R.parents[3]',"P=next(p for p in R.parents if (p/'verl').is_dir() and (p/'exps').is_dir())")
text=text.replace("choices=['24','128']","choices=['24','128','512']")
path.write_text(text)
path=destination/'summary_metrics.py'
text=path.read_text()
old="Path(__file__).resolve().parents[2]/'unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py'"
assert old in text
text=text.replace(old,"next(p for p in Path(__file__).resolve().parents if (p/'verl').is_dir() and (p/'exps').is_dir())/'work/experiments/unseen-wide5145-20261009/eval-math500-forced-think-20261009/score.py'")
path.write_text(text)
(destination/'runtime').symlink_to(source/'runtime',target_is_directory=True)
rows=[json.loads(x) for x in (HERE/'data/final.jsonl').read_text().splitlines()]
assert len(rows)==512
for index,row in enumerate(rows):
    row.update(sample_index=index,dataset='GSM_Infinite_heldout_512',domain='GSM')
(destination/'questions-512.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in rows))
report=dict(frozen_source=str(source),path_only_adjustments=['project root discovery','summary scorer root'],
            additional_suite='512 disjoint GSM Infinite final',protocol_changed=False,
            sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in destination.glob('*') if f.is_file()},
            frozen_runtime=str(source/'runtime'))
(destination/'setup-proof.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
