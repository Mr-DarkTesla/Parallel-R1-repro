# Blind review: accepted set A

Scope: 15 supplied rows only. `Answer correct` checks the external answer mathematically. `Useful` additionally requires a complete block inside `<think>`, nontrivial correct paths derived independently from the givens, and a conclusion that uses the paths.

Summary: answer correct `YES` for 15/15; useful `YES` for 12/15.

| ID | Answer correct | Useful | Reason |
|---|---|---|---|
| `gsm8k-train/5759` | YES | YES | (8+10=18), (5+10=15), and (18+15=33). Full block is inside `<think>`; two paths independently compute the two name lengths, and the conclusion uses both. |
| `gsm8k-train/6713` | YES | YES | Blueberries cost ((3×16/8)×2.25=13.50), less than the cherry cost of 14; crust costs 4.50, so total is 18. Full block; both fruit-cost paths are nontrivial and independent, and the conclusion compares both. |
| `gsm8k-train/4921` | YES | NO | Bills total 7; coins total (13(0.25)+20(0.10)+8(0.05)+35(0.01)=6); external answer 13 is correct. Block and paths are otherwise valid, but the opening claim says there are “two kinds of coins” although four denominations are given. This factual error makes the training row unreliable. |
| `gsm8k-train/4340` | YES | YES | Saturday pays (20×10=200); Sunday has 10 children and pays 100; total 300. Full block; day-specific paths are nontrivial and independent, and the conclusion uses both. |
| `gsm8k-train/2619` | YES | YES | Total attendance is (10+15+3×10=55); (55/5=11). Full block; paths independently total the two day groups, and the conclusion combines them. |
| `gsm8k-train/467` | YES | NO | Distance is (2+(2-1)+(4-1)=6), so the external answer is correct. Full block and path arithmetic are correct, but the pre-block plan falsely says the third leg is “in terms of the first two,” and Outline 1 names only the grocery-to-pet leg while Path 1 also handles the first leg. This internal mismatch weakens the training signal. |
| `gsm8k-train/6557` | YES | NO | Counts are 32 bass, (32/4=8) trout, and (2×32=64) bluegill; total 104. Full block and conclusion use all three paths, but Path 1 only repeats the given “32 bass” and performs no derivation. It fails the nontrivial-path requirement. |
| `gsm8k-train/6080` | YES | YES | Two pizzas contain 24 slices; diners eat (6+4+2+3=15), leaving 9. Full block; the two paths independently total two diners each, and the conclusion combines them. |
| `gsm8k-train/3750` | YES | YES | Dolls take (12000×45=540000) seconds; 11 accessories per doll take (12000×11×10=1320000); total 1860000. Full block; paths independently compute both production components, and the conclusion uses both. |
| `gsm8k-train/1362` | YES | YES | Joanna ends with (40+4×40=200); Jacques with (60+4×60=300); equal share is ((200+300)/2=250). Full block; paths are independent and the conclusion uses both. |
| `gsm8k-train/3674` | YES | YES | From (m+f=120) and (m=f+4), (f=58) and (m=62). Full block; both paths independently solve one attendee count from the givens, and the conclusion reports both. |
| `gsm8k-train/1746` | YES | YES | Monthly pay per worker is (12×10×5×4=2400); ((500+200)×2400=1680000). Full block; paths independently compute original and new-hire payroll, and the conclusion adds both. |
| `gsm8k-train/1952` | YES | YES | Daily counts (10,14,18,22,26,30) total 120; at 0.10 dollars each, earnings are 12. Full block; paths derive quantity and unit price independently, and the conclusion multiplies both. |
| `gsm8k-train/4374` | YES | YES | Phoebe and dog need (30+30=60) servings; (60/15=4) jars. Full block; paths independently compute both consumers’ needs, and the conclusion uses both. |
| `gsm8k-train/6149` | YES | YES | Chips weigh (6×20=120) oz; 24 cookie tins weigh (24×9=216) oz; ((120+216)/16=21) lb. Full block; paths independently compute both weights, and the conclusion combines them. |
