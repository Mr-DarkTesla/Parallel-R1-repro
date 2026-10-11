# 189 новых задач для собственных траекторий Qwen3-4B

11 октября 2026. Пока подготовлен **список задач**, а не обучающие
ответы. В нём 94 MATH и 95 GSM8K из прежнего очищенного пула.
Порядок унаследован от `data/onpolicy46_candidates.jsonl`.

Сборщик `scripts/exp21/prepare_qwen4b_onpolicy189.py` исключил:

- 64 задачи прежнего on-policy пилота 0.6B;
- 4 задачи 4B focus34, одна из них уже входила в прежний пилот;
- все ID и нормализованные условия из 4B mixed401 train/val, 78
  сохранённых SFT parquet и fixed40. Дополнительных совпадений с ними
  не нашлось.

Итого удалено 67 различных задач из исходных 256. Сравнивались ID и
условия после Unicode NFKC и нормализации пробелов; совпадение ID
без совпадения текста для независимо пронумерованных GSM8K не
подменяет проверку самого условия. `leakcheck.py` проверил все 189
задач против eval-корпуса и полного MATH test по прежнему протоколу:
**0 блокирующих утечек**. Точные пути, числа и причины отсева в
`data/qwen4b_onpolicy189_candidates.audit.json`.

Список уже скопирован на наш pod `vcharkin-exp-vm-0` в
`/tmp/exp21-qwen4b-onpolicy189-candidates.jsonl` и содержит 189 строк.
Проверенная исходная tagged 4B сохранена на нашем checkpoint PVC.
Генератор ниже применяет ту же маску независимых путей и позиции,
что SFT. Gold есть в файле только для последующей оценки и не
попадает в запрос модели.

Обёртка `scripts/exp21/run_qwen4b_onpolicy189_pod.sh` запускает эти
команды после завершения focus34, проверяет отсутствие другого GPU
процесса и пишет сырые ответы и отсев на отдельный persistent
checkpoint PVC. Она держит только `CUDA_VISIBLE_DEVICES=0` и
поддерживает возобновление генерации по исходным `(id, seed)`.

```bash
cd /tmp/exp21-eval-clean-299074e
source /work/venv/bin/activate
CUDA_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 \
python scripts/exp21/generate_onpolicy_masked.py \
  /checkpoints/exp21-global-top5/qwen4b-mixed401-tagged-step128/model \
  /tmp/exp21-qwen4b-onpolicy189-candidates.jsonl \
  /checkpoints/exp21-qwen4b-onpolicy189/rollouts.jsonl \
  --math-count 94 --gsm-count 95 --seeds 0 \
  --temperature 0.6 --top-p 0.95 --top-k 20

python scripts/exp21/filter_onpolicy_rollouts.py \
  /checkpoints/exp21-qwen4b-onpolicy189/rollouts.jsonl \
  /checkpoints/exp21-qwen4b-onpolicy189/filter \
  --candidates /tmp/exp21-qwen4b-onpolicy189-candidates.jsonl
```

Автоматический фильтр проверяет финал, усечение, грамматику и
положение блока внутри `<think>`. Каждый оставшийся пример всё ещё
требует смысловой проверки независимости и полезности путей до SFT.
Ни генерация, ни обучение на этих 189 задачах пока не запускались.
