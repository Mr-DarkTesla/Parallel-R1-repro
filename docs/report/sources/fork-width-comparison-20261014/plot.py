from pathlib import Path
import json
import hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

OUT=Path(__file__).resolve().parent
sources=[OUT.parent/'rl300-fork-width-20261014/data.json',OUT.parent/'rl150-fork-width-20261014/data.json']
widths=list(range(2,9))
groups=[]
for p in sources:
    d=json.loads(p.read_text());sets=d['datasets']
    assert len(sets)==4 and {s['dataset'] for s in sets}=={'MATH500','AIME2024','AIME2025','AIME2026'}
    percentages=[sum(100*s['histogram'].get(str(w),0)/s['forks'] for s in sets)/4 for w in widths]
    average=sum(s['width_all'] for s in sets)/4
    assert abs(sum(percentages)-100)<1e-9
    assert abs(sum(w*pct/100 for w,pct in zip(widths,percentages))-average)<1e-9
    groups.append(dict(checkpoint=d['checkpoint'],percentages=percentages,mean_width=average))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11.5,'figure.facecolor':'white','axes.facecolor':'white',
    'text.color':'#33332f','axes.labelcolor':'#33332f','xtick.color':'#77776e','ytick.color':'#77776e',
    'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#c6c3b9',
    'axes.linewidth':.8,'svg.fonttype':'none','pdf.fonttype':42})
fig,axes=plt.subplots(1,2,figsize=(14,6),sharey=True)
fig.subplots_adjust(left=.065,right=.975,top=.88,bottom=.16,wspace=.16)
for ax,g,title in zip(axes,groups,['Было','Стало']):
    ax.set_title(title,loc='left',fontsize=19,fontweight='bold',pad=12)
    ax.bar(widths,g['percentages'],width=.58,color='#397CC1',zorder=3)
    for w,pct in zip(widths,g['percentages']):
        if pct>0:
            ax.text(w,pct+1.5,f'{pct:.2f}%'.replace('.',','),ha='center',fontsize=11,fontweight='bold')
    ax.set_xticks(widths);ax.set_xlim(1.4,8.6);ax.set_ylim(0,100)
    ax.yaxis.set_major_locator(MultipleLocator(20));ax.tick_params(length=0,pad=8)
    ax.set_xlabel('Число веток в форке',labelpad=10);ax.grid(axis='y',color='#e8e6df',linewidth=.85);ax.set_axisbelow(True)
axes[0].set_ylabel('Средняя доля форков по тестовым наборам, %',labelpad=12)
for ext in ['png','pdf','svg']:fig.savefig(OUT/f'comparison.{ext}',dpi=200,facecolor='white')
manifest=dict(sources=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources],widths=widths,groups=groups,aggregation='Equal 25% weight for each benchmark distribution; mean width is macro mean of per-benchmark fork widths')
(OUT/'data.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(groups,ensure_ascii=False))
