"""Presentation-style macro benchmark comparison of SFT, RL0..300 and Instruct."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT
SOURCE = OUT / "forwards-accuracy-snapshot.json"
source = json.loads(SOURCE.read_text())
FORK_SOURCE = OUT / "fork-snapshot.json"
fork_source = json.loads(FORK_SOURCE.read_text())
NEW_SOURCE = OUT / "new-reward-snapshot.json"
new_source = json.loads(NEW_SOURCE.read_text())
DATASETS = {"MATH500": 500, "AIME2024": 30, "AIME2025": 30, "AIME2026": 30}
LABELS = ["SFT", "RL50", "RL100", "RL150", "RL200", "RL250", "RL300"]
STEPS = [0, 50, 100, 150, 200, 250, 300]
COLORS = {"RL": "#397CC1", "SFT": "#D7A522", "Instruct": "#B9674D", "NewRL": "#2E8B72"}
NEW_LABELS = ["SFT", "NewRL50", "NewRL100", "NewRL150"]
NEW_STEPS = [0, 50, 100, 150]
DASH = (0, (5, 2.5))
values = {}
for model in ["Instruct", *LABELS]:
    benchmarks = []
    precision = Counter()
    for dataset, total in DATASETS.items():
        group = source["models"][model][dataset]
        rows = group["samples"]
        assert group["unknown"] == 0
        assert group["n"] == group["total"] == len(rows) == total
        assert len({r["id"] for r in rows}) == total
        assert {r["id"] for r in rows} == {
            r["id"] for r in source["models"]["SFT"][dataset]["samples"]
        }
        correct = np.array([r["correct"] for r in rows], dtype=float)
        forwards = np.array([r["F"] for r in rows], dtype=float)
        assert np.isin(correct, [0, 1]).all()
        assert np.isfinite(forwards).all() and (forwards > 0).all()
        if model == "Instruct":
            fork_count = 0.
            mean_width = None
            total_forks = 0
        else:
            traces = fork_source["models"][model][dataset]
            traces_by_id = {r["id"]: r for r in traces}
            assert len(traces) == len(traces_by_id) == total
            assert set(traces_by_id) == {r["id"] for r in rows}
            for old in rows:
                new = traces_by_id[old["id"]]
                for key in ("correct", "F", "tokens", "precision"):
                    assert new[key] == old[key], (model, dataset, old["id"], key)
            widths = [w for r in traces for w in r["widths"]]
            total_forks = sum(r["forks"] for r in traces)
            assert total_forks == len(widths) and total_forks > 0
            fork_count = total_forks / total
            mean_width = float(np.mean(widths))
        benchmarks.append(dict(dataset=dataset, n=total, correct=int(correct.sum()),
                               accuracy=100 * float(correct.mean()),
                               forwards=float(forwards.mean()), forks=fork_count,
                               width=mean_width, total_executed_forks=total_forks))
        precision.update(r["precision"] for r in rows)
    values[model] = dict(
        accuracy=float(np.mean([b["accuracy"] for b in benchmarks])),
        forwards=float(np.mean([b["forwards"] for b in benchmarks])),
        forks=float(np.mean([b["forks"] for b in benchmarks])),
        width=None if model == "Instruct" else float(np.mean([b["width"] for b in benchmarks])),
        benchmarks=benchmarks, precision=dict(precision),
    )

for model in NEW_LABELS[1:]:
    benchmarks = []
    precision = Counter()
    for dataset, total in DATASETS.items():
        rows = new_source["models"][model][dataset]
        assert len(rows) == len({r["id"] for r in rows}) == total
        assert {r["id"] for r in rows} == {
            r["id"] for r in source["models"]["SFT"][dataset]["samples"]
        }
        assert all(r["model_sha256"] == new_source["protocols"][model]["model_sha256"] for r in rows)
        widths = [w for r in rows for w in r["widths"]]
        total_forks = sum(r["forks"] for r in rows)
        assert total_forks == len(widths) and total_forks > 0
        benchmarks.append(dict(dataset=dataset, n=total, correct=sum(r["correct"] for r in rows),
                               accuracy=100 * float(np.mean([r["correct"] for r in rows])),
                               forwards=float(np.mean([r["F"] for r in rows])),
                               forks=total_forks / total, width=float(np.mean(widths)),
                               total_executed_forks=total_forks))
        precision.update(r["precision"] for r in rows)
    values[model] = {
        **{metric: float(np.mean([b[metric] for b in benchmarks]))
           for metric in ["accuracy", "forwards", "width", "forks"]},
        "benchmarks": benchmarks, "precision": dict(precision),
    }

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11.5,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "text.color": "#33332f", "axes.labelcolor": "#33332f",
    "xtick.color": "#77776e", "ytick.color": "#77776e",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#c6c3b9", "axes.linewidth": .8,
    "svg.fonttype": "none", "pdf.fonttype": 42,
})
fig, axes = plt.subplots(2, 2, figsize=(15.2, 8.6))
fig.subplots_adjust(left=.075, right=.958, top=.93, bottom=.17, wspace=.21, hspace=.42)
green_artists = []

def darker(color, factor=.60):
    return matplotlib.colors.to_hex(np.array(matplotlib.colors.to_rgb(color)) * factor)

for ax, metric, title, ylabel in [
    (axes[0, 0], "accuracy", "Средняя accuracy на бенчмарках", "Accuracy, %"),
    (axes[0, 1], "forwards", "Средние форварды на ответ", "Среднее число форвардов"),
    (axes[1, 0], "width", "Средняя ширина форка", "Веток на выполненный форк"),
    (axes[1, 1], "forks", "Среднее число форков на ответ", "Форков на ответ"),
]:
    ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=12)
    ax.set_xlabel("Итерация RL", labelpad=9)
    ax.set_ylabel(ylabel, labelpad=10)
    ax.set_xlim(-4, 335)
    ax.set_xticks(STEPS)
    ax.tick_params(length=0, pad=7)
    ax.grid(axis="y", color="#e8e6df", linewidth=.85)
    ax.set_axisbelow(True)
    if metric == "accuracy":
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_locator(MultipleLocator(20))
    elif metric == "forwards":
        ax.set_ylim(0, 16000)
        ax.yaxis.set_major_locator(MultipleLocator(4000))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{int(y):,}".replace(",", " ")))
    elif metric == "width":
        ax.set_ylim(0, 6)
        ax.yaxis.set_major_locator(MultipleLocator(1))
    else:
        ax.set_ylim(-.05, 1.5)
        ax.set_yticks([0, .5, 1, 1.5])
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:g}".replace(".", ",")))
    def value_label(value):
        if metric == "accuracy":
            return f"{value:.1f}%".replace(".", ",")
        if metric == "forwards":
            return f"{value:,.0f}".replace(",", " ")
        return f"{value:.2f}".replace(".", ",")
    for model in ("SFT", "Instruct"):
        if metric == "forks" and model == "Instruct":
            continue
        y = values[model][metric]
        if y is None:
            continue
        line, = ax.plot([0, 300], [y, y], color=COLORS[model], lw=2.1,
                        linestyle=DASH,
                        solid_capstyle="round", zorder=2)
        line.set_path_effects([pe.Stroke(linewidth=2.6, foreground=darker(COLORS[model], .88)), pe.Normal()])
        text = value_label(y)
        ax.annotate(text, (300, y), xytext=(8, 0), textcoords="offset points",
                    color=darker(COLORS[model]), fontsize=11, fontweight="bold", va="center")
    ys = [values[label][metric] for label in LABELS]
    line, = ax.plot(STEPS, ys, color=COLORS["RL"], lw=2.1,
                    linestyle="-", marker="o", markersize=5,
                    markerfacecolor=COLORS["RL"], markeredgewidth=0,
                    solid_capstyle="round", solid_joinstyle="round", zorder=4)
    line.set_path_effects([pe.Stroke(linewidth=2.6, foreground=darker(COLORS["RL"], .88)), pe.Normal()])
    ax.scatter([0], [values["SFT"][metric]], s=36, color=COLORS["SFT"], zorder=6)
    value_at_150 = values["RL150"][metric]
    ax.annotate(value_label(value_at_150), (150, value_at_150), xytext=(0, 11),
                textcoords="offset points", ha="center", va="bottom",
                color=darker(COLORS["RL"]), fontsize=11, fontweight="bold")
    last = value_label(ys[-1])
    ax.annotate(last, (300, ys[-1]), xytext=(8, 0), textcoords="offset points",
                color=darker(COLORS["RL"]), fontsize=11, fontweight="bold", va="center")
    new_ys = [values[label][metric] for label in NEW_LABELS]
    line, = ax.plot(NEW_STEPS, new_ys, color=COLORS["NewRL"], lw=2.1,
                    linestyle="-", marker="o", markersize=5,
                    markerfacecolor=COLORS["NewRL"], markeredgewidth=0,
                    solid_capstyle="round", solid_joinstyle="round", zorder=5)
    line.set_path_effects([pe.Stroke(linewidth=2.6, foreground=darker(COLORS["NewRL"], .88)), pe.Normal()])
    green_artists.append(line)
    for step, value in [(NEW_STEPS[-1], new_ys[-1])]:
        offset, ha, va = (8, -14 if metric == "width" else 0), "left", "center"
        annotation = ax.annotate(value_label(value), (step, value), xytext=offset,
                                 textcoords="offset points", ha=ha, va=va,
                                 color=darker(COLORS["NewRL"]), fontsize=11,
                                 fontweight="bold",
                                 bbox=dict(facecolor="white", edgecolor="none", pad=.15))
        green_artists.append(annotation)
    # Both RL trajectories share the SFT checkpoint at iteration zero.
    ax.scatter([0], [values["SFT"][metric]], s=36, color=COLORS["SFT"], zorder=7)

handles = [
    Line2D([0], [0], color=COLORS["RL"], lw=2.1, linestyle="-", marker="o", markersize=5, label="RL"),
    Line2D([0], [0], color=COLORS["NewRL"], lw=2.1, linestyle="-", marker="o", markersize=5, label="RL (новая награда)"),
    Line2D([0], [0], color=COLORS["SFT"], lw=2.1, linestyle=DASH, marker="o", markersize=5, label="SFT (итерация 0)"),
    Line2D([0], [0], color=COLORS["Instruct"], lw=2.1, linestyle=DASH, label="Instruct"),
]
legend = fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.51, .055),
                    ncol=4, frameon=False, fontsize=11.8, handlelength=3.4, columnspacing=2)
for extension in ("png", "pdf", "svg"):
    fig.savefig(OUT / f"comparison.{extension}", dpi=200, facecolor="white")

for artist in green_artists:
    artist.set_visible(False)
legend.remove()
fig.legend(handles=[handles[0], *handles[2:]], loc="lower center",
           bbox_to_anchor=(.51, .055), ncol=3, frameon=False,
           fontsize=11.8, handlelength=3.4, columnspacing=2)
for extension in ("png", "pdf", "svg"):
    fig.savefig(OUT / f"comparison-original.{extension}", dpi=200, facecolor="white")
plt.close(fig)

with (OUT / "points.csv").open("w") as stream:
    writer = csv.DictWriter(stream, fieldnames=["model", "iteration", "accuracy", "forwards", "width", "forks"])
    writer.writeheader()
    for label, step in zip(LABELS, STEPS):
        writer.writerow(dict(model=label, iteration=step, accuracy=values[label]["accuracy"],
                             forwards=values[label]["forwards"], width=values[label]["width"], forks=values[label]["forks"]))
    for label, step in zip(NEW_LABELS[1:], NEW_STEPS[1:]):
        writer.writerow(dict(model=label, iteration=step, accuracy=values[label]["accuracy"],
                             forwards=values[label]["forwards"], width=values[label]["width"], forks=values[label]["forks"]))
    writer.writerow(dict(model="Instruct", iteration="", accuracy=values["Instruct"]["accuracy"],
                         forwards=values["Instruct"]["forwards"], width=None, forks=0))
report = dict(
    source=dict(path=str(SOURCE.relative_to(ROOT)), sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                snapshot_at=source["snapshot_at"]),
    fork_source=dict(path=str(FORK_SOURCE.relative_to(ROOT)),
                     sha256=hashlib.sha256(FORK_SOURCE.read_bytes()).hexdigest(),
                     extracted_at=fork_source["extracted_at"],
                     all_old_sample_fields_matched=True),
    new_reward_source=dict(path=str(NEW_SOURCE.relative_to(ROOT)),
                           sha256=hashlib.sha256(NEW_SOURCE.read_bytes()).hexdigest(),
                           extracted_at=new_source["extracted_at"],
                           initial_model=new_source["initial_model"],
                           reward=new_source["reward"],
                           training_root=new_source["training_root"],
                           protocols=new_source["protocols"]),
    benchmark_weights={d: .25 for d in DATASETS},
    aggregation="Equal-weight mean of four per-benchmark means, over all answers; not pooled 590-task mean",
    coverage=DATASETS, steps=STEPS, new_steps=NEW_STEPS, models=values,
    forward_semantics="Saved instrumented per-request generation model.forward participation, including prefill; not total generated tokens or global batched engine call count",
    protocol=dict(response_budget=32768, path_budget=768, samples_per_question=1, temperature=1.0, top_p=1.0),
    fork_semantics="Executed fork count per answer, including all zero-fork and invalid-format answers; stats.forks equals len(widths)",
    width_semantics="For each benchmark, mean width over executed forks across all answers, then equal-weight macro mean across benchmarks; undefined for native Instruct because it executes no forks",
    display=dict(smoothing=False, point_markers=True, point_value_labels="RL at 150 and 300; new-reward RL at 150; horizontal baselines at right",
                 labelled_rl_iterations={"RL": [150, 300], "NewRL": [150]},
                 variants=["comparison (with new reward)", "comparison-original (without new reward)"],
                 dashed_lines=["SFT", "Instruct"], confidence_intervals=False,
                 reference_lines="Unchanged SFT and Instruct checkpoints shown as horizontal baselines; RL curve begins at SFT on iteration 0"),
    caveats=[
        "RL300 consists of 74 FP32 and 516 BF16 answers; all other displayed models use BF16.",
        "Instruct uses native thinking; SFT/RL use the structured parallel runtime.",
        "Inference results are the archived complete evaluation snapshot of 2026-10-13, not a new model run.",
        "The new-reward run uses DAPO2000 training and BF16 evaluation with response32000/path4000; the old RL uses response32768/path768, so this is not an isolated reward-only comparison.",
        "The new trajectory reuses the existing SFT benchmark evaluation at iteration 0, representing the same initial weights but the original response32768/path768 protocol.",
    ],
    optional_metrics=[
        "Macro mean executed fork count per answer, including zero-fork answers",
        "Macro mean branch width conditional on completed forks; width is undefined for Instruct",
        "Macro percentage of answers with at least one completed fork",
        "Accuracy vs forwards checkpoint trajectory",
    ],
)
(OUT / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({m: {k: v[k] for k in ("accuracy", "forwards", "width", "forks")} for m, v in values.items()}, ensure_ascii=False))
