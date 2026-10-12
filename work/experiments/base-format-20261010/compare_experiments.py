"""Compare every completed 128-question arm without pooling protocols."""
from pathlib import Path
import json
import collections
import os
import datetime

P = Path.cwd()
W = P / 'work/experiments'
B = W / 'base-format-20261010'
OUT = B / 'statistics'
os.environ['MPLCONFIGDIR'] = str(P / 't/base-statistics-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def read(p):return json.loads(p.read_text())
def describe(v):
    a=np.asarray(v,dtype=float)
    return dict(n=len(v),mean=float(a.mean()),median=float(np.median(a)),p95=float(np.percentile(a,95)),max=float(a.max())) if len(a) else dict(n=0,mean=None,median=None,p95=None,max=None)

records=[]
for path in sorted(W.glob('*/evaluations/*/summary.json')):
    s=read(path)
    if s.get('planned')!=128:continue
    scored=[json.loads(l) for l in (path.parent/'scores.jsonl').open()]
    assert len(scored)==s['completed']==128 and sum(r['grade']['correct'] for r in scored)==s['correct']
    assert read(path.parent/'worker-exits.json')==[0]*8
    width=[];rounds=[]
    for r in scored:
        groups=[];current=0
        for c in r.get('trace',{}).get('policy_calls',[]):
            if c['phase']=='path':current+=1
            elif current:groups.append(current);current=0
        if current:groups.append(current)
        assert len(groups)==r.get('stats',{}).get('forks',0)
        width.extend(groups);rounds.append(len(groups))
    records.append(dict(name=path.parent.name,completed=128,correct=s['correct'],accuracy=s['correct']/128,
        fork_tasks=sum(x>0 for x in rounds),fork_fraction=sum(x>0 for x in rounds)/128,
        actual_rounds=len(width),actual_width=describe(width),width_histogram=dict(collections.Counter(width)),
        basic_valid=s['format_valid'],format_fraction=s['format_valid']/128,
        parallel_valid=s['parallel_protocol_valid'],correct_and_parallel=s['correct_and_parallel_valid'],
        by_dataset={k:dict(correct=v['correct'],n=v['completed']) for k,v in s['by_dataset'].items()},
        sampled_tokens=describe([r['cost']['T_sampled'] for r in scored]),critical_depth=describe([r['cost']['F'] for r in scored]),
        format_schema=s['format_schema_version'],backend=s['backend_labels'],model=s['model'],source=str(path)))

training=[]
for label,root in [('LR5e-4',W/'instruct-token-warmup-20261010/runs/production'),
                   ('LR1e-3',W/'instruct-token-warmup-20261010/variants/lr-1e-3/runs/production'),
                   ('LR2e-4',W/'instruct-token-warmup-20261010/variants/lr-2e-4/runs/production'),
                   ('Format x5',W/'format-loss-20261010/runs/production'),
                   ('Base full',B/'runs/production')]:
    r=read(root/'result.json');assert r['state']=='complete'
    v=read(root/'epoch3.json')['val_teacher_forced_loss'] if (root/'epoch3.json').exists() else r['val_loss']
    training.append(dict(label=label,steps=r['steps'],epochs=r['epochs'],val_loss=v,trainable_parameters=r.get('trainable_parameters',4022468096),source=str(root)))
report=dict(verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),fixed_original_native_baseline=98,
            records=records,training=training,
            limits=['Native, old structured, new guard, and no-think Base have different protocols and format schemas.',
                    'Old summary regex widths replaced by actual policy path-call groups.',
                    'No scores pooled across modes; native XML format score is not a native-quality criterion.'])
(OUT/'all-experiments.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
index={r['name']:r for r in records}
names=[('LR1e-3 · старый runtime','lr-1e-3-trained-structured-128'),
       ('LR2e-4 · старый runtime','lr-2e-4-trained-structured-128'),
       ('LR5e-4 · новый guard','baseline-lr-5e-4-constrained-128'),
       ('Format x5 · guard','weighted-format-constrained-128'),
       ('Format x5 + пример · guard','weighted-format-fewshot-128'),
       ('Base full · без think','base-no-think-unconstrained-128')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,
    'figure.facecolor':'#f8fafc','axes.facecolor':'white','svg.fonttype':'none','text.color':'#0f172a'})
fig,axes=plt.subplots(1,3,figsize=(15,5.5),sharey=True)
fig.subplots_adjust(left=.24,right=.98,top=.76,bottom=.17,wspace=.22)
fig.suptitle('Результаты SFT-экспериментов · каждый eval на 128 задачах',fontsize=17,y=.96,fontweight='bold')
fig.text(.5,.865,'Разные режимы показаны отдельно; исходный native baseline остаётся 98/128 = 76.56%',ha='center',fontsize=11)
colors=['#94a3b8']*5+['#0f766e'];y=np.arange(len(names))
for a,key,title in zip(axes,['accuracy','fork_fraction','format_fraction'],['Accuracy','Задачи с реальными форками','Корректный формат']):
    values=[index[name][key]*100 for _,name in names];a.barh(y,values,color=colors,height=.64)
    for iy,v in enumerate(values):a.text(min(v+1,99),iy,f'{v:.1f}%',va='center',fontsize=10)
    a.set(xlim=(0,114),xticks=[0,25,50,75,100],xlabel='%',title=title);a.grid(axis='x',alpha=.15);a.set_axisbelow(True)
axes[0].set_yticks(y,[label for label,_ in names]);axes[0].invert_yaxis();axes[0].axvline(98/128*100,color='#d97706',ls='--',lw=1.4)
fig.text(.02,.035,'Guard исправляет ограничения декодинга. Base обучал все 4.02B весов; остальные SFT меняли 6 строк токенов.',fontsize=10,color='#64748b')
for ext in ['png','svg']:fig.savefig(OUT/('experiment-comparison.'+ext),dpi=170,facecolor=fig.get_facecolor())
print(json.dumps(report,ensure_ascii=False))
