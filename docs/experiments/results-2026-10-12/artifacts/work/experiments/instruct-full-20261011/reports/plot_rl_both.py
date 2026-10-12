import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
p=Path(__file__).parent;x=json.loads((p/"latest-rl-compact.json").read_text())
fig,axs=plt.subplots(1,3,figsize=(13,4),layout="constrained")
for key,label,color in [("R1","R1: forward cost","#197eaf"),("R2","R2: cost + width / rounds bonus","#b95f24")]:
 rows=x[key]["val"];s=[r["step"] for r in rows]
 for ax,field in zip(axs,["correct","F","width"]):
  ax.plot(s,[100*r[field]/r["completed"] if field=="correct" else r[field] for r in rows],"o-",label=label,color=color)
for ax,title in zip(axs,["Accuracy on clean validation n=32 (%)","Measured model.forward calls / task","Mean completed round width"]):
 ax.set_ylabel(title);ax.set_xlabel("Training iteration");ax.grid(alpha=.2)
axs[0].set_ylim(0,100);axs[0].legend(fontsize=8)
fig.suptitle("Full500 RL early checkpoints: same fixed clean validation 32 / FP32 temperature1\nSelection validation; no RL MATH benchmark result yet",fontsize=12)
fig.savefig(p/"rl-both-progress.png",dpi=170);fig.savefig(p/"rl-both-progress.pdf")
