# Blind independent-computation audit

33 questions screened. Accepted: 21. Rejected: 12. No gold labels, model answers, or other agent folders read. Source question strings preserved directly from input objects.

Accepted traces contain common setup, two independent computation sections, and a combination after both sections inside think. Final Answer occurs once outside think. No Multiverse tags added.

Strong examples: math-train/1544 independently eliminates separate prices; math-train/4436 independently derives an upper bound and an attaining feasible point; math-train/7203 independently computes vector determinant and norm product; math-train/1983 independently computes conditioning and joint-event areas.

Elementary valid examples: math-train/694 computes two original summands; math-train/253 expands two original products; gsm8k-train/4150 computes food and clothes expenditures independently. Their branches are short but correspond to distinct original problem components.

Rejected examples: math-train/4241 requires a confidently proved shortest polygon ordering; math-train/4411 does not explicitly make coefficients integers; math-train/3086 and math-train/4042 naturally form sequential solutions. math-train/2883 has only trivial coordinate differences.

Assumptions: ordinary fair independent flips in math-train/1975; independent games in math-train/2513; independent uniform arrival times in math-train/1983. These are standard interpretations of stated random experiments. No independence between weather days is assumed.

Verification: build.py records generation; validation.txt records structural checks and exact rational arithmetic checks.
