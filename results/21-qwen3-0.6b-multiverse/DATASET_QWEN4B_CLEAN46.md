# Qwen3-4B: 46 проверенных задач для SFT

11 октября 2026. **Набор готов; модель на нём ещё не обучалась.**
Блоки находятся внутри `<think>`. 32 ответа сгенерированы самой 4B с
независимой маской путей, ещё 14 ответов написаны заново после отбора
ошибочных генераций. Поле `output_provenance` различает эти источники.

## Отбор

| Шаг | Задач |
|---|---:|
| Новые вопросы GSM8K train и MATH train после leakcheck | 189 |
| Верный финал, полный блок, длина и отсутствие усечения | 119 |
| Первый смысловой просмотр сырых ответов | 41 |
| Повторный слепой просмотр сырых ответов | 36 |
| Полный независимый обзор всех 47 в следующей версии | 43 пригодных из 47 |
| Исправлено и повторно принято из четырёх отказов | 3 |
| Исключено как слишком простое для двух полезных путей | 1 |
| **Итоговых полезных решений** | **46** |

Первые 11 исправлений выбраны из 28 написанных по 78 смысловым отказам;
50 задач авторы сразу пропустили. Ещё три исправления сделаны после
полной проверки первой версии из 47. `math_verify` подтвердил финалы
всех написанных исправлений. Полный обзор старых 47 решений нашёл четыре
слабых пути при 47 верных финалах. Три новые версии прошли отдельное
слепое ревью **3/3**; `gsm8k-train/1856` осталась исключённой. Значит,
каждое из **46** итоговых решений прочитано независимым проверяющим и
признано полезным; это результат отбора, а не оценка доли пригодных
генераций. Протоколы:
`audit/qwen4b_onpolicy189_repaired47_blind30_review.md` и
`audit/qwen4b_onpolicy189_repair_batch_4_blind_review.md`.

Исходный пул прошёл `dataset_survey/scripts/leakcheck.py` против всех
используемых eval-наборов и полного MATH test, блокирующих совпадений 0.
GSM8K dev исключён до генерации. В составе 27 GSM8K и 19 MATH; типы
ответа: 30 integer, 11 expression, 5 fraction. Файлы происхождения:
`audit/qwen4b_onpolicy189_repair14_manifest.json`,
`audit/qwen4b_onpolicy189_repaired14_rollouts.jsonl`,
`audit/qwen4b_onpolicy189_clean46_manifest.json`. 14 отредактированных
ответов имеют `raw_model_generation=false`; остальные 175 записей в
полном файле 189 генераций не изменены.

## Парная сборка

В каждом плече **247 train** и **50 одинаковых val** строк. Положительные
46 задач предъявлены по три раза (138 строк). Подмешаны 55 верных
thinking и 54 верных no-thinking ответа 4B без тегов. В plain-плече из
каждой положительной строки удалены только структурные теги; слова,
числа, вопросы, порядок и replay совпадают. Проверены грамматика,
`<think>`-расположение, финал, валидность исходного leakcheck, отсутствие
пересечения вопросов с val и fixed40, предел 4096 токенов. Максимальная
полная строка: 1603 токена train и 3513 val. Машинный отчёт:
`audit/qwen4b_onpolicy189_clean46_pair_report.json`. Четыре parquet:
`data/qwen4b_onpolicy189_clean46_{tagged,plain}_{train,val}.parquet`.

## Пример новой правки

Задача `math-train/7012`: по параметризации прямой найти пару `(s,l)`.
Пути проверяют разные свойства прямой: первый наклон, второй точку при
`t=0`. Они не видят результат друг друга при обучении.

```text
<think>
<Parallel>
<Goal>
<Outline>1: Determine $l$ from the direction of the parametrized line.</Outline>
<Outline>2: Determine $s$ from the base point of the parametrized line.</Outline>
</Goal>
<Path>1: The direction vector is $(l,-5)$, so its slope is $-5/l$. It must equal the line's slope $1/2$, hence $-5/l=1/2$. Solving gives $l=-10$.</Path>
<Path>2: At $t=0$, the parametrization gives the point $(-7,s)$ on the line. Substitution into $y=\frac12x+4$ gives $s=\frac12(-7)+4=\frac12$.</Path>
<Conclusion>The direction condition gives $l=-10$, and the base-point condition gives $s=\frac12$. Together they give $(s,l)=\left( \frac{1}{2}, -10 \right)$.</Conclusion>
</Parallel>
</think>
Final Answer: $\left( \frac{1}{2}, -10 \right)$
```

Полный вопрос и остальные исправления находятся в
`audit/qwen4b_onpolicy189_repair_batch_4_drafts.jsonl`. Версия из 47
положительных задач сохранена только для аудита и не должна обучаться.
