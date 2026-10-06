import argparse
import json
import re
import statistics
from pathlib import Path

parser = argparse.ArgumentParser(description='Measure checkpoint save overhead from training logs')
parser.add_argument('run', type=Path)
args = parser.parse_args()
run = args.run
rows=[]
for line in (run/'train.log').open():
    if 'training/global_step:' not in line:
        continue
    values=dict(re.findall(r'([A-Za-z0-9_@./-]+):(-?[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)',line))
    keys=('training/global_step','timing_s/step','timing_s/save_checkpoint','timing_s/testing','perf/max_memory_allocated_gb')
    rows.append({k:float(values[k]) for k in keys if k in values})
recent=rows[-20:]
step=statistics.mean(r['timing_s/step']-r.get('timing_s/testing',0) for r in recent)
save=statistics.mean(r['timing_s/save_checkpoint'] for r in recent)
print(json.dumps(dict(last_step=rows[-1]['training/global_step'],observed_steps=len(rows),recent_steps=len(recent),
                     mean_step_without_validation_s=step,mean_save_s=save,save_share=save/step,
                     mean_step_with_validation_s=statistics.mean(r['timing_s/step'] for r in recent),
                     max_gpu_allocated_gib=max(r['perf/max_memory_allocated_gb'] for r in rows),
                     projected_save_time_300_steps_min=save*300/60,
                     projected_save_time_every5_min=save*60/60,
                     projected_save_time_every10_min=save*30/60),indent=2))
