import argparse
import json
import re
import statistics
from pathlib import Path

parser = argparse.ArgumentParser(description='Summarize training timings and validation accuracy')
parser.add_argument('run', type=Path)
args = parser.parse_args()
run = args.run
steps = []
for line in (run / 'train.log').open():
    if 'training/global_step:' not in line:
        continue
    metrics = dict(re.findall(r'([A-Za-z0-9_@./-]+):(-?[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)', line))
    steps.append({key: float(metrics[key]) for key in ('training/global_step', 'timing_s/step', 'timing_s/testing', 'parallel/ratio', 'parallel/relative_position_mean', 'response_length/mean', 'actor/grad_norm') if key in metrics})
print(json.dumps({'recent_steps': steps[-10:], 'mean_step_s_without_validation_last10': statistics.mean(s['timing_s/step']-s.get('timing_s/testing', 0) for s in steps[-10:])}, indent=2))
validations = []
for file in sorted((run / 'validation').glob('*.jsonl'), key=lambda p:int(p.stem)):
    scores=[]
    for line in file.open():
        row=json.loads(line)
        scores.append(row['score'])
    validations.append({'step':int(file.stem), 'samples':len(scores), 'positive_reward_answers':sum(s>0 for s in scores), 'positive_reward_rate':sum(s>0 for s in scores)/len(scores), 'mean_reward':statistics.mean(scores)})
print(json.dumps({'validation_history':validations}, indent=2))
