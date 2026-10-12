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
new=json.loads((EXPS/'gsm-unseen-split-rewards-400-20261008/completed-snapshot-20261008.json').read_text())
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
    recipes.append(('Бонус за параллельность, раздельный A · 400 шагов','#944fbd',gain['validation'],gain['training_series']))

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
fig.suptitle('GSM-Infinite: все 4 запуска завершены • снимок 8 октября, 14:58 МСК\nПолные кривые каждого запуска; пунктир — 400 шагов. Train сглажен за 20 шагов; validation без сглаживания.',fontsize=14)
fig.savefig(R/'gsm-all-experiments-final.png',dpi=170);fig.savefig(R/'gsm-all-experiments-final.svg');plt.close(fig)

fig, axes = plt.subplots(2, 3, figsize=(17, 8), layout='constrained')
for row, (mode, title) in enumerate([
    ('gated_depth', 'Штраф правильным: R = c − 0,0001 × c × D'),
    ('parallel_gain', 'Бонус: R = c + 0,2 × c × valid_parallel × (1 − D/T)'),
]):
    tr = new['stages'][mode]['training_series']
    assert [int(m['training/global_step']) for m in tr] == list(range(1,401))
    smooth(axes[row,0],tr,'reward/accuracy_mean','#18845c','За правильность')
    smooth(axes[row,0],tr,'reward/total_mean','#3f65bf','Итоговая награда')
    smooth(axes[row,1],tr,'reward/aux_mean','#944fbd','Штраф' if mode=='gated_depth' else 'Бонус')
    smooth(axes[row,2],tr,'advantage/accuracy_abs_mean','#18845c','От правильности')
    smooth(axes[row,2],tr,'advantage/aux_abs_mean','#944fbd','От штрафа / бонуса')
    for col, (heading, unit) in enumerate([
        ('Правильность и итоговая награда','Средняя награда'),
        ('Вклад штрафа / бонуса','Средний вклад в награду'),
        ('Сигнал после раздельного расчёта advantage','Средний |A|'),
    ]):
        ax=axes[row,col]
        style(ax,heading,unit)
        ax.set_xlim(0,405)
        ax.legend(frameon=False,fontsize=9)
    axes[row,0].set_ylim(0,1)
    axes[row,1].set_ylim(-.055,.045)
    axes[row,1].axhline(0,color='#333333',lw=.7)
    axes[row,2].set_yscale('log')
    axes[row,2].set_ylim(.003,1)
    axes[row,0].text(0,1.16,title,transform=axes[row,0].transAxes,fontsize=12,fontweight='bold')
fig.suptitle('Два новых опыта: из чего складывается награда и обучающий сигнал\nОба завершили 400 шагов. Тонкие линии — сырые значения, толстые — среднее за 20 шагов.',fontsize=14)
fig.savefig(R/'reward-components-final.png',dpi=170)
fig.savefig(R/'reward-components-final.svg')
plt.close(fig)
print('Saved final comparison and reward-component charts')
