"""Executed fork width from SHA256-verified RL300 benchmark trace snapshot."""
from pathlib import Path
from collections import Counter
from statistics import mean
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

OUT = Path(__file__).resolve().parent
SOURCE = OUT.parent / 'rl300-benchmark-summary-20261014/fork-snapshot.json'
source = json.loads(SOURCE.read_text())
model = source['models']['RL300']
datasets = [('MATH500', 500), ('AIME2024', 30), ('AIME2025', 30), ('AIME2026', 30)]
data = []
for dataset,n in datasets:
    rows = model[dataset]
    assert len(rows) == len({r['id'] for r in rows}) == n
    assert all(r['forks'] == len(r['widths']) for r in rows)
    assert all(r['model_sha256'] == '8b4921297d797c4a58c851abdb98ea6dd75eeb4c5af958e5292caa9e2681aa39' for r in rows)
    widths = [w for r in rows for w in r['widths']]
    valid = [w for r in rows if r['format_valid'] for w in r['widths']]
    data.append(dict(dataset=dataset, questions=n, questions_with_fork=sum(bool(r['widths']) for r in rows), forks=len(widths), width_all=mean(widths), width_valid=mean(valid), valid_forks=len(valid), histogram=dict(sorted(Counter(widths).items()))))
total_forks=sum(d['forks'] for d in data)
pooled=sum(d['width_all']*d['forks'] for d in data)/total_forks
plt.rcParams.update({
    'font.family':'DejaVu Sans','font.size':11.5,'figure.facecolor':'white','axes.facecolor':'white',
    'text.color':'#33332f','axes.labelcolor':'#33332f','xtick.color':'#77776e','ytick.color':'#77776e',
    'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,
    'axes.edgecolor':'#c6c3b9','axes.linewidth':.8,'svg.fonttype':'none','pdf.fonttype':42,
})
fig,axes=plt.subplots(2,2,figsize=(14,9.4))
fig.subplots_adjust(left=.07,right=.96,top=.86,bottom=.13,wspace=.23,hspace=.48)
for ax,d in zip(axes.flat,data):
    widths=list(range(2,9)); pct=[100*d['histogram'].get(w,0)/d['forks'] for w in widths]
    ax.barh(range(7),pct,height=.49,color='#397CC1',zorder=3)
    for i,p in enumerate(pct):
        if p:
            ax.text(p+1.15,i,f'{p:.2f}%'.replace('.',','),va='center',fontsize=11.2,fontweight='bold',color='#33332f')
    ax.set_yticks(range(7),[str(w) for w in widths]);ax.invert_yaxis();ax.set_xlim(0,110)
    ax.xaxis.set_major_locator(MultipleLocator(20));ax.set_xlabel('Доля форков, %',labelpad=8)
    ax.set_ylabel('Веток в форке',labelpad=8);ax.tick_params(length=0,pad=7)
    ax.grid(axis='x',color='#e8e6df',linewidth=.85);ax.set_axisbelow(True)
    ax.set_title(d['dataset'],loc='left',fontsize=16,fontweight='bold',pad=27)
    ax.text(0,1.025,f"Среднее {d['width_all']:.3f} · {d['forks']} форков · {d['questions_with_fork']}/{d['questions']} задач с форком".replace('.',','),transform=ax.transAxes,fontsize=10.5,color='#77776e')
fig.suptitle('RL-300 · ширина форков на тестовых наборах',x=.07,y=.975,ha='left',fontsize=19,fontweight='bold')
fig.text(.07,.925,f'Среднее по всем {total_forks} форкам: {pooled:.3f} ветки'.replace('.',','),fontsize=13,color='#77776e')
fig.text(.07,.066,'Все ответы, включая неверные и ошибки формата. Каждый выполненный форк имеет одинаковый вес; задачи без форка не добавляют нули.',fontsize=10,color='#77776e')
fig.text(.07,.038,'Прежний RL-300: BF16/FP32 · response 32768 · path 768 · context 40960. Протокол отличается от нового SFT → RL-150.',fontsize=10,color='#77776e')
for ext in ['png','pdf','svg']:fig.savefig(OUT/f'fork-width.{ext}',dpi=200,facecolor='white')
manifest=dict(checkpoint=300,source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),source_files_verified=74,completed=590,datasets=data,total_forks=total_forks,width_all=pooled,definition='Equal weight per executed fork across all answers including wrong/format-invalid; no zero for no-fork answers',protocol=dict(response=32768,path=768,context=40960,precision='mixed BF16/FP32'))
(OUT/'data.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False))
