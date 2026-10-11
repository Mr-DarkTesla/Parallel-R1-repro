# Teacher trajectory paragraph transform

Статус: **proposal_only**. Из 203 raw teacher candidates
консервативно предложены 66 блока. Ни одна строка не
принята в SFT: до обучения нужны независимое semantic review, проверка ответа
и отдельный leakcheck итогового выбранного поднабора.

Transformer сохраняет дословные три исходных reasoning-абзаца: первые два
помещает в `Path 1/2`, третий помещает в `Conclusion`, а внешний `Final Answer:`
оставляет после `</think>`. Добавляются только теги и два Outline. В Goal не
попадают числа, формулы или внешний ответ.

## Автоматические gates

- raw trace: ровно один `<think>`, без прежних Parallel-тегов;
- ровно три абзаца; оба Path не короче 80 символов;
- второй Path не содержит явной ссылки на предыдущий результат;
- есть явный linguistic marker независимости и комбинационная операция в
  третьем абзаце;
- generated response проходит `mv_format.parse`, нумерацию, placement тега и
  сохранение external answer.

| Teacher source | Proposals |
| --- | ---: |
| `results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/next120_traces_checked.jsonl` | 32 |
| `results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/next80_traces_checked.jsonl` | 23 |
| `results/21-qwen3-0.6b-multiverse/audit/think_trace_sol/noninteger60_traces_checked.jsonl` | 11 |

## Пропущенные кандидаты

Каждый пропуск сохранён ниже с причиной, чтобы повторный запуск не превращал
неоднозначный текст в искусственный параллельный пример.

| ID | Причина |
| --- | --- |
| `gsm8k-train/1130` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1231` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1344` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1408` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1508` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/1548` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1551` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/1558` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1565` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1674` | combination paragraph is shorter than 40 characters |
| `gsm8k-train/1678` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1922` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1938` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/1942` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/1981` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/1988` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/2048` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/2084` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/2114` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/2121` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/2145` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/2193` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/2212` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/2232` | expected exactly 3 reasoning paragraphs, found 4 |
| `gsm8k-train/2249` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/2360` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/245` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/293` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/45` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/481` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/573` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/58` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/604` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/616` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/634` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/660` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/682` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/781` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/798` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/840` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/857` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/873` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/896` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/908` | expected exactly 3 reasoning paragraphs, found 1 |
| `gsm8k-train/922` | no explicit linguistic evidence that first two paragraphs are independent |
| `gsm8k-train/925` | third paragraph lacks an explicit combination operation |
| `gsm8k-train/994` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1097` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/125` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/144` | third paragraph lacks an explicit combination operation |
| `math-train/1604` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1655` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1708` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1753` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1760` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1818` | third paragraph lacks an explicit combination operation |
| `math-train/1825` | third paragraph lacks an explicit combination operation |
| `math-train/1844` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1849` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1869` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1881` | third paragraph lacks an explicit combination operation |
| `math-train/1910` | third paragraph lacks an explicit combination operation |
| `math-train/1949` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/1957` | third paragraph lacks an explicit combination operation |
| `math-train/2001` | third paragraph lacks an explicit combination operation |
| `math-train/2021` | third paragraph lacks an explicit combination operation |
| `math-train/2060` | third paragraph lacks an explicit combination operation |
| `math-train/2184` | third paragraph lacks an explicit combination operation |
| `math-train/219` | third paragraph lacks an explicit combination operation |
| `math-train/2234` | third paragraph lacks an explicit combination operation |
| `math-train/2246` | third paragraph lacks an explicit combination operation |
| `math-train/2273` | third paragraph lacks an explicit combination operation |
| `math-train/2293` | third paragraph lacks an explicit combination operation |
| `math-train/2294` | third paragraph lacks an explicit combination operation |
| `math-train/2336` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2349` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2359` | third paragraph lacks an explicit combination operation |
| `math-train/2364` | third paragraph lacks an explicit combination operation |
| `math-train/2371` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2373` | expected exactly 3 reasoning paragraphs, found 4 |
| `math-train/2381` | third paragraph lacks an explicit combination operation |
| `math-train/2386` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2409` | expected exactly 3 reasoning paragraphs, found 4 |
| `math-train/2411` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2416` | third paragraph lacks an explicit combination operation |
| `math-train/2418` | third paragraph lacks an explicit combination operation |
| `math-train/2419` | third paragraph lacks an explicit combination operation |
| `math-train/2427` | expected exactly 3 reasoning paragraphs, found 4 |
| `math-train/2432` | expected exactly 3 reasoning paragraphs, found 4 |
| `math-train/2445` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2450` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2453` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2454` | combination paragraph is shorter than 40 characters |
| `math-train/2459` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2468` | third paragraph lacks an explicit combination operation |
| `math-train/2486` | third paragraph lacks an explicit combination operation |
| `math-train/253` | third paragraph lacks an explicit combination operation |
| `math-train/256` | third paragraph lacks an explicit combination operation |
| `math-train/2563` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2589` | third paragraph lacks an explicit combination operation |
| `math-train/2595` | combination paragraph is shorter than 40 characters |
| `math-train/2597` | third paragraph lacks an explicit combination operation |
| `math-train/2601` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2604` | combination paragraph is shorter than 40 characters |
| `math-train/2679` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2723` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2742` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2743` | combination paragraph is shorter than 40 characters |
| `math-train/2804` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2807` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2829` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2835` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2840` | third paragraph lacks an explicit combination operation |
| `math-train/2851` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2878` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2884` | combination paragraph is shorter than 40 characters |
| `math-train/2899` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/2905` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/3045` | third paragraph lacks an explicit combination operation |
| `math-train/3054` | third paragraph lacks an explicit combination operation |
| `math-train/3456` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/3509` | third paragraph lacks an explicit combination operation |
| `math-train/3511` | third paragraph lacks an explicit combination operation |
| `math-train/3518` | third paragraph lacks an explicit combination operation |
| `math-train/3537` | third paragraph lacks an explicit combination operation |
| `math-train/3672` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/377` | combination paragraph is shorter than 40 characters |
| `math-train/405` | combination paragraph is shorter than 40 characters |
| `math-train/458` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/5936` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/6553` | third paragraph lacks an explicit combination operation |
| `math-train/6840` | third paragraph lacks an explicit combination operation |
| `math-train/6864` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/7264` | third paragraph lacks an explicit combination operation |
| `math-train/765` | third paragraph lacks an explicit combination operation |
| `math-train/799` | no explicit linguistic evidence that first two paragraphs are independent |
| `math-train/954` | third paragraph lacks an explicit combination operation |

## Проверка

`response` в JSONL остаётся только предложением (`proposal_not_accepted`).
В нём нет изменений чисел и слов исходных reasoning-абзацев; проверка не
доказывает содержательную независимость. GPU, proxy и платные вызовы не
использовались.

```bash
python3 -B scripts/exp21/convert_teacher_trajectories.py
```
