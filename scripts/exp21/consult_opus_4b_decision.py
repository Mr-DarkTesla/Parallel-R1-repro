"""Bounded Opus advice on the 4B/0.6B pilot decision; no trace annotation."""

import json
from datetime import datetime, timezone
from pathlib import Path

from claude_call import call


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/21-qwen3-0.6b-multiverse/audit"
SYSTEM = ("Ты технический рецензент SFT Qwen3 и Multiverse. Дай краткий, "
          "проверяемый совет на русском. Не пиши и не размечай reasoning-трейсы. "
          "Разделяй факты и гипотезы; не выдумывай метрики.")
USER = """Состояние опыта 11 октября 2026, одна наша H100 после 09:00.
Цель: Qwen3-0.6B post-trained с полноценным <Parallel> внутри <think>, независимые Path, минимальная потеря точности. Десять новых тегов одиночными токенами с разной инициализацией; обучение использует Multiverse attention mask/positions, отдельный lr для строк тегов.

Факты:
- Исходная 0.6B на masked fixed40 имеет 34/40 правильных внешних ответов.
- Проверенные 196 Sol6.1 траекторий внутри <think>, 383 строки train/arm, 24 шага, основной lr=3e-6, tag_lr_mult=100: tagged 10/40 вручную верных ответов, 0/40 полных блоков, 33/40 вложенных <Parallel>; прежний plain 26/40, но он ошибочно потерял текст Conclusion. Исправленный equal-text plain сейчас проходит 4B сравнение.
- Новые 367 Claude M1 решений перенесены внутрь <think> без правки текста; парный 0.6B SFT 70 шагов в очереди повторного запуска, результатов ещё нет.
- Подготовленная Qwen3-4B до обучения с тегами: 0/40 блоков, robust ответ 33/40, внешняя строка 24/40, 7 обрезаний. На том же Sol196 завершены paired tagged/plain 16 шагов, фиксированная оценка идёт. Tagged шаг4 на первых 10 GSM8K: 0/10 блоков, 7/10 robust ответов, 3 обрезания; остальные шаги ещё не оценены.
- Первый запуск SFT погиб на cgroup RAM 160GiB при checkpoint, не на GPU; после evict собственных файлов из page cache и BF16 checkpoint полный 4B SFT завершился. Эта проблема решена, выводов о качестве из неё нет.
- Новый 4B teacher из 320 leak-clean задач: 163 правильных необрезанных; после строгой семантической проверки только 25 исходных и ещё 9 переписанных траекторий пригодны, 34 всего. Качество важнее числа.

Вопросы:
1) Какой конкретный минимальный диагностический тест покажет, что теги плохо учатся, а не просто не инициируются из-за промпта? Укажи наблюдаемые величины и критерий решения.
2) Как при одном GPU расставить следующие два SFT опыта на уже готовых данных после 4B и M1 оценки? Допускается поменять tag_lr_mult, но plain должен отличаться от tagged только удалением тегов. Предложи контроль потери точности.
3) Стоит ли отбрасывать 4B ветку после шага4 0/10 блоков, либо сначала смотреть шаг16? Назови правило ранней остановки, учитывая малую выборку.

Не предлагай новый платный сбор данных, frozen-наборы, отказ от независимых путей или блоки вне <think>."""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "claude_fourth_advice_prompt.json").write_text(
        json.dumps({"system": SYSTEM, "user": USER, "model": "opus[1m]"}, ensure_ascii=False, indent=2) + "\n")
    result = call(SYSTEM, USER, timeout=900, model="opus[1m]", retries=1)
    result["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "claude_fourth_advice_response.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (OUT / "claude_fourth_advice_response.md").write_text(result.get("text", "") + "\n")
    print(json.dumps({"is_error": result.get("is_error"), "cost_usd": result.get("cost_usd"),
                      "response_chars": len(result.get("text", ""))}, ensure_ascii=False))
    if result.get("is_error") or not result.get("text"):
        raise SystemExit("Opus consultation failed")


if __name__ == "__main__":
    main()
