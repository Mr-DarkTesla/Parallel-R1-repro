"""Bounded technical advice for the next 0.6B inside-thinking SFT experiment."""

import json
from datetime import datetime, timezone
from pathlib import Path

from claude_call import call


OUT = Path(__file__).resolve().parents[2] / "results/21-qwen3-0.6b-multiverse/audit"
SYSTEM = ("Ты технический рецензент SFT малых Qwen3. Ответь конкретно и кратко. "
          "Не размечай reasoning-трейсы. Разделяй измеренные факты и гипотезы.")
USER = """Цель: post-trained Qwen3-0.6B должна сама генерировать корректный
<Parallel> внутри <think> с двумя независимыми <Path> и верным ответом,
без большой потери обычных GSM8K/MATH/ARC/MMLU-Pro/IFEval метрик.
Десять тегов добавлены как отдельные спецтокены с разной инициализацией.
SFT использует настоящие Multiverse attention mask/positions; tag_lr_mult=100.
Один наш H100. Допускается тратить ещё GPU-время, но frozen-наборы до выбора
не открывать. Текущий прокси-бюджет $200, потрачено не менее $75.63.

Измерения на одинаковом masked greedy fixed40:
- Исходная 0.6B: 34/40 верных ответов, 0/40 блоков.
- 0.6B с 367 верными Claude M1 решениями, блоки перенесены внутрь <think>
  без изменения текста, 64 шага: 27/40 полных блоков, лишь 12/40 верных
  ответов. M2 на 367 собственных Qwen-текстах: 20/40 блоков и 20/40
  верных ответов. Оба варианта потеряли IFEval.
- 0.6B selective v4 step56: 27/40 верных, 19/40 полных,
  лишь 2/40 строго полезных независимых блока. Короткое продолжение
  recovery8: 29/40 верных, 2/40 полезных.
- 4B с Sol196 inside-think после 16 шагов tagged: 36/40 верных,
  0/40 блоков; equal-text plain: 34/40 верных, 0/40 блоков.
- Подготовлены 401 положительная задача для 4B, 367 M1 + 34 дважды
  проверенные собственные 4B решения. Парный 4B SFT 128 шагов уже в очереди.

Нужен один следующий опыт именно для 0.6B, после текущей очереди.
Предложи минимальный парный рецепт tagged/plain, который позволит
понять, можно ли выучить добровольный старт и завершение тегов без
переписывания всей математики модели. Укажи точный выбор родителя,
состав обучающих строк, что оптимизировать/заморозить, диапазон шагов
и lr, диагностические измерения после каждого сохранённого шага,
критерий ранней остановки по dev. Учитывай, что предыдущий tag-only
опыт дал 27/40 верных, но 0/40 полных блоков. Не предлагай
принудительную вставку тегов декодером как успех, блоки вне <think>,
новый дорогой сбор без доказанной нужды или сравнение на разных промптах.
Если считаешь цель недостижимой для 0.6B при текущих данных, скажи,
какое дешёвое диагностическое измерение это опровергнет или подтвердит.
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "opus_fifth_06b_prompt.json").write_text(
        json.dumps({"system": SYSTEM, "user": USER, "model": "opus[1m]"},
                   ensure_ascii=False, indent=2) + "\n")
    result = call(SYSTEM, USER, timeout=900, model="opus[1m]", retries=1)
    result["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "opus_fifth_06b_response.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (OUT / "opus_fifth_06b_response.md").write_text(result.get("text", "") + "\n")
    print(json.dumps({"error": result.get("is_error"), "cost_usd": result.get("cost_usd"),
                      "chars": len(result.get("text", ""))}, ensure_ascii=False))
    if result.get("is_error") or not result.get("text"):
        raise SystemExit("Opus consultation failed")


if __name__ == "__main__":
    main()
