## strongest

- cand `math-train/1173` vs `math_train_replay(info)/math-train/1173` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 1, 'ng8': 6, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: Evaluate $\log_3 27\sqrt3$. Express your answer as an improper fraction. || ans=\frac72
  - E: Evaluate $\log_3 27\sqrt3$. Express your answer as an improper fraction. || ans=\frac72
- cand `math-train/1128` vs `math_train_replay(info)/math-train/1128` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 16, 'ng8': 20, 'formula_or_nums_same_ans': 1, 'ng8_contain': 0.952, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: If $x+y=\frac{7}{12}$ and $x-y=\frac{1}{12}$, what is the value of $x^2-y^2$? Express your answer as a common fraction. || ans=\frac{7}{144}
  - E: If $x+y=\frac{7}{12}$ and $x-y=\frac{1}{12}$, what is the value of $x^2-y^2$? Express your answer as a common fraction. || ans=\frac{7}{144}
- cand `math-train/1227` vs `math_train_replay(info)/math-train/1227` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 1, 'ng8': 1, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: Evaluate $\log_82$. || ans=\frac13
  - E: Evaluate $\log_82$. || ans=\frac13
- cand `gsm8k-train/6828` vs `math_train_replay(info)/math-train/779` signals={'leak': False, 'strong': False, 'jac': 0.333, 'ng8_ok': False, 'dup': False, 'tier': None}
  - C: A school bought pencils and pens. A pencil costs $2.50, while a pen costs $3.50. How much do 38 pencils and 56 pens cost? || ans=291
  - E: The cost of five pencils and one pen is $\$2.50$, and the cost of one pencil and two pens is $\$1.85$. What is the cost of two pencils and one pen? || ans=1.45
- cand `math-train/1821` vs `math_test_full(info)/math-test/3264` signals={'leak': False, 'strong': False, 'ng8': 1, 'ng8_contain': 0.1, 'ng8_ok': False, 'dup': False, 'tier': None}
  - C: What is the units digit of the sum $1! + 2! + 3! + 4! + 5! + \cdots + 1000!$? || ans=3
  - E: What is the units digit of the sum of the squares of the first nine positive integers? || ans=5
## borderline jac 0.45-0.7 (no exact/ng13)
