Separate actual4B inference gate, prepared but not launched.

The durable existing-lane owner invokes `width8_inference_proof.py` with
`--config <this directory>/config.json --device cuda:0 --output <this directory>/actual`.
The output directory must not exist. Exit0 and `actual/result.json` passed=true
are both required; exceptions write passed=false and return nonzero.

The proof loads baseline/R1step32/R2step32 sequentially in FP32, disables TF32
and autograd, and uses the frozen native Instruct prefix and execute think guard.
Widths2/4/8 use proof-only forced wide paths with unequal lengths. Instrumented
model.forward input shapes prove every candidate max_paths8 fork is one full
width batch, not microgroups. Real first two MATH500 questions run unchanged
4096/768/16384 budgets and seeds42161011+index*1000. Sampled raw IDs, masks,
origins, prefixes and seeds must match current max_paths2 control exactly;
old-logp/replay/perturbation differences must meet max.01/mean.002/p95.005.
Results include actual forward counts, complete paired traces, per-case wall
time, allocated/reserved memory and capacity. Changing masked padding values
and another row's content must preserve likelihood within the stated limits.

This protocol intentionally changes intra-problem physical forward cost to
fullwidth batching. The historical max_paths2 run is only the paired control.
There is no cross-problem batching or reward counterfactual in this proof.
Successful inference does not establish resident optimizer memory, backward,
distributed synchronization or resume parity. Those require the separately
owned actual8GPU corrected training two-step/resume gate before any frozen
R1/R2 training is replaced. No worker or allocation is created by this script.

Result schema: `passed`, `state`, `source_sha256`, `input_sha256`, `models[]`.
Each model contains `wide_fixtures[]` with width/logp/replay/padding/sibling
drift, `measured_forward_calls`, prefix lengths and `timings` keyed2/8. Each
timing has seconds, actual model-forward count, observed model input shapes,
peak allocated/reserved/free/total bytes. `sampled_traces[]` contains question
ID/index/seed, exact action/mask/prefix proof, replay drift, widths, tokens,
actual F and paired timing. The checkpoint paths remain explicit in config.
