"""Accuracy-first selection, followed by the frozen Base benchmark protocol."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'verl').is_dir() and (p/'exps').is_dir())

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run',required=True)
    args=parser.parse_args()
    run=Path(args.run).resolve()
    if not run.is_relative_to(HERE/'runs'):
        raise ValueError('Benchmark must use this isolated RL campaign')
    result=json.loads((run/'result.json').read_text())
    if not result.get('completed'):
        raise ValueError('Training did not complete')
    candidates=[]
    for directory in run.glob('validation-*'):
        row=json.loads((directory/'summary.json').read_text())
        step=row['step']
        if step and (run/f'checkpoint-{step:04}/complete.json').exists():
            candidates.append(row)
    if not candidates:
        raise ValueError('No exported checkpoint with complete independent selection validation')
    # Accuracy first, canonical format next; actual physical generation cost breaks ties.
    best=max(candidates,key=lambda r:(r['correct'],r['format_valid'],-sum(r['actual_forward_calls']),-r['step']))
    model=run/f"checkpoint-{best['step']:04}/hf"
    decision=dict(checkpoint=str(model),selection=best,
                  criterion='selection accuracy, format, lower physical forwards, earlier step',
                  benchmark_used_for_selection=False,
                  frozen_protocol='vLLM BF16, temperature.6 top_p.95 top_k20 seed42+sample_index, response4096 path2048')
    target=run/'benchmark-selection.json'
    if target.exists():
        raise FileExistsError(target)
    target.write_text(json.dumps(decision,indent=2)+'\n')
    evaluator=HERE/'evaluations/evaluate.py'
    environment=os.environ.copy()
    environment.update(PYTHONPATH=str(evaluator.parent)+':'+str(evaluator.parent/'runtime'),
                       PYTHONUNBUFFERED='1',OMP_NUM_THREADS='1',HF_HUB_OFFLINE='1',
                       TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
    for suite in ['128','512']:
        argv=[sys.executable,'-B',str(evaluator),'--model',str(model),'--mode','structured',
              '--name',run.name+'-selected-'+suite,'--suite',suite,
              '--system-file',str(ROOT/'work/experiments/base-format-20261010/system.txt')]
        subprocess.run(argv,cwd=ROOT,env=environment,check=True)
    decision['completed']=True
    decision['evaluator_sha256']=hashlib.sha256(evaluator.read_bytes()).hexdigest()
    (run/'benchmark-result.json').write_text(json.dumps(decision,indent=2)+'\n')

if __name__=='__main__':
    main()
