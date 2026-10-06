"""Stream completed-step telemetry into a Figure-3 progress snapshot."""
import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('run', type=Path)
parser.add_argument('--out', type=Path, required=True)
parser.add_argument('--expected-samples', type=int, default=256,
                    help='Expected train trajectories per completed step (batch size times rollout.n)')
parser.add_argument('--label', help='Experiment label; defaults to the run directory name')
args = parser.parse_args()
last = int((args.run / 'checkpoints/latest_checkpointed_iteration.txt').read_text())
groups = defaultdict(lambda: dict(samples=0, tags=[], forks=[], with_tags=0, with_forks=0, truncated=0, outside=0))
for file in sorted((args.run / 'telemetry').glob('traces-*.jsonl')):
    # Ignore records appended after this snapshot starts.
    size = file.stat().st_size
    with file.open('rb') as stream:
        while stream.tell() < size:
            line = stream.readline()
            if stream.tell() > size:
                break
            try:
                trace = json.loads(line)
            except ValueError:
                continue
            step = int(trace['trajectory']['step'])
            if not 1 <= step <= last:
                continue
            split = 'val' if trace['trajectory']['validate'] else 'train'
            group = groups[(split, step)]
            length = trace['response_tokens']
            tags = trace['parallel_relative_positions']
            forks = [f['response_token_index']/length for f in trace['forks'] if length and f['response_token_index'] < length]
            group['samples'] += 1
            group['tags'].extend(tags)
            group['forks'].extend(forks)
            group['with_tags'] += bool(tags)
            group['with_forks'] += bool(trace['forks'])
            group['truncated'] += trace['truncated']
            group['outside'] += len(trace['forks'])-len(forks)
rows = []
for (split, step), group in sorted(groups.items()):
    rows.append(dict(split=split, step=step, samples=group['samples'],
                     tag_blocks=len(group['tags']), retained_executed_forks=len(group['forks']),
                     tag_position_mean=statistics.mean(group['tags']) if group['tags'] else None,
                     executed_fork_position_mean=statistics.mean(group['forks']) if group['forks'] else None,
                     tag_response_ratio=group['with_tags']/group['samples'],
                     executed_fork_response_ratio=group['with_forks']/group['samples'],
                     truncated_ratio=group['truncated']/group['samples'],
                     forks_outside_retained_response=group['outside']))
train = [r for r in rows if r['split']=='train']
if len(train) != last or any(r['samples'] != args.expected_samples for r in train):
    raise RuntimeError('Incomplete completed-step snapshot; do not plot partial batches')
args.out.mkdir(parents=True, exist_ok=True)
with (args.out / 'figure3-progress.csv').open('w', newline='') as stream:
    writer=csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def smooth(values, window=5):
    return [statistics.mean(values[max(0,i-window+1):i+1]) for i in range(len(values))]

plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10})
fig, axes=plt.subplots(2,1,figsize=(11,7.5),sharex=True)
series=[('tag_position_mean','tag_response_ratio','#2563eb','Все теги <Parallel>'),
        ('executed_fork_position_mean','executed_fork_response_ratio','#ea580c','Реальные форки')]
for pos, ratio, color, label in series:
    for ax, key in zip(axes,(pos,ratio)):
        values=[r[key] for r in train]
        ax.plot([r['step'] for r in train],values,color=color,alpha=.25,lw=1)
        ax.plot([r['step'] for r in train],smooth(values),color=color,lw=2,label=label+' · train, среднее за 5 шагов')
        val=[r for r in rows if r['split']=='val' and r[key] is not None]
        ax.scatter([r['step'] for r in val],[r[key] for r in val],color=color,
                   marker='o' if color=='#2563eb' else '^',s=36,zorder=3,
                   label=label+' · полная validation')
axes[0].set_ylabel('Средняя позиция / длина ответа')
axes[1].set_ylabel('Доля ответов с тегом / форком')
axes[1].set_xlabel('Завершённый шаг RL')
for ax in axes:
    ax.set_ylim(0,1)
    ax.set_xlim(1,last)
    ax.grid(alpha=.18)
    ax.legend(loc='best',fontsize=8)
fig.suptitle(f'Parallel-R1 · {args.label or args.run.name} · шаги 1–{last}',fontsize=15,fontweight='bold')
fig.text(.5,.015,'Тонкие линии — каждый train batch; толстые — сглаживание. Позиции усреднены по блокам; prompt исключён.\nЭто диагностика эксперимента, не подтверждение воспроизведения Figure 3.',ha='center',fontsize=9,color='#475569')
fig.tight_layout(rect=(0,.065,1,.955))
fig.savefig(args.out / 'figure3-progress.png',dpi=180)
fig.savefig(args.out / 'figure3-progress.pdf')
summary=dict(last_saved_step=last, train_samples=sum(r['samples'] for r in train),
             first_10_mean={key:statistics.mean(r[key] for r in train[:10]) for key in ('tag_position_mean','executed_fork_position_mean','tag_response_ratio','executed_fork_response_ratio')},
             last_10_mean={key:statistics.mean(r[key] for r in train[-10:]) for key in ('tag_position_mean','executed_fork_position_mean','tag_response_ratio','executed_fork_response_ratio')},
             last_validation=[r for r in rows if r['split']=='val'][-1:])
(args.out / 'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
