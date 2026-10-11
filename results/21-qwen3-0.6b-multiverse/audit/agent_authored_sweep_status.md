# Agent-authored tagged/plain fixed40 sweep: status

Подготовлен отдельный fail-closed анализатор:

```bash
python3 -B scripts/exp21/compare_agent_authored_sweep.py
```

Он ожидает архивы `agent_authored_{tagged,plain}_p8_step{1..8}_masked_pilot.tgz`, проверяет идентичность 40 prompt и `masked` decoder, сравнивает tagged с plain на том же step и обе ветви с исправленным C0. Для каждой пары отдаёт 10 000 paired bootstrap 95% CI по raw accuracy, syntax blocks, truncation, tokens и forward passes; GSM8K/MATH показаны отдельно.

Семантическая external accuracy и strict useful blocks намеренно остаются `pending`, пока появится полный review manifest. В нём должны быть все строки с numbered block и документированные override raw scorer. Скрипт не выводит strict useful на основании одной только грамматики.

На момент создания этих файлов локальные archives agent-authored отсутствуют, поэтому таблица результатов и выбор лучшего шага ещё не сформированы. После pull архива нужно запустить команду выше, выбрать step только по raw таблице как provisional, вручную проверить полный текст всех попыток block у выбранного step и затем заполнить `agent_authored_sweep_manual_reviews.json` до повторного запуска.
