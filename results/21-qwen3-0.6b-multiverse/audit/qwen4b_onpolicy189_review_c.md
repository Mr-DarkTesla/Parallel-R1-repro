# Qwen4B on-policy 189: independent-path audit C

Reviewed all 33 assigned provisional rows (IDs 66–98) in
`qwen4b_onpolicy189_review_c_input.jsonl`.

Strict PASS requires two distinct, nontrivial, mathematically correct paths
derived independently from the givens; a conclusion that materially uses both;
a correct final answer; and all Parallel structure inside `<think>`.

| ID | Verdict | Reason |
|---|---|---|
| gsm8k-train/1746 | PASS | Independent payroll calculations for 500 original and 200 new employees are correct; conclusion combines them to correct `1680000`. |
| gsm8k-train/2257 | FAIL | Path 2 only restates given one-quarter fraction; it is not a nontrivial independent derivation. Final `750` is correct. |
| math-train/3154 | PASS | Arc-to-base-radius and sector-radius-to-slant-height are independent correct facts; conclusion uses both for correct `4sqrt(2)`. |
| gsm8k-train/6713 | PASS | Blueberry and cherry fruit costs are independently correct; conclusion compares both and yields correct cheapest-pie cost `18`. |
| gsm8k-train/1974 | FAIL | Path 2 leaves senior allowance as symbolic `2x+5` instead of independently evaluating it from the given middle allowance. Final `150%` is correct. |
| gsm8k-train/3878 | FAIL | Path 2 merely repeats the given price `$0.50`; no second nontrivial path. Final `80` is correct. |
| gsm8k-train/3292 | FAIL | Path 2 merely repeats the given deaf-student count `180`; no second nontrivial path. Final `240` is correct. |
| gsm8k-train/6845 | PASS | Apple and orange cost/revenue/profit calculations are independent and correct; conclusion sums them to correct `$3`. |
| math-train/529 | PASS | Independent numerator `3^7` and denominator `2^7` calculations are correct; conclusion combines them with leading `3` to correct `6561/128`. |
| gsm8k-train/3750 | PASS | Doll time and accessory time are independent correct calculations; conclusion adds them to correct `1860000`. |
| math-train/3474 | FAIL | Path 2 reuses Path 1's derived `z=13`, so paths are sequential. Final `109.2` is correct. |
| gsm8k-train/5759 | PASS | Full-name letter counts for Jonathan and sister are independent correct subtotals; conclusion combines them to `33`. |
| math-train/1155 | FAIL | Arbitrary case split is redundant: Path 1's linear denominator calculation already applies globally, while Path 2 contributes no independent necessary derivation. Final domain is correct. |
| gsm8k-train/6557 | PASS | Trout and blue-gill counts are independent, nontrivial calculations from given bass count; conclusion combines them with bass to correct `104`. |
| gsm8k-train/5025 | PASS | Each applicant's net earnings calculation is independent and correct; conclusion compares them to correct `850`. |
| gsm8k-train/1103 | PASS | Total rose and orchid counts are independent correct subtotals; conclusion combines them before correct lily calculation `6`. |
| math-train/3440 | FAIL | Paths split one telescoping cancellation into numerator and last denominator, with Path 2 only restating the terminal denominator; no independent second solution. Final `1/50` is correct. |
| gsm8k-train/1347 | FAIL | Path 2 only repeats the given five extra cabinets; it is not nontrivial. Final `26` is correct. |
| gsm8k-train/4149 | FAIL | Path 2 incorrectly totals capacity as `217` instead of `399`; two correct paths absent. Final `299` is correct. |
| math-train/6329 | FAIL | Path 2 repeats Path 1's derivation of `y=w+30`, so it is not independent. Final `115` is correct. |
| gsm8k-train/3356 | FAIL | Path 2 repeats Path 1's `80-20=60` computation, so paths are dependent. Final `30` is correct. |
| math-train/5385 | FAIL | Path 2 relies on repeating block derived in Path 1; it has no independent basis for sixth digit. Final `5` is correct. |
| math-train/5764 | PASS | Highest powers of `2` and `3` are independently and correctly derived; conclusion materially combines them with prime factor `5` to correct LCM `180`. |
| gsm8k-train/5075 | FAIL | Path 2 merely restates given `$10` discount per qualifying `$100`; no second nontrivial path. Final `230` is correct. |
| gsm8k-train/1673 | FAIL | Path 2 only repeats given `$10` on hand; it is not a nontrivial independent derivation. Final `8` is correct. |
| math-train/1406 | FAIL | Paths calculate only two of four FOIL products; conclusion explicitly leaves required terms outside block, so it does not materially solve expansion. Final polynomial is correct. |
| gsm8k-train/6960 | FAIL | Path 2 uses Path 1's derived mowing income `$15`, so paths are sequential. Final `45` is correct. |
| gsm8k-train/4029 | FAIL | Path 2 wrongly treats pencil cost as `100*0.90` and confuses it with pop cost; two correct paths absent. Final `300` is correct. |
| math-train/4960 | FAIL | Path 2's asserted divisor list for variable `a+4` is false and does not establish its claim. Final gcd `4` is correct. |
| math-train/6162 | FAIL | Path 2 computes remainder using Path 1's quotient `7`; paths are dependent. Final `49` is correct. |
| gsm8k-train/3303 | FAIL | Both paths repeat same second-week calculation (`350`, `105`); Path 2 is not independent. Final `196` is correct. |
| math-train/505 | FAIL | Paths are duplicate applications of the same geometric-series formula; conclusion only equates them. Final `116050/59049` is correct. |
| gsm8k-train/5916 | FAIL | Path 1 merely repeats given female count `13`; no second nontrivial path. Final `52` is correct. |

Summary: 11 PASS, 22 FAIL. All 33 rows keep Parallel structure inside
`<think>`, and all 22 FAIL rows have correct final answers. Therefore every
FAIL ID above is a final-answer scorer false positive if that scorer accepted
the row solely from final-answer accuracy: `gsm8k-train/2257`,
`gsm8k-train/1974`, `gsm8k-train/3878`, `gsm8k-train/3292`,
`math-train/3474`, `math-train/1155`, `math-train/3440`,
`gsm8k-train/1347`, `gsm8k-train/4149`, `math-train/6329`,
`gsm8k-train/3356`, `math-train/5385`, `gsm8k-train/5075`,
`gsm8k-train/1673`, `math-train/1406`, `gsm8k-train/6960`,
`gsm8k-train/4029`, `math-train/4960`, `math-train/6162`,
`gsm8k-train/3303`, `math-train/505`, and `gsm8k-train/5916`.
