import json
import os
import statistics
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

os.environ.setdefault('MPLCONFIGDIR','${TMPDIR}/r1-mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=Path(__file__).resolve().parent
d=json.loads((p/'live-metrics.json').read_text())
live=json.loads((p/'latest-s2.json').read_text())
def merge(names):
    result={}
    for name in names:
        for log in d['runs'][name]['logs'].values():
            for r in log['metrics']:
                if 'training/global_step' in r:
                    result[int(r['training/global_step'])]=r
    return result
old=merge(['rl-unseen-s1-20261006','rl-unseen-s1-20261007-seq128'])
s1=merge(['rl-unseen-s1-bs32-20261007'])
s2={s:r for s,r in merge(['rl-unseen-s2-bs32-20261007']).items() if s<=30}
s2.update({int(r['training/global_step']):r for r in live['metrics']})
series=[('S1 · batch 256',old,'#64748b'),('S1 · batch 32',s1,'#2563eb'),('S2 · batch 32',s2,'#d15b19')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#cbd5e1','grid.color':'#e2e8f0','text.color':'#1e293b'})
fig,ax=plt.subplots(figsize=(12,6.4))
fig.suptitle('Длина ответа в ходе обучения',x=.09,y=.97,ha='left',fontsize=22,fontweight='bold')
obs=datetime.fromisoformat(live['observed_at']).astimezone(ZoneInfo('Europe/Moscow'))
fig.text(.09,.885,f'Qwen3-0.6B · обучающие rollout · снимок {obs:%d.%m.%Y %H:%M} МСК',color='#64748b')
summary={}
for label,rr,color in series:
    rows=sorted((s,r['response_length/mean']) for s,r in rr.items())
    ax.plot([s for s,v in rows],[v for s,v in rows],color=color,lw=.7,alpha=.2)
    smooth=[(rows[i][0],statistics.mean(v for s,v in rows[i-9:i+1])) for i in range(9,len(rows)) if rows[i][0]-rows[i-9][0]==9]
    ax.plot([s for s,v in smooth],[v for s,v in smooth],color=color,lw=2.6,label=label)
    ax.scatter(*smooth[-1],color=color,s=25)
    ax.annotate(f'{smooth[-1][1]:.0f}',smooth[-1],xytext=(6,0),textcoords='offset points',color=color,fontweight='bold')
    windows=[]
    for start in range(1,max(rr)+1,50):
        values=[v for s,v in rows if start<=s<start+50]
        windows.append({'start':start,'end':min(start+49,max(rr)),'logged_steps':len(values),'mean_tokens':statistics.mean(values)})
    summary[label]={'first50_mean':statistics.mean(v for s,v in rows if s<=50),'last50_mean':statistics.mean(v for s,v in rows if s>max(rr)-50),'last10_mean':smooth[-1][1],'windows':windows}
ax.set_xlabel('Шаг RL');ax.set_ylabel('Среднее число токенов в ответе')
ax.set_xlim(0,525);ax.set_ylim(350,1600);ax.grid(axis='y');ax.set_axisbelow(True)
ax.legend(frameon=False,loc='upper left')
fig.text(.09,.076,'Тонкие линии — среднее по батчу; толстые — среднее за 10 последовательных шагов.',fontsize=10,color='#64748b')
fig.text(.09,.043,'Без prompt и padding; включены все ветки, summary и служебные теги. Шаги разных batch не равны по объёму данных.',fontsize=9,color='#64748b')
fig.subplots_adjust(left=.09,right=.96,top=.81,bottom=.19)
for ext in ['png','svg']:fig.savefig(p/f'response-length.{ext}',dpi=160,facecolor='white')
(p/'response-length-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
