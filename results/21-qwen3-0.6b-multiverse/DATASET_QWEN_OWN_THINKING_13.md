# Собственные thinking-трейсы Qwen: 13 строгих plan-only блоков

10 октября 2026. Источник: 300 уже сохранённых верных ответов Qwen3-0.6B в `data/replay_th.jsonl`, полученных до этой разметки. Текстовые субагенты добавляли только план и теги внутри исходного `<think>`, не переписывая рассуждение. Новых вызовов GPU и VK AI Proxy для разметки не было. Эти 13 задач **не новые для обучения**: исходные ответы уже входили в replay. В текущий SFT `deep75` этот набор не включён, чтобы один и тот же Qwen-ответ не встречался одновременно как tagged и untagged без отдельного контроля.

## Отбор

| Этап | Осталось | Причина |
|---|---:|---|
| Сохранённые верные thinking-ответы | 300 | MATH 131, GSM8K 82, ARC 87 |
| Строгий скрининг | 213 | ARC пока не брали; нужны две независимые вычислительные части |
| Подходят по структуре | 16 | Большинство исходных трейсов строят одну зависимую цепочку |
| Размечены и независимо приняты | 14 | `math-train/1283` и `/4511` не удалось разделить без нарушения зависимости или дословности |
| Финальный набор после leakcheck | 13 | `math-train/840` исключён по слабому сходству условия с `math-test/314` из полного MATH test |

В 25 из 213 трейсов проверяющие отметили существенную ошибку или противоречие **в промежуточном тексте**, хотя финальный ответ до скрининга был принят как верный. Это построчные качественные оценки, а не измерение частоты ошибок всех ответов модели. Результаты по каждому из 213: `audit/qwen_trace_screen/screen_{a,b,c}.jsonl`.

У всех 14 размеченных до leakcheck решений независимое ревью подтвердило ответ, существенные шаги, полезность путей и сохранность исходного Qwen-текста. `checks.py` прошёл 14/14: грамматика, нумерация, ответ, числа, отсутствие межпутевых ссылок и восстановление текста после удаления плана и тегов. Финальные 13 проходят leakcheck с **0 утечек против наших eval и полного MATH test**, 0 дублей или вариантов eval. Три совпадения с информационным корпусом MATH train ожидаемы и не являются eval-утечкой. История до исключения `840`: `leakcheck_accepted14.*`; финальная: `leakcheck_accepted13.summary.json` и `accepted13_with_gold.jsonl`.

По токенизатору подготовленной Qwen3-0.6B полный обучающий ряд: 578–1809 токенов, среднее 1112,3; 0/13 длиннее лимита 4096 (`audit/qwen_trace_screen/token_lengths13.json`). Итоговый текст: `accepted13.jsonl`, независимые ревью: `tagged_{a,b,c}_review.jsonl`. Воспроизведение финального отбора: `python -B scripts/exp21/finalize_qwen_trace13.py`.

## Пример `math-train/5938`

**Вопрос.** Compute $(4+8)^2+(4^2+8^2)$.

**Ответ.** Исходная Qwen отдельно вычислила два слагаемых. После блока она сложила результаты. Её повторы и самопроверка оставлены дословно; они показывают реальный стиль модели.

```text
<think>
Okay, let's see. I need to compute this expression: (4 + 8) squared plus (4 squared plus 8 squared). Hmm, let me break it down step by step. First, I should handle the parentheses and then the exponents.

<Parallel>
<Goal>
<Outline>1: Evaluate the squared sum (4 + 8)^2.</Outline>
<Outline>2: Evaluate the separate-square term 4^2 + 8^2.</Outline>
</Goal>
<Path>1:
Starting with the first part: (4 + 8). Adding 4 and 8 gives me 12. Then, I square that result. So, 12 squared. Wait, squaring 12... Let me think. 12 times 12 is 144. Got that part.

</Path>
<Path>2:
Now, the second part is (4 squared plus 8 squared). Let me compute each term separately. 4 squared is 16, right? And 8 squared is 64. Adding those together: 16 + 64 equals 80. Okay, so that part is 80.

</Path>
<Conclusion>Add the two evaluated terms.</Conclusion>
</Parallel>

Now, the original problem is combining both parts: (12 squared) plus (80). So, 144 plus 80. Let me add those. 144 + 80... Hmm, 144 + 80 is 224. Let me check that again. 144 + 80 is 224. Yeah, that seems right.

Wait, just to make sure I didn't make any mistakes. Let me verify each step once more.

First term: (4 + 8) = 12. Squared is 144. Second term: 4² is 16, 8² is 64, sum is 80. Then 144 + 80 is indeed 224. Yeah, that looks correct. I don't see any errors here.

So, the final answer should be 224. Let me make sure there's no step I missed. The problem is straightforward, combining two parts. No parentheses in the second part? Wait, the problem says (4^2 + 8^2), which is 4 squared plus 8 squared. So, that's correct.

Final Answer: 224
</think>

Final Answer: 224
```
