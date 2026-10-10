# Новый источник собственных thinking-трасс Qwen

10 октября 2026. Предварительная подготовка входов, без нового SFT и без расходов VK AI Proxy. Цель: получить длинные собственные решения Qwen3-0.6B, в которых независимые вычисления уже стоят отдельными частями; затем текстовые исполнители вставят только план и теги внутрь `<think>`. Качество решает отбор, а не целевое число строк.

Источник вопросов: `data/more_m2_new_inputs.jsonl`, где исходная Qwen раньше правильно решила задачи в no-thinking. Старые ответы не передаются генератору thinking и не становятся учебными целями. Исключены ID всех принятых M1/M2, их добавок 180+180, replay, Sol deep75 и ранее размеченных Qwen-трасс. `scripts/exp21/select_structured_thinking_inputs.py` с seed 20261010 взял 1500 новых ID: 550 GSM8K integer, 600 MATH integer, 230 MATH expression, 120 MATH fraction. Эталоны в `inputs1500_with_gold.jsonl` нужны только для последующей проверки ответа.

`dataset_survey/scripts/leakcheck.py` v2 нашёл 0 утечек против всех наших eval, но 11 слабых совпадений с полным MATH test. Они исключены. Дополнительно исключены пять задач с сильным совпадением или Jaccard ≥0,6 с полным MATH test, включая шаблон вида `sqrt(x+a)=b`. Осталось **1484 входа**: 550 GSM8K integer, 593 MATH integer, 225 expression, 116 fraction. Повторная проверка `leakcheck_inputs_clean.summary.json` даёт 0 утечек против наших eval и полного MATH test, 0 точных дублей и вариантов eval. Информационный корпус MATH train содержит ожидаемые совпадения и не является eval. Список исключений: `excluded_math_test.json`.

Промпты thinking для этих 1484 задач содержат 109–357 токенов по подготовленному токенизатору Qwen; все помещаются в окно генерации 5120 токенов с лимитом ответа 4096. Это проверка входа, не гарантия пригодности длинного выхода для SFT.

После завершения полной парной оценки и масочного пилота на собственном pod `vcharkin-exp-vm-0` в 04:29 МСК запущен один GPU-процесс PID 40859:

```sh
nohup bash /work/exp21/qwen_structured_thinking/run_qwen_structured_thinking_pod.sh > /work/exp21/qwen_structured_thinking/wrapper.log 2>&1 < /dev/null &
```

`generate_pool.py` использует для thinking промпт с необязательными `Part 1:`/`Part 2:` без XML-тегов; режим и параметры Qwen зафиксированы в этом скрипте. Сначала `grade_gen.py` отбросит неверный ответ, обрезание и испорченную структуру `<think>`. Далее будет отдельный строгий просмотр независимости частей и математических шагов; до него эти 1484 входа не считаются обучающими примерами. VK AI Proxy не вызывается, новых расходов из лимита $200 нет.

Подготовка входов воспроизводится из корня ветки:

```sh
python3 -B scripts/exp21/select_structured_thinking_inputs.py
/tmp/exp21-audit-venv/bin/python -B /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/scripts/leakcheck.py results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking/inputs1500_with_gold.jsonl results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking/leakcheck_inputs1500 --corpus /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/eval_corpus
python3 -B scripts/exp21/filter_structured_thinking_leaks.py
/tmp/exp21-audit-venv/bin/python -B /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/scripts/leakcheck.py results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking/inputs_clean_with_gold.jsonl results/21-qwen3-0.6b-multiverse/audit/qwen_structured_thinking/leakcheck_inputs_clean --corpus /Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/dataset_survey/eval_corpus
```

## Итог генерации и просмотра

Генерация на одном H100 завершилась в 04:34 МСК. Из 1484 ответов автоматическая проверка сохранила **1194 верных финальных ответа** с целым `<think>` и без обрезания. Только **149** из них содержали `Part 1:` и `Part 2:` в нужном порядке внутри рассуждения. Это кандидаты, а не готовый датасет: `candidate_screen.json`, `candidates149_blind.jsonl`, `generated.jsonl`, `graded.jsonl`. Сырые файлы и журналы также сохранены в `qwen_structured_generation.tgz`.

Три исполнителя Sol 6.1 независимо от эталонов прочитали все 149 полных вопросов и ответов. Их оценки: **16 полезных**, 68 слабых, 65 с ошибками рассуждения. Наличие верного финального ответа часто скрывало ложный промежуточный шаг или зависимость между названными частями. Примеры, причины отсева и все решения находятся в `agent_{a,b,c}/screen.jsonl`, `tagged.jsonl`, `review.md`.

Второй независимый проверяющий прочитал все 16 размеченных ответов уже с эталонами. Финальный ответ верен в 16/16, синтаксис и нумерация тегов проходят 16/16, исходный текст и порядок сохранены 16/16, пути независимы 16/16. Но **строгий семантический приём равен 0/16**: каждый вновь добавленный `<Conclusion>` лишь предлагает объединить части, а само объединение остаётся после `</Parallel>`. Кроме того, два исходных трейса содержат неточные математические формулировки, два являются независимыми проверками одного ответа вне текущего узкого промпта, а у одного нет строки `Final Answer:`. Эти проблемы нельзя скрывать автоматической проверкой грамматики. Построчные вердикты и воспроизводимая проверка: `independent_review/`.

**Решение:** эти 16 не включать в SFT в текущем виде. Честная правка потребует перенести границу `Conclusion` на существующий текст объединения без переписывания ответа и заново независимо проверить все строки. До такой правки качественный выход новой генерации равен нулю, несмотря на 1194 верных финальных ответа. Новых расходов VK AI Proxy нет.
