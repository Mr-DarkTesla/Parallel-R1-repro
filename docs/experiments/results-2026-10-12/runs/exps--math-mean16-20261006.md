# exps/math-mean16-20261006

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Метрики и полнота результатов

- [exps/math-mean16-20261006/results/eval/seen-async/driver.log](../artifacts/exps/math-mean16-20261006/results/eval/seen-async/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/math-mean16-20261006/results/eval/seen-async/summary.json](../artifacts/exps/math-mean16-20261006/results/eval/seen-async/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "answers": 5056,
  "correct": 1490,
  "mean": 0.2946993670886076,
  "seconds": 813.0505316620693,
  "mean_unique_outputs": 16.0
}
```

</details>

- [exps/math-mean16-20261006/results/eval/seen-sync/driver.log](../artifacts/exps/math-mean16-20261006/results/eval/seen-sync/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/math-mean16-20261006/results/eval/seen-sync/summary.json](../artifacts/exps/math-mean16-20261006/results/eval/seen-sync/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "answers": 5056,
  "correct": 1356,
  "mean": 0.26819620253164556,
  "seconds": 658.863563076593,
  "mean_unique_outputs": 16.0
}
```

</details>

- [exps/math-mean16-20261006/results/eval/unseen-async/driver.log](../artifacts/exps/math-mean16-20261006/results/eval/unseen-async/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/math-mean16-20261006/results/eval/unseen-async/summary.json](../artifacts/exps/math-mean16-20261006/results/eval/unseen-async/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "answers": 5056,
  "correct": 1379,
  "mean": 0.27274525316455694,
  "seconds": 815.5991424536332,
  "mean_unique_outputs": 16.0
}
```

</details>

- [exps/math-mean16-20261006/results/eval/unseen-sync/driver.log](../artifacts/exps/math-mean16-20261006/results/eval/unseen-sync/driver.telemetry.json) — remote_nfs, снимок 2026-10-12T17:38:42.513579+00:00.

- [exps/math-mean16-20261006/results/eval/unseen-sync/summary.json](../artifacts/exps/math-mean16-20261006/results/eval/unseen-sync/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "answers": 5056,
  "correct": 1282,
  "mean": 0.2535601265822785,
  "seconds": 642.6678768899292,
  "mean_unique_outputs": 16.0
}
```

</details>

- [exps/math-mean16-20261006/status.json](../artifacts/exps/math-mean16-20261006/status.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "seen-sync": {
    "updated": "2026-10-06T07:44:07.874228+00:00",
    "status": "complete",
    "answers": 5056,
    "mean": 0.26819620253164556
  },
  "seen-async": {
    "updated": "2026-10-06T07:46:42.062669+00:00",
    "status": "complete",
    "answers": 5056,
    "mean": 0.2946993670886076
  },
  "unseen-async": {
    "updated": "2026-10-06T07:46:44.613227+00:00",
    "status": "complete",
    "answers": 5056,
    "mean": 0.27274525316455694
  },
  "unseen-sync": {
    "updated": "2026-10-06T07:43:51.687724+00:00",
    "status": "complete",
    "answers": 5056,
    "mean": 0.2535601265822785
  }
}
```

</details>

- [exps/math-mean16-20261006/summary.json](../artifacts/exps/math-mean16-20261006/summary.json) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "complete": true,
  "questions": 316,
  "answers_per_model": 5056,
  "finished": "2026-10-06T07:46:45.096509+00:00",
  "estimates": {
    "seen-sync": {
      "mean": 0.26819620253164556,
      "ci95": [
        0.23655063291139242,
        0.3004351265822785
      ]
    },
    "seen-async": {
      "mean": 0.2946993670886076,
      "ci95": [
        0.26127373417721517,
        0.3287183544303797
      ]
    },
    "unseen-sync": {
      "mean": 0.2535601265822785,
      "ci95": [
        0.22389240506329114,
        0.28401898734177217
      ]
    },
    "unseen-async": {
      "mean": 0.27274525316455694,
      "ci95": [
        0.24149525316455697,
        0.3045935522151902
      ]
    }
  },
  "comparisons": [
    {
      "a": "seen-sync",
      "b": "seen-async",
      "difference": -0.026503164556962024,
      "ci95": [
        -0.04034810126582278,
        -0.013053797468354444
      ],
      "ci_family95": [
        -0.04509493670886078,
        -0.008702531645569611
      ]
    },
    {
      "a": "seen-sync",
      "b": "unseen-sync",
      "difference": 0.014636075949367089,
      "ci95": [
        -0.0007911392405063333,
        0.030261075949367056
      ],
      "ci_family95": [
        -0.0061313291139240556,
        0.03540348101265822
      ]
    },
    {
      "a": "seen-sync",
      "b": "unseen-async",
      "difference": -0.004549050632911392,
      "ci95": [
        -0.019778481012658222,
        0.010680379746835444
      ],
      "ci_family95": [
        -0.02492088607594939,
        0.015625
      ]
    },
    {
      "a": "seen-async",
      "b": "unseen-sync",
      "difference": 0.04113924050632911,
      "ci95": [
        0.0276898734177215,
        0.05498417721518986
      ],
      "ci_family95": [
        0.022745253164557,
        0.05973101265822789
      ]
    },
    {
      "a": "seen-async",
      "b": "unseen-async",
      "difference": 0.021954113924050632,
      "ci95": [
        0.008900316455696222,
        0.035007911392405056
      ],
      "ci_family95": [
        0.004549050632911389,
        0.039556962025316444
      ]
    },
    {
      "a": "unseen-sync",
      "b": "unseen-async",
      "difference": -0.019185126582278483,
      "ci95": [
        -0.03263449367088608,
        -0.005735759493670889
      ],
      "ci_family95": [
        -0.037381329113924056,
        -0.0011867088607595
      ]
    }
  ]
}
```

</details>

## Исходники рецепта и награды

- [exps/math-mean16-20261006/run.py](../artifacts/exps/math-mean16-20261006/run.py) — remote_nfs, снимок 2026-10-12T17:43:08.720015+00:00.
