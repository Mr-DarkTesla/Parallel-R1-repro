from pathlib import Path
import json, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R=Path('${PROJECT_ROOT}')
P=Path(__file__).resolve().parent
paths={'SFT0':R/'work/experiments/eval-baselines-32k-20261013/full-sft/result.json'}
for step in [50,100,150]:
    paths[f'old{step}']=R/f'work/experiments/eval-intermediates-vllm-rolling-32k-20261013/checkpoint-{step:04}/result.json'
    paths[f'new{step}']=R/f'work/experiments/rl-r4-posteval-20261013/sft/checkpoint-{step:04}/result.json'
data={}
for label,p in paths.items():
    if not p.exists(): continue
    d=json.loads(p.read_text())
    assert d['passed'] and d['completed']==590
    assert all(x['passed'] and x['technical_unknown']==0 for x in d['datasets'])
    if label.startswith('new'):
        C=p.parent/'control'
        assert all(json.loads((C/f'exit-rank-{i}.json').read_text())['returncode']==0 for i in range(16))
    data[label]={'source':str(p),'datasets':d['datasets']}
(P/'data.json').write_text(json.dumps(data,indent=2))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#f7f9fc','axes.facecolor':'white'})
fig,axes=plt.subplots(2,4,figsize=(16,8.6))
colors={'old':'#7855a5','new':'#dd6b35'}
names=['MATH500','AIME2024','AIME2025','AIME2026']
for col,ds in enumerate(names):
    for row,metric in enumerate(['accuracy','actual_forwards_all']):
        ax=axes[row,col]
        base=next(x for x in data['SFT0']['datasets'] if x['dataset']==ds)
        value=lambda x:100*x['accuracy'] if metric=='accuracy' else x[metric]
        b=value(base)
        ax.scatter([0],[b],marker='s',s=55,color='#467b92',zorder=4,label='SFT до RL (старый eval)')
        ax.annotate(f'{b:.1f}'+('%' if row==0 else ''),(0,b),xytext=(7,7),textcoords='offset points',fontsize=9,color='#467b92')
        for lane in ['old','new']:
            pts=[]
            if lane=='old': pts.append((0,b))
            for step in [50,100,150]:
                key=f'{lane}{step}'
                if key in data:
                    x=next(x for x in data[key]['datasets'] if x['dataset']==ds)
                    pts.append((step,value(x)))
            if not pts: continue
            ax.plot([x for x,y in pts],[y for x,y in pts],'-o',color=colors[lane],lw=2,ms=6,label='Старый RL →300' if lane=='old' else 'Новый RL от SFT · DAPO')
            for step,y in pts:
                if step==0:continue
                ax.annotate(f'{y:.1f}'+('%' if row==0 else ''),(step,y),xytext=(0,10 if lane=='old' else -18),textcoords='offset points',ha='center',fontsize=9,color=colors[lane],fontweight='bold')
        ax.set_xlim(-10,165);ax.set_xticks([0,50,100,150]);ax.grid(alpha=.17);ax.set_axisbelow(True)
        if row==0:
            ax.set_title(ds,loc='left',fontweight='bold');ax.set_ylim(0,90 if ds=='MATH500' else 32)
        else:
            ax.set_ylim(0,1650 if ds=='MATH500' else 4900);ax.set_xlabel('Итерация RL')
        if col==0:ax.set_ylabel('Accuracy, %' if row==0 else 'Среднее forwards / задача')
handles,labels=axes[0,0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper left',bbox_to_anchor=(.06,.92),ncol=3,frameon=False)
fig.suptitle('Старый RL и новый DAPO: независимые benchmark оценки',x=.06,ha='left',fontsize=18,fontweight='bold',y=.98)
fig.text(.06,.075,'Все вопросы: MATH500 n=500; каждый AIME n=30. Один ответ на вопрос. Forwards — фактическое участие задачи в generation model.forward.',fontsize=10,color='#526176')
fig.text(.06,.047,'Протоколы НЕ совпадают: SFT0 / старый RL — response32768, path768; новый — response32000, path4000. Все точки BF16.',fontsize=10,color='#526176')
fig.text(.06,.020,'Обучение также различается: прежние данные + strong_width reward против DAPO2000 + correctness/forward penalty. Незавершённые оценки не показаны.',fontsize=9,color='#526176')
fig.subplots_adjust(left=.065,right=.985,top=.82,bottom=.16,wspace=.28,hspace=.25)
for ext in ['png','pdf','svg']:fig.savefig(P/f'comparison.{ext}',dpi=170)
print(json.dumps({'completed_points':list(data),'new_steps':[int(k[3:]) for k in data if k.startswith('new')]}))

for metric,leaf,title in [('accuracy','accuracy','Accuracy на benchmark'),('actual_forwards_all','forwards','Среднее число generation forwards на задачу')]:
    fig,axs=plt.subplots(1,4,figsize=(14,4.8))
    for ax,ds in zip(axs,names):
        value=lambda x:100*x['accuracy'] if metric=='accuracy' else x[metric]
        b=value(next(x for x in data['SFT0']['datasets'] if x['dataset']==ds))
        ax.scatter([0],[b],marker='s',s=45,color='#467b92',zorder=4,label='SFT до RL · старый eval')
        ax.annotate(f'{b:.1f}'+('%' if metric=='accuracy' else ''),(0,b),xytext=(4,7),textcoords='offset points',fontsize=9,color='#467b92')
        for lane in ['old','new']:
            pts=[(0,b)] if lane=='old' else []
            for step in [50,100,150]:
                key=f'{lane}{step}'
                if key in data:pts.append((step,value(next(x for x in data[key]['datasets'] if x['dataset']==ds))))
            ax.plot([x for x,y in pts],[y for x,y in pts],'-o',color=colors[lane],lw=2,ms=5,label='Старый RL →300' if lane=='old' else 'Новый RL от SFT · DAPO')
            for x,y in pts:
                if x==0:continue
                ax.annotate(f'{y:.1f}'+('%' if metric=='accuracy' else ''),(x,y),xytext=(0,8 if lane=='old' else -16),textcoords='offset points',ha='center',fontsize=9,color=colors[lane],fontweight='bold')
        ax.set_title(ds,loc='left',fontweight='bold');ax.set_xlim(-10,165);ax.set_xticks([0,50,100,150]);ax.set_xlabel('Итерация RL');ax.grid(alpha=.17);ax.set_axisbelow(True)
        ax.set_ylim(0,(90 if ds=='MATH500' else 32) if metric=='accuracy' else (1650 if ds=='MATH500' else 4900))
    axs[0].set_ylabel('Accuracy, %' if metric=='accuracy' else 'Forwards / задача')
    h,l=axs[0].get_legend_handles_labels();fig.legend(h,l,loc='upper left',bbox_to_anchor=(.065,.92),ncol=3,frameon=False,fontsize=10)
    fig.suptitle(title,x=.065,ha='left',y=.99,fontsize=17,fontweight='bold')
    fig.text(.065,.065,'Полный eval: MATH500 n=500; AIME n=30 каждый. n=1. Средние по ВСЕМ вопросам, включая неправильные и невалидные.',fontsize=9,color='#526176')
    fig.text(.065,.025,'Разные train-данные/reward. Eval старого: response32768/path768; нового:32000/4000. Все точки BF16; не строго matched comparison.',fontsize=9,color='#526176')
    fig.subplots_adjust(left=.065,right=.985,top=.75,bottom=.21,wspace=.27)
    for ext in ['png','pdf']:fig.savefig(P/f'{leaf}.{ext}',dpi=170)
