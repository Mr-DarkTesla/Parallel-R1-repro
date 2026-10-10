# Какие строки v5 действительно увидела модель

11 октября 2026. Расчёт по сохранённому `results/rows.csv` из
[`selective_v5_train_meta.tgz`](../eval_archives/selective_v5_train_meta.tgz)
и исходному [`sft_selective_blocks_v5_train.parquet`](../data/sft_selective_blocks_v5_train.parquet).
`sft.sh` записал точный порядок `DistributedSampler` с seed 0;
обучение шло 64 шага с глобальным batch 32 и закончилось в первой
эпохе.

| Тип строки | В train | Показано модели за 64 шага |
| --- | ---: | ---: |
| `parallel_th` | 555 | 415 |
| `replay_nt` | 879 | 652 |
| `replay_th` | 804 | 612 |
| `control_th` | 510 | 369 |
| Всего | 2748 | 2048 |

Из 305 разных задач с положительным параллельным ответом модель увидела
280, не увидела 25. Среди 415 показанных положительных строк 278 MATH
и 137 GSM8K. Все 2048 показанных строк различны, поскольку проход не
дошёл до конца первой эпохи. Это точная экспозиция данных, а не оценка
по ожидаемой доле.

Недостаточная экспозиция может мешать изучению содержательного
объединения путей, но сама по себе не доказывает причину неудачных
блоков: в ранних вариантах с более частыми положительными строками
грамматика улучшалась вместе с падением точности. Проверять гипотезу
нужно отдельным опытом с контролем на тех же текстах и одинаковой
оценкой на dev.

Воспроизведение:

```bash
python3 - <<'PY'
import tarfile, pandas as pd
from pathlib import Path
root = Path('results/21-qwen3-0.6b-multiverse')
with tarfile.open(root/'eval_archives/selective_v5_train_meta.tgz') as tar:
    rows = pd.read_csv(tar.extractfile('results/rows.csv'))
train = pd.read_parquet(root/'data/sft_selective_blocks_v5_train.parquet')
train['kind'] = train.extra_info.map(lambda x: x['kind'])
used = train.iloc[rows.row.to_numpy()]
print(len(used), used.kind.value_counts().to_dict())
print(used[used.kind == 'parallel_th'].id.nunique())
PY
```
