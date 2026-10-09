# Пилот: подробные решения Sol 6.1 с блоками внутри `<think>`

Статус 10 октября 2026: 24 принятых примера, **в SFT пока не включены**. Это проверка качества нового источника длинных математических объяснений и подхода «только план». На вызовы VK AI Proxy потрачено $0; текстовые субагенты и проверка токенизатором не запускали второй GPU-процесс.

## Источник и отсев

Исходный пул: `data/pool.jsonl`, задачи MATH train после вычитания GSM8K dev, наших eval и ранее принятого набора. Для пилота дополнительно исключены 187 принятых Sol, expanded M1/M2, 594 фактических Qwen replay и первые 20 пробных задач. Из допустимых задач с уровнями 3–5 и длиной вопроса 130–1000 символов отобраны 120 слепых вопросов, по 40 с целым, дробным и символьным эталоном. Структурный фильтр искал задачи с составными вычислениями, но не принимал решение о правильности ответа.

| Шаг | Осталось | Причина отсева |
|---|---:|---|
| Слепая выборка | 120 | Стратификация по типу ответа |
| Независимые полезные части по условию | 30 | 90 задач зависимые или слишком короткие для двух путей |
| Основной список | 25 | 2 в резерве; 3 структурно годных исключены по слабым совпадениям с MATH test |
| Математически решены | 24 | `math-train/3423` противоречива: `x=-1` требует `f(-1)=0`, но кодомен исключает 0 |
| Размечены и независимо приняты | 24 | 7 целых, 8 дробных, 9 символьных эталонов |

Среди 120 проверка `dataset_survey/scripts/leakcheck.py` не нашла утечек по своему порогу, но вручную исключены пять слабых совпадений с полным MATH test: train ID `2052`, `3758`, `501`, `3538`, `2368`. Для финальных 24: 0 сигналов утечки против наших eval, 0 дублей или вариантов полного MATH test, 0 даже слабых совпадений с MATH test (`audit/deep_trace_pilot/leakcheck_accepted24.summary.json`). 17 совпадений с информационным корпусом MATH train записаны отдельно; он не является eval-набором. История отбора: `screen120_selection.json`, `screen120_review.jsonl`, `selected25_manifest.json`.

## Проверка ответов и блоков

Sol 6.1 писал публичные математические объяснения, не видя эталонов. Средняя длина объяснения 1277 символов; у прежних 187 Sol она была около 725. 23/24 финальных ответов напрямую подтверждены `math_verify`. В `math-train/2326` вопрос требует букву; ответ `C` преобразован по явным вариантам вопроса в `0.20` и затем сопоставлен с эталоном. Каждый шаг всех 24 решений прочитан координатором и независимыми проверяющими; вычислительных ошибок среди принятых не обнаружено. Исходные решения: `audit/deep_trace_pilot/accepted24_source_blind.jsonl`, построчный аудит: `accepted24_audit.json`, независимые ревью: `review25_{a,b}.jsonl`.

Другие текстовые исполнители вставили **только** `<Parallel>`, `<Goal>`, два нумерованных `<Outline>`, два нумерованных `<Path>` и `<Conclusion>` внутрь существующего `<think>`. После удаления добавленного плана и тегов исходные объяснения, все числа и финальные ответы восстанавливаются дословно с точностью до пробелов. 24/24 имеют ровно один грамматически правильный нумерованный блок и два содержательно независимых пути; кратчайший путь 158 символов. 22/24 проходят прежний автоматический `checks.py` целиком. В двух оставшихся единственный сигнал `xref` ложный: `imaginary part 4*c*s` ошибочно читается как ссылка на «part 4», а `Likewise` в `math-train/5272` относится к рассуждению **внутри того же пути**. Оба случая независимо прочитаны и записаны в `tagged24_a_review.md`; исходный текст сохранён.

Токенизатор подготовленной Qwen3-0.6B с десятью различно инициализированными спецтокенами посчитал полный SFT-ряд через тот же `build_sft.row('parallel_th', ...)` и chat template: минимум 545, среднее 713, максимум 873 токена, 0/24 длиннее лимита 4096 (`token_lengths24.json`). Проверка сделана на CPU собственного pod во время одного GPU-прогона оценки. В обучение эти 24 пока не добавлены.

Полные размеченные ответы: `audit/deep_trace_pilot/tagged24.jsonl`. Независимые проверки вставки тегов: `tagged24_{a,b}_review.jsonl`. Промежуточные и отвергнутые случаи сохранены в `audit/deep_trace_pilot/README.md` и соседних JSONL.

## Пример из обучения, `math-train/6288`

**Вопрос.** Four concentric circles are drawn with radii of 1, 3, 5 and 7. The inner circle is painted black, the ring around it is white, the next ring is black and the outer ring is white. What is the ratio of the black area to the white area? Express your answer as a common fraction.

**Целевой ответ.** Оба цвета вычисляются без доступа к результату соседнего пути; отношение считается после блока.

```text
<think>
A disk of radius R has area pi R^2, and an annulus between radii r and R has area pi(R^2-r^2). Identify the black and white regions from the ordered radii, then calculate each color independently.

<Parallel>
<Goal>
<Outline>1: Calculate the total area of the black regions.</Outline>
<Outline>2: Calculate the total area of the white regions.</Outline>
</Goal>
<Path>1: Calculation 1: Black consists of the inner disk of radius 1 and the annulus between radii 3 and 5. The disk contributes pi, while the annulus contributes pi(5^2-3^2)=16pi. These disjoint black regions have total area 17pi.

</Path>
<Path>2: Calculation 2: White consists of the annulus between radii 1 and 3 and the annulus between radii 5 and 7. Their areas are pi(3^2-1^2)=8pi and pi(7^2-5^2)=24pi. Adding these directly, without using the black total, gives white area 32pi.</Path>
<Conclusion>Use the color totals in the requested ratio.</Conclusion>
</Parallel>

The requested black-to-white ratio is 17pi/(32pi)=17/32. Numerator and denominator have no common factor, so this already is a common fraction in lowest terms.
</think>
Final Answer: \frac{17}{32}
```

## Воспроизведение ключевых проверок

Финальный вход leakcheck `audit/deep_trace_pilot/accepted24_with_gold.jsonl` содержит ID, вопрос и эталон из исходного пула. Команда:

```bash
/tmp/exp21-audit-venv/bin/python -B /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/scripts/leakcheck.py \
  /Users/v.charkin/Documents/dev/projects/parallel-r1-exp21/results/21-qwen3-0.6b-multiverse/audit/deep_trace_pilot/accepted24_with_gold.jsonl \
  /Users/v.charkin/Documents/dev/projects/parallel-r1-exp21/results/21-qwen3-0.6b-multiverse/audit/deep_trace_pilot/leakcheck_accepted24 \
  --corpus /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/eval_corpus
```
