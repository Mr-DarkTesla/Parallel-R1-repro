from pathlib import Path
import json,csv,statistics,datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R=Path('${PROJECT_ROOT}');P=Path(__file__).resolve().parent
roots={}
for lane,outer in [('sft','rl-r4-dapo2k-sft-16gpu-20261013'),('rl300','rl-r4-dapo2k-rl300-16gpu-scheduled-20261013')]:
    roots[lane]=Path(json.loads((R/'work/experiments'/outer/'cloud-submission.json').read_text())['current_run_root'])
roots['old50']=R/'work/experiments/rl-r2-24gpu-20261012/recovery-20261012-global-parity'
roots['old300']=R/'work/experiments/rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory'
def read(root):
    out=[]
    for l in (root/'production/metrics.jsonl').read_text().splitlines():
        d=json.loads(l);rs=d['ranks'];rewards=[w for r in rs for w in r['rewards']]
        n=len(rewards);correct=sum(r['correct'] for r in rs)
        assert n==sum(r['group'] for r in rs)
        assert correct==sum(w['accuracy_reward']>0 for w in rewards)
        assert len(set(r['rank'] for r in rs))==len(rs)
        all4=all(r['group']==4 for r in rs)
        out.append(dict(step=d['step'],n_responses=n,correct=correct,accuracy=100*correct/n,
            prompt_at_least_one_pct=100*sum(r['correct']>0 for r in rs)/len(rs) if all4 else None,
            prompts=len(rs) if all4 else None,reward=statistics.mean(w['score'] for w in rewards),
            forwards=statistics.mean(w['actual_generation_forward_calls'] for w in rewards),
            positive_update=all(r['optimizer_step'] and r['backbone_update_l2']>0 for r in rs),
            guard_pass=all(r['replay_guard_passed'] for r in rs)))
    return out
data={k:read(v) for k,v in roots.items()}
data['old']=[x for x in data['old50'] if x['step']<=50]+[x for x in data['old300'] if 51<=x['step']<=150]
(P/'data.json').write_text(json.dumps(dict(sources={k:str(v/'production/metrics.jsonl') for k,v in roots.items()},data=data),indent=2))
with (P/'curves.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['lane',*data['sft'][0].keys()]);w.writeheader()
    for lane in ['sft','rl300','old']:
        for row in data[lane]:w.writerow(dict(lane=lane,**row))
def moving(rows,key,window=10):
    return [statistics.mean(r[key] for r in rows[max(0,i-window+1):i+1]) for i in range(len(rows))]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#f7f9fc','axes.facecolor':'white'})
fig,axes=plt.subplots(3,2,figsize=(14,11),sharex='col')
for col,lane in enumerate(['sft','rl300']):
    rows=data[lane];steps=[r['step'] for r in rows];window=10 if lane=='sft' else 3
    for i,key in enumerate(['accuracy','reward','forwards']):
        ax=axes[i,col];raw=[r[key] for r in rows]
        ax.plot(steps,raw,lw=1,color='#de763c',alpha=.25,label='Каждый батч')
        ax.plot(steps,moving(rows,key,window),lw=2.5,color='#d7662e',label=f'Среднее за {window} updates')
        ax.grid(alpha=.17);ax.set_axisbelow(True)
        if key=='accuracy':
            ax.plot(steps,moving(rows,'prompt_at_least_one_pct',window),lw=2,color='#398c7c',ls='--',label='Хотя бы 1 правильный из 4')
            ax.set_ylim(0,105);ax.set_ylabel('Правильных, %')
            if lane=='sft':
                old=data['old'];ax.plot([r['step'] for r in old],moving(old,'accuracy'),color='#8060a9',lw=1.8,label='Старый RL: ответы, среднее10')
            ax.set_title('RL от SFT · 1–150' if lane=='sft' else f'RL от300 · 301–{steps[-1]}',loc='left',fontweight='bold')
        elif key=='reward':ax.set_ylabel('Средний фактический reward');ax.set_ylim(0,1)
        else:ax.set_ylabel('Среднее generation forwards');ax.set_xlabel('Завершённый global update')
        if i==0:ax.legend(frameon=False,fontsize=9,loc='lower left')
        if lane=='sft':ax.set_xlim(1,150)
        else:ax.set_xticks(steps);ax.set_xlim(steps[0]-.3,steps[-1]+.3)
    last=rows[-min(10,len(rows)):];n=sum(r['n_responses'] for r in last);c=sum(r['correct'] for r in last)
    fig.text(.065 if col==0 else .545,.105,f'Последние {len(last)} батчей: {c}/{n} ответов = {100*c/n:.1f}%; reward {statistics.mean(r["reward"] for r in last):.3f}',fontsize=11,fontweight='bold')
fig.suptitle('Что решаем во время RL: correctness, reward и forwards',x=.065,ha='left',y=.98,fontsize=18,fontweight='bold')
fig.text(.065,.943,'Текущие прогоны: 16 train-задач × 4 ответа = 64 ответа/update. Оранжевый — доля правильных ответов; зелёный — хотя бы один из четырёх.',fontsize=10,color='#526176')
fig.text(.065,.075,'Это sampled TRAIN-батчи, НЕ MATH500/AIME. Сложность задач меняется; соседние точки не оценивают качество на фиксированном наборе.',fontsize=10,color='#526176')
fig.text(.065,.050,'Фиолетовая линия — старый RL на другом train-корпусе (96 ответов/update до50, затем64); прямое сравнение процентов ограничено.',fontsize=10,color='#526176')
fig.text(.065,.025,'Reward текущих прогонов: C × [1 − 0.9(1 − exp(−ln9 × F/10000))]. Старый reward strong_width имеет другую шкалу и здесь не смешан.',fontsize=9,color='#526176')
fig.subplots_adjust(left=.065,right=.985,top=.885,bottom=.155,hspace=.22,wspace=.17)
for ext in ['png','pdf']:fig.savefig(P/f'training-curves.{ext}',dpi=170)
summary={}
for lane in ['sft','rl300']:
    rows=data[lane];windows={}
    for tag,part in [('first10',rows[:10]),('last10',rows[-10:]),('all',rows)]:
        n=sum(x['n_responses'] for x in part);c=sum(x['correct'] for x in part)
        windows[tag]=dict(steps=[part[0]['step'],part[-1]['step']],correct=c,n=n,accuracy=100*c/n,reward=statistics.mean(x['reward'] for x in part),forwards=statistics.mean(x['forwards'] for x in part),prompt_at_least_one_pct=statistics.mean(x['prompt_at_least_one_pct'] for x in part))
    summary[lane]=windows
(P/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
