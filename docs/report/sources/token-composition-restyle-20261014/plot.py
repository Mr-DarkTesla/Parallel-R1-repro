"""Restyle the archived RL300/MATH500 response-token composition."""
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
ROOT = OUT.parents[2]
SOURCE = ROOT / "work/experiments/eval-comparison-20261013/token-composition-math500.json"
source = json.loads(SOURCE.read_text())
CATEGORIES = ["plan", "branches", "summary", "answer", "other_thought", "service"]
LABELS = ["План", "Ветки", "Summary", "Финальный ответ", "Прочее рассуждение", "Служебные токены"]
COLORS = ["#D7A522", "#397CC1", "#B9674D", "#6D8884", "#89949D", "#C5C5C5"]

assert source["checkpoint"] == 300 and source["dataset"] == "MATH500"
assert len(source["records"]) == 500
assert len({r["id"] for r in source["records"]}) == 500
groups = {}
for key in ("all", "valid"):
    rows = [r for r in source["records"] if key == "all" or r["valid"]]
    counts = np.asarray([[r["counts"][c] for c in CATEGORIES] for r in rows], dtype=np.int64)
    totals = np.asarray([r["total"] for r in rows], dtype=np.int64)
    assert np.array_equal(counts.sum(axis=1), totals)
    expected = source["groups"][key]
    assert len(rows) == expected["n"] and int(totals.sum()) == expected["total_response_tokens"]
    for index, category in enumerate(CATEGORIES):
        assert int(counts[:, index].sum()) == expected["tokens"][category]
    percentages = 100 * counts.sum(axis=0) / totals.sum()
    assert np.allclose(percentages, [expected["pct"][c] for c in CATEGORIES])
    rng = np.random.default_rng(20261013)
    bootstrap = []
    for _ in range(20):
        indices = rng.integers(0, len(rows), size=(1000, len(rows)))
        bootstrap.append(100 * counts[indices].sum(axis=1) / totals[indices].sum(axis=1)[:, None])
    low, high = np.quantile(np.concatenate(bootstrap), [.025, .975], axis=0)
    groups[key] = dict(n=len(rows), total_tokens=int(totals.sum()),
                       percentages=percentages.tolist(),
                       ci95_low=low.tolist(), ci95_high=high.tolist(),
                       counts=counts.sum(axis=0).tolist())

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
axes = [ax]
fig.subplots_adjust(left=.30, right=.965, top=.94, bottom=.16)
positions = np.arange(len(CATEGORIES))
for ax, key in [(axes[0], "all")]:
    group = groups[key]
    percentages = np.array(group["percentages"])
    low = np.array(group["ci95_low"])
    high = np.array(group["ci95_high"])
    ax.barh(positions, percentages, height=.49, color=COLORS, zorder=3)
    ax.errorbar(percentages, positions,
                xerr=np.vstack([percentages - low, high - percentages]),
                fmt="none", color="#55554e", elinewidth=1, capsize=2.5, zorder=4)
    for index, percentage in enumerate(percentages):
        ax.text(high[index] + 1.1, index, f"{percentage:.2f}%".replace(".", ","),
                va="center", color="#33332f", fontsize=11.2, fontweight="bold")
    ax.set_yticks(positions, LABELS)
    ax.set_xlim(0, 65)
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.set_xlabel("Доля токенов ответа, %", labelpad=10)
    ax.tick_params(length=0, pad=8)
    ax.grid(axis="x", color="#e8e6df", linewidth=.85)
    ax.set_axisbelow(True)
axes[0].invert_yaxis()
for extension in ("png", "pdf", "svg"):
    fig.savefig(OUT / f"composition.{extension}", dpi=200, facecolor="white")
plt.close(fig)

with (OUT / "shares.csv").open("w") as stream:
    writer = csv.DictWriter(stream, fieldnames=["group", "n", "category", "tokens", "share_pct", "ci95_low", "ci95_high"])
    writer.writeheader()
    for key, group in groups.items():
        for index, category in enumerate(CATEGORIES):
            writer.writerow(dict(group=key, n=group["n"], category=category,
                                 tokens=group["counts"][index], share_pct=group["percentages"][index],
                                 ci95_low=group["ci95_low"][index], ci95_high=group["ci95_high"][index]))
report = dict(
    source=dict(path=str(SOURCE.relative_to(ROOT)), sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                snapshot_at=source["snapshot_at"]),
    checkpoint=source["checkpoint"], dataset=source["dataset"], categories=CATEGORIES,
    palette=dict(zip(CATEGORIES, COLORS)), groups=groups,
    denominator="Sum of all response token IDs, including runtime-inserted headers/tags; excludes prompt",
    aggregation="Pooled token proportions, not an unweighted mean of per-task proportions",
    confidence="95% percentile bootstrap over tasks, 20000 draws, seed 20261013",
    definitions=source["definitions"],
    valid_format_is_not_correctness=True,
    display=dict(groups=["all"], panel_titles=False),
)
(OUT / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(groups, ensure_ascii=False))
