"""Four-panel comparison of the three archived GSM-Infinite RL experiments."""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
OLD = ROOT / "exps/gsm-unseen-two-rewards-20261008"
NEW = ROOT / "exps/gsm-unseen-split-rewards-400-20261008"
SOURCES = [OLD / "monitoring-20261008-0839-msk.json",
           OLD / "reward-analysis.json", NEW / "completed-snapshot-20261008.json"]
history, analysis, newer = [json.loads(p.read_text()) for p in SOURCES]

# Presentation palette: saturated blue, gold, and muted terracotta.
PALETTE = {"blue": "#397CC1", "yellow": "#D7A522", "sand": "#B9674D",
           "background": "#ffffff", "text": "#33332f", "grid": "#e8e6df"}
RUNS = [
    dict(key="s2", label="S2", color=PALETTE["blue"], style="-",
         train=analysis["training"]["s2"], val=history["stages"]["s2"]["validation"],
         reward="8/10 steps: 2c-1; 2/10: +1 correct plain, +1.2 correct valid parallel, -1 otherwise",
         advantage="(R-mean_group(R))/(sample_std_group(R)+1e-6)"),
    dict(key="depth", label=r"$R = c - 10^{-4} F$", color=PALETTE["yellow"], style="-",
         train=analysis["training"]["depth"], val=history["stages"]["depth"]["validation"],
         reward="c-0.0001*D", advantage="(R-mean_group(R))/(sample_std_group(R)+1e-6)"),
    dict(key="gated_depth", label=r"$R = c\bigl(1 - 10^{-4} F\bigr)$", color=PALETTE["sand"], style="-",
         train=newer["stages"]["gated_depth"]["training_series"],
         val=newer["stages"]["gated_depth"]["validation"], reward="c-0.0001*c*D",
         advantage="(c-mean_group(c))/(sample_std_group(c)+1e-6)-0.0001*(c*D-mean_group(c*D))"),
]

def darken(hex_color, factor=0.68):
    rgb = np.array(matplotlib.colors.to_rgb(hex_color)) * factor
    return matplotlib.colors.to_hex(rgb)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11.5,
    "figure.facecolor": PALETTE["background"], "axes.facecolor": PALETTE["background"],
    "text.color": PALETTE["text"], "axes.labelcolor": PALETTE["text"],
    "xtick.color": "#77776e", "ytick.color": "#77776e",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#c6c3b9", "axes.linewidth": 0.8,
    "svg.fonttype": "none", "pdf.fonttype": 42,
    "font.serif": ["Computer Modern Roman"],
    "text.latex.preamble": r"\usepackage{amsmath}",
})
fig, axes = plt.subplots(2, 2, figsize=(15.2, 8.6))
fig.subplots_adjust(left=.075, right=.958, top=.93, bottom=.22, wspace=.21, hspace=.42)
SMOOTHING = {"parallel/critical_depth_mean": 40, "parallel/forks_mean": 30}
panels = [
    (axes[0, 0], "Accuracy на MATH", "Accuracy, %", "APO_MATH300"),
    (axes[0, 1], "Форварды на ответ", "Среднее число форвардов", "parallel/critical_depth_mean"),
    (axes[1, 0], "Accuracy на GSM-Infinite", "Accuracy, %", "gsm_infinite_heldout"),
    (axes[1, 1], "Parallel-блоки на ответ", "Среднее число блоков на ответ", "parallel/forks_mean"),
]
export = []
endpoints = {}
for ax, title, ylabel, metric in panels:
    ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=12)
    ax.set_xlabel("Итерация RL", labelpad=9)
    ax.set_ylabel(ylabel, labelpad=10)
    ax.set_xlim(0, 870)
    ax.set_xticks([0, 200, 400, 600, 800])
    ax.tick_params(length=0, pad=7)
    ax.grid(axis="y", color=PALETTE["grid"], linewidth=.85)
    ax.set_axisbelow(True)
    if metric == "APO_MATH300":
        ax.set_ylim(0, 50)
        ax.yaxis.set_major_locator(MultipleLocator(10))
    elif metric == "gsm_infinite_heldout":
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_locator(MultipleLocator(20))
    elif metric == "parallel/critical_depth_mean":
        ax.set_ylim(0, 700)
        ax.yaxis.set_major_locator(MultipleLocator(200))
    else:
        ax.set_ylim(-.07, 2.45)
        ax.set_yticks([0, .5, 1, 1.5, 2])
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}".replace(".", ",")))
    for run in RUNS:
        val = metric in ("APO_MATH300", "gsm_infinite_heldout")
        if val:
            rows = run["val"]
            x = np.array([r["step"] for r in rows])
            y = np.array([100 * r["sources"][metric]["acc"] for r in rows])
            for row, step, value in zip(rows, x, y):
                source = row["sources"][metric]
                export.append(dict(run=run["key"], metric=metric, iteration=int(step), value=float(value),
                                   n=source["n"], correct=source["correct"], smoothing_window=1))
        else:
            rows = run["train"]
            x = np.array([int(r["training/global_step"]) for r in rows])
            assert x.tolist() == list(range(1, len(rows) + 1))
            raw = np.array([r[metric] for r in rows])
            assert np.isfinite(raw).all()
            window = SMOOTHING[metric]
            y = np.convolve(raw, np.ones(window) / window, mode="valid")
            x = x[window - 1:]
            for row, value in zip(rows, raw):
                export.append(dict(run=run["key"], metric=metric, iteration=int(row["training/global_step"]),
                                   value=float(value), n=256, correct="", smoothing_window=window))
        line, = ax.plot(x, y, color=run["color"], lw=2.1, linestyle=run["style"],
                        solid_capstyle="round", solid_joinstyle="round", zorder=4)
        # A subtle border gives the thin lines a crisp edge.
        line.set_path_effects([pe.Stroke(linewidth=2.6, foreground=darken(run["color"], .88)), pe.Normal()])
        endpoint = f"{y[-1]:.1f}%" if val else f"{y[-1]:.0f}" if "depth" in metric else f"{y[-1]:.2f}"
        endpoint = endpoint.replace(".", ",")
        offset = (8, 0)
        if metric == "APO_MATH300" and run["key"] == "gated_depth":
            offset = (8, -18)
        if metric == "gsm_infinite_heldout" and run["key"] == "gated_depth":
            offset = (8, 16)
        if metric == "parallel/forks_mean" and run["key"] in ("depth", "gated_depth"):
            offset = (8, 10)
        ax.annotate(endpoint, (x[-1], y[-1]), xytext=offset, textcoords="offset points",
                    fontsize=11, color=darken(run["color"], .60), fontweight="bold", va="center")
        endpoints.setdefault(run["key"], {})[metric] = dict(iteration=int(x[-1]), value=float(y[-1]))

handles = []
for run in RUNS:
    line = Line2D([0], [0], color=run["color"], lw=2.1, linestyle=run["style"], label=run["label"])
    line.set_path_effects([pe.Stroke(linewidth=2.6, foreground=darken(run["color"], .88)), pe.Normal()])
    handles.append(line)
legend = fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.51, .09), ncol=3, frameon=False,
                    fontsize=11.8, handlelength=3.4, columnspacing=2)
for label in legend.get_texts():
    if label.get_text().startswith("$"):
        label.set_usetex(True)
        label.set_fontfamily("serif")

# Real LaTeX formulas and the existing Cyrillic font share the same baseline.
def notation_line(math, explanation, y):
    formula = TextArea(math, textprops=dict(usetex=True, fontfamily="serif",
                                           fontsize=11.5, color="#77776e"))
    prose = TextArea(explanation, textprops=dict(fontsize=11.5, color="#77776e"))
    line = HPacker(children=[formula, prose], align="baseline", pad=0, sep=4)
    anchor = AnchoredOffsetbox(loc="center", child=line, bbox_to_anchor=(.51, y),
                               bbox_transform=fig.transFigure, frameon=False, pad=0, borderpad=0)
    fig.add_artist(anchor)

notation_line(r"$c \in \{0,\,1\}$", "это правильность ответа", .065)
notation_line(r"$F$", "это число форвардов", .034)

for ext in ("png", "svg", "pdf"):
    fig.savefig(OUT / f"comparison.{ext}", dpi=200, facecolor=PALETTE["background"])
plt.close(fig)
with (OUT / "source-points.csv").open("w") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(export[0]))
    writer.writeheader()
    writer.writerows(export)
manifest = dict(
    sources=[dict(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in SOURCES],
    palette=PALETTE, formula_renderer="LaTeX with Computer Modern and amsmath",
    training_smoothing=dict(method="trailing arithmetic mean, plotted at last step", windows=SMOOTHING),
    validation="one stochastic answer per task; MATH n=316, GSM-Infinite n=256",
    forwards="logical critical path: sum main/summary generated tokens + sum(max generated path tokens per fork); excludes prefill and runtime-inserted tokens",
    blocks="mean executed fork count over all 256 training answers; width fixed at 2",
    runs=[{k: v for k, v in run.items() if k not in ("train", "val")} for run in RUNS],
    endpoints=endpoints, physical_gpu_forward_measurement=False,
)
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(dict(output=str(OUT / "comparison.png"), source_points=len(export), endpoints=endpoints), ensure_ascii=False))
