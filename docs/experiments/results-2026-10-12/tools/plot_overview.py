"""Render report figures exclusively from archived metrics.

Run with Python 3, matplotlib and numpy; no remote access or model execution.
"""
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
records = []


def read(path):
    return json.loads((ART / path).read_text())


def save(fig, name, sources, description, svg=True):
    outputs = []
    for ext in (["png", "svg"] if svg else ["png"]):
        path = FIG / f"{name}.{ext}"
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150, facecolor="white", bbox_inches="tight")
        outputs.append(str(path.relative_to(ROOT)))
    plt.close(fig)
    records.append({"outputs": outputs, "description": description,
                    "sources": [{"path": "artifacts/" + p,
                                 "sha256": hashlib.sha256((ART / p).read_bytes()).hexdigest()}
                                for p in sources]})


def bars(ax, labels, values, color="#2877A0", title="", limit=100):
    ax.barh(labels, values, color=color, height=.65)
    ax.invert_yaxis()
    ax.set_xlim(0, limit)
    ax.set_xlabel("Accuracy, %")
    ax.set_title(title, loc="left", fontweight="bold")
    ax.grid(axis="x", alpha=.2)
    ax.set_axisbelow(True)
    for i, value in enumerate(values):
        ax.text(value + 1, i, f"{value:.2f}%", va="center", fontsize=9)


def overviews():
    old_path = "exps/branch-review-20261007/summary.json"
    old = read(old_path)
    labels, values = [], []
    for key, val in old.items():
        if isinstance(val, dict) and "math" in val:
            labels.append(key.replace(" · ", "\n"))
            values.append(100 * val["math"])
    gsm_path = "exps/gsm-unseen-two-rewards-20261008/report.json"
    split_path = "exps/gsm-unseen-split-rewards-400-20261008/completed-snapshot-20261008.json"
    gsm, split = read(gsm_path), read(split_path)
    names = ["S2 / 800 steps", "Unconditional depth / 800", "Gated depth / 400", "Parallel bonus / 400"]
    entries = [gsm["s2"]["validation"], gsm["depth"]["validation"],
               split["stages"]["gated_depth"]["final_verification"]["validation"],
               split["stages"]["parallel_gain"]["final_verification"]["validation"]]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), layout="constrained")
    bars(axes[0], labels, values, title="DAPO training — MATH-316")
    bars(axes[1], names, [100 * e["APO_MATH300"]["acc"] for e in entries],
         color="#AD673D", title="GSM-Infinite training — MATH-316")
    fig.suptitle("Qwen3-0.6B legacy RL: final saved observations\nDifferent batches, rewards and training budgets; descriptive comparison", fontsize=13)
    save(fig, "qwen06b-legacy-rl", [old_path, gsm_path, split_path],
         "Final MATH316 validation; legacy runtime, unequal budgets. Full GSM curves remain in the archived figures.")

    night_path = "work/experiments/night-20261010/reports/final-math500-comparison.json"
    night = read(night_path)["results"]
    names = ["New SFT, 3000 examples", "Old mixed SFT, 5145 examples", "RL corrected75", "RL MATH split40", "RL MATH accuracy80", "RL MATH accuracy40"]
    keys = ["new-sft-math500", "old-mixed-sft-commonbudget-math500", "final-sirius-math500", "final-tmp2-math500", "final-tmp3-math500", "secondary-mathaccuracy40-math500"]
    fig, ax = plt.subplots(figsize=(11, 5), layout="constrained")
    y = np.arange(len(keys))
    for shift, field, label, color in [(-.18, "correct", "Answer correctness", "#2877A0"), (.18, "correct_and_parallel_valid", "Correct + valid executed parallel", "#AD673D")]:
        vals = [100 * night[k][field] / night[k]["completed"] for k in keys]
        ax.barh(y + shift, vals, .34, label=label, color=color)
        for i, v in enumerate(vals): ax.text(v + .3, i + shift, f"{v:.1f}", va="center", fontsize=9)
    ax.set_yticks(y, names); ax.invert_yaxis(); ax.set_xlim(0, 32)
    ax.set_xlabel("% of all 500 questions"); ax.legend(loc="lower right", fontsize=9)
    ax.set_title("Qwen3-0.6B, October 9–10: MATH-500\n4096 response / 2048 path tokens; one sample per question", loc="left")
    ax.grid(axis="x", alpha=.2); ax.set_axisbelow(True)
    save(fig, "qwen06b-night-math500", [night_path], "Same saved evaluation budget; selected RL checkpoints and unequal training histories. Critical depth is not physical parallel speedup.")

    r1_path = "work/experiments/rl-instruct-20261011/math500-paired-audit/R1-checkpoint-0064.json"
    r2_path = "work/experiments/rl-instruct-20261011/math500-paired-audit/R2-checkpoint-0064.json"
    r50_path = "work/experiments/rl-r2-32gpu-batch32-20261012/evaluation-math500/summary.json"
    r1, r2, r50 = read(r1_path), read(r2_path), read(r50_path)
    labels = ["Full SFT, step42", "R1 step64 / train128", "R2 step64 / train128", "R2 step50 / train1024"]
    acc = [100*r1["baseline"]["accuracy"], 100*r1["candidate"]["accuracy"], 100*r2["candidate"]["accuracy"], 100*r50["correct"]/r50["completed"]]
    valid = [100*r1["baseline"]["parallel_valid"]/500, 100*r1["candidate"]["parallel_valid"]/500, 100*r2["candidate"]["parallel_valid"]/500, 100*r50["format_and_fork_count_all"]/500]
    fig, axes = plt.subplots(1, 2, figsize=(14, 4.5), layout="constrained")
    bars(axes[0], labels, acc, title="Answer correctness")
    bars(axes[1], labels, valid, color="#AD673D", title="Valid format + executed fork")
    axes[1].set_xlabel("% of all 500 questions")
    fig.suptitle("Qwen3-4B: complete MATH-500 evaluations\nFP32, fullwidth8, 4096 response / 768 path tokens; training datasets and histories differ", fontsize=13)
    save(fig, "qwen4b-math500", [r1_path, r2_path, r50_path], "All500 denominator. The step50 point is a different training campaign and is not a paired training ablation.")

    paper_path = "work/experiments/paperbench-32k-20261012/attempt2-main-thread/result.json"
    paper = read(paper_path)
    keys = ["AIME2024", "AIME2025", "AIME2026", "AMC2023"]
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    x = np.arange(4)
    for shift, key, label, color in [(-.19,"rl50","RL50 FP32: keep77 + rerun53", "#2877A0"),(.19,"native","Original Instruct BF16 vLLM", "#AD673D")]:
        values = [100*paper[key]["by_dataset"][k]["accuracy"] for k in keys]
        ax.bar(x+shift, values, .36, label=label, color=color)
        for i,v in enumerate(values):
            d=paper[key]["by_dataset"][keys[i]]
            ax.text(i+shift,v+1,f"{d['correct']}/{d['n']}\n{v:.1f}%",ha="center",fontsize=9)
    ax.set_xticks(x,keys); ax.set_ylim(0,106); ax.set_ylabel("Accuracy, %")
    ax.set_title("Qwen3-4B: competition benchmarks, 32k response limit\nOne sample/question. Runtime/precision differ; RL retains 77 finished 4k traces.")
    ax.legend(loc="upper left",fontsize=9);ax.grid(axis="y",alpha=.2);ax.set_axisbelow(True)
    save(fig,"qwen4b-paperbench32k",[paper_path],"RL hybrid protocol: 77 completed4k traces plus rerun53 at32k; native130 fresh BF16 vLLM. No exact-compute comparison.")


def finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def normalized(row):
    step = row.get("step", row.get("training/global_step"))
    if "ranks" in row:
        ranks = row["ranks"]
        if not ranks: return None
        vals = {"step": step}
        for key, label, fn in [("loss","rank_mean_loss",np.mean),("grad_norm","rank_max_grad_norm",max),("seconds","max_rank_local_seconds",max)]:
            numbers = [r[key] for r in ranks if finite(r.get(key))]
            if numbers: vals[label] = float(fn(numbers))
        total = sum(r.get("group", 0) for r in ranks)
        if total and all(finite(r.get("correct")) for r in ranks):
            vals["training_accuracy_pct"] = 100*sum(r["correct"] for r in ranks)/total
        return vals
    d = row.get("metrics", row)
    vals = {"step": step if step is not None else d.get("training/global_step")}
    groups = {
        "loss": ["loss", "actor/pg_loss"],
        "grad_norm": ["grad_norm", "row_grad_norm", "actor/grad_norm"],
        "step_seconds": ["timing_s/step"],
        "training_accuracy_pct": ["night/accuracy", "reward/accuracy_mean", "critic/score/mean"],
        "learning_rate": ["lr", "actor/lr"],
        "row_update_l2": ["row_update_l2", "transformer_update_l2"],
    }
    for label, keys in groups.items():
        for k in keys:
            if finite(d.get(k)):
                vals[label] = d[k]*(100 if label=="training_accuracy_pct" else 1)
                break
    return vals


def training():
    paths = sorted(ART.rglob("*metrics.jsonl"))
    for path in paths:
        if "fixture" in str(path): continue
        raw = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        rows = [normalized(r) for r in raw]
        rows = [r for r in rows if r and finite(r.get("step"))]
        if len(rows)<2: continue
        # A repeated saved step is represented by its final observation.
        rows = sorted({r["step"]: r for r in rows}.values(), key=lambda r:r["step"])
        fields = [k for k in rows[0] if k!="step" and sum(k in r for r in rows)>=2][:4]
        if not fields: continue
        fig, axes=plt.subplots(1,len(fields),figsize=(4*len(fields),3.4),squeeze=False,layout="constrained")
        for ax, field in zip(axes[0],fields):
            rr=[r for r in rows if field in r]
            ax.plot([r["step"] for r in rr],[r[field] for r in rr],".-",lw=1.3,ms=3,color="#2877A0")
            ax.set_xlabel("Saved training step");ax.set_title(field.replace("_"," "),fontsize=10);ax.grid(alpha=.2)
        rel=str(path.relative_to(ART))
        title=rel.removeprefix("work/experiments/")
        # Split long source paths at a directory boundary.
        mid=title.find("/",max(0,len(title)//2-15))
        if len(title)>95 and mid>=0:title=title[:mid]+"\n"+title[mid+1:]
        fig.suptitle(title+"\nRaw saved observations; training/smoke telemetry, not a held-out benchmark",fontsize=10)
        slug=rel.split("/")[2]+"--"+hashlib.sha256(rel.encode()).hexdigest()[:10]
        save(fig,"training/"+slug,[rel],"Raw saved telemetry. Repeated steps use last saved row. Rank loss is an arithmetic rank mean; local seconds is max rank duration, not instrumented global step time.",svg=False)


if __name__=="__main__":
    overviews();training()
    (FIG/"manifest.json").write_text(json.dumps(records,indent=2)+"\n")
    lines=["# Графики\n","Все новые графики воспроизводятся из сохранённых рядом JSON/JSONL. Никакого inference или обучения скрипт не запускает.\n"]
    for rec in records:
        png=rec["outputs"][0]
        lines.append(f"- [{png}]({png}): {rec['description']}")
    lines += ["\n## Исходные исторические графики\n"]
    m=json.loads((ROOT/"manifest.json").read_text())
    for r in m["artifacts"]:
        if r["kind"]=="figure":lines.append(f"- [{r['source']}]({r['artifact']})")
    (ROOT/"FIGURES.md").write_text("\n".join(lines)+"\n")
    print(f"Rendered {len(records)} figure groups")
