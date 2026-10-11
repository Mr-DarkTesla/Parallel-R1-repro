# Qwen3-4B: 47 проверенных параллельных решений

11 октября 2026. **Данные подготовлены, SFT ещё не запущен.** Цель этой
версии: сохранить 36 дважды проверенных собственных masked-траекторий
4B и добавить только те ручные исправления, в которых два пути
действительно работают независимо. Исправленные решения нельзя
называть сырыми генерациями Qwen.

## Происхождение и отсев

| Этап | Строк |
|---|---:|
| Новые задачи MATH train и GSM8K train, прошедшие leakcheck | 189 |
| Масочная генерация 4B: верный ответ, грамматика, длина | 119 |
| Первое смысловое ревью: принятые сырые решения | 41 |
| Второе слепое ревью этих 41: окончательно принятые | 36 |
| Из 78 смысловых отказов передано трём авторам на правку | 78 |
| Авторы пропустили задачи без честного параллельного разбиения | 50 |
| Написано полных исправленных решений | 28 |
| Слепое ревью и личное чтение приняли исправлений | 11 |
| Итог: разных задач с качественным блоком | **47** |

У всех 28 написанных правок финальный ответ совпал с gold при
`math_verify`; 17 отвергнуты из-за слабого второго пути, повторов или
неиспользованного результата. Слепые решения:
`audit/qwen4b_onpolicy189_repair_batch_1_2_blind_review.md` и
`audit/qwen4b_onpolicy189_repair_batch_3_blind_review.md`.
Дополнительное чтение всей третьей партии исключило ещё два ложных
принятия: `audit/qwen4b_onpolicy189_repair_batch_3_primary_review.md`.
Из второй партии принят ровно один пример; пропуски документированы
в отдельных `...notes.md`. Все 47 итоговых строк имеют верный финал и
прошли независимый смысловой просмотр.

Источники вопросов и gold: тот же зафиксированный пул `data/qwen4b_onpolicy189_candidates.jsonl`.
GSM8K dev был исключён до генерации. `dataset_survey/scripts/leakcheck.py`
не нашёл блокирующих совпадений ни с нашими eval-наборами, ни с полным
MATH test. Состав: 28 GSM8K, 19 MATH; по типу ответа 31 integer,
11 expression, 5 fraction.

Каждая правка записана отдельно от исходного Qwen-ответа с полем
`output_provenance.raw_model_generation=false`, ссылкой на черновик и
решение ревью. Ассемблер оставляет 178 из 189 ответов без изменений и
заменяет только 11 утверждённых ID. После замены тот же строгий
`filter_onpolicy_rollouts.py` нашёл все 11 среди 119 структурно и по
ответу пригодных строк. Манифесты: `audit/qwen4b_onpolicy189_repair11_manifest.json`
и `audit/qwen4b_onpolicy189_repaired47_manifest.json`; исходные и
собранные выходы: `audit/qwen4b_onpolicy189_repair_batch_*_drafts.jsonl`
и `audit/qwen4b_onpolicy189_repaired11_rollouts.jsonl`.

## Парные данные SFT

Оба плеча содержат по **247 train** и **50 одинаковых val** строк:
47 положительных решений по три копии, 53 верных собственных thinking
и 53 верных собственных no-thinking ответов 4B. В tagged-плече блоки
находятся внутри `<think>`; plain удаляет только десять типов тегов,
сохраняя слова и порядок. Проверены совпадение ID и текстов без тегов,
отсутствие пересечений вопросов с val и fixed40, leakcheck и лимит
4096 токенов. Максимальная полная train-строка 1580 токенов.
Точные данные: `data/qwen4b_onpolicy189_repaired47_{tagged,plain}_{train,val}.parquet`.
Машинный отчёт: `audit/qwen4b_onpolicy189_repaired47_pair_report.json`.

## Пример новой правки

Вопрос `math-train/5103` полностью:

> A roll of quarters contains $40$ quarters and a roll of dimes contains
> $50$ dimes. James has a jar that contains $83$ quarters and $159$ dimes.
> Lindsay has a jar that contains $129$ quarters and $266$ dimes. James
> and Lindsay pool these quarters and dimes and make complete rolls with
> as many of the coins as possible. In dollars, how much are the leftover
> quarters and dimes worth?

```text
<think>
Compute leftover quarters and leftover dimes independently, then value them.
<Parallel>
<Goal>
<Outline>1: find the value of leftover quarters after making 40-coin rolls</Outline>
<Outline>2: find the value of leftover dimes after making 50-coin rolls</Outline>
</Goal>
<Path>
1: There are 83 + 129 = 212 quarters. Five rolls use 5 × 40 = 200, leaving 12 quarters worth 12 × $0.25 = $3.00.
</Path>
<Path>
2: There are 159 + 266 = 425 dimes. Eight rolls use 8 × 50 = 400, leaving 25 dimes worth 25 × $0.10 = $2.50.
</Path>
<Conclusion>
The leftover coin values add to $3.00 + $2.50 = $5.50.
</Conclusion>
</Parallel>
</think>
Final Answer: $5.50
```

Ещё два полных исходных примера и ответы без исправлений:
`DATASET_QWEN4B_ONPOLICY189.md`.
