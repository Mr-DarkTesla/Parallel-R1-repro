# Independent review: agent-authored remaining GSM

## Scope

Reviewed all 24 rows in `data/onpolicy_agent_authored_gsm_remaining.jsonl` against the literal questions in `data/onpolicy46_questions_only.jsonl` and the reference answer in `data/onpolicy46_candidates.jsonl`. Checked arithmetic, external answer, path independence and usefulness, conclusion, placement inside `<think>`, and absence of a precomputed answer before `<Parallel>`.

A Path that only restates a supplied quantity without a separate necessary computation is rejected under the requested strict rule.

| ID | Verdict | Review finding |
|---|---|---|
| `gsm8k-train/1362` | **accept** | Each person's final gumball holding is independently computed; pooling and equal split are correct. Gold and external answer: 250. |
| `gsm8k-train/346` | **accept** | Two wall-area groups are independently substantive; area, coverage conversion, and answer are correct. Gold/external: 15. |
| `gsm8k-train/4921` | **accept** | Bills and all coin denominations are independently valued, then correctly added. Gold/external: 13. |
| `gsm8k-train/5711` | **accept** | Fixed expenses and net hourly earnings are distinct computations; break-even equation is correct. Gold/external: 3. |
| `gsm8k-train/2502` | **reject** | Answer arithmetic is correct (gold/external: 50), and the base-game Path is substantive. Path 2 merely repeats the prompt's given 30 enjoyable expansion hours and explicitly performs no independent calculation. This violates the strict no-repeated-given-number branch rule. |
| `gsm8k-train/6149` | **accept** | Chip and cookie total weights are independently computed; ounce-to-pound conversion is correct. Gold/external: 21. |
| `gsm8k-train/2619` | **accept** | Monday-Tuesday and Wednesday-Friday attendance totals are distinct and correctly averaged. Gold/external: 11. |
| `gsm8k-train/6195` | **accept** | Each person's percentage-derived pink-crayon count is independent and correct. Gold/external: 14. |
| `gsm8k-train/982` | **accept** | Production and consumption totals are independently substantive; subtraction is correct. Gold/external: 134. |
| `gsm8k-train/1295` | **accept** | Friend and relative revenue calculations are independent and correct. Gold/external: 25. |
| `gsm8k-train/2200` | **accept** | Chicken and sheep leg contributions are independently computed and added correctly. Gold/external: 34. |
| `gsm8k-train/7086` | **accept** | Five-day popcorn and cotton-candy revenues are separately computed; operating-cost subtraction is correct. Gold/external: 895. |
| `gsm8k-train/4340` | **accept** | Saturday and Sunday revenues are independently derived and correctly added. Gold/external: 300. |
| `gsm8k-train/467` | **accept** | Outward and return route distances each receive a real calculation and add correctly. Gold/external: 6. |
| `gsm8k-train/4013` | **accept** | Deposits and purchases are separately totaled; remaining balance is correct. Gold/external: 14. |
| `gsm8k-train/1502` | **accept** | Cupcake supply and attendee count are independent calculations; subtraction is correct. Gold/external: 4. |
| `gsm8k-train/2376` | **accept** | Brownie-plus-ice-cream and topping subtotals are independently computed; total is correct. Gold/external: 7. |
| `gsm8k-train/5074` | **accept** | Nose and ear revenue streams have independent price/count calculations and sum correctly. Gold/external: 390. |
| `gsm8k-train/1856` | **accept** | Danny's and his sister's slice totals are independent and correct. Gold/external: 45. |
| `gsm8k-train/3106` | **accept** | Original-shipment remainder and later shipment are independently computed and added correctly. Gold/external: 2500. |
| `gsm8k-train/6080` | **accept** | The two diner groups calculate disjoint pizza consumption; the slice remainder is correct. Gold/external: 9. |
| `gsm8k-train/5172` | **reject** | Answer arithmetic is correct (gold 20, external 20%), and the non-pushup Path is substantive. Path 1 only repeats the prompt's given 8 pushups without an independent calculation, violating the strict no-repeated-given-number branch rule. |
| `gsm8k-train/6845` | **accept** | Apple and orange costs/revenues are independently computed; the profit sum is correct. Gold/external: 3. |
| `gsm8k-train/3750` | **accept** | Doll and accessory machine times are distinct substantive calculations and add correctly. Gold/external: 1860000. |

## Aggregate

- Accepted: **22/24**
- Rejected: **2/24** (`gsm8k-train/2502`, `gsm8k-train/5172`)
- Gold mismatch among accepted rows: **0**
- Wrong external answer among accepted rows: **0**
- Full Parallel block inside `<think>`: **24/24**
- Precomputed answer before the block: **0/24**
