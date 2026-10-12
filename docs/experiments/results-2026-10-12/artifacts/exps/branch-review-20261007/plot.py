import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

os.environ.setdefault('MPLCONFIGDIR', '${TMPDIR}/r1-mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p = Path(__file__).resolve().parent
data = json.loads((p / 'live-metrics.json').read_text())
live = json.loads((p / 'latest-s2.json').read_text())
runs = data['runs']
key = 'val-core/APO_MATH300/acc/mean@1'
baseline = next(r[key] for r in runs['rl-unseen-s1-20261006']['logs']['driver.log']['metrics'] if key in r)

def rows(names):
    result = {}
    for name in names:
        for log in runs[name]['logs'].values():
            for r in log['metrics']:
                if 'training/global_step' in r:
                    result[int(r['training/global_step'])] = r
    return result

old = rows(['rl-unseen-s1-20261006', 'rl-unseen-s1-20261007-seq128'])
s1 = rows(['rl-unseen-s1-bs32-20261007'])
s2 = {s:r for s,r in rows(['rl-unseen-s2-bs32-20261007']).items() if s <= 30}
s2.update({int(r['training/global_step']):r for r in live['metrics']})
last = max(s2)
state = 'завершён' if live['status'].get('state') == 'complete' else ('выполняется' if live['alive'] else 'процесс завершён')
series = [
    ('S1 · batch 256 · остановлен на 280', old, '#64748b'),
    ('S1 · batch 32 · завершён, 300 шагов', s1, '#2563eb'),
    (f'S2 · batch 32 · {last}/500, {state}', s2, '#d15b19'),
]
observed = datetime.fromisoformat(live['observed_at']).astimezone(ZoneInfo('Europe/Moscow'))
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11,
                     'axes.spines.top':False, 'axes.spines.right':False,
                     'axes.edgecolor':'#cbd5e1', 'text.color':'#1e293b',
                     'axes.labelcolor':'#475569', 'grid.color':'#e2e8f0'})
fig, axes = plt.subplots(1, 2, figsize=(14, 6.8))
fig.suptitle('Qwen3-0.6B: прогресс RL из Unseen-SFT', x=.07, y=.97,
             ha='left', fontsize=21, fontweight='bold')
fig.text(.07, .915, f'Снимок {observed:%d.%m.%Y %H:%M} МСК · все прогоны на 8 GPU', color='#64748b')
a, b = axes
for label, rr, color in series:
    ordered = sorted(rr.items())
    vals = [(s,r[key]*100) for s,r in ordered if key in r]
    a.plot([s for s,v in vals], [v for s,v in vals], 'o-', color=color, lw=2, ms=4, label=label)
    s,v = vals[-1]
    a.annotate(f'{v:.1f}%', (s,v), xytext=(5,7), textcoords='offset points', color=color, fontweight='bold')
    pts = [(s,r['parallel/ratio']*100) for s,r in ordered if 'parallel/ratio' in r]
    b.plot([s for s,v in pts], [v for s,v in pts], color=color, alpha=.16, lw=.7)
    smooth = [(pts[i][0],sum(v for s,v in pts[i-9:i+1])/10) for i in range(9,len(pts)) if pts[i][0]-pts[i-9][0]==9]
    b.plot([s for s,v in smooth], [v for s,v in smooth], color=color, lw=2)
a.axhline(baseline*100, color='#94a3b8', ls='--', lw=1.3)
a.text(490, baseline*100+.6, f'Исходный SFT: {baseline*100:.1f}%', ha='right', color='#64748b', fontsize=9)
a.set_title('Качество: MATH-316', loc='left', fontweight='bold', pad=14)
a.set_ylabel('Accuracy, % · один ответ на задачу')
a.set_ylim(15,58)
b.set_title('Параллельные ответы на обучении', loc='left', fontweight='bold', pad=14)
b.set_ylabel('Доля ответов с <Parallel>, %')
b.set_ylim(-3,103)
for ax in axes:
    ax.set_xlim(0,510)
    ax.set_xlabel('Шаг RL')
    ax.grid(axis='y')
    ax.set_axisbelow(True)
a.legend(loc='upper left', fontsize=9, frameon=False)
fig.text(.07,.075,'Слева — завершённые валидации, линии соединяют наблюдения. Справа — шаги и среднее за 10 шагов.',fontsize=9,color='#64748b')
fig.text(.07,.045,'Шаги разных batch не равны по объёму данных и времени; настройки ускорения различались. Преимущество batch не установлено.',fontsize=9,color='#64748b')
fig.subplots_adjust(left=.07,right=.98,top=.83,bottom=.18,wspace=.2)
for ext in ('png','svg'):
    fig.savefig(p/f'rl-progress.{ext}',dpi=170,facecolor='white')
summary = {'observed_at':live['observed_at'],'s2_last_step':last,'s2_alive':live['alive'], 's2_log_age_s':live['age_s'], 'baseline_math':baseline}
for label,rr,color in series:
    vals=[(s,r[key]) for s,r in sorted(rr.items()) if key in r]
    summary[label]={'latest_validation_step':vals[-1][0],'math':vals[-1][1]}
summary['s2_parallel_last10']=sum(s2[s]['parallel/ratio'] for s in sorted(s2)[-10:])/10
(p/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2,ensure_ascii=False))
