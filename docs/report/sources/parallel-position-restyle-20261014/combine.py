"""Overlay the published Figure 3 and our updates through iteration 250."""
from pathlib import Path
import json

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.ticker import PercentFormatter

OUT=Path(__file__).resolve().parent
source=json.loads((OUT.parent/'rl300-parallel-position-20261014/data.json').read_text())
rows=sorted([r for v in source['runs'].values() for r in v['rows']],key=lambda r:r['step'])
assert [r['step'] for r in rows]==list(range(1,301))
ours=[]
for i in range(len(rows)):
    part=rows[max(0,i-9):i+1]
    ours.append(sum(r['blocks']*r['mean_relative_position'] for r in part)/sum(r['blocks'] for r in part))
paper=json.loads((OUT/'paper-figure3-points.json').read_text())
plt.rcParams.update({
    'font.family':'DejaVu Sans','font.size':11.5,
    'figure.facecolor':'white','axes.facecolor':'white',
    'text.color':'#33332f','axes.labelcolor':'#33332f',
    'xtick.color':'#77776e','ytick.color':'#77776e',
    'axes.spines.top':False,'axes.spines.right':False,
    'axes.edgecolor':'#c6c3b9','axes.linewidth':.8,'svg.fonttype':'none',
})
fig,ax=plt.subplots(figsize=(8.4,4.9))
fig.subplots_adjust(left=.135,right=.975,top=.965,bottom=.17)
ax.set_xlabel('Итерация RL',labelpad=9)
ax.set_ylabel('Позиция начала <Parallel>, %',labelpad=10)
ax.set_xlim(0,250);ax.set_xticks([0,50,100,150,200,250])
ax.set_ylim(0,1);ax.set_yticks([0,.2,.4,.6,.8,1])
ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
ax.tick_params(length=0,pad=7)
ax.grid(axis='y',color='#e8e6df',linewidth=.85);ax.set_axisbelow(True)
for label,x,y,color in [
    ('Статья',[p['iteration'] for p in paper],[p['relative_position'] for p in paper],'#B9674D'),
    ('Наш',[r['step'] for r in rows],ours,'#397CC1'),
]:
    visible=[(a,b) for a,b in zip(x,y) if a<=250]
    line,=ax.plot([a for a,b in visible],[b for a,b in visible],label=label,color=color,lw=2.1,linestyle='-',
        solid_capstyle='round',solid_joinstyle='round')
    edge=matplotlib.colors.to_hex(np.array(matplotlib.colors.to_rgb(color))*.88)
    line.set_path_effects([pe.Stroke(linewidth=2.6,foreground=edge),pe.Normal()])
ax.legend(loc='upper left',frameon=False,handlelength=3.1,fontsize=12)
for ext in ['png','svg']:
    fig.savefig(OUT/f'comparison.{ext}',dpi=220,facecolor='white')
manifest=json.loads((OUT/'manifest.json').read_text())
manifest['combined']=dict(outputs=['comparison.png','comparison.svg'],
    displayed_iterations=[0,250],
    legend={'Статья':'#B9674D','Наш':'#397CC1'},
    content='two solid curves in shared axes, with legend; no title or prose captions')
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print(str(OUT/'comparison.png'))
