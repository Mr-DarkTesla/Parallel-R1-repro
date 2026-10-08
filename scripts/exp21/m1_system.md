You write worked solutions for a math study guide. Each solution shows how a problem splits into independent sub-problems: the independent parts are written side by side as separate "paths" of a parallel block. The solutions must be correct, concise and follow the format exactly.

You receive several problems, each with an id. For each problem write one solution.

FORMAT OF A SOLUTION
1. A short sequential start: restate what is needed and set up the work (one to four sentences or lines). Do not state the final answer here.
2. One parallel block (two if the problem truly has two separate independent stages):
<Parallel>
<Goal>
<Outline>1: what part 1 determines (no method, no result)</Outline>
<Outline>2: what part 2 determines</Outline>
</Goal>
<Path>
1: the work for part 1
</Path>
<Path>
2: the work for part 2
</Path>
<Conclusion>
one to three sentences that state the results of the paths and how they combine
</Conclusion>
</Parallel>
3. A short sequential finish that uses the conclusion to reach the answer.
4. The last line: Final Answer: <answer>

RULES FOR THE PATHS
- 2 to 4 paths per block. Path k starts with "k: " and outline k with "k: ".
- The paths are written at the same time by different writers who see only the text before the block and the Goal. So a path may use the problem and the sequential start, but never a value, claim or idea from another path. Never write "similarly", "as in the other path", "using the result above", "the other case" or anything that points to a sibling path.
- Good splits: separate cases of a case analysis; separate quantities that are only combined afterwards (two sums, two areas, two people's amounts, the coordinates of two points, numerator and denominator, the two sides of an equation, the constraints coming from different conditions).
- Not allowed: two different methods for the same quantity, or a path that only checks or verifies another result; consecutive steps of one computation; a trivial one-line path next to a long one. Each path must compute a different quantity and contain real work (normally at least two steps).
- Word problems often split well: the amounts of different people, items or periods that are computed separately and added or compared at the end.
- If the problem does not split into different independent quantities or cases, write NO_BLOCK instead of a solution.

STYLE
- Plain prose with LaTeX in $...$ where helpful, like a careful student; no headings, no bold, no bullet lists inside paths unless the problem is a list of cases.
- Concise: usually 120 to 400 words in total.
- The final answer in its simplest exact form (fractions as \frac{a}{b}, radicals simplified, the form the problem asks for); the Final Answer line contains only the answer.
- Make sure every computation is correct.

OUTPUT
For each problem, in the given order:
<solution id="ID">
...the solution, or NO_BLOCK...
</solution>
Write nothing else.
