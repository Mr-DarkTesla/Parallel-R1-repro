"""Readable index of saved SFT/RL execution settings; requires PyYAML."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"


def dig(x, key, default="—"):
    for part in key.split("."):
        if not isinstance(x, dict) or part not in x:
            return default
        x = x[part]
    return default if x is None else x


def cell(x):
    if isinstance(x, (list, dict)):
        x = json.dumps(x, ensure_ascii=False)
    return str(x).replace("|", "\\|").replace("\n", " ")


def compact_path(x):
    if isinstance(x, str) and "/" in x:
        return "/".join(x.split("/")[-4:])
    return cell(x)


rows = []
for path in sorted(ART.rglob("*")):
    if not path.is_file() or "fixture" in str(path):
        continue
    is_yaml = path.suffix in {".yaml", ".yml"} and path.name in {"config.yaml", "resolved-config.yaml", "eval-preflight.yaml"}
    is_json = path.suffix == ".json" and "config" in path.name
    if not (is_yaml or is_json):
        continue
    try:
        x = yaml.safe_load(path.read_text()) if is_yaml else json.loads(path.read_text())
    except (ValueError, yaml.YAMLError):
        continue
    if not isinstance(x, dict):
        continue
    rel = str(path.relative_to(ROOT))
    if "actor_rollout_ref" in x:
        record = dict(kind="RL / legacy verl", model=dig(x,"actor_rollout_ref.model.path"),
                      data=dig(x,"data.train_files"), gpus=f"{dig(x,'trainer.nnodes')} × {dig(x,'trainer.n_gpus_per_node')}",
                      batch=dig(x,"data.train_batch_size"), n=dig(x,"actor_rollout_ref.rollout.n"),
                      minibatch=dig(x,"actor_rollout_ref.actor.ppo_mini_batch_size"),
                      microbatch=dig(x,"actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu"),
                      lr=dig(x,"actor_rollout_ref.actor.optim.lr"), steps=dig(x,"trainer.total_training_steps"),
                      precision=dig(x,"actor_rollout_ref.actor.fsdp_config.model_dtype"),
                      reward=dig(x,"algorithm.adv_estimator"),
                      response=dig(x,"data.max_response_length"),
                      temperature=dig(x,"actor_rollout_ref.rollout.temperature"))
    elif "optim" in x and "data" in x:
        record = dict(kind="SFT", model=dig(x,"model.partial_pretrain"), data=dig(x,"data.train_files"),
                      gpus=f"{dig(x,'trainer.nnodes')} × {dig(x,'trainer.n_gpus_per_node')}",
                      batch=dig(x,"data.train_batch_size"), n="—", minibatch="—",
                      microbatch=dig(x,"data.micro_batch_size_per_gpu"), lr=dig(x,"optim.lr"),
                      steps=f"{dig(x,'trainer.total_training_steps')} steps / {dig(x,'trainer.total_epochs')} epochs",
                      precision=dig(x,"model.fsdp_config.model_dtype"), reward="response CE",
                      response=dig(x,"data.max_length"), temperature="—")
    elif "world_size" in x and "lr" in x:
        batch = dig(x,"global_batch.prompts_per_step", "not explicitly recorded")
        record = dict(kind="RL / structured replay",model=dig(x,"model"),data=dig(x,"train"),
                      gpus=dig(x,"world_size"),batch=batch,n=dig(x,"global_batch.rollouts_per_prompt",dig(x,"reward_group",dig(x,"group"))),
                      minibatch=dig(x,"ppo_epochs"),microbatch=dig(x,"group"),lr=dig(x,"lr"),
                      steps=dig(x,"steps"),precision=dig(x,"precision_mode",dig(x,"actor_dtype")),
                      reward=dig(x,"reward_mode"),response=dig(x,"response_budget"),temperature=dig(x,"temperature","see worker/protocol"))
    else:
        continue
    rows.append(dict(source=rel,**record))

out=["# Конфигурации SFT и RL\n",
     "Таблицы извлечены из сохранённых Hydra/runtime-конфигураций. Наличие настройки означает сохранённый рецепт; выполненные шаги и полнота проверяются по метрикам соответствующего запуска. `—` означает, что поле отсутствует или равно null, а не нулевое значение. Пути модели и данных сокращены в таблице; полный путь, seed, optimizer, loss, KL, sampling, data hashes и overrides доступны по ссылке на конфигурацию.\n",
     "Для structured replay поле `group` может быть числом локальных ответов на rank; размер reward group берётся отдельно. В 32-GPU batch32 конфигурации это 1 локальный ответ и 4 ответа в reward group.\n"]
for kind in sorted({r["kind"] for r in rows}):
    out += [f"## {kind}\n", "| Источник | Модель / checkpoint | Данные | GPU | Prompt batch | n / reward group | LR | Steps / epochs | Precision | Loss / advantage / reward | Response / max length |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["kind"]!=kind:continue
        name=r["source"].removeprefix("artifacts/")
        out.append("| "+" | ".join([f"[{name}]({r['source']})",compact_path(r["model"]),compact_path(r["data"])]+[cell(r[k]) for k in ["gpus","batch","n","lr","steps","precision","reward","response"]])+" |")
(ROOT/"TRAINING_CONFIGURATIONS.md").write_text("\n".join(out)+"\n")
(ROOT/"training-configurations.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False)+"\n")
print(f"Indexed {len(rows)} SFT/RL configurations")
