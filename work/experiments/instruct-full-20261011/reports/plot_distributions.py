import json, hashlib, csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
p=Path(__file__).parent
raw=json.loads((p/"matched128-distribution-data.json").read_text())
cmp=json.loads((p.parent/"matched-eval128-comparison.json").read_text())
keys=["warmup-lr1e3-guard-structured-128","epoch1-guard-structured-128"]
labels=["Instruct token warmup","Full SFT (old dataset)"]
colors=["#717d96","#197eaf"]
data=[]
for k in keys:
 rows=raw["runs"][k]["rows"]
 details={r["id"]:r for r in cmp["results"][k]["details"]}
 for r in rows:
  g=[g for g in details.get(r["id"], {"groups": []})["groups"] if g["path_calls"]>0 and g["summary_call"]]
  r["rounds"]=len(g);r["widths"]=[g["path_calls"] for g in g]
 data.append(rows)
fig,axs=plt.subplots(2,3,figsize=(15,8.5),layout="constrained")
ax=axs[0,0]; cats=["Accuracy","Valid format","Executed fork","Canonical parallel"]
for i,rows in enumerate(data):
 vals=[100*np.mean([r[f] for r in rows]) for f in ["correct","format_valid","rounds","parallel_valid"]]
 # executed fork rate is boolean, not mean round count
 vals[2]=100*np.mean([r["rounds"]>0 for r in rows])
 bars=ax.bar(np.arange(4)+(i-.5)*.36,vals,.36,label=labels[i],color=colors[i])
 ax.bar_label(bars,fmt="%.1f",fontsize=8)
ax.set_xticks(range(4),cats,rotation=15);ax.set_ylim(0,110);ax.set_ylabel("Percent of 128 tasks");ax.legend(fontsize=8)
ax=axs[0,1]
for i,rows in enumerate(data):
 w=[w for r in rows for w in r["widths"]];counts=[w.count(j) for j in range(2,7)]
 ax.bar(np.arange(2,7)+(i-.5)*.36,np.array(counts)/len(w)*100,.36,color=colors[i],label=f"{labels[i]} (n={len(w)} rounds)")
ax.set_xticks(range(2,7));ax.set_xlabel("Actual completed round width");ax.set_ylabel("Percent of completed rounds");ax.legend(fontsize=7)
ax=axs[0,2]
for i,rows in enumerate(data):
 counts=[sum(r["rounds"]==j for r in rows) for j in range(3)]
 ax.bar(np.arange(3)+(i-.5)*.36,counts,.36,color=colors[i],label=labels[i])
ax.set_xticks(range(3));ax.set_xlabel("Completed fork / merge rounds per task");ax.set_ylabel("Tasks (n=128 per run)")
for ax,field,title in [(axs[1,0],"sampled_tokens","Sampled output tokens"),(axs[1,1],"critical_path_proxy_F","Critical-path F proxy (NOT physical calls)"),(axs[1,2],"wall_seconds","Wall seconds per task")]:
 for i,rows in enumerate(data):
  v=np.sort([r[field] for r in rows]);ax.step(v,np.arange(1,len(v)+1)/len(v),where="post",color=colors[i],label=labels[i]);ax.axvline(np.median(v),color=colors[i],alpha=.3,ls=":")
 ax.set_xlabel(title);ax.set_ylabel("Cumulative fraction of tasks");ax.grid(alpha=.2)
fig.suptitle("Matched guarded evaluation: 64 GSM + 64 MATH tasks per run\nSame prompt / runtime guard, temperature 0.6, top-p 0.95, top-k 20; runtime injects Path headers / bridges",fontsize=13)
fig.savefig(p/"matched128-distributions.png",dpi=170)
fig.savefig(p/"matched128-distributions.pdf")
with (p/"matched128-per-task.csv").open("w") as f:
 fields=["run","id","dataset","correct","format_valid","parallel_valid","rounds","widths","sampled_tokens","critical_path_proxy_F","wall_seconds"]
 writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
 for k,rows in zip(keys,data):
  for r in rows:writer.writerow({"run":k,**r})
manifest={"sources":{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [p/"matched128-distribution-data.json",p.parent/"matched-eval128-comparison.json"]},"benchmark_selection":False,"F_semantics":"critical-path proxy, not instrumented physical model.forward","width_semantics":"completed groups with path_calls>0 and summary_call; conditional denominator 4 vs 127"}
(p/"plot-manifest.json").write_text(json.dumps(manifest,indent=2))
