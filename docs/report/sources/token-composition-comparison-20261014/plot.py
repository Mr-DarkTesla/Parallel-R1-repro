"""Side-by-side all-answer token composition without panel headings."""
from pathlib import Path
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

OUT = Path(__file__).resolve().parent
PARENT = OUT.parent
OLD = PARENT / "token-composition-restyle-20261014/manifest.json"
NEW = PARENT / "rl150-new-reward-token-composition-20261014/manifest.json"
old, new = [json.loads(p.read_text()) for p in (OLD, NEW)]
CATEGORIES = ["plan", "branches", "summary", "answer", "other_thought", "service"]
LABELS = ["План", "Ветки", "Summary", "Финальный ответ", "Прочее рассуждение", "Служебные токены"]
COLORS = ["#D7A522", "#397CC1", "#B9674D", "#6D8884", "#89949D", "#C5C5C5"]
assert old["checkpoint"] == 300 and old["groups"]["all"]["n"] == 500
assert new["checkpoint_identity"]["checkpoint"] == 150 and new["n"] == 500
assert old["categories"] == [r["category"] for r in new["shares"]] == CATEGORIES
groups = [
    old["groups"]["all"],
    dict(percentages=[r["share_pct"] for r in new["shares"]],
         ci95_low=[r["ci95_low"] for r in new["shares"]],
         ci95_high=[r["ci95_high"] for r in new["shares"]]),
]
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11.5,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "text.color": "#33332f", "axes.labelcolor": "#33332f",
    "xtick.color": "#77776e", "ytick.color": "#77776e",
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.edgecolor": "#c6c3b9", "axes.linewidth": .8,
    "svg.fonttype": "none", "pdf.fonttype": 42,
})
fig, axes = plt.subplots(1, 2, figsize=(15.2, 6.0), sharey=True)
fig.subplots_adjust(left=.175, right=.965, top=.88, bottom=.16, wspace=.13)
positions = np.arange(len(CATEGORIES))
for ax, group, title in zip(axes, groups, ["Было", "Стало"]):
    ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=12)
    percentages = np.asarray(group["percentages"])
    low, high = [np.asarray(group[k]) for k in ("ci95_low", "ci95_high")]
    ax.barh(positions, percentages, height=.49, color=COLORS, zorder=3)
    ax.errorbar(percentages, positions, xerr=np.vstack([percentages - low, high - percentages]),
                fmt="none", color="#55554e", elinewidth=1, capsize=2.5, zorder=4)
    for i, percentage in enumerate(percentages):
        ax.text(high[i] + 1.1, i, f"{percentage:.2f}%".replace(".", ","),
                va="center", color="#33332f", fontsize=11.2, fontweight="bold")
    ax.set_yticks(positions, LABELS)
    ax.set_xlim(0, 65)
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.set_xlabel("Доля токенов ответа, %", labelpad=10)
    ax.tick_params(length=0, pad=8)
    ax.grid(axis="x", color="#e8e6df", linewidth=.85)
    ax.set_axisbelow(True)
axes[0].invert_yaxis()
for ext in ("png", "pdf", "svg"):
    fig.savefig(OUT / f"comparison.{ext}", dpi=200, facecolor="white")
plt.close(fig)
manifest = dict(
    sources=[dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (OLD, NEW)],
    panel_order=["RL300 old reward", "SFT -> RL150 new R4 reward"],
    dataset="MATH500", n_each=500, groups="all answers", panel_titles=["Было", "Стало"],
    percentages=[g["percentages"] for g in groups],
    palette=dict(zip(CATEGORIES, COLORS)), confidence="95% task-bootstrap CI",
    caveat="Different checkpoints and response/path budgets; descriptive token composition, not a reward-only controlled comparison",
)
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(OUT / "comparison.png")
