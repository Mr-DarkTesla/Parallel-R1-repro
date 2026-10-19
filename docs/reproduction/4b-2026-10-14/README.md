# Воспроизведение Qwen3-4B: SFT, RL300 и RL150 с новой наградой

Снимок 14 октября 2026. SFT-корпус и вся логика разметки также опубликованы в [отдельном Dataset](https://huggingface.co/datasets/sirius-parallel-r1/Parallel-R1-GSM-Infinite-Counted-SFT-3000). Цель — запустить тот же эксперимент на другой Linux-машине с теми же входами, исходниками и настройками. Готовые веса RL300 опубликованы в приватном репозитории [sirius-parallel-r1/Parallel-R1-Qwen3-4B-Instruct-RL300](https://huggingface.co/sirius-parallel-r1/Parallel-R1-Qwen3-4B-Instruct-RL300). Доступ к организации нужен и для весов, и для корпуса в `reproduction/reproduction-inputs.tar.gz`.

## Как однозначно различать эксперименты

| Имя | Старт | Обновления | GPU / batch | Данные | Награда |
|---|---|---:|---|---|---|
| Warmup шести токенов | `Qwen/Qwen3-4B` @ `1cfa9a7208912126459214e8b04321603b3df60c` | 129, 3 эпохи | 8 / 64, последний неполный | SFT 2700 | CE, обучаются только шесть embedding/head строк |
| Full SFT | Warmup `lr-1e-3/final` | 42, 1 эпоха | 8 / 64 | тот же SFT 2700, val300 | полная response CE |
| R2 RL50 | Full SFT | 1–50 | 24 / 24 prompts × 4 = 96 responses | CNK12/Orca 1024, val32 | ступенчатая стоимость forwards + width/round bonus |
| **R2 RL300** | веса именно этого RL50; новый Adam | 51–300 | 32 / 16 × 4 = 64 | тот же corpus1024 | та же R2 reward |
| **R4 RL150, новая награда** | **Full SFT**, новый Adam | 1–150 | 16 / 16 × 4 = 64 | DAPO 2000, тот же val32 | correctness × экспоненциальная стоимость forwards |

R4 RL150 не продолжает RL300. Старый R2 checkpoint150 — другой эксперимент. Предшествующие аварийные попытки, batch32 handoff, последующий R3 и продолжения после сохранённых checkpoint’ов не входят в эти три рецепта. Полные исходные конфигурации находятся в `snapshot/work/experiments/.../production-config*.json`; их нужно читать вместе с историей этапов выше: исходный target500 не означает, что RL300 содержит 500 обновлений.

Все ранги подтвердили 50, 250 и 150 принятых optimizer updates соответственно, без пропусков; см. [training-progress.json](training-progress.json). Полные RL exports содержат 4 022 468 096 обучаемых параметров, FP32 веса, tokenizer и config, без optimizer/RNG. RL300: `model.safetensors` 16 089 918 232 байта, SHA-256 `8b4921297d797c4a58c851abdb98ea6dd75eeb4c5af958e5292caa9e2681aa39`. Новая RL150: SHA-256 `a15058092190e857c6f68a337d69e0c149602e1ab50f8384a92d2c04007ef28f`.

Dataset revision: `d53dc009ab33da8effa4d2a67b5aa42b66623614`; точные files/hashes и проверки — в [dataset-publication.json](dataset-publication.json). Код annotation, raw teacher/judge responses и accepted/rejected journal входят в опубликованный Dataset.

## Что фиксируется

- [input-manifest.json](input-manifest.json): исходный SHA-256, размер и тип каждого входа. Данные сохраняются побайтово, включая порядок строк и split.
- [source-snapshot.tar.gz](source-snapshot.tar.gz): замкнутый снимок кода, конфигураций и зависимостей scorer’а с переносимыми путями. В `snapshot/` оставлены напрямую читаемые экспериментальные исходники; архив содержит также полное дерево исторического SFT trainer и Math-Verify.
- [bundle.json](bundle.json): SHA-256 полного архива на Hugging Face. В нём оригинальные входы, candidate pool, полный accepted/rejected journal, raw teacher/judge responses, pilot approvals, tokenizer, небольшой tensor начальных шести строк, SFT Parquet/JSONL, RL JSONL, benchmark questions и исторические proofs.
- [environment.json](environment.json): версии реально установленного окружения; [requirements.txt](requirements.txt) выделяет основные зависимости.
- [sft-remote.json](sft-remote.json): фиксированный SFT revision `8fc2dfa4aeab320a8286a484cfbe7ab7df3da514` и хеши весов. Используется репозиторий `sirius-parallel-r1/Parallel-R1-Qwen3-4B-Instruct-SFT`.
- [publication.json](publication.json): проверенный immutable HF revision итоговой публикации и Git baseline. Для загрузки используйте именно этот revision, а не изменяемый `main` HF репозитория.

Серверные конфигурации и все `sealed_inputs` сверены с хешами `control/production-approved.json`: расхождений нет для трёх RL этапов. При переносе меняются только абсолютные пути и конечный target соответствующего этапа. `prepare_phase.py` создаёт новый receipt с хешами перенесённых файлов; исторический GPU proof явно помечен как исторический. Это не свидетельство нового smoke на вашей машине.

## Окружение и восстановление на другой машине

Историческая платформа: Linux, Python3.12.3, NVIDIA A100 **80 GB**, 8 GPU на узел, общий файловый каталог на всех узлах. PyTorch2.6.0/CUDA12.4, Transformers4.53.2, vLLM0.8.5.post1, FlashAttention2.7.4.post1. RL50 требует 3 узла, RL300 — 4, R4 RL150 — 2. Смена числа GPU либо precision будет отдельным вариантом эксперимента. Для точного исторического протокола нужны эти числа GPU.

Создайте отдельное окружение Python, установите PyTorch с CUDA12.4, затем зависимости. FlashAttention собирается после установки PyTorch, с `--no-build-isolation`. Полный список исторических версий сохранён в `environment.json`; успешная установка ещё не подтверждает совместимость другого driver/GPU.

```bash
python3.12 -m venv /path/to/env
source /path/to/env/bin/activate
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install --no-build-isolation -r docs/reproduction/4b-2026-10-14/requirements.txt
python docs/reproduction/4b-2026-10-14/verify_snapshot.py
```

Получите приватный архив через свой HF read-token. Скрипты не содержат токен; используйте обычный `HF_TOKEN` либо локальную авторизацию `huggingface_hub`.

```python
import json
from pathlib import Path
from huggingface_hub import hf_hub_download
D = Path('docs/reproduction/4b-2026-10-14')
publication = json.loads((D/'publication.json').read_text())
archive = hf_hub_download(publication['repo'],
    filename='reproduction/reproduction-inputs.tar.gz',
    revision=publication['revision'])
print(archive)
```

```bash
D="$PWD/docs/reproduction/4b-2026-10-14"
python "$D/restore.py" --bundle /path/from/hf_hub_download \
  --target /shared/new-r1-reproduction --download-models
export REPRO_ROOT=/shared/new-r1-reproduction
```

`restore.py` требует **новую директорию**, проверяет полный архив и каждый файл, затем переписывает местоположение в исходниках/configs. `--download-models` скачивает pinned native Qwen3-4B и pinned Full SFT; последний подходит для непосредственного повторения RL. Для повторения SFT заново используйте отдельный новый target без `--download-models`, скачайте native checkpoint командой ниже и выполните warmup + SFT. Готовый Full SFT в `runs/epoch1/final` нельзя оставлять на месте при повторном запуске epoch1.

## Как получен SFT-корпус

Это **3000 новых accepted GSM-Infinite** примеров, не смесь с 2145 более ранними. Источники: `InfiniAILab/gsm_infinite_hard_0` и `gsm_infinite_medium_0`; дополнительный резерв pinned revision `49b0c72bca4c257a378d07da41561fe081ec5ad5`. Полный source manifest с хешами, исключениями и prompt version находится в `snapshot/exps/deepseek-gsm-wide3000-v2-20261009/`.

Teacher — `deepseek-v4.1-flash`, thinking включён, `reasoning_effort=50`, temperature0.6/top_p0.95/max_tokens32768; seed — первые 8 hex SHA-256 ID, по модулю 2147483647. Семантический judge — тот же teacher, temperature0/top_p1/max_tokens16384, JSON response. Точные [teacher prompt](snapshot/exps/deepseek-gsm-wide3000-v2-20261009/prompt-wide-explicit.txt), [judge prompt](snapshot/exps/deepseek-gsm-wide3000-v2-20261009/judge-prompt.txt) и [student system](snapshot/exps/deepseek-gsm-wide3000-v2-20261009/student-system.txt) сохранены.

Acceptance: законченный ответ, валидные counted forks/Plan/Path/Summary, совпадение конечного ответа с reference, все семантические поля judge положительные, отсутствие given-only paths, ограничение student context. Фильтр по средней ширине был снят: корректные узкие траектории сохранялись. Число раундов адаптивное, ширина2–8; последовательные ответы допустимы. Split по `split_group`, 2700 train / 300 val, без пересечения групп. Serialization `counted-forks-think-tail-final-v4`: вся работа внутри одного `<think>`, финальный ответ после `</think>`.

Историческая статистика: 3486 forks, средняя ширина3.2917; 2510 примеров с одним раундом, 473 с двумя, 10 с тремя и 7 последовательных; 784 примера с verification paths. Точный корпус в архиве: `exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think/{train,val}.jsonl`. SHA-256: train `7379ecfc7053771313df1bc63c6324a3f3f8ee72bdfc818015bdc35ae600b24a`, val `d5a868ef8fc42a50f21a7e9cb657da1a894b882ddeabb256b6f1eeb6112a23c5`.

Повторный API-запрос к teacher не гарантирует тот же корпус: serving weights/revision teacher не были зафиксированы, inference стохастический. Поэтому для повторения **исторического обучения** используется сохранённый accepted корпус. Исходники генерации описывают процедуру происхождения; создание нового корпуса будет новым экспериментом. Семантический judge того же teacher не является формальным доказательством каждой ветки.

## Warmup и полная SFT

Скачайте исходную модель в новый target:

```python
from huggingface_hub import snapshot_download
snapshot_download('Qwen/Qwen3-4B',
    revision='1cfa9a7208912126459214e8b04321603b3df60c',
    local_dir='/shared/new-r1-sft/work/experiments/night-20261010/qwen3-4b-tag-probe-20261010/model')
```

Шесть controls используют reserved IDs151669–151674, vocabulary не увеличивается. Начальные FP32 строки — среднее native pieces каждой строки токена; embedding и output head действительно tied. Warmup обучает только15360 параметров, остальные веса заморожены: 8GPU, seed20261010, AdamW lr0.001/betas0.9,0.999/eps1e-8/weight_decay0, BF16 compute/FP32 обучаемые строки, 3 эпохи, accumulation8 на GPU, batch64 с неполным хвостом, 129 updates. LR: пять шагов разогрева, затем cosine до 0.1 от base. Prompt и принудительные headers loss0; точные masks и позиции — в `data.py`.

```bash
cd "$REPRO_ROOT"
W=work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3
bash "$W/run_train.sh" production
bash work/experiments/instruct-full-20261011/run_train.sh epoch1
```

Подготовленные SFT Parquet и compiler уже восстановлены из архива; повторно запускать исторический `prepare.py` не требуется.

Full SFT: все 4 022 468 096 параметров, FSDP1, FP32 model storage/BF16 forward, gradient checkpointing, SDPA с sibling isolation и повторяющимися позициями. Native chat template и EOS `<|im_end|>`. Полная response CE, включая controls; prompt/padding loss0. Batch64, microbatch1/GPU, max_length8192, seed1. AdamW lr1e-5, betas0.9/0.95, weight_decay0.01, eps1e-8, clip1; cosine, warmup ratio0.1 (4 шага), одна эпоха42updates/2688 exposures. Параметры Hydra полностью задаются сохранёнными `run_train.sh` и `code/verl/trainer/config/{sft_trainer,sft_qwen3_06b}.yaml`. Полученная val response CE **0.3917267322540283**. Export — BF16 HF weights, без optimizer/RNG.

## R2: RL50 → RL300

Corpus1024 = 512 CNK12 + 512 Orca из `open-r1/Big-Math-RL-Verified-Processed`, revision `c79efbb6d3b75e3a2bcc27a5c569119918132345`; предыдущие128 сохранены, 304 ранее проверенных + 720 gold-blind teacher-corroborated. Валидатор исключает benchmark/validation overlaps текстовыми правилами; семантическую деконтаминацию не гарантирует. Замороженные train/val JSONL находятся в `work/experiments/rl-r2-24gpu-20261012/data/`. Train SHA-256 `6bcab08da6bc6b22ddacc58ac5aeb5a18abcc509c4f68d7457cd79d8acb4e317`, val `cb02ef017baff97bed5568e60a53f9673c04f657f59d81349f1a6484e3f30a6a`.

Для correctness C∈{0,1}, format-valid V, фактически исполненных widths w и числа rounds r:

```
P(F) = min(0.4, 0.02 * floor(F / 200))
U = mean(min(w - 1, 3) / 3), либо 0 при отсутствии forks
R = C * (1 - P(F) + V * (0.3 * U + 0.05 * min(r, 4)))
```

F — **физические generation model.forward calls**; technical/audit/replay forwards в штраф не входят. Бонус постоянный, без annealing. Incorrect reward0. Формат определяет только бонус. Advantage = reward − mean четырёх responses одного prompt, без std normalization/whitening.

Оба этапа: synchronous fresh rollout, один PPO epoch и одно Adam update на batch; clip0.2, max_grad_norm1, AdamW lr1e-6/betas0.9,0.999/eps1e-8/weight_decay0, Zero1, no KL/reference-model penalty, no entropy bonus, no async. Sampling temperature1/top_p1, response4096/path768/context16384/fullwidth8. Prompt/header/bridge loss0, все sampled actions, включая terminal, loss1; PPO token loss делится на фиксированный response budget4096 и затем усредняется по responses. Все siblings исполняются одновременно в одном forward, изолированные контексты и позиции воспроизводятся в replay.

RL50: seed/data_seed20261012, 24GPU, FP32 HF actor и learner. RL300: 32GPU, vLLM BF16 actor, FP32 learner masters/gradient reduction, BF16 learner compute, TF32 выключен. Token-TIS = exp(logp_old − logq), clamp[0,2], без batch normalization; PPO ratio использует learner old/current. Handoff на step50 загружает только веса, сбрасывает Adam; `initial_step=50`, `prompt_exposure_offset=1200`. Порядок: seeded shuffle1024 каждого epoch; следующие250 шагов потребляют ещё4000 prompt exposures (итого5200). Relative exposure и seeds не зависят от числа nodes. Между фазами нужен полный clean exit предыдущей allocation.

```bash
python "$D/prepare_phase.py" --root "$REPRO_ROOT" --phase rl50
# На каждом из 3 узлов, NODE_RANK=0,1,2, один общий MASTER_ADDR:
NODE_RANK=0 MASTER_ADDR=10.0.0.1 bash "$D/launch_phase.sh" rl50
# После checkpoint0050 и завершения всех 24 процессов:
python "$D/prepare_phase.py" --root "$REPRO_ROOT" --phase rl300
# На каждом из 4 узлов, NODE_RANK=0,1,2,3:
NODE_RANK=0 MASTER_ADDR=10.0.0.1 bash "$D/launch_phase.sh" rl300
```

## R4: RL150 с новой наградой от SFT

Из `BytedTsinghua-SIA/DAPO-Math-17k` @ `61829aa9fe754403c5559e46423772deac5a329b` берутся первые10000 исходных строк, удаляются дубликаты/конфликтующие answers и normalized-exact overlaps с сохранёнными MATH500/AIME/AMC/cleanval questions. Затем `random.Random(20261013).sample(pool,2000)`. Удаляются только фиксированные instruction prefix/suffix, все параграфы задачи сохраняются. Selected source indices, URL, raw Parquet SHA и train SHA — в `work/experiments/rl-r4-dapo2k-paired-20261013/data/manifest.json`. Готовые2000 строк сохранены; [prepare_data.py](snapshot/work/experiments/rl-r4-dapo2k-paired-20261013/prepare_data.py) позволяет заново получить выборку из pinned source.

```
R = C * (1 - 0.9 * (1 - exp(-ln(9) * F / 10000)))
```

При F=10000 correct reward0.2; предел0.1. Incorrect0. Format, width и число rounds являются diagnostics, их бонус0. Прочие настройки PPO/Adam/TIS те же, что у BF16 этапа R2, но response **32000**, path **4000**, context **40960** и loss denominator **32000**. 16GPU, batch16×4=64, seed/data_seed20261013, initial_step0, exposure_offset0, новый Adam. Rollout seeds используют relative step. Один episode на actor wave; fullwidth8 сохраняется. 150updates/2400 prompt exposures. Checkpoints50/100/150.

```bash
python "$D/prepare_phase.py" --root "$REPRO_ROOT" --phase rl150-new-reward
# На каждом из 2 узлов, NODE_RANK=0,1:
NODE_RANK=0 MASTER_ADDR=10.0.0.1 bash "$D/launch_phase.sh" rl150-new-reward
```

Для всех RL этапов replay guard: max drift0.01/mean0.002/p95 0.005; collective rejection не обновляет Adam, считается technical unknown; stop после3 подряд либо >10% после20 phase iterations. Исторически до опубликованных checkpoints rejections0 на всех ranks. Benchmark не используется для выбора curriculum/reward/checkpoint.

## Проверка результата и границы воспроизводимости

Ожидаются `reproduction-output/checkpoint-{0050,0300,0150}/complete.json`, все rank metrics с нужным step/accepted update count, tokenizer/config и полный safetensors. `complete.json` обязан иметь `weights_only=true`, `all_master_finite=true`, `trainable=4022468096`. Для исторических весов сверяйте SHA с manifests; для повторно обученных — сохраняйте новые hashes, config, environment, rank histories и независимую evaluation.

Исторический cleanval:32 фиксированных вопросов, seed91261011, temperature1/top_p1; у R2 caps4096/768/16384, у R4 caps32000/4000/40960. Это диагностика на32 вопросах. Benchmark scoring извлекает только окончательный ответ после `</think>`; веточные boxed ответы не считаются финальным решением. Math-Verify0.8.0 и его фактическая dependency closure сохранены в архиве: scorer использует vendored SymPy1.14.0 и ANTLR4.13.2, отдельно от глобального окружения learner; см. `scorer-environment.json`. Данные train batch не заменяют независимые MATH/AIME оценки. Более поздние 32k/BF16 benchmark runs следует сравнивать отдельно от исходных4k/FP32.

Проверены SHA всех входов, полное восстановление в новую директорию, сборка конфигураций всех трёх RL фаз, hash gates, синтаксис опубликованных исходников и CPU batching tests. **Полное повторное GPU обучение на другом компьютере в ходе публикации не запускалось.** Другие GPU/driver/kernel ordering и стохастический sampling могут изменить trajectories и конечные веса даже с теми же seeds. Это однозначный рецепт и фиксированные исторические артефакты; побитовая идентичность нового обучения не заявляется.
