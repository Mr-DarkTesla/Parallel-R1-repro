`python scripts/compare_runs.py results/02r-sft-prompt-positions-rerun results/11-len8k-control`
(02r: `eval_math300_x8.txt` и `free_generation_tags.jsonl` взяты из `/work/runs/02r-sft-prompt-positions-rerun`; проверка тегов 02r
есть только для шагов 138 и 184, поэтому строка 02r в последней таблице — шаг 184, у 11 — финальный шаг 230.)

### AIME24 (x16)

| run | mean@16 | pass@16 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 0.6 | 3.3 | 95.8 | 79.3 | 87.7 | 2.9 |
| 11-len8k-control | 0.8 | 10.0 | 96.7 | 76.8 | 87.9 | 2.3 |

### AIME25 (x16)

| run | mean@16 | pass@16 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 0.4 | 6.7 | 98.3 | 79.2 | 87.9 | 2.3 |
| 11-len8k-control | 0.2 | 3.3 | 96.0 | 79.5 | 89.0 | 1.5 |

### AMC23 (x16)

| run | mean@16 | pass@16 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 10.9 | 52.5 | 98.4 | 78.0 | 88.1 | 1.1 |
| 11-len8k-control | 10.6 | 47.5 | 97.7 | 77.1 | 87.6 | 0.6 |

### MATH300 (x1)

| run | mean@1 | pass@1 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 26.9 | 26.9 | 98.1 | 80.5 | 89.5 | 0.6 |
| 11-len8k-control | 27.2 | 27.2 | 98.4 | 81.5 | 89.4 | 0.3 |

### MATH300_x8 (x8)

| run | mean@8 | pass@8 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 27.3 | 60.4 | 98.3 | 80.7 | 89.7 | 1.1 |
| 11-len8k-control | 26.9 | 60.8 | 98.6 | 79.4 | 88.5 | 0.8 |

### LIMO (x4)

| run | mean@4 | pass@4 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 1.1 | 4.2 | 96.2 | 77.2 | 87.4 | 3.7 |
| 11-len8k-control | 1.2 | 4.0 | 96.7 | 77.0 | 87.3 | 1.9 |

### Free generation, final checkpoint: valid responses / correct tags

| run | GSM8K T=0 | GSM8K T=1 | MATH300 T=0 | MATH300 T=1 |
|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 52% / 56% | 12% / 28% | 67% / 79% | 18% / 35% |
| 11-len8k-control | 54% / 53% | 16% / 39% | 72% / 78% | 19% / 38% |
