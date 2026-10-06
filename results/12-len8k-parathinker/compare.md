`python scripts/compare_runs.py results/02r-sft-prompt-positions-rerun results/11-len8k-control results/12-len8k-parathinker`
(02r: `eval_math300_x8.txt` и `free_generation_tags.jsonl` из `/work/runs/02r-sft-prompt-positions-rerun`; проверка тегов 02r есть
только для шагов 138 и 184, поэтому строка 02r в последней таблице — шаг 184; у 11 — шаг 230, у 12 — шаг 290. 02r оценивался с лимитом
ответа 3000, 11 и 12 — 8192.)

### AIME24 (x16)

| run | mean@16 | pass@16 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 0.6 | 3.3 | 95.8 | 79.3 | 87.7 | 2.9 |
| 11-len8k-control | 0.8 | 10.0 | 96.7 | 76.8 | 87.9 | 2.3 |
| 12-len8k-parathinker | 0.2 | 3.3 | 97.7 | 22.7 | 51.4 | 67.3 |

### AIME25 (x16)

| run | mean@16 | pass@16 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 0.4 | 6.7 | 98.3 | 79.2 | 87.9 | 2.3 |
| 11-len8k-control | 0.2 | 3.3 | 96.0 | 79.5 | 89.0 | 1.5 |
| 12-len8k-parathinker | 0.0 | 0.0 | 95.2 | 18.2 | 45.7 | 74.4 |

### AMC23 (x16)

| run | mean@16 | pass@16 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 10.9 | 52.5 | 98.4 | 78.0 | 88.1 | 1.1 |
| 11-len8k-control | 10.6 | 47.5 | 97.7 | 77.1 | 87.6 | 0.6 |
| 12-len8k-parathinker | 7.7 | 50.0 | 93.4 | 38.1 | 63.1 | 46.9 |

### MATH300 (x1)

| run | mean@1 | pass@1 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 26.9 | 26.9 | 98.1 | 80.5 | 89.5 | 0.6 |
| 11-len8k-control | 27.2 | 27.2 | 98.4 | 81.5 | 89.4 | 0.3 |
| 12-len8k-parathinker | 24.4 | 24.4 | 98.1 | 56.2 | 71.7 | 30.7 |

### MATH300_x8 (x8)

| run | mean@8 | pass@8 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 27.3 | 60.4 | 98.3 | 80.7 | 89.7 | 1.1 |
| 11-len8k-control | 26.9 | 60.8 | 98.6 | 79.4 | 88.5 | 0.8 |
| 12-len8k-parathinker | 24.2 | 60.1 | 96.7 | 57.5 | 75.4 | 29.7 |

### LIMO (x4)

| run | mean@4 | pass@4 | with <Parallel> | valid responses | correct tags | no final answer |
|---|---|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 1.1 | 4.2 | 96.2 | 77.2 | 87.4 | 3.7 |
| 11-len8k-control | 1.2 | 4.0 | 96.7 | 77.0 | 87.3 | 1.9 |
| 12-len8k-parathinker | 0.5 | 1.7 | 94.4 | 26.4 | 54.9 | 64.9 |

### Free generation, final checkpoint: valid responses / correct tags

| run | GSM8K T=0 | GSM8K T=1 | MATH300 T=0 | MATH300 T=1 |
|---|---|---|---|---|
| 02r-sft-prompt-positions-rerun | 52% / 56% | 12% / 28% | 67% / 79% | 18% / 35% |
| 11-len8k-control | 54% / 53% | 16% / 39% | 72% / 78% | 19% / 38% |
| 12-len8k-parathinker | 59% / 60% | 23% / 43% | 17% / 44% | 11% / 31% |

## Длина ответов в eval (11 и 12, лимит 8192)

Из `/work/runs/<run>/eval_<test>/generations/0.jsonl`: длина `output` в токенах токенизатора `Qwen3-0.6B-Base-add-special-token`
без `<|endoftext|>`-паддинга; «упёрся в лимит» = в ответе нет ни одного паддинга (≈ 8192 токенов). Поле `output` — ответ вместе со
вставками роллаута, поэтому длина приблизительная. «нет Final Answer» здесь — нет подстроки `Final Answer` (мягче, чем в таблицах выше).

| run | тест | ответов | медиана токенов | p90 | упёрся в лимит, % | нет Final Answer, % | оба, % | точность, % |
|---|---|---|---|---|---|---|---|---|
| 11 | apo | 1916 | 802 | 1404 | 0.4 | 1.2 | 0.4 | 8.30 |
| 11 | limo | 3268 | 892 | 1590 | 0.9 | 1.9 | 0.9 | 1.16 |
| 11 | math300_x8 | 2528 | 645 | 1150 | 0.2 | 0.8 | 0.2 | 26.90 |
| 12 | apo | 1916 | 8188 | 8192 | 55.7 | 51.0 | 50.8 | 6.63 |
| 12 | limo | 3268 | 8190 | 8192 | 64.7 | 61.1 | 60.8 | 0.49 |
| 12 | math300_x8 | 2528 | 3238 | 8192 | 29.0 | 23.7 | 23.5 | 24.17 |
