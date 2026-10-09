# Blind screening: screen400_d

Reviewed 100 questions in input order. Yes: 8. No: 92.

Criterion: two naturally useful independent substantive subcomputations, each able to support a Multiverse Path longer than 80 characters from the original question/shared setup. Reject padded arithmetic, repeated full methods, symmetry duplicates and chains requiring the sibling result.

Read only screen400_d.jsonl as question data. No answers computed; no gold, pool or evaluation data accessed. No external calls or infrastructure actions.

Two questions flagged likely unsolvable under literal wording: 2507 (independent quitting versus exactly two quitters), 4411 (missing integer coefficient restriction). These judgments concern the supplied questions, without repair or assumed gold.

## Decisions

1. math-train/5018: no. One shared shifted-integer divisibility and lcm calculation.
2. math-train/2003: no. Same-color favorable terms are tiny binomial counts; total count is routine.
3. math-train/3707: no. Asymptote constraints determine coefficients before the remaining intersection calculation.
4. math-train/1982: no. One sum of three short expected-payoff terms.
5. math-train/6519: no. Double count is trivial beside a short unordered-pair count.
6. math-train/576: no. One common-result parameter and linear sum equation.
7. math-train/673: no. Single translated-vertex calculation.
8. math-train/5437: yes. Clever-integer population and favorable multiples admit independent finite counts.
   Path 1: Enumerate all even integers in the stated interval whose decimal digits sum to the required value, separating digit lengths as needed.
   Path 2: Enumerate multiples of the requested divisor within the original interval and retain those satisfying evenness and the digit-sum condition.
9. math-train/616: no. One consecutive-odd-integer substitution and equation.
10. math-train/4676: no. Single hyperbola focus formula.
11. math-train/3085: yes. The given area ratio combines two separate geometric area expressions.
   Path 1: Using shared coordinates parameterized by the side ratio and the similarity-determined interior point, derive the area of triangle AED.
   Path 2: From the same shared coordinates and original similarity conditions, derive the area of triangle CEB without the other area expression.
12. math-train/6591: no. One inequality and integer bound.
13. math-train/3188: no. Single regular-hexagon area formula.
14. math-train/2269: no. One circular angle/arc configuration probability.
15. math-train/1985: no. One equal-gender complementary binomial probability.
16. math-train/2947: yes. Upward and downward elementary triangles have distinct bounded line-index counts.
   Path 1: Count elementary equilateral triangles in one orientation from the admissible indices of the three original parallel-line families.
   Path 2: Count triangles in the opposite orientation with its own line-index bounds; combine the two nonoverlapping orientation counts.
17. math-train/3655: no. Nested radical denesting is a dependent sequence.
18. math-train/6717: no. Single total-children and nonempty-family average.
19. math-train/3896: yes. Two grouped root products reduce independently by the given quadratic equations.
   Path 1: Evaluate the product of the two minus-gamma factors using the original quadratic for alpha and beta, then gamma own quadratic.
   Path 2: Evaluate the product of the two plus-delta factors using those same original root equations, then combine via the second root-product relation.
20. math-train/3242: no. One similar-triangle area-scaling calculation.
21. math-train/1226: no. Routine elimination and substitution; repeated independent elimination is unnecessary.
22. math-train/2363: no. One short suit-permutation probability.
23. math-train/6120: no. Single rhombus side-angle area formula.
24. math-train/6101: no. Single ordered podium selection count.
25. math-train/490: no. Single intercept substitution.
26. math-train/4677: no. Conjugate-root factor precedes the dependent remaining-root and root-sum calculation.
27. math-train/3818: no. One complex-cube or ratio-polynomial derivation and Vieta evaluation.
28. math-train/6341: no. Half-perimeter travel determines the meeting location in one short chain.
29. math-train/6165: no. One short total-cost expression.
30. math-train/4394: no. One difference-product identity determines the cross ratio.
31. math-train/2415: no. Single weighted die expectation.
32. math-train/2694: no. Dependent nested inscribed-radius scaling.
33. math-train/1938: no. One daily expected rainfall multiplied by the number of days.
34. math-train/1822: no. One digit-transition graph and length/reachability analysis.
35. math-train/5320: no. One coupled residue-minimum/Frobenius analysis; no clear independent useful pair.
36. math-train/697: no. Single equal-perimeter equation.
37. math-train/3381: no. One crosswalk parallelogram area/altitude relation.
38. math-train/3729: no. Major-axis data precede the minor-axis and area calculation.
39. math-train/2475: no. Single digit-divisibility count.
40. math-train/2177: yes. Axis-aligned and slanted collinear triples need separate degenerate counts.
   Path 1: Count collinear triples on horizontal and vertical grid lines, treating each line and its possible three-point subsets.
   Path 2: Count collinear triples on nonaxis grid lines by feasible integer directions and line lengths; subtract both counts from all triples.
41. math-train/2325: no. One short conditional side-count probability.
42. math-train/505: no. Single finite geometric-series calculation.
43. math-train/6312: no. One missing-side Pythagorean calculation followed by perimeter.
44. math-train/2506: no. One equal-gender complementary binomial probability.
45. math-train/3805: no. Single Pascal row-sum identity and logarithm.
46. math-train/1983: no. One conditional planar area ratio; the conditioning area is trivial.
47. math-train/3676: no. Conjugate root and root sum immediately determine the integer root.
48. math-train/334: no. Intersection quadratic precedes short coordinate substitutions; those substitutions are not substantive.
49. math-train/2799: no. One coupled side-assignment and removed-corner geometry search.
50. math-train/4085: no. Root-sum restriction precedes tiny symmetric-product arithmetic.
51. math-train/6967: no. Single triple-angle identity coefficient comparison.
52. math-train/2476: no. Ending-digit cases are short binomial terms, not two substantive branches.
53. math-train/3412: no. One global functional-equation classification; arbitrary trial functions are alternative checks.
54. math-train/3633: yes. The two outer roots induce separate inner quadratic root-count branches.
   Path 1: After shared parameterization of the two outer roots, classify how many distinct real x values map to the lower outer root.
   Path 2: Independently classify real preimages of the upper outer root, including tangency and discriminant boundaries; combine the counts.
55. math-train/1593: no. Single minimum distinct-positive allocation sum.
56. math-train/1751: no. Single odds-to-probability conversion.
57. math-train/2421: no. Single binomial probability.
58. math-train/702: no. Single prime-residue restriction along the progression.
59. math-train/3535: no. Polynomial identity determines constants before denominator exclusions.
60. math-train/5294: yes. Digit frequency and reciprocal-digit arithmetic are independent ingredients.
   Path 1: Count occurrences of each nonzero digit among all integers through the stated power of ten, handling leading zeros and the upper endpoint.
   Path 2: Compute the reciprocal sum over the possible nonzero digit values and its reduced-denominator divisibility requirements; combine with frequencies later.
61. math-train/825: no. Single compounded late-charge calculation.
62. math-train/5458: no. Single prime factorization and divisor-count formula.
63. math-train/2182: no. Changed-attribute pair counts are small multiplicity products.
64. math-train/5015: no. Single modular-cycle length calculation.
65. math-train/404: no. One recurring-turn win probability or geometric series.
66. math-train/2180: no. One feasible subset-score interval/count argument.
67. math-train/6638: no. Single pentagon angle-sum equation.
68. math-train/3406: no. Containment constraint and ellipse-area optimization are coupled; the two circles are symmetric duplicates.
69. math-train/6950: no. One root-of-unity polynomial conversion and extremal-angle selection.
70. math-train/2523: no. Single sphere surface-area formula.
71. math-train/6581: no. Single mixture proportion.
72. math-train/4294: no. Ellipse focal geometry, area and rectangle perimeter form one coupled chain.
73. math-train/6349: no. Single lcm/time conversion.
74. math-train/7134: no. Conjugate-root shape analysis is substantive; constant-term product is trivial.
75. math-train/2437: no. One tied-first-six-games probability and a trivial final-game factor.
76. math-train/2631: no. One equal-chord center-distance geometry calculation.
77. math-train/3749: no. One consecutive-factor parameter and finite range count.
78. math-train/313: no. Single rational line-equation rearrangement.
79. math-train/1592: no. One two-equation penny-transfer system.
80. math-train/7085: no. The two required cross-product components give tiny linear equations.
81. math-train/1787: no. Single remaining-letter permutation count.
82. math-train/859: no. Routine elimination and substitution.
83. math-train/728: no. Single quarter-disk identification and area calculation.
84. math-train/7214: no. One combined complex multiplier calculation.
85. math-train/5777: no. Single relative unit-price division.
86. math-train/2392: no. Single partner-symmetry probability.
87. math-train/4802: no. Available-multiple counts are trivial; common-multiple probability is one short chain.
88. math-train/2221: no. Single favorable triangular-area probability.
89. math-train/5582: yes. Unrestricted compositions and upper-bound violations are separate counts.
   Path 1: Count ordered positive integer triples with the requested sum by a composition argument, initially omitting the die upper bounds.
   Path 2: Count triples violating a die upper bound using the original sum, and determine whether violations overlap; subtract and normalize.
90. math-train/4988: no. Single congruence class in an interval and progression sum.
91. math-train/7189: no. One parameterized cross-product norm minimization.
92. math-train/1971: no. Single three-way symmetry argument.
93. math-train/2507: no. Exactly two equally likely quitters conflicts with the stated independence; intended conditional sampling is unspecified.
   Flag: Literal independence of all equal-probability quitting events cannot coexist with exactly two quitters. Sampling exactly two without replacement would require dropping that independence assertion.
94. math-train/2784: no. Thales identifies an altitude, then a single area/base calculation suffices.
95. math-train/1782: no. One parity exclusion and short remaining-pair check.
96. math-train/788: no. Signed radical extraction and subsequent sum/cube simplification are sequential and short.
97. math-train/6796: no. Real-root cases are trivial; nonreal conjugate classification provides the only substantive part.
98. math-train/4544: no. One transformed-square intersection-area calculation; symmetric corner cuts repeat the same computation.
99. math-train/4113: no. Single complementary-tuple polynomial identity and pairing count.
100. math-train/4411: no. Integer coefficient restrictions are missing; rational-root divisibility constraints and a unique root are unavailable.
   Flag: The question never states that a,b,c,d,e,f,g are integers. With unrestricted coefficients, many negative noninteger rational values can be made common roots, so the requested root is undetermined.
