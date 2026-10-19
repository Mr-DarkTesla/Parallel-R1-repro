from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

P=Path(__file__).resolve().parent
data=json.loads((P/'data.json').read_text())
plt.rcParams.update({
 'font.family':'DejaVu Sans','font.size':14,
 'figure.facecolor':'white','axes.facecolor':'white',
 'text.color':'#33332f','axes.labelcolor':'#33332f',
 'xtick.color':'#77776e','ytick.color':'#77776e',
 'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,
 'axes.edgecolor':'#c6c3b9','axes.linewidth':.8,
 'svg.fonttype':'none','pdf.fonttype':42,
})
fig,ax=plt.subplots(figsize=(11.5,5.8))
x=np.arange(4);width=.28
for offset,key,color,label in [(-.5,'normal','#6D8884','Обычный инференс'),(.5,'random2','#B9674D','Две случайные ветки')]:
 values=[100*r['correct']/r['completed'] for r in data[key]]
 bars=ax.bar(x+offset*width,values,width,color=color,label=label,zorder=3)
 for bar,value in zip(bars,values):
  ax.text(bar.get_x()+bar.get_width()/2,value+1.8,f'{value:.1f}%'.replace('.',','),ha='center',va='bottom',fontsize=13,color='#33332f')
ax.set_xticks(x,['MATH500','AIME 2024','AIME 2025','AIME 2026'])
ax.set_ylim(0,100);ax.set_yticks([0,20,40,60,80,100])
ax.set_ylabel('Accuracy, %',labelpad=14)
ax.set_xlabel('Тестовый набор',labelpad=14)
ax.tick_params(length=0,pad=10)
ax.grid(axis='y',color='#e8e6df',linewidth=.85);ax.set_axisbelow(True)
ax.legend(loc='upper center',bbox_to_anchor=(.5,1.16),ncol=2,frameon=False,fontsize=14,handlelength=1.5,columnspacing=2.0)
fig.subplots_adjust(left=.085,right=.985,top=.85,bottom=.17)
for ext in ['png','pdf','svg']:fig.savefig(P/f'paired-bars-slide.{ext}',dpi=220,facecolor='white')
