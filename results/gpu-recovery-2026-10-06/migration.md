# Переход на два пода по 2 H100 (2026-10-06/07)

Итог: работают `vcharkin-exp-vm-a` и `vcharkin-exp-vm-b`, по 2 H100 на разных узлах, у каждого свой PVC. Старый `vcharkin-exp-vm` в 0,
`vcharkin-exp-vm-extra` удалён. Всего 4 H100. Тома не удалялись.

## Ресурсы после перехода (02:59 MSK 07.10)

| Ресурс | Узел | Ready | GPU | PVC `/work` |
|---|---|---|---|---|
| `vcharkin-exp-vm-a-0` | ml-kub-node806.i | True, restarts 0 | 2× H100 80GB HBM3 | `vcharkin-parallel-r1-pvc` (исходный, 154G из 196G) |
| `vcharkin-exp-vm-b-0` | ml-kub-node801.i | True, restarts 0 | 2× H100 80GB HBM3 | `vcharkin-parallel-r1-b-pvc` (новый, Bound, 74G из 196G) |
| `vcharkin-exp-vm` | — | 0/0 | — | исходный (StatefulSet сохранён) |

В каждом поде PID 1 — `run_gpu_queues.sh 2`, работают `queue_runner.sh 0` и `queue_runner.sh 1` из `/work/runner-src` (6581e92).
Очереди `gpu0.txt`/`gpu1.txt` пусты на обоих томах. GPU после старта 0 MiB / 0%. Нагрузку для проверки не давал.
Автоматика простоя может через 1.5–2 ч выключить пустые поды. Это штатно: после разрешённого scale-up очереди стартуют сами.

## Как остановили старые поды

- Все задачи main закончились к 22:04: 8 прогонов `*-16k` по 5 json, 4 greedy IFEval, exp11. Все END exit=0, `.failed` нет.
- С 22:04 до 23:46 опрос каждые 2 мин показывал 4 пустые очереди и ни одного процесса генерации/обучения/оценки.
  В 23:45 автоматика простоя сама масштабировала `vcharkin-exp-vm` в 0. Вручную main не останавливал.
- Архив результатов и логов main (без генераций и чекпоинтов) снят в 22:19 и лежит вне репозитория:
  `outputs/continuation-2026-10-06/migration/main-results-logs-2220.tgz`.
- exp12 закончился на extra в 01:24. Finalizer запушил `exp/11-len8k-control` 7b3479c и `exp/12-len8k-parathinker` 20c9fe6
  (сверено через `git ls-remote origin`) и в 01:36 удалил extra.
- В 01:40 и 01:41 повторно проверено: подов нет, ни один под не монтирует PVC проекта.

## Копирование на PVC B (`infra/copy-workspace-b.yaml`)

CPU Job (8 CPU / 32Gi, 32 cpu.slots), source смонтирован read-only. Перед копированием Job выводит очереди source: все 4 по 0 строк.

| Попытка | Время | Результат |
|---|---|---|
| 1 | 01:41–01:47 | OOMKilled (137) на `cp -a assets` |
| 2 | 01:53–02:01 | OOMKilled на `cp -a assets` с `sync -f` каждые 3 с |
| 3 | 02:12–02:52 | Complete, exit 0, `COPY_READY` |

Исправления в Job:
- Коммиты worktree читаются через `git --git-dir=/source/parallel-r1/.git/worktrees/<dir>`: `.git` worktree указывает на
  `/work/parallel-r1`, а в Job это целевой том.
- Файлы от 64 MiB копируются через `dd iflag=direct oflag=direct`, остальные через `tar` с периодическим `sync`.
  В лог раз в 30 с пишется `memory.stat`. В попытке 3 page cache был 1.4–6 GB, dirty около 0.

Что Job сделал на B:
- скопировал `assets`, `venv`, `bench_data`;
- `git fetch` всех веток в `/work/parallel-r1` (HEAD 72edf31);
- создал detached worktree `setup-src` c45770b, `bench-src` 850b1b0, `runner-src` 6581e92 и скопировал их `data_preprocess_scripts/data`;
- импорт `torch 2.6.0+cu124`, `transformers 4.51.3`, `verl` прошёл; есть config Qwen3-0.6B и `parathinker/train_mix.parquet`.

`runs`, `bench`, `exps` и очереди не копировались. После успеха завершённый Job удалён, оба PVC открепились.
На поде B импорт повторён: verl берётся из `/work/setup-src/verl`.

## Ограничения

- Сравниваемые SFT-прогоны (02r, 04, 05, 11, 12) и их генерации есть только на томе A. Новые запуски, которые сравниваются
  с ними через `paired_compare.py`, ставить в A или переносить нужные генерации на B.
- На B нет worktree экспериментов. Ветки есть в `/work/parallel-r1`; `start_experiment.sh` берёт закреплённый коммит.
- Тома независимы, но namespace, хранилище openebs и автоматика простоя общие.
- На исходном томе свободно 33G.
- Событие `FileSystemResizeFailed ... read-only` при монтировании source в Job безвредно. У B был один `FailedMount timed out`,
  пока том отсоединялся от узла Job; повтор прошёл сам.

Команды, логи попыток и опросы: `outputs/continuation-2026-10-06/migration/` (progress.md, poll.log, copy-attempt{1,2}.log,
copy-attempt3-success.log).

## Независимая приёмка (03:08 MSK 07.10)

Проверка завершилась успешно: 65 из 65 условий. A на `ml-kub-node806.i`, B на `ml-kub-node801.i`, оба Ready.
В каждом видны ровно две H100, использование памяти и загрузка GPU равны нулю, процессов GPU нет.
Обязательное размещение на разных узлах сохранено. На обоих подах работают очереди 0/1, строки очередей пусты.
Старый StatefulSet сохранён с replicas=0; extra и завершённый Job отсутствуют; оба PVC Bound.

На обоих томах проверены подготовленная Qwen3-4B: vocab 151936, BF16, связанные веса, шесть новых токенов,
исходный шаблон чата и заголовки всех shards. Исходная Qwen3-4B сохранена. Импорты выполнены только на CPU.
Число строк SFT: полный набор 5558, фильтр 4248, случайный контроль 4248, dev 296. ID уникальны,
пересечения train/dev нет. Данные оценки содержат 296/482/299/999 проблем, ID режимов согласованы.
Свободно 32.3 GiB на A и 112.6 GiB на B. На B есть COPY_READY; прежние runs сохранены на A.

В объектах Pod кластер добавляет `nvidia.com/gpu: 2` к заданному `nvidia.com/gpu.h100.pa: 2`.
Проверка принимает только согласованную пару на одном контейнере и отдельно проверяет физическое число GPU через nvidia-smi.

Полный журнал приёмки:
`/Users/v.charkin/Documents/ChatGPT/R1/outputs/instruct4b-2026-10-06/migration_acceptance_alias/evidence-20261007-030709/verification.json`.
Чистая инфраструктурная ветка и публикация проверены отдельно. Локальный архив main содержит 84 JSON метрик,
в том числе 40 результатов 16k и четыре greedy IFEval.

## Повторная приёмка после простоя 07.10

К 11:55 оба новых StatefulSet имели replicas=0. Авторизация Teleport истекла в 11:51; вход восстановлен до 08.10 11:54. Старый основной StatefulSet оставлен replicas=0. Подняты только A/B с прежними PVC и обязательным размещением на разных узлах.

Свежая полная приёмка 2026-10-07T12:14:20+0300: **65/65 успешно**. A: `ml-kub-node803.i`; B: `ml-kub-node806.i`. На каждом по 2 H100, обе GPU простаивают, очереди пусты, незапланированных ML-процессов нет. Данные, COPY_READY и импорты повторно проверены.

Журнал: `/Users/v.charkin/Documents/ChatGPT/R1/outputs/continuation-2026-10-06/heartbeats/2026-10-07-current-acceptance/evidence-20261007-121129/verification.json`. После публикации этой приёмки root выдаёт MIGRATION_READY и отключает автоматизацию переноса.
