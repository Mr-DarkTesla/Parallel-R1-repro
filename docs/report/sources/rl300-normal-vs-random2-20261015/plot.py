from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

R=Path('${PROJECT_ROOT}')
P=Path(__file__).resolve().parent
paths=[R/'work/experiments/eval-rl300-vllm-rolling-32k-20261013/result.json',R/'work/experiments/eval-rl300-random2-8gpu-20261014/result.json']
results=[json.loads(p.read_text()) for p in paths]
assert all(r['passed'] and r['completed']==590 for r in results)
names=['MATH500','AIME2024','AIME2025','AIME2026']
rows=[[next(x for x in r['datasets'] if x['dataset']==name) for name in names] for r in results]
assert all(x['technical_unknown']==0 and x['model_sha256']=='8b4921297d797c4a58c851abdb98ea6dd75eeb4c5af958e5292caa9e2681aa39' for group in rows for x in group)
(P/'data.json').write_text(json.dumps(dict(sources=list(map(str,paths)),normal=rows[0],random2=rows[1],matched_protocol=False),indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
fig,ax=plt.subplots(figsize=(12.8,7.4))
x=np.arange(4);width=.31
colors=['#4f76b5','#e48a42']
for offset,group,color,label in zip([-.5,.5],rows,colors,['До: обычный инференс','После: две случайные ветки']):
    vals=[100*r['correct']/r['completed'] for r in group]
    bars=ax.bar(x+offset*width,vals,width,color=color,label=label,zorder=3)
    for bar,v,r in zip(bars,vals,group):
        ax.text(bar.get_x()+bar.get_width()/2,v+1.7,f"{v:.1f}%\n{r['correct']}/{r['completed']}",ha='center',va='bottom',fontsize=12,fontweight='bold',color='#243347',linespacing=1.45)
labels=[]
for i,name in enumerate(names):
    labels.append(name.replace('AIME','AIME ')+f"\nF: {rows[0][i]['actual_forwards_all']:.1f} → {rows[1][i]['actual_forwards_all']:.1f}")
ax.set_xticks(x,labels);ax.tick_params(axis='x',length=0,pad=12)
ax.set_ylim(0,102);ax.set_yticks(range(0,101,20));ax.set_ylabel('Accuracy, %');ax.grid(axis='y',alpha=.18,zorder=0)
fig.suptitle('RL300: обычный инференс и две случайные ветки',x=.075,ha='left',y=.98,fontsize=20,fontweight='bold',color='#243347')
fig.legend(*ax.get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(.065,.925),ncol=2,frameon=False,fontsize=12)
fig.text(.075,.115,'F — средние generation forwards по ВСЕМ вопросам: MATH500 n=500; каждый AIME n=30.',fontsize=11,color='#526176')
fig.text(.075,.075,'Протоколы различаются: до — FP32/BF16, response32768/path768; после — BF16, response32000/path4000.',fontsize=10.5,color='#97552a')
fig.text(.075,.04,'Один и тот же checkpoint RL300, один ответ на вопрос. Разницу нельзя приписать только удалению веток.',fontsize=10.5,color='#97552a')
fig.subplots_adjust(left=.075,right=.98,top=.82,bottom=.245)
for ext in ['png','pdf','svg']:fig.savefig(P/f'paired-bars.{ext}',dpi=180)
print(json.dumps({'normal_accuracy':[r['accuracy'] for r in rows[0]],'random2_accuracy':[r['accuracy'] for r in rows[1]]}))
