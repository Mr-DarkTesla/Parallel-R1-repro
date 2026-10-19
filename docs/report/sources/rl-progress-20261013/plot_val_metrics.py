from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
p=Path(__file__).resolve().parent;points=json.loads((p/'val32-series.json').read_text())['points']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#9ba7b8','axes.labelcolor':'#27364b','xtick.color':'#27364b','ytick.color':'#27364b'})
fig,axes=plt.subplots(3,1,figsize=(10,9),dpi=170,sharex=True)
fig.patch.set_facecolor('white');old=[x for x in points if x['step']<=50];new=[x for x in points if x['step']>50]
settings=[('accuracy','Accuracy: правильные ответы / все 32 задачи',100,lambda x:f"{100*x['accuracy']:.1f}%\n{x['correct']}/32"),('forwards_valid','Actual generation forwards / задачу с правильным форматом',1,lambda x:f"{x['forwards_valid']:.0f}\nn={x['format_valid']}"),('width_valid','Средняя ширина исполненного форка · правильный формат',1,lambda x:f"{x['width_valid']:.2f}")]
for ax,(key,title,factor,label) in zip(axes,settings):
 for group,color,name in [(old,'#7a8799','0–50: HF FP32'),(new,'#2463cc','100–300: vLLM BF16')]:
  ax.plot([r['step'] for r in group],[r[key]*factor for r in group],color=color,marker='o',markersize=6,lw=2,label=name)
 ax.axvspan(50,100,color='#eef1f5',zorder=0);ax.grid(axis='y',color='#e8edf3',lw=.8);ax.set_axisbelow(True);ax.set_title(title,loc='left',fontweight='bold',fontsize=11,pad=13)
 for r in points:
  ax.annotate(label(r).replace('.',','),(r['step'],r[key]*factor),xytext=(0,8),textcoords='offset points',ha='center',va='bottom',fontsize=9,color='#27364b')
 ax.set_xlim(-12,max(r['step'] for r in points)+15)
axes[0].set_ylim(0,110);axes[0].set_yticks(range(0,101,25));axes[0].yaxis.set_major_formatter(PercentFormatter(100));axes[0].axhline(50,color='#acb5c2',ls=':',lw=1)
axes[1].set_ylim(0,1100);axes[1].set_yticks([0,250,500,750,1000])
axes[2].set_ylim(1,8);axes[2].set_yticks([2,4,6,8]);axes[2].set_xticks([r['step'] for r in points]);axes[2].set_xlabel('Логический шаг RL')
axes[0].legend(loc='lower right',frameon=False,fontsize=9)
fig.suptitle('Clean val32 · accuracy, actual forwards и ширина',x=.095,ha='left',fontweight='bold',fontsize=15,y=.98)
fig.text(.095,.025,'F и ширина: только правильный формат; ширина усреднена по исполненным форкам.\nF — физические generation model.forward, без learner replay/backward. После шага 50: другой backend/precision, новый Adam.\nТе же 32 задачи и фиксированный seed; 1 ответ/задачу. Это малая validation, не MATH500.',fontsize=9,color='#5a687a')
fig.subplots_adjust(left=.095,right=.98,top=.91,bottom=.12,hspace=.40)
fig.savefig(p/'val32-metrics.png',bbox_inches='tight');fig.savefig(p/'val32-metrics.svg',bbox_inches='tight')
with (p/'val32-metrics.csv').open('w',newline='') as f:
 keys=[k for k in points[0] if k!='source'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:r[k] for k in keys} for r in points)
print(p/'val32-metrics.png')
