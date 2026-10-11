# Qwen3-4B on-policy 189: готовый парный SFT-набор

Статус на 11 октября 2026: masked-генерация от Qwen3-4B mixed401 выполнена
для всех 189 кандидатов. Собраны tagged и plain наборы, по 247 train и 50 val
строк на плечо. Парный SFT запущен; это не результат обучения.

## Источник и защита от утечек

- Кандидатный пул: 189 задач, 95 GSM8K и 94 MATH, в порядке
  `onpolicy46_candidates.jsonl`.
- Источник модели: tagged checkpoint Qwen3-4B mixed401, step 128; у каждой
  задачи сгенерирована одна masked-траектория.
- `qwen4b_onpolicy189_candidates.audit.json` исключает пересечения с
  onpolicy46, focus34, mixed401, сохранёнными SFT и fixed40. Проверены ID и
  нормализованные условия; среди выбранных задач совпадений нет.
- `leakcheck.py` проверил 189 задач против eval-корпуса: 0 блокирующих утечек.
  Сигналы с информационными наборами не являются пропуском проверки.

## Автоматический и ручной отбор

Из 189 генераций автоматический фильтр оставил 119 provisional и отклонил 70.
Причины отклонения пересекаются: `wrong_external_final` встречается у 61
строки, также встречаются незакрытый `<think>`, усечение, ненумерованные пути и
неполный Parallel-блок. Поэтому нельзя называть эти 119 или исходные 189
«90% качественных».

Все 119 provisional строк прочитаны по строгому критерию: два разных,
нетривиальных и верных независимых Path, Conclusion существенно объединяет их,
внешний ответ верен, а полный Parallel-блок находится внутри `<think>`.
Ранний срез прошёл первичное ручное чтение 22 строк и независимое чтение тех же
22; затем покрытие расширено до всех 119 строк отдельными ревью. Итог: 41 PASS,
78 FAIL. У 78 FAIL внешний ответ часто верен, но пути зависимы, тривиальны или
математически неверны.

Приняты 41 строки: 27 GSM8K и 14 MATH; типы ответов: 30 integer, 7 expression,
4 fraction. Решения и причины лежат в
`audit/qwen4b_onpolicy189_semantic_manifest.json` и ревью
`audit/qwen4b_onpolicy189_{early30_independent_review,review_a,review_b,review_c,review_d}.md`.

## Состав парных наборов

Каждое плечо получает:

- 123 positive: 41 принятая on-policy траектория, по 3 копии;
- 64 корректных, clean и неусечённых 4B thinking replay;
- 60 корректных, clean и неусечённых 4B native no-thinking replay.

Итого 247 train строк и 50 val строк на плечо. Tagged и plain имеют одинаковый
порядок и слова: plain получается только удалением тегов. Максимальная полная
длина: train 1580, val 3513 токенов. Пересечений train с val и fixed40 по
нормализованному условию нет.

Артефакты: `data/qwen4b_onpolicy189_{tagged,plain}_{train,val}.parquet`,
`audit/qwen4b_onpolicy189_pair_report.json`,
`eval_archives/qwen4b_onpolicy189_seed0/`.

## Проверяемый источник чисел

`audit/qwen4b_onpolicy189_pair_report.json` фиксирует состав, порядок, длины и
пересечения. `eval_archives/qwen4b_onpolicy189_seed0/summary.json` фиксирует
189 генераций, 119 provisional и 70 автоматических отклонений.

## Примеры принятых траекторий

`gsm8k-train/1362`. Полный исходный вопрос:

> Joanna and Jacques had 40 and 60 gumballs, respectively, in their dishes.
> They then purchased 4 times the number of gumballs they had initially and
> added these to their dishes. If they decided to put together their gumballs
> and shared them equally, how many gumballs did each get?

```text
<think>
Each person's final count is the initial number plus four times the initial number. Then the two counts are added and divided equally.

<Parallel>
<Goal>
<Outline>1: the number of gumballs Joanna had after buying more</Outline>
<Outline>2: the number of gumballs Jacques had after buying more</Outline>
</Goal>
<Path>
1: Joanna had 40 gumballs. She bought $4 \times 40 = 160$ more. Her final count is $40 + 160 = 200$.
</Path>
<Path>
2: Jacques initially had 60 gumballs. He bought $4 \times 60 = 240$ more, so he had $60 + 240 = 300$ gumballs.
</Path>
<Conclusion>
Joanna had 200 gumballs and Jacques had 300 gumballs after buying more. Together they had $200 + 300 = 500$ gumballs.
</Conclusion>
</Parallel>

Each got $500 \div 2 = 250$ gumballs.
</think>
Final Answer: 250
```

`math-train/1828`. Полный исходный вопрос:

> Two standard dice are rolled. What is the expected number of 1's obtained?
> Express your answer as a common fraction.

```text
<think>
The expected number is the sum over all outcomes of the probability of the outcome times the number of 1's in it. Each outcome is a pair of dice, so we consider the outcomes with 0, 1 or 2 ones.

<Parallel>
<Goal>
<Outline>1: the number of outcomes with no ones</Outline>
<Outline>2: the number of outcomes with exactly one 1</Outline>
</Goal>
<Path>
1: A die has 6 faces, so a die without a 1 has 5 faces. For two dice, the number of outcomes with no ones is $5\cdot 5=25$.
</Path>
<Path>
2: Exactly one die is 1. That die can be either of the two, and the other is from $\{2,3,4,5,6\}$. So there are $2\cdot5=10$ outcomes with exactly one 1.
</Path>
<Conclusion>
There are 25 outcomes with no ones and 10 outcomes with exactly one 1, for a total of $25+10=35$ outcomes.
</Conclusion>
</Parallel>

The remaining $36-35=1$ outcome has two ones. The expected value is
$$
\frac{25\cdot 0+10\cdot 1+1\cdot 2}{36}=\frac{12}{36}=\frac{1}{3}.
$$
</think>
Final Answer: $\frac{1}{3}$
```
