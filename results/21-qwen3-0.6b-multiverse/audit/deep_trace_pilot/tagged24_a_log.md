# Разметка accepted24_source_a

Источник: `accepted24_source_a.jsonl`, 12 строк; порядок сохранён. Изменены только `tagged24_a.jsonl` и этот журнал.

Независимая оценка: во всех объяснениях есть два расчёта, использующих вопрос и общий префикс. Их исходные абзацы целиком помещены в соседние Path. Общие предпосылки оставлены перед блоком; объединение результатов после него.

В каждом think ровно один полный нумерованный блок с двумя Outline и Path. Все исходные слова, числа, формулы и Final Answer сохранены. Добавлены лишь теги, номера веток и короткие Goal/Conclusion. Во всех Path не менее 80 символов. В Outline нет конечного ответа; в добавленных Outline/Conclusion нет формулировок проверки совпадения.

Проверка выполнялась `/tmp/exp21-audit-venv/bin/python -B` с импортом `scripts/exp21/mv_format.py` и `scripts/exp21/checks.py`. Вызов: `check(response, candidate(original), 'math', original=original)`. Ответ для сравнения взят исключительно из исходного публичного объяснения. Gold/eval не читались; GPU, Kubernetes и прокси не использовались.

Результат: 10 строк проходят все проверки. Две строки помечены `tagged_heuristic_exception` и имеют только false-positive `xref`:

- `math-train/6774`: исходное `imaginary part 4*c*s*(c^2-s^2)` совпадает с регулярным выражением `part [1-9]`. Это формула мнимой части, межветочной ссылки нет.
- `math-train/5272`: исходное `Likewise gcd(t,u)>1.` продолжает условие `gcd(h,t)>1` внутри второго Path. Это ссылка внутри одной ветки. Обе фразы и семантические исключения согласованы с родительским агентом.

Остальные проверки обеих строк проходят. Исходные слова не менялись ради эвристики. Длина в токенах Qwen3 здесь не проверялась; токенизатор для этого шага не запрашивался.

Ход выполнения: системный `python3` не имел `math_verify`; использован существующий `/tmp/exp21-audit-venv/bin/python -B`. Первая проверка остановилась на `xref` строки 6774 до записи файлов. После разбора двух ложных срабатываний выполнена запись и повторная проверка. Неудачная shell-команда с вложенным разделителем heredoc исправлена; она не выполнила запись.

Подробные результаты:

```json
[
  {
    "id": "math-train/6855",
    "status": "tagged",
    "path_characters": [
      209,
      583
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "\\sqrt{2}"
  },
  {
    "id": "math-train/6774",
    "status": "tagged_heuristic_exception",
    "path_characters": [
      409,
      336
    ],
    "xref_matches": [
      "part 4"
    ],
    "ok": false,
    "issues": [
      "xref"
    ],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "\\frac{6}{25}"
  },
  {
    "id": "math-train/2170",
    "status": "tagged",
    "path_characters": [
      210,
      1027
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "2148"
  },
  {
    "id": "math-train/2846",
    "status": "tagged",
    "path_characters": [
      496,
      426
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "5\\sqrt{13}"
  },
  {
    "id": "math-train/3082",
    "status": "tagged",
    "path_characters": [
      336,
      662
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "\\frac{7}{2}"
  },
  {
    "id": "math-train/5272",
    "status": "tagged_heuristic_exception",
    "path_characters": [
      260,
      512
    ],
    "xref_matches": [
      "Likewise"
    ],
    "ok": false,
    "issues": [
      "xref"
    ],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "757"
  },
  {
    "id": "math-train/5482",
    "status": "tagged",
    "path_characters": [
      176,
      293
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "73"
  },
  {
    "id": "math-train/7186",
    "status": "tagged",
    "path_characters": [
      466,
      551
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "30"
  },
  {
    "id": "math-train/5349",
    "status": "tagged",
    "path_characters": [
      313,
      845
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "680"
  },
  {
    "id": "math-train/3177",
    "status": "tagged",
    "path_characters": [
      414,
      649
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "39"
  },
  {
    "id": "math-train/6952",
    "status": "tagged",
    "path_characters": [
      415,
      470
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "(3,-2,2)"
  },
  {
    "id": "math-train/2464",
    "status": "tagged",
    "path_characters": [
      307,
      482
    ],
    "xref_matches": [],
    "ok": true,
    "issues": [],
    "blocks": 1,
    "paths": [
      2
    ],
    "candidate": "\\frac{7}{24}"
  }
]
```

Повторная проверка:

```bash
/tmp/exp21-audit-venv/bin/python -B - <<'VALIDATE_A_END'
import json, sys
from pathlib import Path
root = Path('/Users/v.charkin/Documents/dev/projects/parallel-r1-exp21')
sys.path.insert(0, str(root / 'scripts/exp21'))
from checks import check, candidate
from mv_format import parse
base = root / 'results/21-qwen3-0.6b-multiverse/audit/deep_trace_pilot'
source = [json.loads(x) for x in (base / 'accepted24_source_a.jsonl').read_text().splitlines()]
tagged = [json.loads(x) for x in (base / 'tagged24_a.jsonl').read_text().splitlines()]
assert [r['id'] for r in source] == [r['id'] for r in tagged]
for original, row in zip(source, tagged):
    assert original['question'] == row['question']
    result = check(row['response'], candidate(original['response']), 'math', original=original['response'])
    parsed = parse(row['response'])
    assert parsed['valid'] and len(parsed['blocks']) == 1 and parsed['blocks'][0]['numbered']
    assert row['response'].index('<think>') < parsed['blocks'][0]['start'] < parsed['blocks'][0]['end'] < row['response'].index('</think>')
    expected = ['xref'] if row['id'] in {'math-train/6774', 'math-train/5272'} else []
    assert result['issues'] == expected, (row['id'], result)
    assert candidate(original['response']) == candidate(row['response'])
    print(row['id'], row['status'], result['issues'])
VALIDATE_A_END
```
