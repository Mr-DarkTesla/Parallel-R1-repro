"""Export verified per-task statistics and publication-ready static distributions."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import os

P = Path.cwd()
B = P / 'work/experiments/base-format-20261010'
E = B / 'evaluations/base-no-think-unconstrained-128'
N = P / 'work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128'
OUT = B / 'statistics'
OUT.mkdir(exist_ok=True)
os.environ['MPLCONFIGDIR'] = str(P / 't/base-statistics-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def rows(p):
    return [json.loads(line) for line in p.open()]

def describe(values):
    a = np.asarray(values, dtype=float)
    if not len(a):
        return dict(n=0, mean=None, median=None, p95=None, min=None, max=None)
    return dict(n=int(len(a)), sum=float(a.sum()), mean=float(a.mean()), median=float(np.median(a)),
                p25=float(np.percentile(a,25)), p75=float(np.percentile(a,75)),
                p90=float(np.percentile(a,90)), p95=float(np.percentile(a,95)),
                min=float(a.min()), max=float(a.max()))

scored = rows(E / 'scores.jsonl')
native = rows(N / 'scores.jsonl')
assert len(scored) == len(native) == 128
assert {r['id'] for r in scored} == {r['id'] for r in native}
compact = []
branches = []
widths = []
phase_tokens = collections.Counter()
phase_calls = collections.Counter()
for r in sorted(scored, key=lambda x:x['sample_index']):
    groups = []
    current = 0
    for call in r['trace']['policy_calls']:
        phase_tokens[call['phase']] += len(call['generated_ids'])
        phase_calls[call['phase']] += 1
        if call['phase'] == 'path':
            current += 1
            branches.append(dict(task_id=r['id'], dataset=r['dataset'], correct=r['grade']['correct'],
                                 sampled_tokens=len(call['generated_ids'])))
        elif current:
            groups.append(current)
            current = 0
    if current:
        groups.append(current)
    assert len(groups) == r['stats']['forks']
    assert groups == r['cost']['widths']
    widths.extend(groups)
    c = r['cost']
    assert r['trace']['forced_think_prefix_tokens'] == 0
    compact.append(dict(id=r['id'], dataset=r['dataset'], correct=bool(r['grade']['correct']),
        format_valid=bool(r['format_valid']), parallel_valid=bool(r['parallel_protocol_valid']),
        fork_rounds=len(groups), widths=groups, critical_depth=c['F'], sampled_tokens=c['T_sampled'],
        forced_tokens=c['T_forced'], assembled_tokens=c['T_assembled'], generation_calls=c['generation_calls'],
        path_calls=sum(groups), elapsed_seconds=c['wall_seconds'], truncated=bool(c['truncated']),
        invalid_width=bool(r['stats']['invalid_width']), logical_work_over_depth=c['T_sampled']/c['F']))
assert len(widths)==125 and sum(widths)==len(branches)==299
assert sum(r['correct'] for r in compact)==84
fields=['fork_rounds','critical_depth','sampled_tokens','forced_tokens','assembled_tokens',
        'generation_calls','path_calls','elapsed_seconds','logical_work_over_depth']
stats = dict(verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), n=128,
    user_accepts_current_accuracy_tradeoff=True, original_baseline=dict(correct=98,n=128,accuracy=98/128),
    accuracy=dict(correct=84,n=128,fraction=84/128,delta_pp=(84-98)/128*100),
    fork_coverage=dict(tasks=120,n=128,fraction=120/128),
    basic_format=dict(valid=126,n=128,fraction=126/128),
    canonical_parallel=dict(valid=120,n=128,fraction=120/128),
    correct_and_parallel=dict(count=78,n=128,fraction=78/128,among_forked=78/120),
    rounds_histogram=dict(sorted(collections.Counter(r['fork_rounds'] for r in compact).items())),
    width_histogram=dict(sorted(collections.Counter(widths).items())), width=describe(widths),
    branch_sampled_tokens=describe([r['sampled_tokens'] for r in branches]),
    metrics={key:describe([r[key] for r in compact]) for key in fields},
    by_correctness={str(correct):dict(n=sum(r['correct']==correct for r in compact),
      metrics={key:describe([r[key] for r in compact if r['correct']==correct]) for key in fields},
      widths=describe([w for r in compact if r['correct']==correct for w in r['widths']])) for correct in [True,False]},
    by_dataset={d:dict(n=64,correct=sum(r['correct'] for r in compact if r['dataset']==d),
      fork_tasks=sum(r['fork_rounds']>0 for r in compact if r['dataset']==d),
      basic_valid=sum(r['format_valid'] for r in compact if r['dataset']==d),
      metrics={key:describe([r[key] for r in compact if r['dataset']==d]) for key in fields},
      widths=describe([w for r in compact if r['dataset']==d for w in r['widths']])) for d in ['gsm','math']},
    native_tokens={key:describe([r['cost'][key] for r in native]) for key in ['F','T_sampled','T_forced','T_assembled']},
    token_phases={phase:dict(tokens=int(value),fraction=value/sum(phase_tokens.values()),calls=phase_calls[phase])
                  for phase,value in phase_tokens.items()},
    invalid_width_tasks=sum(r['invalid_width'] for r in compact), truncations=sum(r['truncated'] for r in compact),
    definitions=dict(width='Executed sibling path calls per actual fork round; 125 rounds.',
      rounds='Actual fork rounds per task; zero included.',
      critical_depth='F: logical sequential sampled-token critical path, not GPU forwards or measured parallel time.',
      sampled_tokens='T: all retained sampled output tokens across main, width, paths and summary calls.',
      forced_tokens='Runtime-injected Path headers/IDs and synchronization bridges; no forced think, Plan, opener or width.',
      elapsed_seconds='Generation elapsed per task, excluding engine startup; HF executes path calls serially.',
      logical_work_over_depth='T/F: logical cost ratio, not measured speedup.',
      native_comparison='Same fixed128 questions; different model/template/backend. Token counts are descriptive, not a causal SFT or latency comparison.'),
    protocol=dict(model='Qwen3-4B-Base full SFT126steps, no think',seed='42+sample_index',temperature=.6,top_p=.95,top_k=20,
      response_cap=4096,path_cap=2048,constrained_decoding=False,backend='hf_structured_serial_backend',
      source_sha256=hashlib.sha256((E/'scores.jsonl').read_bytes()).hexdigest(),
      baseline_source_sha256=hashlib.sha256((N/'scores.jsonl').read_bytes()).hexdigest()))
(OUT/'statistics.json').write_text(json.dumps(stats,indent=2,ensure_ascii=False)+'\n')
(OUT/'per-task.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in compact))
(OUT/'per-path.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in branches))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
    'axes.spines.right':False,'axes.titleweight':'bold','figure.facecolor':'#f8fafc',
    'axes.facecolor':'white','axes.labelcolor':'#334155','text.color':'#0f172a',
    'xtick.color':'#475569','ytick.color':'#475569','svg.fonttype':'none'})
good='#0284c7'; bad='#ea580c'; teal='#0f766e'; grey='#64748b'

def save(fig,name):
    fig.savefig(OUT/(name+'.png'),dpi=170,facecolor=fig.get_facecolor())
    fig.savefig(OUT/(name+'.svg'),facecolor=fig.get_facecolor())
    plt.close(fig)

fig, ax = plt.subplots(2,3,figsize=(15,9.5))
fig.subplots_adjust(top=.84,bottom=.09,hspace=.5,wspace=.28)
fig.suptitle('Qwen3-4B-Base после полного SFT · 128 задач',fontsize=19,y=.965,fontweight='bold')
fig.text(.5,.914,'Accuracy 65.63%  |  форки в 93.75% задач  |  формат 98.44%  |  средняя ширина 2.392',ha='center',fontsize=12)
count=collections.Counter(widths);a=ax[0,0];a.bar(list(count),list(count.values()),color=teal,width=.66)
for x,y in count.items():a.text(x,y+1,str(y),ha='center')
a.set(title='Ширина реально выполненных форков',xlabel='Число ветвей',ylabel='Раундов (всего 125)',xticks=range(2,7));a.set_ylim(0,max(count.values())*1.18)
count=collections.Counter(r['fork_rounds'] for r in compact);a=ax[0,1];a.bar(list(count),list(count.values()),color=good,width=.66)
for x,y in count.items():a.text(x,y+1,str(y),ha='center')
a.set(title='Число параллельных раундов',xlabel='Раундов на задачу',ylabel='Задач',xticks=range(4));a.set_ylim(0,max(count.values())*1.18)
for a,key,title,xlabel in [(ax[0,2],'critical_depth','Глубина критического пути F','Логических токенов по критическому пути'),
                          (ax[1,0],'sampled_tokens','Все сгенерированные токены T','Сумма токенов всех вызовов')]:
    bins=np.histogram_bin_edges([r[key] for r in compact],bins=14)
    a.hist([[r[key] for r in compact if r['correct']],[r[key] for r in compact if not r['correct']]],
           bins=bins,stacked=True,color=[good,bad],label=['Правильно (84)','Ошибка (44)'],edgecolor='white',linewidth=.6)
    a.set(title=title,xlabel=xlabel,ylabel='Задач');a.legend(frameon=False,fontsize=9)
a=ax[1,1]
for correct,color,label in [(True,good,'Правильно'),(False,bad,'Ошибка')]:
    q=[r for r in compact if r['correct']==correct]
    a.scatter([r['critical_depth'] for r in q],[r['sampled_tokens'] for r in q],c=color,s=23,alpha=.75,label=label)
limit=max(r['sampled_tokens'] for r in compact)*1.06;a.plot([0,limit],[0,limit],color=grey,lw=1,ls='--',label='T = F')
a.set(title='Работа T и критический путь F',xlabel='Глубина F',ylabel='Сумма сгенерированных токенов T',xlim=(0,limit),ylim=(0,limit));a.legend(frameon=False,fontsize=9)
a=ax[1,2];labels=['Правильный + parallel','Правильный ответ','Валидный parallel','Правильный формат'];vals=[78,84,120,126]
a.barh(labels,vals,color=[good,good,teal,teal],height=.6)
for y,v in enumerate(vals):
    a.text(3,y,labels[y],va='center',fontsize=9,color='white',fontweight='bold')
    a.text(v+1,y,f'{v}/128 · {v/128:.1%}',va='center',fontsize=9)
a.set_yticks([])
a.set(title='Качество ответа и протокола',xlabel='Задач',xlim=(0,155));a.grid(axis='x',alpha=.15);a.set_axisbelow(True)
fig.text(.02,.025,'F — логическая глубина, не измеренное ускорение. Parallel и ширину выбирает модель; Path-заголовки вставляет runtime.',fontsize=9,color=grey)
save(fig,'base-distributions')

fig,ax=plt.subplots(2,2,figsize=(12,9))
fig.subplots_adjust(top=.86,bottom=.10,hspace=.46,wspace=.28)
fig.suptitle('Токены, длина ветвей и логическая параллельность',fontsize=17,y=.965,fontweight='bold')
fig.text(.5,.918,'Один и тот же набор 128 задач; Base и исходный Instruct используют разные режимы',ha='center',fontsize=11)
for a,key,title in [(ax[0,0],'T_sampled','Сгенерированные токены'),(ax[0,1],'F','Логическая глубина')]:
    x=[r['cost'][key] for r in native]; y=[r['cost'][key] for r in scored]
    bins=np.linspace(0,max(x+y),17)
    a.hist(x,bins=bins,color='#94a3b8',alpha=.6,label=f'Исходный Instruct · среднее {np.mean(x):.0f}')
    a.hist(y,bins=bins,color=good,alpha=.65,label=f'Base SFT · среднее {np.mean(y):.0f}')
    a.set(title=title,xlabel='Токенов',ylabel='Задач');a.legend(frameon=False,fontsize=9)
a=ax[1,0];a.hist([r['sampled_tokens'] for r in branches],bins=20,color=teal,edgecolor='white')
a.set(title='Длина отдельной ветви',xlabel='Сгенерированных токенов в Path',ylabel='Ветвей (всего 299)')
a=ax[1,1];a.hist([r['logical_work_over_depth'] for r in compact],bins=16,color=good,edgecolor='white')
a.set(title='Отношение работы к критическому пути',xlabel='T / F · логическая модель стоимости',ylabel='Задач')
fig.text(.02,.027,'HF runtime выполняет ветви последовательно. T/F и сравнение токенов не являются измерением GPU speedup.',fontsize=9,color=grey)
save(fig,'token-and-path-distributions')
print(json.dumps(dict(output=str(OUT),width=stats['width'],rounds=stats['rounds_histogram'],
    metrics=stats['metrics'],branch_tokens=stats['branch_sampled_tokens'],native=stats['native_tokens']),ensure_ascii=False))
