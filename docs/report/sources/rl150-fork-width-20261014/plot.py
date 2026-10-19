import json
from pathlib import Path
from collections import Counter
from statistics import mean
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root = Path('work/experiments/rl-r4-posteval-20261013/sft/checkpoint-0150')
out = Path('work/experiments/rl150-fork-width-20261014')
out.mkdir(exist_ok=True)
result = json.loads((root/'result.json').read_text())
assert result['passed'] and result['completed'] == 590
data = []
examples = []
for dataset, n in [('MATH500',500),('AIME2024',30),('AIME2025',30),('AIME2026',30)]:
    rows = [json.loads(l) for p in sorted((root/'runs'/dataset).glob('rank-*.jsonl')) for l in p.open() if l.strip()]
    raw = [json.loads(l) for p in sorted((root/'runs'/dataset).glob('raw-rank-*.jsonl')) for l in p.open() if l.strip()]
    assert len(rows) == len(raw) == n and len({r['id'] for r in rows}) == n
    assert {r['id'] for r in raw} == {r['id'] for r in rows}
    assert not any(r['technical_unknown'] for r in rows)
    widths = [w for r in rows for w in r['widths']]
    valid = [w for r in rows if r['format_valid'] for w in r['widths']]
    hist = Counter(widths)
    data.append(dict(dataset=dataset, questions=n, questions_with_fork=sum(bool(r['widths']) for r in rows), forks=len(widths), width_all=mean(widths), valid_forks=len(valid), width_valid=mean(valid), histogram=dict(sorted(hist.items()))))
    for r in rows:
        if r['widths'] and len(examples) < 8:
            examples.append({k:r[k] for k in ['dataset','id','problem','output','widths','fork_batch_ledger','format_valid','grade']})
all_widths = [int(w) for d in data for w,count in d['histogram'].items() for _ in range(count)]
summary = dict(checkpoint=150, model_sha256=result['datasets'][0]['model_sha256'], definition='Number of sibling branches per recorded fork, each fork weighted equally; includes wrong and format-invalid answers. No-fork questions do not contribute a zero.', datasets=data, total_forks=len(all_widths), width_all=mean(all_widths), trace_root=str(root))
(out/'data.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(out/'trace-examples.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,4,figsize=(16,4.8))
for ax,d in zip(axs,data):
    xs=list(range(1,9)); ys=[100*d['histogram'].get(x,0)/d['forks'] for x in xs]
    ax.bar(xs,ys,color='#527ac3',width=.75)
    ax.axvline(d['width_all'],color='#df792b',linewidth=2,label=f"Среднее: {d['width_all']:.3f}")
    ax.set_title(d['dataset']+f"\n{d['forks']} форков · {d['questions_with_fork']}/{d['questions']} задач с форком")
    ax.set_xticks(xs); ax.set_xlabel('Число веток в форке');ax.set_ylim(0,100);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);ax.legend(frameon=False,fontsize=10)
axs[0].set_ylabel('Доля всех записанных форков, %')
fig.suptitle('SFT → RL-150 · новая награда · ширина форков на независимом тесте',fontsize=17,y=.98)
fig.text(.055,.055,f"Все 590 задач, включая неверные ответы и ошибки формата. Среднее по {len(all_widths)} форкам: {mean(all_widths):.3f} ветки.",fontsize=11)
fig.text(.055,.015,'Каждый форк имеет одинаковый вес; задачи без форка не добавляют нули. BF16 · response 32000 · path 4000 · context 40960.',fontsize=10,color='#526176')
fig.tight_layout(rect=[0,.12,1,.9])
for suffix in ['png','pdf','svg']:fig.savefig(out/f'fork-width.{suffix}',dpi=180)
print(json.dumps(summary,ensure_ascii=False))
