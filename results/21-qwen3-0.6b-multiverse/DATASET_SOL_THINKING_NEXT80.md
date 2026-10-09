# Карточка: Sol 6.1, вторая партия внутренних блоков

Статус: **68 проверенных примеров**, до обучения. Это отдельный способ получить публичные рассуждения внутри `<think>`: Sol 6.1 решает задачу без эталона, другой Sol 6.1 задаёт только границы и план параллельного блока. Сборщик сохраняет исходные слова, формулы и числа в вычислительных путях. Это не M1 Claude и не M2 на собственном тексте Qwen.

## Источник и отсев

Вопросы взяты из очищенного `data/pool.jsonl`: 40 MATH train и 40 GSM8K train. В файле для исполнителей `audit/think_trace_sol/decomposable80_next.jsonl` эталонных ответов нет. Ранее размеченные задачи, replay и validation исключены; с предыдущими 29 принятыми строками пересечений нет. GSM8K dev удалён ещё при сборке пула.

| Этап | Число | Проверка |
|---|---:|---|
| Отобранные задачи | 80 | Декомпозируемость по условию, уникальные ID |
| Самостоятельные решения | 79 | `gsm8k-train/1213` исключён: формулировка «насколько больше у Lyssa» противоречит числам, у неё на 3 верных ответа меньше |
| Верный итог по `checks.correct` | 79 | Сопоставление с gold после генерации, `next80_trace_answer_precheck.jsonl` |
| Независимые пути и автоматические проверки | 69 | 10 честных `no_block`; 0 ошибок грамматики, ответа, дословности или длины среди 69 |
| Независимое чтение 30 случайных, поровну MATH/GSM8K | **30/30** | У всех верный ответ, верное рассуждение и полезный блок |
| Полное чтение оставшихся 39 | **38/39** | Лично 20/20; другой рецензент 18/19, `gsm8k-train/1028` исключён за неполное разложение |
| Итог после чтения всех | **68** | У всех итоговых строк верны ответ и рассуждение; блок признан полезным |

Протоколы чтения: `audit/think_trace_sol/next80_independent_review30.jsonl`, `next80_personal_review20.jsonl`, `next80_review_remaining19_verdict.jsonl`. Один дополнительный пример `gsm8k-train/1028` имел верный ответ, но расчёт олова впервые появляется после блока; для строгой полноты разложения его исключили. Сводка решения: `audit/think_trace_sol/final_review_and_selection.json`.

У 69 автоматически принятых: 36 MATH, 33 GSM8K; 44 целых, 14 дробей и 11 выражений. Блоков с двумя путями 66, с тремя путями 3. Средняя длина промпта и ответа по токенизатору Qwen 436,2 токена, максимум 534 при лимите 4096. Финальные **68** строк после полного чтения: `audit/think_trace_sol/next80_final.jsonl`.

## Утечки

`dataset_survey/scripts/leakcheck.py` v2 проверил все 80 исходных задач против наших eval-наборов и полного MATH test: 0 утечек против eval, 0 дублей и близких вариантов MATH test. Два слабых совпадения с MATH test просмотрены вручную: `math-train/2359` и `math-test/1476` задают разные вероятностные события; `math-train/2419` и `math-test/1558` оба про бутерброды, но первый считает сочетания с запретами, второй спрашивает вероятность аллергии при других ингредиентах. Сводка: `audit/think_trace_sol/leakcheck80_next.summary.json`, пары в `.hits.jsonl`.

## Пример

`math-train/2349`: в каждом из двух ящиков по 20 плиток. Требуется вероятность, что плитка из A меньше 15, а плитка из B чётная или больше 25. Условия по разным ящикам можно вычислить независимо.

```text
<think>
<Parallel>
<Goal>
<Outline>1: Find the qualifying fraction of numbers in box A.</Outline>
<Outline>2: Count the qualifying numbers in box B.</Outline>
</Goal>
<Path>
1: Box A contains the numbers 1 through 20. Exactly 1 through 14 are less than 15, so the event concerning A has probability 14/20=7/10.
</Path>
<Path>
2: In B, the even numbers from 11 through 30 are 12,14,...,30, ten numbers. The numbers greater than 25 are 26 through 30, five numbers; 26,28,30 appear in both groups. Hence the union has 10+5-3=12 numbers.
</Path>
<Conclusion>
Multiply the independent event probabilities.
</Conclusion>
</Parallel>

The draws come from separate boxes, so the two conditions are independent. Their joint probability is (14/20)(12/20)=21/50.
</think>
Final Answer: 21/50
```

## Применение

Данные готовы для CPU-подготовки SFT и контроля `control_th` на тех же текстах без тегов. Обучение и оценка этой партии ещё не проводились. Результаты прошлых M1/M2 не являются оценкой этой партии. По данным разметки нельзя утверждать, что модель научилась генерировать внутренние блоки или сохранила IFEval.
