# Trace diagnosis, 2026-10-10

Original native-thinking baseline remains fixed at 98/128 (76.5625%), GSM53/64 and MATH45/64. Additional backend diagnostics must not redefine it. Original artifacts and frozen sources are unchanged.

## Verified behavior

LR1e-3 structured24: 8 attempted blocks, 7 invalid width headers, only1 executed round (width4). That executed round occurred after think and gave an incorrect answer.

LR1e-3 structured128: accuracy90/128 (70.3125%), 28 attempted blocks, 23 invalid width headers, 5 executed rounds on5 tasks (3.90625%). Actual executed widths4,7,2,4,3; mean4.0; mean rounds per task0.0390625. Nineteen attempted blocks occurred after think. No canonical parallel-valid response. Native accuracy stayed98/128.

LR2e-4 structured128: accuracy81/128 (63.28125%), 27 attempted blocks, all27 after think and invalid width, no executed round. Mean executed width is undefined, not0.

Fresh weighted/constrained partial66: no Plan inside think,46 Plan after think, no fork. This is partial coverage, not a final quality result. After-think XML control masking is active. Raw responses sometimes fall back to bare > and numeric lists when XML controls are forbidden. Repetition does not count as a parallel computation.

## Mechanism and limits

The dominant observed pattern is serial native reasoning followed by protocol formatting in the visible answer. Runtime state restrictions suppress illegal openings but do not teach decomposition before reasoning. Width strings such as `<Parallel> 3\n` and `<Parallel>3  \n` are rejected by the strict old width parser; the new guard constrains width, but that only matters after a block begins. Existing system prompt offers optional parallel work, permits sequential reasoning, and has no complete worked example.

Training has 15360 trainable parameters, only6 tied control-token rows. It directly teaches control-token representations and scores, while the transformer and native output rows for Plan, digits, think boundaries and ordinary reasoning remain frozen. The hypothesis is that this is too little adaptation for changing native reasoning organization. It is not proof that a stronger row-only curriculum cannot work; prompt embeddings containing control tokens can affect native-token logits.

## Prepared corrective diagnostic

`parallel-inside-think-example-system.txt` gives a short explicit early-decomposition instruction and one synthetic complete correct two-branch calculation inside think. No runtime Plan/fork insertion. Same weighted checkpoint, current constrained decoder, questions128, budgets, scorer, temperature and seeds. Queue tmp2 task120 after its already-running task110. Output `format-loss-20261010/evaluations/weighted-format-fewshot-128`.

This isolates prompt placement and demonstration. Report accuracy against unchanged original98/128, forked-task rate, round count, mean rounds/task, executed-width distribution, canonical-valid parallel rate and correct-and-parallel-valid count separately. Prompt compliance is not learned SFT behavior. If the example elicits useful forks while retaining accuracy, matching training/inference prompt is the next row-only SFT experiment. If it still yields serial-only thinking, broader adaptation is a separate proposed scope; do not silently unfreeze backbone or launch LoRA under the current six-row-only contract.

## Resource allocation

Existing24GPU only: Sirius currentweighted/guarded128; tmp3 baseline5e-4/guarded128 (following completed LR2e-4); tmp2 already-running additional HF diagnostic, followed by prompt-placement test128. No new allocations or restarted stopped parents. No more LR scans until the behavioral failure is resolved. No forced forks counted as autonomous.

## Metric correction

Legacy summary widths are regex matches from text and include rejected headers. `diagnose.py` counts actual contiguous path-call groups from immutable policy calls and asserts group count equals actual forks. Original summaries are retained; separate diagnosis artifacts contain corrected executed widths. Partial and complete runs remain distinct.
