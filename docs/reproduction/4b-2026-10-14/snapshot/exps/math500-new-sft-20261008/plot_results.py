"""Reproduce figures from the 500 matched evaluation rows per checkpoint."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
NAMES = ['gsm_infinite_ep5', 'sft_messages_ep5', 'mixed_ep1']
LABELS = ['GSM-Infinite · ep5', 'sft_messages · ep5', 'Mixed · ep1']
SHORT = ['GSM-Infinite', 'sft_messages', 'Mixed']
COLORS = ['#2478BB', '#D77B24', '#318E72']
summary = json.loads((ROOT / 'summary.json').read_text())
assert summary['complete']
S = [summary['models'][n] for n in NAMES]
R = [sorted([json.loads(x) for x in (ROOT/'runs'/n/'trace-statistics.jsonl').read_text().splitlines()], key=lambda x:x['index']) for n in NAMES]
for s, rows in zip(S, R):
    assert len(rows) == 500 and [r['index'] for r in rows] == list(range(500))
    assert sum(r['correct'] for r in rows) == s['correct']
    assert sum(r['forks'] > 0 for r in rows) / 500 == s['parallel_ratio']

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':14,
    'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,
    'axes.edgecolor':'#BBC4CE','axes.labelcolor':'#334155','text.color':'#172B46',
    'xtick.color':'#475569','ytick.color':'#475569','figure.facecolor':'#F7F9FC',
    'axes.facecolor':'#FFFFFF','grid.color':'#E3E9F0','grid.linewidth':0.7,
    'savefig.facecolor':'#F7F9FC'})

def save(fig, name):
    fig.savefig(OUT/f'{name}.png', dpi=170)
    fig.savefig(OUT/f'{name}.pdf')
    plt.close(fig)

fig, ax = plt.subplots(1,2,figsize=(13,5.3))
fig.subplots_adjust(left=.065,right=.975,bottom=.22,top=.76,wspace=.3)
fig.suptitle('MATH-500: точность и использование форков',x=.065,y=.97,ha='left',fontsize=20,weight='bold')
fig.text(.065,.88,'Qwen3-0.6B-Base + Unseen SFT • 500 задач × 1 ответ • Math-Verify 0.8.0',fontsize=11)
x=np.arange(3)
acc=np.array([s['accuracy']*100 for s in S])
err=np.array([[a-s['ci95'][0]*100,s['ci95'][1]*100-a] for a,s in zip(acc,S)]).T
ax[0].bar(x,acc,color=COLORS,width=.58,zorder=3)
ax[0].errorbar(x,acc,yerr=err,fmt='none',ecolor='#172B46',capsize=5,lw=1.6,zorder=4)
for i,(v,s) in enumerate(zip(acc,S)):
    ax[0].text(i,s['ci95'][1]*100+.8,f'{v:.1f}%  ({s["correct"]}/500)',ha='center',weight='bold',fontsize=11)
ax[0].set(title='Точность · 95% Wilson CI',ylim=(0,24),xticks=x,xticklabels=SHORT,ylabel='Верных ответов, %')
ax[0].grid(axis='y',zorder=0)
stack=np.array([[sum(r['forks']==0 for r in rows),sum(r['forks']==1 for r in rows),sum(r['forks']>=2 for r in rows)] for rows in R])/5
left=np.zeros(3)
for j,(color,label) in enumerate(zip(['#CED7E2','#477EAC','#E59838'],['0 форков','1 форк','≥2 форков'])):
    ax[1].barh(x,stack[:,j],left=left,color=color,label=label,height=.53)
    for i,v in enumerate(stack[:,j]):
        if v>=4:ax[1].text(left[i]+v/2,i,f'{v:g}%',ha='center',va='center',fontsize=9 if v<8 else 11,color='white' if j==1 else '#172B46',weight='bold')
    left+=stack[:,j]
ax[1].set(title='Сколько форков в одном решении',xlim=(0,100),yticks=x,yticklabels=SHORT,xlabel='Доля всех 500 решений, %')
ax[1].invert_yaxis()
ax[1].legend(loc='upper center',bbox_to_anchor=(.5,-.18),ncol=3,frameon=False,fontsize=10)
fig.text(.065,.075,'≥2 форков: GSM 6/500 (1,2%) · sft_messages 0/500 · Mixed 1/500 (0,2%). Максимум: 3 / 1 / 2.',fontsize=10)
fig.text(.065,.027,'Форк исполняет 2 ветки по настройке runtime. Эти результаты не измеряют адаптивную ширину.',fontsize=10,color='#627184')
save(fig,'accuracy_parallelism')

fig,axs=plt.subplots(2,2,figsize=(13,9.5))
fig.subplots_adjust(left=.075,right=.97,bottom=.18,top=.86,hspace=.55,wspace=.30)
fig.suptitle('Что происходит внутри решений',x=.075,y=.965,ha='left',fontsize=20,weight='bold')
fig.legend([plt.Line2D([0],[0],color=c,lw=5) for c in COLORS],LABELS,loc='upper left',bbox_to_anchor=(.07,.925),ncol=3,frameon=False)
a=axs[0,0]
for rows,c,l in zip(R,COLORS,SHORT):
    lengths=np.sort([r['response_tokens'] for r in rows]); a.step(lengths,np.arange(1,501)/5,where='post',color=c,label=l,lw=2)
a.axvline(30720,color='#7C8898',ls='--',lw=1)
a.set(xscale='log',xlim=(10,45000),ylim=(0,101),title='Длина ответа · накопленная доля',xlabel='Токены всего ответа, логарифмическая шкала',ylabel='Решений не длиннее X, %')
a.grid(alpha=.7)
a=axs[0,1]
metrics=['Без извлечённого\nфинального ответа','Достигли лимита\n30 720 токенов','Несбалансированные\nструктурные теги']
for i,(s,c) in enumerate(zip(S,COLORS)):
    values=np.array([s['invalid_final_answers'],s['response_budget_exhausted'],s['unbalanced_tags']])/5
    bars=a.bar(np.arange(3)+(i-1)*.25,values,width=.23,color=c,zorder=3)
    for b,v in zip(bars,values): a.text(b.get_x()+b.get_width()/2,v+.6,f'{v:g}',ha='center',fontsize=9)
a.set(title='Проблемы формата и остановки',xticks=np.arange(3),xticklabels=metrics,ylabel='Доля всех 500 решений, %',ylim=(0,35))
a.tick_params(axis='x',labelsize=9);a.grid(axis='y',zorder=0)
a=axs[1,0]
bottom=np.zeros(3)
for phase,c,label in [('main','#BBCBD9','Основной ход'),('path','#417EAD','Ветки'),('summary','#E2A356','Синхронизация')]:
    values=np.array([s['phase_tokens'][phase]/sum(s['phase_tokens'].values())*100 for s in S])
    a.bar(x,values,bottom=bottom,color=c,label=label,width=.6,zorder=3)
    for i,v in enumerate(values):
        if v>5:a.text(i,bottom[i]+v/2,f'{v:.1f}%',ha='center',va='center',color='white' if phase=='path' else '#172B46',fontsize=10)
    bottom+=values
a.set(title='На что ушли сгенерированные токены',xticks=x,xticklabels=SHORT,ylim=(0,100),ylabel='Доля суммарных токенов, %')
a.legend(loc='upper center',bbox_to_anchor=(.5,-.17),ncol=3,frameon=False,fontsize=9)
a=axs[1,1]
for s,c in zip(S,COLORS):
    a.plot(range(1,6),[s['accuracy_by_level'][str(k)]['accuracy']*100 for k in range(1,6)],color=c,marker='o',lw=2)
a.set(title='Точность по сложности MATH',xticks=range(1,6),xlabel='Уровень задачи (1 → 5)',ylabel='Верных ответов, %',ylim=(0,55))
a.grid(alpha=.7)
fig.text(.075,.046,'Доли токенов взвешены по длине: длинные зацикленные ответы сильно влияют на GSM и sft_messages.',fontsize=10)
fig.text(.075,.018,'Ограничение оценки: vLLM-продолжение не применяет custom Unseen mask/positions к объединённому контексту.',fontsize=10,color='#627184')
save(fig,'trace_diagnostics')

# Paired bootstrap keeps question identities matched across checkpoints.
rng=np.random.default_rng(42)
bootstrap=rng.integers(0,500,size=(10000,500))
comparisons=[]
for i,j in [(0,1),(0,2),(1,2)]:
    d=np.array([int(a['correct'])-int(b['correct']) for a,b in zip(R[i],R[j])])
    comparisons.append(dict(a=NAMES[i],b=NAMES[j],delta_pp=float(d.mean()*100),
        paired_bootstrap_ci95_pp=(np.quantile(d[bootstrap].mean(axis=1),[.025,.975])*100).tolist(),
        a_only_correct=int((d==1).sum()),b_only_correct=int((d==-1).sum())))
derived={'paired_accuracy_comparisons':comparisons,'seed':42,'bootstrap_replicates':10000,
    'models':{n:{'branch_token_share_weighted':s['phase_tokens']['path']/sum(s['phase_tokens'].values()),
        'max_forks':max(r['forks'] for r in rows),'strict_format_parallel_count':sum(r['strict_parallel_format'] for r in rows),
        'budget_reached_correct':sum(r['correct'] and r['response_at_budget'] for r in rows),
        'total_generated_tokens':sum(r['generated_tokens'] for r in rows)} for n,s,rows in zip(NAMES,S,R)}}
(ROOT/'derived-statistics.json').write_text(json.dumps(derived,indent=2)+'\n')
print(json.dumps(derived,indent=2))
