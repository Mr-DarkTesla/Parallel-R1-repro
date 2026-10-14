"""Seal continuation to step64 from a root-reviewed clean validation checkpoint."""
import argparse,json,hashlib
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()

from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['forward_only','strong_width'],required=True);p.add_argument('--checkpoint-step',type=int,choices=[4,8,16],default=16);a=p.parse_args();base=Path(__file__).resolve().parent.parent;initial=base/'production-configs'/(a.mode+'-stage16.json');cfg=json.loads(initial.read_text());run=Path(cfg['output']);result=json.loads((run/'result.json').read_text());assert result['completed'];resume=run/f'checkpoint-{a.checkpoint_step:04}';assert json.loads((resume/'complete.json').read_text())['step']==a.checkpoint_step
summary=json.loads((run/f'validation-{a.checkpoint_step:04}/summary.json').read_text());baseline=json.loads((run/'validation-0000/summary.json').read_text());decision=dict(checkpoint_step=a.checkpoint_step,selected_checkpoint=str(resume),selection='Root-reviewed clean group-disjoint fixed-seed val32, no MATH500 selection',correct=summary['correct'],initial_sft_correct=baseline['correct'],delta_correct=summary['correct']-baseline['correct'],continuation_target=64)
root=next(p for p in base.parents if (p/'verl').is_dir() and (p/'exps').is_dir())
manifest_path=base/f'{a.mode}-resume-step{a.checkpoint_step}-manifest.json'
files=[p for p in resume.rglob('*') if p.is_file() and not p.name.startswith('._')]
files += [run/'validation-0000/summary.json',run/f'validation-{a.checkpoint_step:04}/summary.json',initial]
manifest=dict(checkpoint=str(resume),root=str(root),selection=decision,files={str(p):sha(p) for p in files})
assert not manifest_path.exists();manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
cfg['sealed_inputs'][str(manifest_path.relative_to(root))]=str(manifest_path)
cfg.update(resume_manifest=str(manifest_path),resume_manifest_sha256=sha(manifest_path),resume=str(resume),steps=64,checkpoint_steps=[32,48,64],output=str(base/'production-runs'/(a.mode+'-continue64')),initial_sft_validation=str(run/'validation-0000/summary.json'),continuation_decision=decision)
p=base/'production-configs'/(a.mode+'-continue64.json');assert not p.exists();p.write_text(json.dumps(cfg,indent=2)+'\n');print(json.dumps(dict(config=str(p),config_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),decision=decision)))
