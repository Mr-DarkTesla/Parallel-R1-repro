# Blind solutions: selected52_a

Date: 2026-10-10.

Scope: 18 questions from `selected52_a.jsonl`, in supplied order. Read project `AGENTS.md`; no answer pools, gold labels, evaluation data, or other solutions. No external calls, GPU, Kubernetes, proxy, or experiment execution. Edited only `traces52_a.jsonl` and this log. Public mathematical explanations contain shared setup, two substantive independent parts, and combination. All suggested splits are mathematically sound; all rows marked `parallelizable=true`, `status=solved`.

## Results and independent checks

- math-train/3337: sqrt(2)+sqrt(5). Integer legs must be 1 and 2 in different hypotenuse-3 right triangles. Areas sqrt(2) and sqrt(5).
- math-train/4071: x^4-6x^3+8x^2+4x-4. Conjugate factors independently derived; coefficient multiplication checked in Python.
- math-train/3061: 574. Squares 430, circles 144. Finite-segment slab intersection independently enumerated using exact fractions; square corner tangencies included.
- math-train/4602: 936. Exhaustively enumerated all 3^10 strings. Valid words 15936; vowel-count contributions 1024,5120,7168,2560,64.
- math-train/2000: 72. Bounded multiplicity enumeration independently confirms 4 vowel multisets and 18 consonant multisets.
- math-train/3520: 1247. Missing abscissa 17 from zero cubic coefficient; focus-distance identity x^2+1/4 verified algebraically.
- math-train/2205: 129. Exhaustively enumerated all 2^12 subsets; cardinality contributions 1,12,45,56,15.
- math-train/4208: 85. Common rotating orthonormal axes give base 2|9sin(theta)-2cos(theta)| and altitude |9sin(theta)-2cos(theta)|. Cauchy-Schwarz maximum 85 is attained.
- math-train/3700: 5. Exact fractional partial sums both 1364 at n=5; even parity impossible for n>=1.
- math-train/4842: 795. Exhaustive prime-pair enumeration confirms admissible products 138,777,795.
- math-train/1790: 195. Direct integer enumeration 1..600 confirms count.
- math-train/3181: (1+sqrt(5))/2. Four pivot radii independently reconstructed from quarter-turn positions: sqrt(5)/2,1/2,1/2,sqrt(5)/2.
- math-train/2305: 66. 72 pair-orientation constructions, 3 all-nonagon triangles each counted 3 times.
- math-train/7391: 241/220. Even coefficient sum 241, odd imaginary coefficient sum -220. Product identity checked for signs using P(i)=241-220i and P(-i)=241+220i.
- math-train/5123: 6. Original stamps 2016, stamps on full new pages 2010.
- math-train/4351: 250500. Enumerated q=1..251000 with exact integer-square discriminant checks; 500 excluded integral residual pairs.
- math-train/2260: 1/14. Exact factorial ratio 5!*4!/8! simplified using Fraction.
- math-train/7467: 2016532. Exact rational union of both solution families checked for every n=2..101. General overlap proof gives one duplicated root only for n=1 mod 4. Full arithmetic sum 2017033 minus 501.

## Commands and validation evidence

Initial reads: `pwd`, `rg --files -g AGENTS.md -g selected52_a.jsonl`, `cat AGENTS.md`, `cat results/21-qwen3-0.6b-multiverse/audit/deep_trace_round2/selected52_a.jsonl`.

Python invocation `python` failed with `zsh:1: command not found: python`; switched to `python3`. All subsequent Python commands completed with exit code 0.

Creation: a `python3` heredoc loaded the selected JSONL, stored independently derived explanations by ID, preserved source questions and order, and wrote exactly 18 JSON lines via `json.dumps(...,ensure_ascii=False)`.

Structural validation confirmed exactly 18 unique IDs, same source ID/question order, precisely required fields, `solved` statuses, true parallelizable flags, one opening/closing think tag per response, a final answer, and both parts longer than 80 characters. No byte comparisons or hashes.

Independent enumeration commands, reproducible Python fragments:

```python
from fractions import Fraction
import itertools, math

# Finite-segment square slabs and circle distances.
m=n=0
for a in range(1002):
    near=3*a//7
    for b in range(max(0,near-2),min(429,near+2)+1):
        lower=max(Fraction(0),Fraction(10*a-1,70),Fraction(10*b-1,30))
        upper=min(Fraction(143),Fraction(10*a+1,70),Fraction(10*b+1,30))
        m += lower<=upper
        k=3*a-7*b
        projection=7*a+3*b
        n += 100*k*k<=58 and 0<=projection<=143*58
assert (m,n,m+n)==(430,144,574)

# Exhaustive words.
count=0
for letters in itertools.product('MOP',repeat=10):
    pos=[i for i,l in enumerate(letters) if l=='O']
    count += all(b-a>=3 for a,b in zip(pos,pos[1:]))
assert count==15936

# Bounded multiset counts.
vowels=sum(sum(t)==2 for t in itertools.product(range(3),range(2),range(2)))
cons=sum(sum(t)==4 for t in itertools.product(range(3),range(3),range(2),range(2),range(2)))
assert (vowels,cons)==(4,18)

# Exhaustive spacy subsets.
spacy=0
for mask in range(1<<12):
    pos=[i for i in range(12) if mask>>i&1]
    spacy += all(b-a>=3 for a,b in zip(pos,pos[1:]))
assert spacy==129

# Exact cubic residual discriminants.
valid=integer_residual=0
for q in range(1,251001):
    d=1002**2-4*q
    sq=math.isqrt(d)
    integer_pair=(sq*sq==d and (1002-sq)%2==0)
    integer_residual += integer_pair
    valid += not integer_pair
assert (integer_residual,valid)==(500,250500)

# Exact sine-family unions and full summation.
for n in range(2,102):
    A={Fraction(2*k,n-1) for k in range((n-1)//2+1)}
    B={Fraction(2*k+1,n+1) for k in range(n//2+1)}
    assert len(A|B)==n+1-(n%4==1)
assert sum(n+1-(n%4==1) for n in range(2,2008))==2016532
```

Validation output:

```text
STRUCTURE PASS: 18 IDs/questions preserved in order; all required fields, tags, and substantive parts valid.
LATTICE PASS: 430 144 574
WORDS PASS: 15936 936
MAGNETS PASS: 4 18 72
SPACY PASS: 129
QUARTIC PASS: ascending coefficients [-4, 4, 8, -6, 1]
PRIME PRODUCTS PASS: [138, 777, 795]
DIGIT5 PASS: 195
GEOMETRIC SUM PASS: 1364
CUBIC PASS: 500 250500
SINE PASS: exact family unions n=2..101; full sum 2016532
REMAINING ARITHMETIC PASS: focus, stamps, seating, equilateral triangles.
```

No uncertain answers or rejected splits. No gold-based correctness claim; evidence is independent derivation and local exact checks.
