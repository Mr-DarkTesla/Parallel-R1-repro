# Исходники графиков

[← к сводке](../README.md)

Скрипты и сохранённые данные, из которых построены графики в [`../figures`](../figures).
Скопированы из локальных `work/experiments/<имя>/` (14–15 октября 2026) без PDF/SVG и файлов больше 2 МБ.

| Папка | График |
|---|---|
| `gsm-legacy-comparison-20261014` | [06b-gsm-length-penalty.png](../figures/06b-gsm-length-penalty.png) — 0.6B, штраф за длину на GSM-Infinite |
| `rl300-fork-width-20261014`, `rl150-fork-width-20261014`, `fork-width-comparison-20261014` | [4b-fork-width-before-after.png](../figures/4b-fork-width-before-after.png) |
| `token-composition-restyle-20261014`, `rl150-new-reward-token-composition-20261014`, `token-composition-comparison-20261014` | [4b-token-composition-before-after.png](../figures/4b-token-composition-before-after.png) |
| `rl300-normal-vs-random2-20261015` | [4b-rl300-random2.png](../figures/4b-rl300-random2.png) |
| `rl300-parallel-position-20261014`, `parallel-position-restyle-20261014` | [4b-parallel-position-vs-paper.png](../figures/4b-parallel-position-vs-paper.png) (точки Figure 3 статьи сняты с графика) |
| `rl-training-curves-20261014` | [4b-rl-train-curves.png](../figures/4b-rl-train-curves.png) |
| `rl50-old-vs-dapo-20261014` | [4b-rl50-old-vs-dapo.png](../figures/4b-rl50-old-vs-dapo.png) |
| `rl-progress-20261013` | [4b-val32-metrics.png](../figures/4b-val32-metrics.png) |

Остальное:

- `4b-rl300-rl150-benchmarks.png` — [docs/reproduction/benchmark-trajectories-2026-10-14](../../reproduction/benchmark-trajectories-2026-10-14/README.md),
  там же полный расчёт и `plot.py`, который запускается без сервера.
- `archive-*.png`, `06b-dapo-20261008.png`, `06b-gsm-20261008.png` — из архива `docs/experiments/` ветки `sft-eval-adaptation`.
- `slide-*.png` — картинки из презентации «Parallel-R1 с видео».

Абсолютные пути заменены на `${PROJECT_ROOT}` (локальный checkout) и `${PROJECT_ROOT}` (корень проекта на общей NFS).
SHA-256 внутри manifest/data файлов относятся к исходным файлам до этой замены. Многие скрипты читают серверные
логи, поэтому без доступа к `${PROJECT_ROOT}` их можно читать как описание расчёта, но не перезапустить;
`plot.py` рядом с `data.json` обычно перестраивает график из сохранённых данных.
