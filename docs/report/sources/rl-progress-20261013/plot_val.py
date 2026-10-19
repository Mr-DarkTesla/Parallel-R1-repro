from pathlib import Path
import json,csv,statistics
from datetime import datetime,timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
p=Path(__file__).resolve().parent;d=json.loads((p/'snapshot.json').read_text())
points=[dict(step=0,correct=16,n=32,backend='HF FP32'),dict(step=50,correct=28,n=32,backend='HF FP32')]
points += [dict(step=r['step'],correct=r['correct'],n=r['completed'],backend='vLLM BF16') for r in d['vals']]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#9ba7b8','axes.labelcolor':'#27364b','xtick.color':'#27364b','ytick.color':'#27364b'})
fig,ax=plt.subplots(figsize=(10,4.7),dpi=170);fig.patch.set_facecolor('white');ax.set_facecolor('white')
old=points[:2];new=points[2:]
ax.plot([x['step'] for x in old],[100*x['correct']/x['n'] for x in old],color='#7a8799',marker='o',markersize=7,lw=2,label='0–50: HF FP32')
ax.plot([x['step'] for x in new],[100*x['correct']/x['n'] for x in new],color='#2463cc',marker='o',markersize=7,lw=2.2,label='100–300: vLLM BF16')
ax.axhline(50,color='#acb5c2',ls=':',lw=1.2)
ax.axvspan(50,100,color='#eef1f5',zorder=0)
for x in points:
 y=100*x['correct']/x['n'];label=f"{x['correct']}/32\n{y:.1f}%".replace('.',',')
 ax.annotate(label,(x['step'],y),xytext=(0,10),textcoords='offset points',ha='center',va='bottom',fontsize=10,color='#27364b')
ax.set_xlim(-12,315);ax.set_ylim(0,103);ax.set_xticks([0,50,100,150,200,250,300]);ax.set_yticks(range(0,101,20));ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_xlabel('Логический шаг RL');ax.set_ylabel('Правильные ответы / все 32 задачи');ax.grid(axis='y',color='#e8edf3',lw=.8);ax.set_axisbelow(True)
ax.set_title('Clean val32: 16/32 перед RL → 29/32 на шаге 300',loc='left',fontweight='bold',pad=16)
ax.legend(loc='lower right',frameon=False,fontsize=10)
fig.text(.095,.02,'Фиксированные задачи и seed; 1 ответ на задачу. После шага 50: смена backend/precision и сброс Adam.\nМалая validation; 1 задача = 3,125 п.п. График не является результатом MATH500.',fontsize=9,color='#5a687a')
fig.subplots_adjust(left=.095,right=.98,top=.84,bottom=.21)
fig.savefig(p/'val32.png',bbox_inches='tight');fig.savefig(p/'val32.svg',bbox_inches='tight')
with (p/'val32-metrics.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['step','correct','n','backend','accuracy']);w.writeheader();w.writerows(dict(**x,accuracy=x['correct']/x['n']) for x in points)
mean=statistics.mean(r['seconds'] for r in d['recent']);now=datetime.fromisoformat(d['now_msk']);eta=now+timedelta(seconds=(500-d['step'])*mean)
print(json.dumps(dict(step=d['step'],mean_seconds=mean,remaining=500-d['step'],remaining_hours=(500-d['step'])*mean/3600,training_eta=eta.isoformat(),plot=str(p/'val32.png'))))
