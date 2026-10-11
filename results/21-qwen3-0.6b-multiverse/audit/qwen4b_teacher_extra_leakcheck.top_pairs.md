## strongest

- cand `math-train/967` vs `math_train_replay(info)/math-train/967` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 3, 'ng8': 8, 'jac': 0.333, 'formula_or_nums_same_ans': 1, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: The expression $\dfrac{\sqrt[3]{5}}{\sqrt[5]{5}}$ equals 5 raised to what power? || ans=2/15
  - E: The expression $\dfrac{\sqrt[3]{5}}{\sqrt[5]{5}}$ equals 5 raised to what power? || ans=2/15
- cand `math-train/6536` vs `math_train_replay(info)/math-train/6536` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 8, 'ng8': 13, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: What is the arithmetic mean of $\frac{2}{5}$ and $\frac{4}{7}$ ? Express your answer as a common fraction. || ans=\frac{17}{35}
  - E: What is the arithmetic mean of $\frac{2}{5}$ and $\frac{4}{7}$ ? Express your answer as a common fraction. || ans=\frac{17}{35}
- cand `math-train/4083` vs `math_train_replay(info)/math-train/4083` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 1, 'ng8': 1, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: Solve the inequality \[-12x^2 + 3x - 5 < 0.\] || ans=(-\infty,\infty)
  - E: Solve the inequality \[-12x^2 + 3x - 5 < 0.\] || ans=(-\infty,\infty)
- cand `math-train/1238` vs `math_train_replay(info)/math-train/1238` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 1, 'ng8': 5, 'formula_or_nums_same_ans': 1, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: Simplify the following expression: \[2x+3x^2+1-(6-2x-3x^2).\] || ans=6x^2+4x-5
  - E: Simplify the following expression: \[2x+3x^2+1-(6-2x-3x^2).\] || ans=6x^2+4x-5
- cand `math-train/392` vs `math_train_replay(info)/math-train/392` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 5, 'ng8': 7, 'formula_or_nums_same_ans': 1, 'ng8_contain': 0.7, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: What is the domain of the function $f(x)=\frac{x+6}{\sqrt{x^2-3x-4}}$? || ans=(-\infty, -1) \cup (4, \infty)
  - E: What is the domain of the function $f(x)=\frac{x+6}{\sqrt{x^2-3x-4}}$? || ans=(-\infty, -1) \cup (4, \infty)
- cand `math-train/7356` vs `math_dev/math-test/4488` signals={'leak': False, 'strong': False, 'jac': 1.0, 'ng8_ok': False, 'dup': False, 'tier': None}
  - C: Compute \[\begin{vmatrix} -5 & 3 \\ 4 & -4 \end{vmatrix}.\] || ans=8
  - E: If $\begin{vmatrix} a & b \\ c & d \end{vmatrix} = -8,$ then find \[\begin{vmatrix} b & a \\ d & c \end{vmatrix}.\] || ans=8
- cand `math-train/582` vs `math_dev/math-test/800` signals={'leak': False, 'strong': False, 'ng8': 2, 'ng8_contain': 0.08, 'ng8_ok': False, 'dup': False, 'tier': None}
  - C: What is the absolute value of the difference between the squares of 101 and 99? || ans=400
  - E: If $A=\frac{1}{4}$ and $B=-\frac{1}{2}$, what is the absolute value of the difference between $18A$ and $18B$? Express your answer as a decimal to the nearest tenth. || ans=13.5
## borderline jac 0.45-0.7 (no exact/ng13)

