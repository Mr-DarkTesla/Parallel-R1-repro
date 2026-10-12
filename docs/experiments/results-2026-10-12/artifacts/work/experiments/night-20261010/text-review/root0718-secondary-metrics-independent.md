Independent predeclared secondary MATH500 audit: PASS

Frozen validation selections remain unchanged.
new-sft-math500: 92/500 correct, strict 464, joint 83; correct nofork 9, forked-invalid 0. F(all) 608.828.
secondary-mathaccuracy40-math500: 102/500 correct, strict 488, joint 89; correct nofork 12, forked-invalid 1. F(all) 523.254.
Paired fresh92: {"gain": 49, "loss": 39, "both_correct": 53, "exact_unadjusted_mcnemar_p": 0.3373990368531191, "F_delta_all": -85.574, "F_delta_both_correct": -50.283018867924525, "F_both_correct_current": {"n": 53, "sum": 19148.0, "mean": 361.2830188679245, "median": 353.0, "p95": 560.8, "min": 94.0, "max": 840.0}, "F_both_correct_fresh": {"n": 53, "sum": 21813.0, "mean": 411.5660377358491, "median": 373.0, "p95": 577.8, "min": 131.0, "max": 2226.0}}
old-mixed-sft-commonbudget-math500: 101/500 correct, strict 223, joint 28; correct nofork 48, forked-invalid 25. F(all) 557.506.
Paired fresh92: {"gain": 59, "loss": 50, "both_correct": 42, "exact_unadjusted_mcnemar_p": 0.4436695012023485, "F_delta_all": -51.322, "F_delta_both_correct": -102.19047619047619, "F_both_correct_current": {"n": 42, "sum": 10859.0, "mean": 258.54761904761904, "median": 252.5, "p95": 457.49999999999994, "min": 57.0, "max": 557.0}, "F_both_correct_fresh": {"n": 42, "sum": 15151.0, "mean": 360.73809523809524, "median": 361.0, "p95": 529.5999999999999, "min": 131.0, "max": 623.0}}

F is idealized sampled critical depth, not measured GPU calls or speedup; backend branches execute serially.
Joint denotes compiled protocol compliance with correctness, not useful/faithful semantic parallelism.
McNemar is exact unadjusted descriptive on fixed500; adaptive training/validation selection and one training seed preclude robustness claims.
No MATH500-based selection or adaptation; secondaries predeclared before test.
Alias byte hashes rechecked; checkpoint 8model/8optimizer shard existence and prior committed-step proof reused, no optimizer-deserialization.

Full independent CPU verification covers1000secondary responses plus500fresh baseline: all question/gold/index/seed/prompt IDs, canonical answer extraction+MathVerify, strict/joint, actual per-call F/T and sampling parameters agree; all76 frozen hashes/checkpoint checks pass. Model file hashes recorded.

Oldmixed101 includes47 primary-correct unfinishedTHINK(no closing tag) plus1 correct duplicate-closingTHINK(index367,test/algebra/1199.json);48 lack exactly one close. Historical think-gated54 and correct-and-basic-valid51 are distinct; unfinishedTHINK total265. Math40 has1correct unfinishedTHINK (historical101). These primary counts measure answer-equivalence, not complete valid solutions. No test-driven selection or adaptation.
