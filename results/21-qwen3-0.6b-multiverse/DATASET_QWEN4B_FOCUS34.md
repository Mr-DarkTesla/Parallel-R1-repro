# Qwen3-4B focus34: paired continuation

Набор продолжает `qwen4b_mixed401_{tagged,plain}_step128`. В train 34
нативные Qwen3-4B траектории, дважды просмотренные и принятые ранее,
повторены по три раза. К ним добавлены собственные 4B replay из исходных
320 генераций: только `correct=true`, `clean=true`, `truncated=false`, без
34 позитивных задач. Tagged и plain плечи имеют одинаковый порядок строк.
В positive-строках plain получается удалением только десяти Multiverse
тегов; replay уже не содержит этих тегов.

Получается 231 train-строка на плечо: 102 positive (`34 × 3`) и 129
уникальных replay. После исключения позитивов из 163 чистых верных
необрезанных 4B генераций других подходящих replay не осталось.

Validation копируется из paired mixed401 без изменения порядка: 50 строк в
каждом плече. Это сохраняет validation continuation родителя. Сборщик
сверяет нормализованные условия train против этих 50 строк и fixed40.

Выходы:

- `data/qwen4b_focus34_tagged_{train,val}.parquet`
- `data/qwen4b_focus34_plain_{train,val}.parquet`
- `audit/qwen4b_focus34_report.json`

Проверки в сборщике: 34/34 позитивных внешних ответа имеют прежний
`math_verify`-аудит; replay несут provenance `grade_gen.py`, где `correct`
означает не обрезанный чистый ответ, проверенный `math_verify`; пары
совпадают после удаления только десяти тегов; все теги позитивов внутри
`<think>`; полный Qwen-токенизированный пример не превышает 4096 токенов.

CPU-команда:

```bash
uv run --offline --no-project --with pandas --with pyarrow --with tokenizers==0.23.2 python scripts/exp21/build_qwen4b_focus34_pair.py
```
