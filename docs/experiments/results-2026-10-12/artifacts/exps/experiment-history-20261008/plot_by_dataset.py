import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

R=Path(__file__).resolve().parent;EXPS=R.parent
old=EXPS/'gsm-unseen-two-rewards-20261008'
hist=json.loads((old/'monitoring-20261008-0839-msk.json').read_text())
oldtr=json.loads((old/'reward-analysis.json').read_text())['training']
new=json.loads((EXPS/'gsm-unseen-split-rewards-400-20261008/combined-latest.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def style(ax,title,ylabel):
    ax.set_title(title,fontsize=12);ax.set_xlabel('Шаг обучения');ax.set_ylabel(ylabel);ax.grid(alpha=.16)
def smooth(ax,rows,key,color,label=None,factor=1):
    rows=[r for r in rows if 'training/global_step' in r and key in r]
    if not rows:return
    x=np.array([r['training/global_step'] for r in rows]);y=np.array([r[key]*factor for r in rows])
    ax.plot(x,y,color=color,alpha=.13,lw=.65)
    n=min(20,len(y));ax.plot(x[n-1:],np.convolve(y,np.ones(n)/n,mode='valid'),color=color,lw=2,label=label)

recipes=[('S2 · 800 шагов','#3f65bf',hist['stages']['s2']['validation'],oldtr['s2']),
 ('Штраф всем · 800 шагов','#d15f4c',hist['stages']['depth']['validation'],oldtr['depth']),
 ('Штраф правильным, раздельный A · 400 шагов','#18845c',new['stages']['gated_depth']['validation'],new['stages']['gated_depth']['training_series'])]
gain=new['stages']['parallel_gain']
if gain['training_series']:
    recipes.append((f"Бонус за параллельность · {gain['metric_steps']}/400",'#944fbd',gain['validation'],gain['training_series']))

fig,axs=plt.subplots(2,3,figsize=(17,8),layout='constrained')
for name,color,vals,tr in recipes:
    for ax,source in [(axs[0,0],'gsm_infinite_heldout'),(axs[0,1],'APO_MATH300')]:
        ax.plot([v['step'] for v in vals],[100*v['sources'][source]['acc'] for v in vals],'-o',color=color,lw=2,ms=3)
    for ax,key in [(axs[0,2],'response_length/mean'),(axs[1,0],'parallel/critical_depth_mean'),(axs[1,1],'parallel/ratio'),(axs[1,2],'parallel/forks_mean')]:
        smooth(ax,tr,key,color,factor=100 if key=='parallel/ratio' else 1)
titles=['GSM: accuracy на 256 отложенных задачах','MATH: accuracy на 316 отложенных задачах','Длина ответа при обучении',
        'Критическая глубина при обучении','Ответы с параллельным блоком','Среднее число параллельных блоков']
units=['%','%','Токены','Шаги генерации','%','Блоков на ответ']
for ax,title,unit in zip(axs.flat,titles,units):
    style(ax,title,unit);ax.set_xlim(0,810);ax.set_ylim(bottom=0);ax.axvline(400,color='#999999',ls=':',lw=.8,alpha=.6)
axs[0,0].set_ylim(0,100);axs[0,1].set_ylim(0,55);axs[1,1].set_ylim(0,103)
handles=[Line2D([0],[0],color=c,lw=3,label=n) for n,c,_,_ in recipes]
if not gain['training_series']:handles.append(Line2D([0],[0],color='#944fbd',ls=':',lw=2,label='Бонус за параллельность: инициализация, кривой ещё нет'))
fig.legend(handles=handles,loc='outside lower center',ncol=2,frameon=False,fontsize=10)
fig.suptitle('GSM-Infinite: все основные RL-эксперименты с исходного Unseen-SFT\nПолные кривые каждого запуска; пунктир — 400 шагов. Train сглажен за 20 шагов; validation без сглаживания.',fontsize=14)
fig.savefig(R/'gsm-all-experiments-1156.png',dpi=170);fig.savefig(R/'gsm-all-experiments-1156.svg');plt.close(fig)

d=json.loads((EXPS/'rl-unseen-s2-bs32-500-20261007/curves.json').read_text())
first=[m for m in d['rl-unseen-s2-bs32-20261007']['training'] if m.get('training/global_step',9999)<=30]
later=[m for m in d['rl-unseen-s2-bs32-500-20261007']['training'] if 'training/global_step' in m]
rows=first+later
assert [int(m['training/global_step']) for m in rows]==list(range(1,501))
valkey='val-core/APO_MATH300/acc/mean@1'
vals=[m for m in rows if valkey in m]
fig,axs=plt.subplots(2,3,figsize=(17,8),layout='constrained');c='#3f65bf'
axs[0,0].plot([m['training/global_step'] for m in vals],[100*m[valkey] for m in vals],'-o',color=c,lw=2,ms=4)
axs[0,0].annotate('38,6%',(500,100*vals[-1][valkey]),xytext=(-44,8),textcoords='offset points',color=c)
smooth(axs[0,1],rows,'critic/score/mean',c)
smooth(axs[0,2],rows,'response_length/mean',c)
smooth(axs[1,0],rows,'parallel/ratio',c,factor=100)
smooth(axs[1,1],rows,'parallel/forks_mean',c)
smooth(axs[1,2],rows,'grpo/positive_response_fraction','#18845c','Ответы с положительной наградой',factor=100)
smooth(axs[1,2],rows,'grpo/zero_advantage_group_fraction','#a45aaa','Группы с нулевым advantage',factor=100)
titles=['MATH-316: validation accuracy','Средняя награда S2 при обучении','Длина ответа при обучении',
        'Ответы с параллельным блоком','Среднее число параллельных блоков','Положительная награда и нулевой advantage']
units=['%','Награда','Токены','%','Блоков на ответ','%']
for ax,title,unit in zip(axs.flat,titles,units):
    style(ax,title,unit);ax.set_xlim(0,510);ax.axvline(30,color='#999999',ls=':',lw=.8,alpha=.7)
axs[0,0].set_ylim(0,50);axs[0,2].set_ylim(bottom=0);axs[1,0].set_ylim(0,103);axs[1,1].set_ylim(bottom=0);axs[1,2].set_ylim(0,103)
axs[1,2].legend(frameon=False,fontsize=9,loc='center right')
fig.suptitle('DAPO: S2, batch 32 × 8 ответов, 500 шагов — завершён\nШаги 1–30 + продолжение 31–500; пунктир — resume. Train сглажен за 20 шагов. Глубина тогда не логировалась.',fontsize=14)
fig.savefig(R/'dapo-s2-500.png',dpi=170);fig.savefig(R/'dapo-s2-500.svg');plt.close(fig)
print(json.dumps({'gsm':'gsm-all-experiments-1156.png','dapo':'dapo-s2-500.png','dapo_steps':len(rows),'current_state':new['status']}))
