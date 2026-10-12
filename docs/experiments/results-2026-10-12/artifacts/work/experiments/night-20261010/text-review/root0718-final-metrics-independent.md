Independent final MATH500 audit: PASS

Frozen validation selections remain unchanged.
new-sft-math500: 92/500 correct, strict 464, joint 83; correct nofork 9, forked-invalid 0. F(all) 608.828.
final-sirius-math500: 115/500 correct, strict 477, joint 108; correct nofork 5, forked-invalid 2. F(all) 535.596.
Paired fresh92: {"gain": 53, "loss": 30, "both_correct": 62, "exact_unadjusted_mcnemar_p": 0.015232201861994659, "F_delta_all": -73.232, "F_delta_both_correct": -3.1129032258064515, "F_both_correct_current": {"n": 62, "sum": 24175.0, "mean": 389.9193548387097, "median": 378.0, "p95": 559.4, "min": 76.0, "max": 798.0}, "F_both_correct_fresh": {"n": 62, "sum": 24368.0, "mean": 393.03225806451616, "median": 361.0, "p95": 617.3999999999996, "min": 131.0, "max": 2226.0}}
final-tmp2-math500: 102/500 correct, strict 487, joint 102; correct nofork 0, forked-invalid 0. F(all) 539.604.
Paired fresh92: {"gain": 50, "loss": 40, "both_correct": 52, "exact_unadjusted_mcnemar_p": 0.34283311942078826, "F_delta_all": -69.224, "F_delta_both_correct": -54.28846153846154, "F_both_correct_current": {"n": 52, "sum": 18245.0, "mean": 350.86538461538464, "median": 332.0, "p95": 489.14999999999986, "min": 207.0, "max": 674.0}, "F_both_correct_fresh": {"n": 52, "sum": 21068.0, "mean": 405.15384615384613, "median": 362.0, "p95": 582.2999999999997, "min": 131.0, "max": 2226.0}}
final-tmp3-math500: 130/500 correct, strict 483, joint 71; correct nofork 55, forked-invalid 4. F(all) 486.750.
Paired fresh92: {"gain": 70, "loss": 32, "both_correct": 60, "exact_unadjusted_mcnemar_p": 0.0002133912534118648, "F_delta_all": -122.078, "F_delta_both_correct": -67.48333333333333, "F_both_correct_current": {"n": 60, "sum": 17647.0, "mean": 294.1166666666667, "median": 250.5, "p95": 551.6999999999999, "min": 67.0, "max": 1123.0}, "F_both_correct_fresh": {"n": 60, "sum": 21696.0, "mean": 361.6, "median": 349.0, "p95": 522.4, "min": 131.0, "max": 731.0}}
secondary-mathaccuracy40-math500: pending 358
old-mixed-sft-commonbudget-math500: pending 346

F is idealized sampled critical depth, not measured GPU calls or speedup; backend branches execute serially.
Joint denotes compiled protocol compliance with correctness, not useful/faithful semantic parallelism.
McNemar is exact unadjusted descriptive on fixed500; adaptive training/validation selection and one training seed preclude robustness claims.
No MATH500-based selection or adaptation; secondaries predeclared before test.
Alias byte hashes rechecked; checkpoint 8model/8optimizer shard existence and prior committed-step proof reused, no optimizer-deserialization.
