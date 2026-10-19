"""Clean presentation plots using the style approved in the referenced chat."""
from pathlib import Path
import csv
import hashlib
import json

import pdfplumber
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.ticker import PercentFormatter

OUT=Path(__file__).resolve().parent
OUR=OUT.parent/'rl300-parallel-position-20261014/data.json'
PAPER=OUT/'source/paper.pdf'
STYLE_SOURCE=OUT.parent/'gsm-legacy-comparison-20261014/plot.py'
PALETTE=dict(blue='#397CC1', background='#ffffff',text='#33332f',grid='#e8e6df')

with pdfplumber.open(PAPER) as pdf:
    page=pdf.pages[10]
    candidates=[c for c in page.curves if c['stroke'] and c['stroking_color']==(1.,0.,0.)]
    assert len(candidates)==1
    curve=candidates[0]
    # Calibrate the vector chart to its grid lines: x 0,250; y .4,.8.
    x0,x250=360.71818,511.82202
    y04,y08=328.86364,224.13417
    points=[((x-x0)/(x250-x0)*250, .4+(y04-y)/(y04-y08)*.4) for x,y in curve['pts']]
    px=np.array([x for x,y in points]);py=np.array([y for x,y in points])
    assert len(points)==119 and np.all(np.diff(px)>0)
    assert np.max(np.abs(px-np.round(px)))<1e-4
    px=np.round(px).astype(int)
    assert px.tolist()==list(range(2,239,2))
    assert np.all((0<py)&(py<1))
paper_points=[dict(iteration=int(x),relative_position=float(y)) for x,y in zip(px,py)]
(OUT/'paper-figure3-points.json').write_text(json.dumps(paper_points,indent=2))
with (OUT/'paper-figure3-points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(paper_points[0]));w.writeheader();w.writerows(paper_points)

ours=json.loads(OUR.read_text())
rows=sorted([r for v in ours['runs'].values() for r in v['rows']],key=lambda r:r['step'])
assert [r['step'] for r in rows]==list(range(1,301))
our_x=np.array([r['step'] for r in rows])
our_y=np.array([r['mean_relative_position'] for r in rows])
our_smooth=[]
for i in range(len(rows)):
    part=rows[max(0,i-9):i+1]
    our_smooth.append(sum(r['blocks']*r['mean_relative_position'] for r in part)/sum(r['blocks'] for r in part))

plt.rcParams.update({
    'font.family':'DejaVu Sans','font.size':11.5,
    'figure.facecolor':PALETTE['background'],'axes.facecolor':PALETTE['background'],
    'text.color':PALETTE['text'],'axes.labelcolor':PALETTE['text'],
    'xtick.color':'#77776e','ytick.color':'#77776e',
    'axes.spines.top':False,'axes.spines.right':False,
    'axes.edgecolor':'#c6c3b9','axes.linewidth':.8,
    'svg.fonttype':'none','pdf.fonttype':42,
})
def style(ax):
    ax.set_xlabel('Итерация RL',labelpad=9)
    ax.set_ylabel('Позиция начала <Parallel>, %',labelpad=10)
    ax.set_xlim(0,300);ax.set_xticks([0,50,100,150,200,250,300])
    ax.set_ylim(0,1);ax.set_yticks([0,.2,.4,.6,.8,1])
    ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
    ax.tick_params(length=0,pad=7)
    ax.grid(axis='y',color=PALETTE['grid'],linewidth=.85);ax.set_axisbelow(True)

def draw(ax,x,y):
    line,=ax.plot(x,y,color=PALETTE['blue'],lw=2.1,linestyle='-',
        solid_capstyle='round',solid_joinstyle='round')
    edge=matplotlib.colors.to_hex(np.array(matplotlib.colors.to_rgb(PALETTE['blue']))*.88)
    line.set_path_effects([pe.Stroke(linewidth=2.6,foreground=edge),pe.Normal()])

for name,x,y in [('ours',our_x,our_smooth),('paper-figure3',px,py)]:
    fig,ax=plt.subplots(figsize=(7.6,4.45))
    fig.subplots_adjust(left=.145,right=.975,top=.965,bottom=.17)
    style(ax);draw(ax,x,y)
    for ext in ['png','pdf','svg']:
        fig.savefig(OUT/f'{name}.{ext}',dpi=220,facecolor='white')
    plt.close(fig)

manifest=dict(
    style_thread='thread://01a139af-0656-72c3-9564-ebbc74514b95?hostId=local',
    style_source=str(STYLE_SOURCE),palette=PALETTE,
    content='axes and ticks only; no titles, captions, legend, annotations, markers or dashed lines',
    axes=dict(x=[0,300],y=[0,1]),
    ours=dict(source=str(OUR),sha256=hashlib.sha256(OUR.read_bytes()).hexdigest(),
        iterations=[1,300],metric='pooled mean of start_token_index / response_ids_length',
        smoothing='trailing 10 completed updates, weighted by number of blocks; shortened prefix window'),
    paper=dict(url='https://arxiv.org/pdf/2509.07980',version='2509.07980v2',page=11,figure=3,
        source_pdf_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),
        method='extract all vertices of red PDF vector path; affine calibration from original grid ticks',
        points=len(px),iterations=[int(px[0]),int(px[-1])],
        calibration=dict(x0=x0,x250=x250,y04=y04,y08=y08),
        smoothing='none; preserve published curve vertices; these are graphical values, not raw author logs'),
)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print(json.dumps(dict(paper_points=len(px),paper_endpoints=[float(py[0]),float(py[-1])],outputs=['ours.png','paper-figure3.png'])))
