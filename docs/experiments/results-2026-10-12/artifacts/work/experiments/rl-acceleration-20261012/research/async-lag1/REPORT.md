# Async lag1 CPU engineering prototype

Implemented an isolated versioned coordinator and explicit three-policy estimator. This is a CPU prototype with no GPU dispatch, serving adapter, production loss change, checkpoint export, or RNG-state export. The exact laneA kernel independently passed CPU autograd and actual eight-rank Gloo before laneA's GPU work was released.

| Proof | Verified result |
|---|---|
| Queue / snapshots / provenance | 17 tests pass on Mac and server CPU |
| Exact laneA three-policy kernel | SHA256 `c1f7541f509bb1cda6873d1b4c14eb31da0bbf12ef06f154ba04fdf4ffd08114` |
| Independent kernel reference | 18 sign / PPO clipping / TIS cap cases; detached q and p0; forced mask 0 / sampled terminal mask 1; q=p0 legacy equality |
| Actual CPU collective | Eight Gloo ranks, fixed 8 prompts × 4 responses, denominator 4096; max gradient error 2.964615315390051e-21, Adam error 0 |
| Collective rejection | One bad sameactor rank makes every rank skip; parameters and Adam step state stay unchanged |

`three-policy-proof.json` is the approved kernel proof and remains byte unchanged. Its exact helper sources are preserved in `proof-sources/`; they match every source hash in that proof. Current coordinator code is separately bound by `queue-proof.json`, `SOURCE_PROVENANCE.json`, and `SOURCE_MANIFEST.json`.

## Queue and weight versions

The one-slot capacity includes a producer reservation while generation is in progress. There can be one learner batch and one future batch, where the future batch is either being generated or queued. It cannot be both queued and accompanied by a third in-flight producer batch.

`begin_production()` acquires eight named group leases on one privately copied immutable actor snapshot. Every group has exactly four responses, every episode keeps the same actor version/hash/compute mode through every main/width/path/summary call, and this prototype deliberately requires one actor snapshot for the complete 32-response batch. The snapshot name identifies a logical weight version shared by replicas, not a GPU/worker identity.

Before admission, the coordinator forecasts consumption at `learner_version + int(update_in_flight)` and requires forecast minus actor version in 0..1. On consumption it checks the actual gap again. The forecast matters: after learner 51 reserves an old actor 50 batch, another actor 50 batch would be consumed at learner 52 and is blocked until actor 51 is published. Merely checking qsize≤1 after generation would let that stale third batch slip through.

Sequence, prompt group identities and episode identities are ordered and consumed once per coordinator session. Reused groups, duplicate producer submissions, duplicate learner acknowledgements, out-of-order sequence and mixed group actor versions fail before an optimizer update. `rollout_iteration` and data exposure cursor advance with new generation attempts, independently of successful optimizer updates and of fork-round count. Given initial version 50, default first rollout iteration 51 and exposure offset 1200 preserve the canonical seed/data schedule; actor version is never substituted for rollout seed iteration.

Actor publication verifies the source committed learner-policy hash and forbids rebinding a version to another payload/name/precision, including after retirement. A snapshot cannot retire while any group lease is active. The toy payload is immutable private bytes; a real backend must provide a private resident copy or wait for a drained engine before changing weights. After completed generation plus sameactor parity, the generation leases release; the queued trace retains q, version and hashes, so the old actor model can retire without refreshing queued q.

Stop closes new admissions. Drain lets the current producer finish, then consumes the pending batch and finishes the current atomic learner update. Abort drops queued work but requires explicit acknowledgements from all eight groups, each confirming all four episodes have stopped, before releasing a producer's weights. A later drain request cannot weaken an earlier abort. The coordinator sends no process signals and cannot infer CUDA request liveness.

## Three separate likelihood roles

For the experimental mode only:

- q is the immutable raw sampled behavior likelihood, such as approved BF16 actor compute at version v.
- p0 is the independently frozen FP32 proximal likelihood at learner version v orv+1, captured for all 32 responses before that batch's optimizer update.
- pθ is the differentiable current learner likelihood at the base revision of that update.

The token loss is `-stop_grad(clamp(exp(p0-q),0,2)) * min(exp(pθ-p0)*A, clip(exp(pθ-p0),.8,1.2)*A)`. Advantages remain `reward - mean(group4)`, with no std division or IS batch normalization. Each rank sums sampled-token losses with scale `learner_world/32/4096`; DDP averaging recovers the global response mean. The R2 reward source is imported directly and verified against immutable SHA256 `b3e755aa880f0cc0bea0234e5b9fbc6f9378c0ef3b0c12b3ee168fe87df68fce`.

The cap 2 and lower 0 are taken from pinned [slime arguments](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/slime/utils/arguments.py#L1175-L1188), its [importance-weight implementation](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/slime/utils/ppo_utils.py#L25-L35), and the [TIS loss wrapper](https://github.com/THUDM/slime/blob/05e3b017fed9e02de418c2fbac9d75602a534be5/slime/backends/megatron_utils/loss.py#L901-L924). Pinned [verl correction config](https://github.com/verl-project/verl/blob/2035f58dcb06d8cad4caee107b30f4045d724367/verl/trainer/config/algorithm/rollout_correction.yaml) defaults correction off; token TIS upper 2 requires explicit enablement. This experiment requires the named mode `experimental_decoupled_token_tis` and does not reinterpret the existing production objective.

For exactly one fresh optimizer update, p0 can be `current_logp.detach().clone()` while current still refers to the pre-update learner policy. The independent serial-reference test verifies that gradient. Async still captures p0 for its own learner update rather than replacing q with newly recomputed likelihoods. `FrozenProximalBatch` binds32 immutable likelihood records to batch sequence, update ID and learner weight hash.

The numerical guard sees only q from generation versus replay with the identical actor version/hash/compute mode. The unchanged limits are maximum .01, mean .002, p95 .005. A failure is a technical unknown with no optimizer update. Intentional behavior-to-proximal drift is telemetry and supplies TIS weights; it never enters that numerical guard. Optional importance rejection is a separate collective decision input and is disabled in this implementation; no new rejection threshold is invented.

Raw sampled IDs and old q are retained in exact per-call contexts, including sampled stop/terminal tokens. The call coverage must equal response_mask: terminal actions have 1, injected headers/bridges have 0. Canonical per-episode generation F continues to enter the unchanged reward; packing other episodes must not discount that F using a cohort's shared backend counter.

## Artifacts and reproduction

- `scheduler.py`: immutable snapshots, generation leases, reservation/backpressure, ordered learner tickets and stop/drain.
- `proximal.py`: complete 32 frozen p0 capture and update binding.
- `three_policy.py`: explicit estimator, independent scalar derivative, masked Torch kernel and three-policy provenance.
- `batch.schema.json` and `example-batch.json`: complete 32 synthetic lag1 fixture with q / p0 / pθ, actor replay values, versions/hashes, raw contexts and terminal masks. No model weights or RNG states are serialized.
- `prove_three_policy.py`, `three-policy-proof.json`, `proof-sources/`: frozen CPU kernel proof used by laneA.
- `prove_queue.py`, `test_scheduler.py`, `queue-proof.json`: current queue and provenance proof.

Run from this directory with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_scheduler`. `prove_queue.py` also verifies the finite fixture, schema constants and frozen-source hashes. An external JSON Schema validator is not installed; semantic invariants are tested through the constructors and coordinator, not claimed as external-validator coverage.

Existing contracts referenced directly: [PPO loss](${PROJECT_ROOT}/experiments/parallel_instruct/train.py), [fixed-batch assignments / seed](${PROJECT_ROOT}/experiments/parallel_instruct/batching.py), [R2 reward](${PROJECT_ROOT}/experiments/parallel_instruct/reward.py), [collective guard](${PROJECT_ROOT}/experiments/parallel_instruct/replay_guard.py), [raw action / forced-mask accounting](${PROJECT_ROOT}/experiments/parallel_instruct/rollout.py), and [exact replay contexts](${PROJECT_ROOT}/experiments/parallel_instruct/structured_replay.py). Their source hashes and pinned upstream artifact hashes are in `SOURCE_PROVENANCE.json`.

## Resources within the current 24-GPU acceleration budget

| Split | Potential fit | Cost that must be measured |
|---|---|---|
| 16 actor / 8 learner GPUs | Actor generation remains the bottleneck after accepted BF16 optimizations | Eight learner ranks each replay four responses; actor snapshot transfer/cache flush still costs time |
| 8 actor / 16 learner GPUs | FP32 replay/backward becomes the bottleneck | Eight actor ranks each generate four responses; additional learner capacity can sit idle |
| Actor and learner on the same busy GPUs | Only an explicitly measured alternative | Extra stable actor weights and KV, model-state isolation, streams and weight-copy synchronization; no free overlap is promised |

Dedicated pools require separate communicators and role ownership, preserving the same32-response batch. Steady-state duration is bounded by the slower actor/learner stage plus non-hidden publication and synchronization costs; these CPU tests establish no speedup. FP32 model parameters alone are 16,089,872,384 bytes; gradients add the same amount and two Adam moments total 32,179,744,768 bytes before sharding, activations, DDP buffers or KV. Actual actor compute can use BF16 AMP while keeping FP32 masters; its approved precision layout and measured memory must be preserved rather than assuming pure BF16 storage.

An actor engine may apply a new learner version only after every whole-episode/group lease drains, followed by version-keyed or flushed prefix/KV caches and weight publication. A logging-only weight_version field is insufficient to pin ongoing calls. Old actor weights need not stay resident after sameactor QA and queue submission, because q is retained; metadata/version history remains available. No new full checkpoints are needed: transient named weight publication is separate from the existing weights-only export schedule, which this prototype leaves untouched.

## Scope still requiring GPU integration

Exactly-once history is in-memory/session scoped; crash recovery and a distributed service/RPC adapter are not implemented. The CPU toy payload demonstrates immutability but does not establish a 4B GPU engine's lease behavior. Whole-episode version pinning, structured masks/positions, fullwidth8, cache invalidation, transport integrity, actual memory/OOM/clean exits, quality and throughput must be proven on a root-assigned free lane before any async training launch. Token TIS capping changes the estimator and does not by itself restore prefix-state sampling distribution; quality/staleness validation remains an experimental gate.
