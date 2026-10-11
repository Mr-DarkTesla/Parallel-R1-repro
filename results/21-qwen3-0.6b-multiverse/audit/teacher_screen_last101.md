# Sol6.1 trajectory pre-screen: records 103–203

Source examined only through `id`, `question`, `reasoning`, and `external_answer`. The candidate gold-answer field was not used.

Strict rule: accept only when the reasoning contains at least two necessary, substantive computations that can proceed independently after shared setup, followed by an aggregation. A rephrasing, verification, or a sequential dependency is rejected.

**Result: 100/101 accept, 1/101 reject.**

| # | ID | Verdict | Paragraph grouping | Reason |
|---:|---|---|---|---|
| 103 | `math-train/1957` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: disjoint favourable pair types; later paragraph combines them. |
| 104 | `math-train/2001` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: red and nonred selection factors; later paragraph combines them. |
| 105 | `math-train/2021` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: rank-role and suit-choice factors; later paragraph combines them. |
| 106 | `math-train/2048` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: exactly-two and exactly-three stay cases; later paragraph combines them. |
| 107 | `math-train/2049` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: rerolls containing the pair face and other-face triples; later paragraph combines them. |
| 108 | `math-train/2060` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: independent selections from the word sources; later paragraph combines them. |
| 109 | `math-train/2184` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: the two possible values below 3; later paragraph combines them. |
| 110 | `math-train/219` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: high-degree and low-degree polynomial terms; later paragraph combines them. |
| 111 | `math-train/2234` | reject | P1 = complete count; P2 = verification; P3 = result | P1 already completes the inclusion-exclusion count; P2 is only a redundant verification by longest run, not a second necessary branch. |
| 112 | `math-train/2246` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: block position and character assignments; later paragraph combines them. |
| 113 | `math-train/2273` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: Brian and Noah roll conditions; later paragraph combines them. |
| 114 | `math-train/2293` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: side-side and diagonal-diagonal pairs; later paragraph combines them. |
| 115 | `math-train/2294` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: internal book orders and order of groups; later paragraph combines them. |
| 116 | `math-train/2333` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: same-color cases by color; later paragraph combines them. |
| 117 | `math-train/2336` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: conditional counts for team-size cases; later paragraph combines them. |
| 118 | `math-train/2349` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: independent conditions from boxes A and B; later paragraph combines them. |
| 119 | `math-train/2359` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: divisibility cases by smaller number; later paragraph combines them. |
| 120 | `math-train/2364` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: position-match and swap-forbidden sets; later paragraph combines them. |
| 121 | `math-train/2371` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: residues of powers of 8 and 12; later paragraph combines them. |
| 122 | `math-train/2373` | accept | P1 \| P2 \| P3 -> P4 (combine) | Two or more necessary independent computations: one-, two-, and three-nonempty-bag cases; later paragraph combines them. |
| 123 | `math-train/2374` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: square sums 4 and 9; later paragraph combines them. |
| 124 | `math-train/2381` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: same-color left-right pairs by color; later paragraph combines them. |
| 125 | `math-train/2386` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: largest-square cases; later paragraph combines them. |
| 126 | `math-train/2389` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: two disjoint return-to-Alice paths; later paragraph combines them. |
| 127 | `math-train/2406` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: even and odd endpoint-digit cases; later paragraph combines them. |
| 128 | `math-train/2409` | accept | P1 \| P2 \| P3 -> P4 (combine) | Two or more necessary independent computations: vowel choice and consonant multiset choice; later paragraph combines them. |
| 129 | `math-train/2411` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: train-arrival ranges before and after minute 50; later paragraph combines them. |
| 130 | `math-train/2416` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: all color sequences and valid block orders; later paragraph combines them. |
| 131 | `math-train/2418` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: opposite rolls equal and different; later paragraph combines them. |
| 132 | `math-train/2419` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: unrestricted count and two forbidden families; later paragraph combines them. |
| 133 | `math-train/2427` | accept | P1 \| P2 \| P3 -> P4 (combine) | Two or more necessary independent computations: valid draws by first-number cases; later paragraph combines them. |
| 134 | `math-train/2432` | accept | P1 \| P2 \| P3 -> P4 (combine) | Two or more necessary independent computations: Earth-like count cases; later paragraph combines them. |
| 135 | `math-train/2439` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: counts A and B; later paragraph combines them. |
| 136 | `math-train/2445` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: two-kings and at-least-one-ace events; later paragraph combines them. |
| 137 | `math-train/2450` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: zero-triplet and one-triplet lineups; later paragraph combines them. |
| 138 | `math-train/2453` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: nonprime cases 1 and prime; later paragraph combines them. |
| 139 | `math-train/2454` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: all diagonal pairs and interior-crossing pairs; later paragraph combines them. |
| 140 | `math-train/2457` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: green-position ranges; later paragraph combines them. |
| 141 | `math-train/2459` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: neither and both officer cases; later paragraph combines them. |
| 142 | `math-train/2468` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: zero-speaker and one-speaker complement cases; later paragraph combines them. |
| 143 | `math-train/2486` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: host selection and guest-team selections; later paragraph combines them. |
| 144 | `math-train/2488` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: Tamika sums and Carlos products; later paragraph combines them. |
| 145 | `math-train/253` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: the two distributed polynomial products; later paragraph combines them. |
| 146 | `math-train/256` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: independent powers of x and y; later paragraph combines them. |
| 147 | `math-train/2563` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: sphere and cylinder volumes; later paragraph combines them. |
| 148 | `math-train/2589` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: clay-block and sculpture volumes; later paragraph combines them. |
| 149 | `math-train/2595` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: centroid x- and y-coordinates; later paragraph combines them. |
| 150 | `math-train/2597` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: sector and triangle areas of the lens; later paragraph combines them. |
| 151 | `math-train/2601` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: cone and hemisphere volumes; later paragraph combines them. |
| 152 | `math-train/2604` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: square area and removed corner areas; later paragraph combines them. |
| 153 | `math-train/2679` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: areas of inscribed and circumscribed hexagons; later paragraph combines them. |
| 154 | `math-train/2723` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: two triangle areas partitioning the quadrilateral; later paragraph combines them. |
| 155 | `math-train/2742` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: cut length and remaining boundary pieces; later paragraph combines them. |
| 156 | `math-train/2743` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: parallel-side lengths and their separation; later paragraph combines them. |
| 157 | `math-train/2804` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: triangle and hexagon area formulae; later paragraph combines them. |
| 158 | `math-train/2807` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: independent translations of B and G; later paragraph combines them. |
| 159 | `math-train/2829` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: two disjoint groups of edge lengths; later paragraph combines them. |
| 160 | `math-train/2835` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: base-area and height scale factors; later paragraph combines them. |
| 161 | `math-train/2840` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: the two altered cylinder volumes; later paragraph combines them. |
| 162 | `math-train/2851` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: box volume and packed-cube volume; later paragraph combines them. |
| 163 | `math-train/2878` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: original sphere and drilled-hole volumes; later paragraph combines them. |
| 164 | `math-train/2884` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: cylinder and cone volumes; later paragraph combines them. |
| 165 | `math-train/2899` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: largest-side cases; later paragraph combines them. |
| 166 | `math-train/2905` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: independent lines through A,C and B,C; later paragraph combines them. |
| 167 | `math-train/3045` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: front and back wheel travel per revolution; later paragraph combines them. |
| 168 | `math-train/3054` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: power-of-a-point relations at P and Q; later paragraph combines them. |
| 169 | `math-train/3309` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: base angles of the two isosceles triangles; later paragraph combines them. |
| 170 | `math-train/3332` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: direct sector and wrapped sectors; later paragraph combines them. |
| 171 | `math-train/3456` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: lower and upper inequality solution sets; later paragraph combines them. |
| 172 | `math-train/3509` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: endpoint functions q=0 and q=1; later paragraph combines them. |
| 173 | `math-train/3511` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: integer pairs grouped by a; later paragraph combines them. |
| 174 | `math-train/3518` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: root difference and sum-of-squares formulae; later paragraph combines them. |
| 175 | `math-train/3527` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: numerator and denominator products; later paragraph combines them. |
| 176 | `math-train/3537` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: logarithmic products b and c; later paragraph combines them. |
| 177 | `math-train/3600` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: x-coordinate and y-coordinate eliminations; later paragraph combines them. |
| 178 | `math-train/3643` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: linear-in-n and constant series contributions; later paragraph combines them. |
| 179 | `math-train/3672` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: logarithm and square-root domain constraints; later paragraph combines them. |
| 180 | `math-train/377` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: high-degree and low-degree polynomial terms; later paragraph combines them. |
| 181 | `math-train/405` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: transformed x- and y-coordinates from f(9); later paragraph combines them. |
| 182 | `math-train/422` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: quarterly and annual balances; later paragraph combines them. |
| 183 | `math-train/458` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: outside and inside absolute-value branches; later paragraph combines them. |
| 184 | `math-train/5660` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: the two parenthesized products; later paragraph combines them. |
| 185 | `math-train/5936` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: numerator and denominator of the complex fraction; later paragraph combines them. |
| 186 | `math-train/6012` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: a- and b-coefficients; later paragraph combines them. |
| 187 | `math-train/6133` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: different-value and same-value coin pairs; later paragraph combines them. |
| 188 | `math-train/6553` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: two possible hypotenuse assignments; later paragraph combines them. |
| 189 | `math-train/6783` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: independent cofactor contributions; later paragraph combines them. |
| 190 | `math-train/6817` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: chord multiplicities and trigonometric chord values; later paragraph combines them. |
| 191 | `math-train/6818` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: two disjoint sets of symmetric cis pairs; later paragraph combines them. |
| 192 | `math-train/6840` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: constant and roots-of-unity cosine contributions; later paragraph combines them. |
| 193 | `math-train/6864` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: constant sine-square contribution and roots-of-unity cosine correction; later paragraph combines them. |
| 194 | `math-train/7264` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: two complementary cosine-factor pairs; later paragraph combines them. |
| 195 | `math-train/765` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: high-degree and low-degree polynomial terms; later paragraph combines them. |
| 196 | `math-train/799` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: outer and middle absolute-value regions; later paragraph combines them. |
| 197 | `math-train/828` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: compound and simple-interest balances; later paragraph combines them. |
| 198 | `math-train/858` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: the two distributed polynomial products; later paragraph combines them. |
| 199 | `math-train/92` | accept | P1 \| P2 \| P3 (third region, then combine) | Two or more necessary independent computations: the three absolute-value regions; later paragraph combines them. |
| 200 | `math-train/954` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: left and right rational-expression factorizations; later paragraph combines them. |
| 201 | `math-train/979` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: compound and simple-interest balances; later paragraph combines them. |
| 202 | `math-train/98` | accept | P1 \| P2 \| P3 (constant term, then assemble) | Two or more necessary independent computations: quadratic, linear, and constant contributions; later paragraph combines them. |
| 203 | `math-train/984` | accept | P1 \| P2 -> P3 (combine) | Two or more necessary independent computations: high-degree and low-degree polynomial terms; later paragraph combines them. |
