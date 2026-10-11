# On-policy 46: MATH decomposition screen

## Scope and source discipline

Screened all **128 MATH** records in `data/onpolicy46_questions_only.jsonl` only. I did not read the candidate, generated-answer, or gold-containing files. The selection contains **35** high-confidence proposals and **93** rejections.

## Acceptance rule

A selected question must support exactly this execution pattern using only its literal prompt:

1. Path 1 computes a necessary, nontrivial quantity, branch, or partial result.
2. Path 2 computes a different necessary, nontrivial quantity or disjoint branch without using Path 1's result.
3. The conclusion joins the two with an explicit operation such as addition, multiplication, intersection, union, comparison, GCD, or ratio.

I rejected a question when its natural solution was a single calculation, when the second step required the first result, when prospective paths would merely duplicate a computation, or when a valid split would require placing a solved quantity in the plan.

## Selection

`data/onpolicy46_decomp_math_proposals.jsonl` has one record per selected ID, with `subgoal1`, `subgoal2`, `combine`, and a brief reason. The proposals deliberately contain no final answer or precomputed numerical result.

| Answer type | Selected |
|---|---:|
| integer | 18 |
| expression | 13 |
| fraction | 4 |
| **total** | **35** |

Selected structures include factor and partial-product splits, disjoint counting or probability cases, independent prime factorizations, endpoint comparisons, coordinate components, geometric volumes, and two-equation symmetric identities. This provides variety without forcing a parallel split into inherently sequential problems.

## Rejection counts

| Reason | Count |
|---|---:|
| One dominant computation, so no second substantive quantity | 47 |
| Natural second step depends on the first result | 31 |
| Coupled proof or global case analysis cannot be split without pre-solving | 15 |
| **total rejected** | **93** |

The screen is deliberately conservative: 35 proposals are below the allowed maximum of 40 because the remaining candidates did not meet the path-independence standard cleanly.
