"""Figure 3 metric for the full training lineage, updates 1-300."""
import base64
import io
import json
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

REMOTE = 'DATA' in globals()
P = Path(__file__).resolve().parent if not REMOTE else None
data = DATA if REMOTE else json.loads((P / 'data.json').read_text())
rows = sorted([r for v in data['runs'].values() for r in v['rows']], key=lambda r: r['step'])
assert [r['step'] for r in rows] == list(range(1, 301))
def aggregate(part):
    blocks = sum(r['blocks'] for r in part)
    first_n = sum(r['responses_with_parallel'] for r in part)
    return dict(mean=sum(r['blocks'] * r['mean_relative_position'] for r in part if r['blocks'])/blocks,
        first_mean=sum(r['responses_with_parallel'] * r['mean_first_relative_position'] for r in part if r['responses_with_parallel'])/first_n,
        blocks=blocks, responses=sum(r['responses'] for r in part),
        responses_with_parallel=first_n,
        mean_start_token=sum(r['blocks'] * r['mean_start_token'] for r in part if r['blocks'])/blocks,
        truncated=sum(r['truncated_responses'] for r in part),
        invalid_format=sum(r['invalid_format_responses'] for r in part))
summary = dict(first20=aggregate(rows[:20]), last20=aggregate(rows[-20:]),
    first50=aggregate(rows[:50]), last50=aggregate(rows[-50:]), all=aggregate(rows))
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
    'axes.spines.top': False, 'axes.spines.right': False,
    'figure.facecolor': 'white', 'axes.facecolor': 'white'})
fig, ax = plt.subplots(figsize=(11.5, 6.7))
fig.subplots_adjust(left=.105, right=.97, top=.80, bottom=.29)
steps = [r['step'] for r in rows]
y = [r['mean_relative_position'] for r in rows]
smooth = [aggregate(rows[max(0, i-9):i+1])['mean'] for i in range(len(rows))]
ax.plot(steps, y, color='#5877b6', lw=.8, alpha=.28, label='Среднее за итерацию')
ax.plot(steps, smooth, color='#3c62a9', lw=2.6, label='Среднее за 10 итераций')
ax.axvline(50.5, color='#778193', ls='--', lw=1.2)
ax.text(54, .98, 'Продолжение от checkpoint 50', transform=ax.get_xaxis_transform(),
        fontsize=9, color='#778193', va='top')
ax.set_xlim(1,300)
ax.set_ylim(0, min(1, max(.3, math.ceil((max(y)+.03)*10)/10)))
ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
ax.set_xticks([1,50,100,150,200,250,300])
ax.set_xlabel('Итерация RL', labelpad=10)
ax.set_ylabel('Средняя позиция начала <Parallel>\n(% длины ответа)', labelpad=10)
ax.grid(alpha=.18)
ax.set_axisbelow(True)
ax.legend(frameon=False, loc='lower right', fontsize=11)
fig.suptitle('Первые 300 итераций RL · начало parallel-блока', x=.055, ha='left',
             y=.96, fontsize=19, fontweight='bold')
fig.text(.055,.875,'Метрика Figure 3: индекс токена <Parallel> / длина ответа; среднее по всем блокам',
         fontsize=11,color='#596579')
fig.text(.105,.16,
    f'Первые 20 итераций: {100*summary["first20"]["mean"]:.1f}%  →  последние 20: {100*summary["last20"]["mean"]:.1f}%',
    fontsize=12,fontweight='bold',color='#3c62a9')
fig.text(.105,.11,'Train-траектории: 1–50 — 96 ответов/update; 51–300 — 64. Лимиты: ответ 4096, ветка 768.',
         fontsize=10,color='#596579')
fig.text(.105,.065,'Без фильтра по правильности и формату; ответы без <Parallel> исключены. Prompt не учитывается.',
         fontsize=10,color='#596579')
fig.text(.105,.025,'Снимок 14.10.2026 · все 300 завершённых updates проверены по global metrics · после50 новый Adam',
         fontsize=9,color='#778193')
if REMOTE:
    images = {}
    for ext in ['png','pdf','svg']:
        buffer=io.BytesIO();fig.savefig(buffer,format=ext,dpi=180)
        images[ext]=base64.b64encode(buffer.getvalue()).decode()
    print('RL300_PLOT_JSON_BEGIN')
    print(json.dumps(dict(images=images,summary=summary)))
else:
    for ext in ['png','pdf','svg']:fig.savefig(P/f'parallel-position.{ext}',dpi=180)
    (P/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
