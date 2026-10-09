## strongest

- cand `math-train/3170` vs `math_train_replay(info)/math-train/3170` signals={'leak': True, 'strong': True, 'exact': 1, 'asy_same': 1, 'ng13': 3, 'ng8': 8, 'anskw': 1.0, 'jac': 1.0, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: $ABCDEFGH$ shown below is a cube with volume 1. Find the volume of pyramid $ABCH$. [asy] import three; triple A,B,C,D,EE,F,G,H; A = (0,0,0); B = (1,0,0); C = (1,1,0); D= (0,1,0); EE = (0,0,1); F = B+EE; G = C + EE; H = D + EE; draw(B--C--D); draw(B--A--D,dashed); draw(EE--F--G--H--EE); draw(A--EE,dashed); draw(B--F); draw(C--G); draw(D--H); label("$A$",A,S); label("$B$",B,W); label("$C$",C,S); lab || ans=\frac16
  - E: $ABCDEFGH$ shown below is a cube with volume 1. Find the volume of pyramid $ABCH$. [asy] import three; triple A,B,C,D,EE,F,G,H; A = (0,0,0); B = (1,0,0); C = (1,1,0); D= (0,1,0); EE = (0,0,1); F = B+EE; G = C + EE; H = D + EE; draw(B--C--D); draw(B--A--D,dashed); draw(EE--F--G--H--EE); draw(A--EE,dashed); draw(B--F); draw(C--G); draw(D--H); label("$A$",A,S); label("$B$",B,W); label("$C$",C,S); lab || ans=\frac16
- cand `math-train/1472` vs `math_train_replay(info)/math-train/1472` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 17, 'ng8': 22, 'formula_or_nums_same_ans': 1, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: If $f(x) = 2x + 3$ and $g(x) = 3x - 2$ find $\frac{f(g(f(2)))}{g(f(g(2)))}$. Express your answer in the form $\frac{a}{b}$. || ans=\frac{41}{31}
  - E: If $f(x) = 2x + 3$ and $g(x) = 3x - 2$ find $\frac{f(g(f(2)))}{g(f(g(2)))}$. Express your answer in the form $\frac{a}{b}$. || ans=\frac{41}{31}
- cand `math-train/6462` vs `math_train_replay(info)/math-train/6462` signals={'leak': True, 'strong': True, 'exact': 1, 'ng13': 1, 'ng8': 3, 'formula_or_nums_same_ans': 1, 'ng8_contain': 1.0, 'ng8_ok': True, 'dup': True, 'tier': 'dup'}
  - C: What is $w + 2 - 3w - 4 + 5w + 6 - 7w - 8$? || ans=-4w - 4
  - E: What is $w + 2 - 3w - 4 + 5w + 6 - 7w - 8$? || ans=-4w - 4
- cand `math-train/840` vs `math_test_full(info)/math-test/314` signals={'leak': True, 'strong': True, 'ng13': 6, 'ng8': 16, 'ng8_contain': 0.281, 'ng8_ok': False, 'dup': False, 'tier': 'weak'}
  - C: Rationalize the denominator of $\frac{5}{2+\sqrt{6}}$. The answer can be written as $\frac{A\sqrt{B}+C}{D}$, where $A$, $B$, $C$, and $D$ are integers, $D$ is positive, and $B$ is not divisible by the square of any prime. If the greatest common divisor of $A$, $C$, and $D$ is 1, find $A+B+C+D$. || ans=3
  - E: Rationalize the denominator of $\frac{\sqrt{5}+\sqrt{2}}{\sqrt{5}-\sqrt{2}}$. The answer can be written as $\frac{A+B\sqrt{C}}{D}$, where $A$, $B$, $C$, and $D$ are integers, $D$ is positive, and $C$ is not divisible by the square of any prime. If the greatest common divisor of $A$, $B$, and $D$ is 1, find $A+B+C+D$. || ans=22
- cand `math-train/999` vs `math300/math300/314` signals={'leak': False, 'strong': False, 'ng8': 1, 'ng8_contain': 0.037, 'ng8_ok': False, 'dup': False, 'tier': None}
  - C: A quadrilateral has vertices at $(0,1)$, $(3,4)$, $(4,3)$ and $(3,0)$. Its perimeter can be expressed in the form $a\sqrt2+b\sqrt{10}$ with $a$ and $b$ integers. What is the sum of $a$ and $b$? || ans=6
  - E: The number $(\sqrt{2}+\sqrt{3})^3$ can be written in the form $a\sqrt{2} + b\sqrt{3} + c\sqrt{6}$, where $a$, $b$, and $c$ are integers. What is $a+b+c$? || ans=20
## borderline jac 0.45-0.7 (no exact/ng13)
