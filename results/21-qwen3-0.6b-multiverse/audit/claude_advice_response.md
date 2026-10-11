## Short version

- **Data:** mainly convert the Sol6.1 traces. Use a teacher only to restructure a trace and to judge whether it really splits into two independent parts. Treat free generation by Qwen3-4B as the backup source. Use DeepSeek free generation last.
- **Training:** build exact pairs. Each problem gets a two-path version and a plain version with the same reasoning and the same answer. Add replay and a consistency term.
- **Switch to 4B** only if 0.6B produces correctly formatted blocks whose branch content is wrong. If it fails to produce blocks at all, the cause is data or training, not model size.
- **Evaluation:** fixed40 is too small to separate checkpoints. Add a larger held-out set with several samples per problem and compare checkpoints problem by problem.

## 1. Getting 180+ more trajectories

| Source | Answer quality | Distribution gap for 0.6B | Main risk | Cost |
|---|---|---|---|---|
| Edited Sol traces (203) | Already checked against the answer | Medium | Fake parallelism forced onto sequential reasoning | Low |
| Qwen3-4B free generation | Needs rejection | **Low** (same family and tokenizer) | Low yield, dependent branches | Low |
| DeepSeek free generation | High | High (long, different style) | 0.6B copies the style and loses accuracy | Medium |

Recommended pipeline:
1. **Pick problems before rewriting.** Have the teacher classify each Sol trace: does it contain two subcomputations whose inputs are known before the split? Expect maybe 30–50% of traces to qualify; that figure is my guess. Skip the rest and don't force them.
2. **Constrain the edit.** Keep the original content tokens as far as possible. Allow only reordering, the split and the merge, with the final answer fixed. Reject the edit if the token edit distance from the source exceeds a threshold.
3. **Run automatic checks before human review:**
   - The tags parse.
   - The masked rendering matches the training renderer.
   - Each branch uses only the shared prefix: render it with the sibling hidden and check that no reference to the sibling remains.
   - The merge actually uses both branch results.
   - The answer matches the reference.
4. **Rank by how natural the trace is for the student.** Score per-token NLL under the training start checkpoint and drop the top-NLL tail. Your on-policy results suggest distribution shift is part of the problem.
5. **Run a $10–15 yield pilot first** (about 30 problems per source), then scale the cheapest valid source.
   - $124.50 remains. Hold back about $30 for review and judging.
   - Stratify by dataset and answer type (integer / expression / fraction) to match the 78 existing examples.
6. **Keep the same review standard as for the 78.** Use blind independent review on at least a sample, plus 100% automatic checks.

Uncertainty: I don't know how many of the 203 Sol traces contain real independence. GSM8K traces are often strictly sequential. Yield could be under 90, in which case Qwen3-4B generation has to cover the gap.

## 2. Getting 0.6B to learn useful branches cheaply

- **Use exact pairs.** For each problem, train on the two-path version and the plain serial version with the same content and the same answer. Then a gap between the tagged run and the plain control measures the format, not new content.
- **Mix in replay.** Use roughly 1:1 to 1:2 tagged to plain correct traces from the model's own distribution. Optionally add a KL term to the start checkpoint on plain tokens.
- **Choose the start point carefully.** The recovery checkpoint is already 5 answers down. Run one arm from the 34/40 baseline as well, or every run inherits that loss.
- **Check the mask and positions first.** This is cheap and important.
  - Mask with no tags present: logits must match the standard forward pass.
  - Mask during training versus mask during inference: the outputs must be identical.
  - Sibling position reuse: the pretrained 0.6B has never seen it. Test one ablation where branch positions continue instead of restarting. If accuracy recovers, the position scheme is causing the loss.
- **Teach when to branch.** Include problems where the plain trace is correct and no block appears. Otherwise the model forces blocks onto problems that don't need them, and accuracy drops.
- **Keep the update small.** Use a low learning rate or LoRA and 2–4 epochs over about 250 examples. Watch held-out tagged-token NLL and plain-token NLL separately. If plain NLL rises, you are losing accuracy.

## 3. When to switch to 4B

Fix the criteria before the next runs:
- **Switch** if, with at least 250 valid examples and matched controls, 0.6B emits well-formed blocks but at least half of them are not useful (dependent or wrong branches), or it drops more than 3/40 against the plain control.
- **Don't switch** if 0.6B rarely emits blocks. That points to data or training, and 4B would hide the problem.
- **Practical setup:** 4B full fine-tuning on one H100 is tight, so use LoRA or 8-bit Adam. If you authorise a second GPU, use it to run the 4B arm in parallel rather than one after the other.

## 4. Fair evaluation and early stopping

- **fixed40 is a dev set, not the final judge.** A gap of 34 vs 29 can be noise at this size.
- **Add a held-out set of 200–300 problems.** Stratify by dataset and answer type, and keep it disjoint from all training problems, including the Sol sources.
- **Sample more than once.** Use greedy decoding plus 4 samples at the production temperature. Report pass@1 averaged over the samples.
- **Compare by problem.** Use McNemar or a paired bootstrap against the plain control with the same seed, data order and step count. Report confidence intervals.
- **Define "useful block" once, in a fixed spec.** Score it automatically, plus blind review on a sample. Don't change the definition between runs.
- **Early stopping:** evaluate every N steps on fixed40. Select the checkpoint with the most useful blocks, subject to accuracy ≥ baseline − δ (for example δ = 1/40). Confirm on the held-out set once. Never select on the held-out set.
- **Checkpoint preservation:** rank by that same rule so the global top five stay consistent across runs.

## Highest-value next two experiments

1. **Data yield pilot (about $15, CPU and API only, can run during the current SFT).** Thirty problems each from three sources: Sol edit, Qwen3-4B generation, DeepSeek generation. Measure valid useful yield per dollar, answer correctness and 0.6B NLL. Scale the winner to more than 180.
2. **Paired 0.6B SFT, 2×2 design, 2 seeds** (needs a second GPU or runs in sequence). About 250 tagged examples with exact plain pairs plus replay. Factors are the start point (baseline vs recovery) and the position scheme (restart vs continue). Evaluate on fixed40 and the held-out set. The result shows whether the main blocker is the start point, the positions or the data.

Biggest uncertainty: whether 0.6B can do useful decomposition at all. Experiment 2 is set up so that its result also answers the question in section 3.
