"""One-panel token composition for new-reward R4 SFT -> RL150, all MATH500."""
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

OUT = Path(__file__).resolve().parent
SOURCE = OUT / "data.json"
data = json.loads(SOURCE.read_text())
assert data["reference_validation"]["matched_all_500_rows"]
assert data["metadata"]["checkpoint"] == 150
assert data["metadata"]["reward"] == "C*(1-.9*(1-exp(-ln(9)*F/10000)))"
CATEGORIES = ["plan", "branches", "summary", "answer", "other_thought", "service"]
LABELS = ["План", "Ветки", "Summary", "Финальный ответ", "Прочее рассуждение", "Служебные токены"]
COLORS = ["#D7A522", "#397CC1", "#B9674D", "#6D8884", "#89949D", "#C5C5C5"]
rows = data["records"]
assert len(rows) == len({r["id"] for r in rows}) == 500
counts = np.asarray([[r["counts"][c] for c in CATEGORIES] for r in rows], dtype=np.int64)
totals = np.asarray([r["total"] for r in rows], dtype=np.int64)
assert np.array_equal(counts.sum(axis=1), totals)
percentages = 100 * counts.sum(axis=0) / totals.sum()
assert np.isclose(percentages.sum(), 100)
rng = np.random.default_rng(20261013)
bootstrap = []
for _ in range(20):
    indices = rng.integers(0, len(rows), size=(1000, len(rows)))
    bootstrap.append(100 * counts[indices].sum(axis=1) / totals[indices].sum(axis=1)[:, None])
low, high = np.quantile(np.concatenate(bootstrap), [.025, .975], axis=0)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11.5,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "text.color": "#33332f", "axes.labelcolor": "#33332f",
    "xtick.color": "#77776e", "ytick.color": "#77776e",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.edgecolor": "#c6c3b9", "axes.linewidth": .8,
    "svg.fonttype": "none", "pdf.fonttype": 42,
})
fig, ax = plt.subplots(figsize=(8.8, 6.0))
fig.subplots_adjust(left=.30, right=.965, top=.94, bottom=.16)
positions = np.arange(len(CATEGORIES))
ax.barh(positions, percentages, height=.49, color=COLORS, zorder=3)
ax.errorbar(percentages, positions, xerr=np.vstack([percentages - low, high - percentages]),
            fmt="none", color="#55554e", elinewidth=1, capsize=2.5, zorder=4)
for index, percentage in enumerate(percentages):
    ax.text(high[index] + 1.1, index, f"{percentage:.2f}%".replace(".", ","),
            va="center", color="#33332f", fontsize=11.2, fontweight="bold")
ax.set_yticks(positions, LABELS)
ax.invert_yaxis()
ax.set_xlim(0, 65)
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.set_xlabel("Доля токенов ответа, %", labelpad=10)
ax.tick_params(length=0, pad=8)
ax.grid(axis="x", color="#e8e6df", linewidth=.85)
ax.set_axisbelow(True)
for extension in ("png", "pdf", "svg"):
    fig.savefig(OUT / f"composition.{extension}", dpi=200, facecolor="white")
plt.close(fig)

shares = []
for index, category in enumerate(CATEGORIES):
    shares.append(dict(category=category, tokens=int(counts[:, index].sum()),
                       share_pct=float(percentages[index]),
                       ci95_low=float(low[index]), ci95_high=float(high[index])))
with (OUT / "shares.csv").open("w") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(shares[0]))
    writer.writeheader()
    writer.writerows(shares)
report = dict(
    source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    checkpoint_identity=data["metadata"], reference_validation=data["reference_validation"],
    dataset="MATH500", group="all", n=500, total_response_tokens=int(totals.sum()),
    counts_including_invalid_format=True,
    aggregation="Pooled share of all response token IDs, including runtime-inserted service tokens; excludes prompt; not unweighted mean per-task percentage",
    confidence="95% percentile task bootstrap, 20000 repetitions, seed20261013",
    palette=dict(zip(CATEGORIES, COLORS)), shares=shares,
)
(OUT / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(dict(output=str(OUT / "composition.png"), n=500,
                     model_sha256=data["metadata"]["model_sha256"], shares=shares), ensure_ascii=False))
