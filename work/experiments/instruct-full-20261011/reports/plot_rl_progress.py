import json,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
p=Path(__file__).parent
source=p/"rl-strong-width-progress-data.json"
x=json.loads(source.read_text());rows=sorted([v for v in x.values() if isinstance(v,dict)],key=lambda r:r["step"])
steps=[r["step"] for r in rows]
fig,axs=plt.subplots(1,3,figsize=(13,4),layout="constrained")
for key,label in [("correct","Accuracy"),("format_valid","Valid format"),("parallel_valid","Canonical parallel")]:axs[0].plot(steps,[100*r[key]/r["completed"] for r in rows],"o-",label=label)
axs[0].set_ylim(0,105);axs[0].set_ylabel("Percent of 32 fixed clean-validation tasks");axs[0].legend(fontsize=8)
axs[1].plot(steps,[np.mean(r["actual_forward_calls"]) for r in rows],"o-",color="#197eaf");axs[1].set_ylabel("Measured model.forward calls / task")
axs[2].plot(steps,[np.mean(r["sampled_tokens"]) for r in rows],"o-",label="Sampled tokens",color="#197eaf");axs[2].set_ylabel("Sampled output tokens / task")
for ax in axs:ax.set_xlabel("R2 full500 training iteration");ax.set_xticks(steps);ax.grid(alpha=.2)
fig.suptitle("Early RL with constant width / round bonus: clean validation n=32\nFP32, temperature 1, top-p 1; separate from matched 128-task benchmark",fontsize=12)
fig.savefig(p/"rl-strong-width-progress.png",dpi=170);fig.savefig(p/"rl-strong-width-progress.pdf")
(p/"rl-progress-plot-manifest.json").write_text(json.dumps({"source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"steps":steps,"validation_count":32,"benchmark":False,"F_semantics":"actual instrumented model.forward calls"},indent=2))
