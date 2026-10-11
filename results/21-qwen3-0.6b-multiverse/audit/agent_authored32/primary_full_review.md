# Primary full-text review of the first 32 authored examples

11 October 2026. Read the complete question and complete solution
for all 16 MATH and 16 GSM8K pilot examples, rather than only the
parser output. Checked arithmetic, both Paths, their use in the
Conclusion, and placement inside `<think>`. This review uses the
same strict two-substantive-path criterion as the Qwen pilots.

All 16 MATH examples were accepted: `110`, `3947`, `6412`, `1024`,
`4730`, `1982`, `5531`, `251`, `7012`, `5103`, `3533`, `986`,
`3849`, `3440`, `505`, `2368` (prefix `math-train/`). The two
independent subcomputations and external answers were correct. The
rounded monetary answer in `1982` is the requested `0.67`; the
external checker initially compared it with the entire gold display
`\frac23 \approx \$0.67`. The checker was corrected to compare the
displayed rounded value after `\approx`, with an explicit
wrong-value check. Rerunning the earlier generic Qwen pilot left
its 25/128 automatic acceptance unchanged.

GSM8K accepted 14/16: `5851`, `2281`, `6467`, `1170`, `2528`,
`4597`, `3721`, `6410`, `201`, `4780`, `6229`, `3862`, `6020`,
`3576` (prefix `gsm8k-train/`). Six external answers originally
used an unclosed LaTeX currency dollar delimiter (`3721`, `6410`,
`4780`, `6229`, `3862`, `6020`); they were changed to bare numbers
without changing the reasoning or answer. The original GSM file is
preserved as `gsm16_before_format_fix.jsonl` in this directory.
`1170` received a clearer second Outline and Conclusion, then an
independent second review accepted the repair.

Rejected two semantically weak GSM8K blocks despite correct final
answers:

| ID | Reason |
| --- | --- |
| `gsm8k-train/5392` | Path 2 restates the given one-log yield as `9 × 1 = 9`; it is not a substantive parallel computation. Independent adjudication of the same structure in a Qwen trace reached the same verdict. |
| `gsm8k-train/5215` | Path 1 repeats the given 32-hair washing loss, leaving only the brushing computation as actual work. |

Independent cross-reviews examined all 32 examples and initially
found 32 mathematically correct answers. Applying the stricter
substantive-path criterion here leaves **30/32 useful blocks
(93.75%)**, with **zero wrong answers** among accepted examples.
All 32 have a single complete block inside `<think>` and an external
answer. The two rejected rows are excluded from any SFT set.
