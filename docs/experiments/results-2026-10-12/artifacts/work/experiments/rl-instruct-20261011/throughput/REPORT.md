# 500-update throughput preparation, 2026-10-11

## Current production profile supersedes the technical-step estimate

Actual production306 (`production-runs/strong_width-stage16`) step1 measured
325.713977–325.714587 seconds across eight ranks, with8 prompts×4 responses.
The saved `production306-step1-profile.json` contains rank metrics and source
hashes. Rank token sums were [4727,6650,1525,2341,3096,1651,1982,2408]; episode
F sums [4209,5794,1285,1942,2772,1420,1672,2217]. Rank1 has4.51× the counted
forward work of rank2; equal synchronized update walltime cannot locate the
generation/backward bottleneck. Peak across ranks was55,392,695,808bytes;
max replay drift0.000102996826171875. Training-answer correctness25/32 is not
validation accuracy and is not quality evidence for a final checkpoint.

At this workload, a linear fourfold trueBS32×4 projection is1302.858seconds
per update:16 updates5.79h;32 updates11.58h;500 updates180.95h (1447.62GPUh
on8 GPUs). A continuation from total step16 to500 has484 remaining updates,
about175.16h under the same projection. The current stage16 has8 prompts per
update, so its separate same-workload projection is1.45h for16 updates.
All these estimates extrapolate one update; none is steady-state measured.

Source audit: train.py starts `seconds` immediately before rollout and samples
it after optimizer and drift/gradient checks. It includes grading/trace writes,
replay/backward and final DDP gradient synchronization, clipping, active-count
all_reduce, optimizer sharding/broadcast and allocation snapshots. It ends
BEFORE gradient clearing, GC/cache cleanup, metric all_gather/write, validation
and checkpoint saving. Thus actual time to next update/completion is greater
than this timer. Neither trace calls nor memory snapshots have timestamps;
generation, replay/backward and synchronization phase durations cannot be
reconstructed from these artifacts. `phase_timer.py` is an isolated opt-in
boundary timer for a separate candidate, including host and current CUDA-stream
events, with no per-token synchronization. It still cannot separate overlapping
NCCL communication from final backward; a GPU profiler would be needed for that.

Production source explicitly sets CUDA matmul and cuDNN `allow_tf32=False`,
float32 matmul precision `highest`, and FP32 model weights. CPU BF16 screening
on tiny Qwen gives max logp drift0.0027194, mean0.0009365, p950.0022581 versus
FP32; strict1e-5 equivalence fails. Sampled IDs match this small fixture, which
does not prove unchanged sampling on4B. No precision change is enabled. TF32
requires GPU hardware and cannot be proven on CPU. A separate real4B TF32 gate
would compare exact structured masks/positions, forced replay drift, seeded
sampled full traces, optimizer-resident memory and whole-update time; BF16
would require additional dtype/logprob-contract review. These are unmeasured
candidate experiments, not speedup claims.

## Historical technical first-step profile

Existing technical-step1 measured all eight ranks at 124.380945–124.381524
seconds. This is the runner's whole-update timer, starting immediately before
rollouts and ending after backward/optimizer work; model loading is excluded.
It is the first update, not a steady-state production measurement. The batch
was 8 prompts globally, four responses per prompt (32 responses), not the
proposed 32 prompts × four responses (128 responses).

Rank-zero sampled 1,387 tokens and charged episode forward calls
242/387/322/264. Across ranks the charged forward sum ranged 1,215–2,015 and
sampled tokens 1,387–2,354. The equal rank walltimes include synchronization;
dividing a rank's walltime by its F does not identify isolated decoder latency.
Rank-zero peak allocated GPU memory was 53,117,827,584 bytes; device capacity
85,094,825,984 bytes. Allocation after optimizer was 36,345,219,072 bytes.

A purely linear fourfold projection is 497.526 seconds/update: stage16 about
2.21h; stage32 about 4.42h; 500 updates about 69.10h, or 552.81 GPU-hours on
eight GPUs. These are planning extrapolations, not measured forecasts. More
prompts can change lengths, nonzero advantage frequency, replay work and rank
imbalance. Resume and production measurements must replace this estimate.

## Isolated candidate

`cohort_decoder.py` batches compatible decoder requests from independent
episode worker threads; the single owner thread executes all model calls.
Each episode retains its own RNG, exact structured call/mask/positions, stop
IDs, budgets and max_paths=2 subgroup boundaries. Different stops are never
coalesced. Each episode is charged sum(max generated length per original
subgroup), exactly its standalone microbatch cost. Server-global shared
physical calls are recorded separately, never passed to episode reward.
Thus batching independent problems cannot create a forward reward discount.

`proof_cohort.py` checks tiny random Qwen3 FP32 on CPU against standalone
microbatch serving: forced actions, independent seeded samples, unequal
prefixes, early stops, action counts, replay log probabilities, episode cost
and another episode's prompt perturbation. This proof does not establish real
4B parity, whole execute() trajectory parity, optimizer-state memory safety or
a production speedup. It does not change frozen technical or production files.

CPU proof passed on Sirius with `CUDA_VISIBLE_DEVICES=`. Forced trajectories
kept episode F=[9,9,9,9], while the server issued nine total forward calls;
sampled trajectories kept F=[7,9,9,6], again nine server calls. All sampled
token IDs matched standalone serving. Maximum logp differences were
4.768e-7 forced and 9.537e-7 sampled; maximum replay differences 9.537e-7 and
4.768e-7. Cross-episode prompt perturbation difference was zero in the final
run. Test tolerance is 1e-5 because scheduling can change batch shapes and
normal FP32 rounding. No GPU speedup is inferred from these forward counts.

Full execute integration subsequently passed through the separate opt-in
`execute_candidate.py` adapter against the frozen long-run standalone executor.
The `proof_execute.py` CPU fixture executes two real fork rounds (widths3/2),
unequal prompt and path lengths, raw EOS replacement in visible Path/Summary
closures, injected headers/bridges and a final segment. All response IDs,
action masks, policy call origins/prefixes/raw actions, widths, lengths and
episode statistics match standalone execution. It checks 1,370 sampled-action
origins, 16 raw-stop replacements, 886 masked sibling queries, repeated
positions and sibling perturbation in full assembled model input. Replay and
old logp max delta are both 9.537e-7; cross-episode perturbation max delta is
9.537e-7. Episode F=[223,226,229,232] and all reward components are unchanged;
server telemetry separately records232 forward calls (11prefill/221decode).
An independent model.forward wrapper counted232 actual calls, exactly matching
the server ledger; the episode reward counts sum910 and stay separate.
Rewards use explicit fixture correctness, not an independently scored answer.

The full grammar fixture uses proof-only forced target actions to guarantee
coverage. Independent seeded sampling is covered by the earlier decoder proof,
but full randomly sampled real4B execute parity is still outstanding. No frozen
runner imports this candidate automatically, and no GPU experiment was launched.

## Next authorized-lane measurement

On an explicitly free existing lane, first use matched real 4B FP32, max_rows=4,
four independent episodes with fixed seeds and frozen prompts; compare
standalone/cohort full output, each policy call, response mask, branch-isolated
replay logps and reward F. Then max_rows=8 only if measured optimizer-persistent
memory fits. Compare the same complete 32-prompt update, including replay and
optimizer, excluding loading/first-update warmup. Record phase timers only to
explain whole-update time. At least two subsequent complete updates should
replace the first-update extrapolation before committing to 500.

Memory scales with padded cohort prefix length: FP32 KV estimate is
rows × cached_length × layers × 2 × kv_heads × head_dim × 4 bytes. Dense prefill
mask adds rows × padded_length² × 4 bytes, before attention temporaries.
For illustration only, 36 layers/8 KV heads/128 head dimension yields about
9 GiB KV for eight rows of length4096, but 36 GiB at length16384; the dense
prefill mask adds 0.5 GiB and 8 GiB respectively. Exact checkpoint config,
optimizer-resident allocations and allocator peaks must be measured. A short
context CPU proof cannot clear max-context memory. BF16 changes logits and
sampling, so no BF16 rollout is enabled without independent matched proofs.
