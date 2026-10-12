# Independent vLLM actor → HF learner contract

PASS on the actual Qwen3-4B-Instruct checkpoint0050, installed patched vLLM 0.8.5.post1, and HF FULL BF16 teacher with FP32 master and gradients. One BF16 pilot, one independent FP32 geometry pilot, and eight parallel GPU cases completed with exit0. Worker2 was released: controller and all GPU children are absent by exact PID/start-tick identity; no queued children remain.

## Qualified boundary

This is a bounded independent probability/mask/gradient proof, not a throughput benchmark or a production optimizer run. No Adam step, IPC refresh, or parameter mutation occurs in this proof. Production trainer qualification belongs to B's separate actual Adam51/52 and weight-refresh receipts. No further GPU jobs are authorized for this namespace after release.

The original actor behavior probabilities `q` remain immutable. The HF FULL BF16 pre-update teacher supplies detached `p0`; the current learner uses the same BF16 arithmetic, giving pre-update `exp(current-p0)=1` exactly. TIS uses detached `clamp(exp(p0-q), 0, 2)` without batch normalization. Loss uses the fixed4096 denominator. The independent n1 proof has response scale1/32; production32 DDP scale is world/32 before DDP averaging.

Raw sampled actions, including EOS, retain loss mask1 and their original q. Injected headers, bridges and canonical terminal replacement tokens have loss0. Replay rebuilds canonical structured masks and semantic positions separately from physical KV slots. Fixtures cover widths2/3/4/6/8, different problems, path EOS, Summary EOS, forced caps and merged repeated positions. All full-vocabulary actor replay comparisons are exact0 over151936 logits; native Think guards are preserved. The stricter CPU trace audit passes all10 actual completed traces and rejects four deliberately corrupted contracts.

## Numerical evidence

The independent FP32 geometry pilot compares native vLLM and HF with the same structured state: maximum action logprob difference3.14713e-5, mean1.05338e-5. HF FP32 cached/full maximum is3.81470e-5. BF16 q→p0 drift is correction telemetry, not the FP32 geometry acceptance test. BF16 natural outputs are allowed to differ.

Eight probability cases have finite FP32 gradients and FP32 masters, BF16 teacher/current logits, exact pre-update PPO ratio1, and TIS cap fraction0. Scripted cases have maximum absolute q→p0 logratio0.193359 and ESS fractions0.994923–0.997936. The eighth case additionally replays one actual natural B fixed32 rollout:411 raw actions,9 forced loss0 tokens, maximum absolute logratio0.205526, mean0.0111084, ESS410.692/411=0.999251, rho range0.889848–1.228171. Its natural trace has width2; the independent actor fixture on that GPU has width8. The natural trace contains no EOS replacement, which is instead exercised by the scripted path and Summary cases.

## Provenance and artifacts

- CP50 model SHA256: `727550dbcb49937625a451e02c8c0c700d80c95685b63d0fcff983e09c00f42c`.
- Train1024 SHA256: `6bcab08da6bc6b22ddacc58ac5aeb5a18abcc509c4f68d7457cd79d8acb4e317`.
- Canonical structured source SHA256: `f9b26772090c5d8af0bff54f26369da5e26f850e79d9261b6f0da5531000881f`.
- Natural trace SHA256: `5c7c4a2983c8336e3e24f912431f7e32519f9195c31e8a55a264cf410b6e4e37`, original actor version`cp50/bfloat16/vllm-dag-v1`, seed4073904032271957942, original episodeF369.
- `RESULT.json`: actual pilots and eight probability cases, aggregate exit0/GPU-empty result.
- `INPUT-AND-SOURCE-SEAL.json`, `UPSTREAM-SEAL.json`: checkpoint, inputs and copied isolated source hashes.
- `CPU-TIS-PROOF.json`, `CPU-MASK-PROOF.json`: CPU math and trace proofs before admission.
- `STRICT-TRACE-CPU-AUDIT.json`: exact raw-action/forced-mask coverage and corruption rejection.
- `WORKER2-RELEASE.json`: controller completion and exact own-process identity audit.
- `src/gpu_contract.py`, `src/probability_contract.py`, `src/trace_contract_v2.py`: runnable isolated adapters and proof.

Every production episode retains its semantic branch-participation F independently of global physical backend calls. Cross-prompt batching must not divide or subsidize reward F. Pure materialization forwards count in physical F and relevant episode F. Full production caps remain4096 response /768 path /16384 context /8 paths; batch32 means32 global responses.
