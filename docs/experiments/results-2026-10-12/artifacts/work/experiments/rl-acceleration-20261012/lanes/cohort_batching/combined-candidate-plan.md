Combined acceleration candidate: C phase cohorts + B row compaction + D semantic KV/replay

The measured fixed32 C candidate gives ~1.17–1.18x early full-update speedup with exactly identical first96 actions/outputs/rewards/episodeF. It is a safe composition candidate, not a strong final acceleration result.

Composition contract:
1. Keep exactly one FP32 model/DDP actor per GPU. C owner is the only caller of model and cache bank. CPU trajectory clients request intact1..8 sibling groups. Aggregate cap32 changes inference shape only.
2. Invoke B+D BatchedHFDecoder directly for aggregate groups; do not invoke B Microbatched wrapper on total19/32 rows. The wrapper's individual-fork8 check remains conceptually enforced by C Client.
3. B compacts completed rows using stable logical→physical indices, preserving row RNG, result order, generated_lengths, and active_row_forward_work.
4. D snapshots finished-row banks BEFORE B batch_select_indices removes those rows. Bank lookups bind exact token IDs, repeated positions, semantic ancestor visibility, and a model weight version. Gather/copy never runs model.forward.
5. Preserve D's fresh final-prefix query on every request: one physical prefill and one call per continuing sampled step. Thus episodeF remains the union of its branch participation, equal max(raw lengths) for a synchronized request. Bank hits reduce query work, never R2 F.
6. Clear/invalidate bank once at safe owner boundaries before fresh-policy rollout / after all clients finish before optimizer advances weight version. Client threads must not independently call clear_cache while other episodes run. Share a bank across episodes only with exact full identity keys and frozen model version.
7. Keep canonical response mask (raw actions1, injected headers/bridges0), native EOS/Think, postThink control-token blocking, structured repeated positions and 4D sibling isolation, frozen reward SHA, per-prompt4 centered rewards, fixed4096 loss denominator, Adam1e-6, and collective replay guard.

Fresh evidence required before promoting composition:
- Same checkpoint50, deterministic train prompt IDs/seed/offset1200 and fixed32 responses; baseline vs combined5 positive fresh-policy updates. Report normal updates2..5 without proof fixture overhead (run resident fixtures outside measured updates).
- Widths2/3/4/6/8 x4 rounds with residents on all8 actors, PLUS aggregate16/32 cross-client cases, unlike standalone width fixtures currently in C.
- GPU call_inputs masks/positions equal canonical inputs after compaction/semantic bank gather; decoder/replay likelihood guard max.01/mean.002/p95.005; injection coverage and per-episode participation counters exact.
- Compare sampled IDs, outputs, rewards, width/depth/F at matching seeds; report any stochastic numerical divergence without benchmark quality selection.
- Time real full update, generation/replay/backward/optimizer, explicit collectives plus NCCL overlap caveat. Report row-slot work, prefix/query tokens, global backendF, episodeF, throughput, allocated/reserved/peak memory, two positive Adam updates minimum, all8 clean exit.
- Benchmark64/128 only as explicit higher prompt counts at4samples/prompt. Retain fixed32 as default; increased generation is free only if measured total wall supports that claim.

No live inputs, controller, or other nodes are changed by this plan. Full token-level continuous admission remains separate from C phase cohorts.
