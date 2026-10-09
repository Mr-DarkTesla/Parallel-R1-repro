# Подробные решения Sol 6.1: 51 блок внутри `<think>`

10 октября 2026. Этот набор пока не участвовал в SFT. Текст создан субагентами Sol 6.1 без GPU и без VK AI Proxy; расход по лимиту прокси: $0. Эталоны ответов были скрыты при решении и разметке.

## Источник и отсев

Исходный корпус: MATH train из `data/pool.jsonl`. Перед отбором исключены GSM8K dev, все наши eval, ранее принятые 187 Sol, expanded M1/M2, собственные верные replay Qwen и предыдущий пилот. Требовались уровень MATH 3–5, длина вопроса 130–1000 символов, отсутствие `[asy]` и возможность разделить вычисление на содержательные независимые части. Seed `20261011` дал 445 кандидатов. После проверки полного MATH test исключены 18 слабых совпадений; seed `20261012` сформировал слепую выборку 400 с 160 целыми, 115 дробными и 125 символьными ответами.

| Этап | Число | Решение |
|---|---:|---|
| Слепая выборка | 400 | Без эталонов у четырёх проверяющих |
| Предварительно параллелизуемы | 57 | Две содержательные ветви по условию |
| Переданы на решение | 52 | Пять с признаками неоднозначного условия исключены |
| Ответ и математика проверены | 52 | 51 совпадает с gold; у `math-train/6780` исходный gold пропускает правильное `k=12` и задача исключена |
| План вставлен внутрь `<think>` | 51 | Исходный текст не переписан |
| Приняты после независимого ревью | 51 | 23 целых, 10 дробных, 18 символьных ответов |

Статусы всех 400 и причины предварительного отсева есть в `audit/deep_trace_round2/screen400_all_review.jsonl`. Исходные решения и отдельное математическое ревью лежат в `traces52_{a,b,c}.jsonl` и `review52_{a,b,c}.jsonl`.

Проверка `dataset_survey/scripts/leakcheck.py` выполнена для финальных 51 против **всех наших eval** и **полного MATH test**: 0 утечек, 0 дублей или вариантов eval, 0 совпадений уровня утечки с MATH test. Есть 20 слабых общих восьмиграмм с MATH test без уровня совпадения вопроса, и 26 точных совпадений с информационным корпусом MATH train; последний не является eval-набором. Полный вывод: `audit/deep_trace_round2/leakcheck_accepted51.summary.json`, вход проверки: `accepted51_with_gold.jsonl`.

## Качество и сохранность текста

Независимые проверяющие прочитали математические шаги всех 52 исходных решений. Для принятых 51: **51/51 верных ответов**, **51/51 полезных и независимых блоков** после исправления двух найденных дефектов маршрутизации. Первый дефект `math-train/7467`: итог двух ветвей стоял внутри второй; предложение вынесено после блока. Второй `math-train/3860`: две части одного случая сначала были разделены между вторым и третьим путём; они объединены. Оба исправления повторно приняты независимыми проверяющими. В первоначальном ревью полезность была 49/51, то есть 96,1%, при нуле неверных ответов.

Автоматическая проверка `scripts/exp21/finalize_deep_round2.py` подтверждает для каждого примера грамматику, нумерацию, один блок внутри `<think>`, два содержательных пути не короче 80 символов, верный финальный ответ, отсутствие ссылок на соседнюю ветвь и дословное восстановление исходного решения после удаления служебного плана и тегов с нормализацией пробелов. **51/51 проходят все проверки**. `checks.py` исправлен так, чтобы начальный заголовок собственной ветви `Part 1:` не считался ссылкой на соседнюю.

По токенизатору подготовленной Qwen3-0.6B полный обучающий ряд с chat template содержит **521–1201 токен**, среднее **691,7**; 0/51 длиннее лимита 4096 (`audit/deep_trace_round2/token_lengths51.json`). Проверка сделана на CPU собственного pod; второй GPU-процесс не запускался.

Финальные размеченные ответы: `audit/deep_trace_round2/accepted51.jsonl`; построчная проверка: `accepted51_audit.jsonl`; независимое ревью разметки: `tagged52_{a,b,c}_review.jsonl`; краткий машинный итог: `accepted51_summary.json`.

## Пример: два треугольника

**Вопрос.** Quadrilateral $ABCD$ has right angles at $B$ and $D$, and $AC=3$. If $ABCD$ has two sides with distinct integer lengths, then what is the area of $ABCD$? Express your answer in simplest radical form.

**Ответ.** Общая часть выводит два возможных целых катета. Каждый путь независимо находит площадь своего прямоугольного треугольника; сложение идёт после блока.

```text
<think>
Draw diagonal AC. Right angles at B and D make triangles ABC and ADC right triangles, each with hypotenuse 3. Every side of the quadrilateral is a positive leg shorter than 3, so its only possible integer lengths are 1 and 2. Two distinct integer side lengths therefore mean both 1 and 2 occur. They cannot lie in the same right triangle, since 1^2+2^2=5 rather than 3^2=9. Thus one triangle contains a leg of length 1 and the other a leg of length 2.

<Parallel>
<Goal>
<Outline>1: Compute area of the right triangle containing integer leg 1.</Outline>
<Outline>2: Compute area of the right triangle containing integer leg 2.</Outline>
</Goal>
<Path>1: Part 1. For the triangle with leg 1, the Pythagorean theorem gives its other leg as sqrt(3^2-1^2)=sqrt(8)=2sqrt(2). Its area is half the product of the perpendicular legs: (1/2)(1)(2sqrt(2))=sqrt(2).

</Path>
<Path>2: Part 2. For the triangle with leg 2, its other leg is sqrt(3^2-2^2)=sqrt(5). Its area is (1/2)(2)(sqrt(5))=sqrt(5). This calculation depends only on the common hypotenuse and the larger integer leg.

</Path>
<Conclusion>Combine the two independent calculations.</Conclusion>
</Parallel>

The diagonal partitions the quadrilateral into these triangles. Add their areas to obtain sqrt(2)+sqrt(5).
</think>
Final Answer: \\sqrt{2}+\\sqrt{5}
```

История команд отбора и проверки: `audit/deep_trace_round2/README.md`. Финализация воспроизводится командой `python -B scripts/exp21/finalize_deep_round2.py` из корня репозитория.
