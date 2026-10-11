## Short version

The likeliest cause is that the tag rows were updated too hard. A data-format problem probably makes it worse. A mask bug is the least likely. One teacher-forced probe on checkpoints you already have can tell these apart without generating anything. Before spending more GPU on 4B, run a 24-step 0.6B rerun with the tag multiplier set to 1. If you skip that, the 4B pair inherits the same confound.

## (1) Failure mechanism and a test that separates the causes

**Evidence:**
- **The ×100 multiplier also changes the output logits.** In the repo test (`tag_lr_steps` / `check_tag_lr`), `tag_lr_mult` scales the update for the tag rows of a single tied embedding. Qwen3 small models tie input and output embeddings; your local 4B-Base config has `tie_word_embeddings: true`. So ×100 moves the tag tokens' output logits directly, not only their input representation. Effective tag LR is 3e-4 with Adam.
- **The damage depends on dose.** 8 steps at ×100 kept 10–11 complete blocks. 24 steps gave 0/40 complete, 33 nested `<Parallel>` and short outputs.
- **The data teaches "emit `<Parallel>` immediately".** 194/196 positives open the reasoning with `<Parallel>` and all use a generic Outline. That gives a strong prior for `<Parallel>` at the start of reasoning, and nothing teaches when not to open a block.
- **This does not separate a mask bug from overshoot.** The tag-LR test passes, but it only checks optimizer arithmetic on synthetic gradients. Separately, `diagnose_tag_transition.py` and `verify_cached_mask.py` render with `enable_thinking=False`, while the Sol rows use `True`. Those diagnostics may therefore have checked a different token layout from the one you trained on.

**Hypothesis:** tag logits are inflated, especially for `<Parallel>` right after an Outline or `<Path>`. That gives nested opens, no closes and early termination. The generic outline adds a template the model copies without content.

**The test:** score with teacher forcing on step 0, 8 and 24 (no generation, one GPU-minute each). Use three probe sets:

| Probe set | Measure |
|---|---|
| A. Training positives | NLL of tag tokens at gold positions; P(`</Path>`, `</Parallel>`) at gold close positions |
| B. ~20 held-out reviewed positives | Same as A, plus NLL of the path body text |
| C. Parent's own fixed-40 outputs (plain, no tags) | P(any tag) summed over all positions; P(`<Parallel>`) at positions inside a `<Path>` |

First render one row through the exact trainer path, decode `labels != -100`, and diff it against the eval prompt prefix.

How to read the result:
- **Mask/position bug:** decoded labels are shifted or tags fall outside the loss mask. Tag NLL on set A does not go down, and recomputed loss differs from the logged trainer loss.
- **Overshoot:** sets A and B fit well, but on set C tag probability at non-tag positions climbs from step 0 to 8 to 24, with the largest jump in P(`<Parallel>` | inside `<Path>`). A causal check is the same 24-step run with ×1 (or ×10). If complete blocks come back, overshoot is confirmed.
- **Teacher format:** tags fit well and set C stays clean, but set B body NLL is high. Generation then dies after the generic outline because there is no content to continue.

## (2) Run order on one GPU

1. **No training:** the probe and label-render diff above on the existing step-24 checkpoints.
2. **0.6B, tagged arm only, 24 steps, `tag_lr_mult=1`** (optionally also 10). This is minutes of compute. It decides the multiplier for 4B. If you skip it, a 4B failure stays ambiguous.
3. **4B baselines:**
   - Untouched 4B with **no added tokens**.
   - 4B with the 10 initialised tag tokens.

   Because the embeddings are tied, the initialised rows have non-zero logits and can be sampled. Report P(tag) per position. If it is close to zero, one fixed-40 eval of the initialised model is enough.
4. **4B pair, 16 steps, with the multiplier from step 2.** Eval is cheap next to training, so eval all of 4, 8 and 16. Stop rule: if step 4 already has more than 50% malformed attempts and P(tag) on set C is rising, kill the 4B tagged line.
5. **0.6B Claude-M1, 70 steps:** move it last or drop it. It tests whether wrapping solutions in `<think>` helps capability, not parallel structure, and it has no paired control.

## (3) Turning existing correct 4B traces into independent `<think>` parallelism

**Option A: two independent correct samples.** For each problem, take two separately sampled correct 4B traces that use different methods.
- Path 1 is trace A's reasoning verbatim; Path 2 is trace B's reasoning verbatim.
- The Conclusion is the shared final-answer sentence copied from one of them.
- Independence holds by construction because the samples were generated separately, and agreement doubles as verification. You will need extra sampling to get two correct, diverse traces per problem, which is cheap on vLLM.

**Option B: split one trace by dependencies.**
- Split the reasoning into steps and find which quantities each step uses and produces (numbers, variables and expressions; regex plus sympy where possible).
- Find sibling groups: at least two segments whose inputs come only from the problem statement or a shared prefix, whose outputs are not used by each other, and whose results are combined by a later step.
- Wrap those segments verbatim in tags. For the 57 Part 1/Part 2 traces, move the original text inside `<think>` and leave only the final answer after it.

**Strict gate (all checks must pass):**
1. **Verbatim:** after stripping tags and normalising whitespace, the result is identical to the source trace or traces. Only tag insertion and reordering are allowed.
2. **Symbolic independence:** no path refers to a quantity first derived in a sibling path.
3. **Measured independence:** with parent-4B teacher forcing, Path 2's NLL with and without Path 1 in context differs by less than about 0.05 nats/token. Swapping path order also leaves both NLLs within that threshold.
4. **Non-trivial paths:** each path has at least N tokens and at least one computation, and the merge step uses outputs from at least two paths.
5. **Correctness and form:** the final answer is correct, tags are well-formed and not nested, all paths are inside `<think>`, and the text after `</think>` is unchanged.
6. **Distribution:** at most about 40% of blocks start at offset 0 of the reasoning. Use no Outline, or the first sentence of each path; never generic text.

## (4) Problems in the queued comparison

- **The multiplier is confounded with the tags.** Only the tagged arm gets ×100 on tied output rows, so tagged vs plain at 4B compares structure plus logit overshoot. Settle the multiplier first (step 2 above).
- **The baseline is contaminated.** "Untouched" 4B with initialised tied tag rows is no longer untouched. Keep a no-added-tokens baseline.
- **Fixed-40 is underpowered.** 26 vs 29 correct is noise: the standard error is about ±3 problems at p≈0.7. "2 truly useful" blocks cannot rank anything. Use paired per-problem McNemar tests, 4 samples per prompt at temperature 0.6, and report truncation separately. 4B traces are longer, so check that `max_new_tokens` does not cut them off.
- **Checkpoints 4 and 8 are not true 4- and 8-step runs.** They are points inside a 16-step warmup/decay schedule. Label them that way, or use a constant LR after warmup.
- **Steps are not matched by exposure.** Compare runs by how many times positive rows were seen, not by step count. 0.6B at 24×32 and 4B at 16×32 over 383 rows give different exposure.
- **The 4B tagged arm inherits the data flaws.** It uses the same 196 rows with the same `<Parallel>`-first opening and generic Outline. If it fails, you can't tell scale from data. Fix the data first (gate item 6) before treating the result as a verdict on 4B.
- **Check for leakage** between the 367 M1 rows, the 196 Sol rows and the fixed-40 problems, using normalised question hashes.

I only read the tag-multiplier test and grepped for `enable_thinking` settings. I didn't run anything, and the trainer's real mask code is still unverified.
