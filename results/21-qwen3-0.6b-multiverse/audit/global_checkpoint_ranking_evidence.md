# Global TOP-5: evidence for all extant exp21 BF16 checkpoints

Audit date: 11 October 2026. Read-only inventory from the running personal
pod `vcharkin-exp-vm-0` in `shared-dzen-ml`. No GPU process, PVC change,
scale, copy, or deletion was performed.

## Scope and decision rule

A checkpoint is an exported model directory with `config.json` declaring
`"torch_dtype": "bfloat16"` and at least one `*.safetensors` weight file.
The scope is Qwen3-0.6B Multiverse experiment 21. The base Qwen assets and
older numbered Parallel-R1 experiments under `/work/runs/{02r,04,05,11,12,13,15}`
are not exp21 candidates and have no exp21 fixed40 result, so they cannot
enter this ranking.

All rows called **comparable** used the same fixed 40 prompts: 20 GSM8K dev
and 20 MATH dev, one greedy masked decode, seed 0, autonomous model generation
of tags and paths. The external-answer measure is a manually verified correct
standalone answer after closed `</think>`. A strict useful block has two
substantive independent correct paths and a correct combination; it does not
need a correct external answer, since external correctness is the next ranking
criterion.

Ranking is lexicographic and follows the retained-checkpoint rule:

1. require at least one complete numbered block inside `<think>`;
2. more strict useful blocks;
3. more correct external answers;
4. fewer truncations;
5. fewer tags outside `<think>`.

This is a selection rule for continued checkpoint work. It does not establish
full-dev or frozen-set superiority from 40 prompts.

## Physical inventory

The current pod confirms all 21 listed paths, BF16 dtype, config and weight
file. `/checkpoints` is the personal `vcharkin-exp21-checkpoints-pvc` (40 GiB,
21 GiB free at audit); `/work` is the personal `vcharkin-parallel-r1-pvc`
(196 GiB, 1.5 GiB free). No foreign PVC was read or mounted.

| Storage | Models | Count | Evaluation state |
|---|---|---:|---|
| `/checkpoints` | selective v4 steps 24, 40, 48, 56, 64 | 5 | complete fixed40 manual audit |
| `/checkpoints` | selective v5 steps 24, 32, 40, 48, 56 | 5 | complete fixed40 manual audit |
| `/checkpoints` | v4 recovery8 step 8 | 1 | complete fixed40 manual audit |
| `/checkpoints` | Deep51 tagged/plain, steps 4 and 8 | 4 | complete fixed40 manual audit |
| `/work` | M1 two-path tagweighted | 1 | same fixed40, full independent semantic review; normalized below |
| `/work` | original M1, Sol187, Sol187 control, deep75, deep75 control | 5 | weights present, but no result meeting current full semantic fixed40 schema |

The four Deep51-2x, Deep69, Deep69-LR10 and Deep69 recovery-recipe exports
are absent from permanent `/checkpoints` and `/work`; their archived results
remain evidence only, not selectable checkpoints.

## Comparable evidence

`B` means response-level complete numbered blocks. `U` means strict useful
blocks. `E` means manual correct external answers. `T` means truncations.
`O` means tags outside `<think>`.

| Checkpoint | Permanent path | B/40 | U/40 | E/40 | T/40 | O/40 | Evidence |
|---|---|---:|---:|---:|---:|---:|---|
| selective v4 step 24 | `/checkpoints/exp21-m1-selective-v4/step_24/model` | 1 | 0 | 28 | 4 | 0 | `audit/selective_v4_checkpoint_paired.json` |
| selective v4 step 40 | `/checkpoints/exp21-m1-selective-v4/step_40/model` | 11 | 1 | 28 | 3 | 0 | same |
| selective v4 step 48 | `/checkpoints/exp21-m1-selective-v4/step_48/model` | 18 | 1 | 25 | 3 | 0 | same |
| selective v4 step 56 | `/checkpoints/exp21-m1-selective-v4/step_56/model` | 19 | 2 | 27 | 4 | 0 | same |
| selective v4 step 64 | `/checkpoints/exp21-m1-selective-v4/step_64/model` | 19 | 2 | 26 | 2 | 1 | same |
| selective v5 step 24 | `/checkpoints/exp21-m1-selective-v5/step_24/model` | 5 | 0 | 27 | 6 | 0 | `audit/selective_v5_checkpoint_paired.json` |
| selective v5 step 32 | `/checkpoints/exp21-m1-selective-v5/step_32/model` | 5 | 0 | 27 | 5 | 0 | same |
| selective v5 step 40 | `/checkpoints/exp21-m1-selective-v5/step_40/model` | 15 | 1 | 25 | 6 | 0 | same |
| selective v5 step 48 | `/checkpoints/exp21-m1-selective-v5/step_48/model` | 19 | 1 | 25 | 4 | 0 | same |
| selective v5 step 56 | `/checkpoints/exp21-m1-selective-v5/step_56/model` | 17 | 2 | 28 | 5 | 0 | same |
| v4 recovery8 step 8 | `/checkpoints/exp21-v4-recovery8/step_8/model` | 12 | 2 | 29 | 2 | 0 | `audit/v4_recovery8_paired.json` |
| Deep51 tagged step 4 | `/checkpoints/exp21-deep51-tagged-p8/step_4/model` | 10 | 1 | 27 | 6 | 0 | `audit/deep51_pair_paired.json` |
| Deep51 tagged step 8 | `/checkpoints/exp21-deep51-tagged-p8/step_8/model` | 11 | 1 | 28 | 5 | 0 | same |
| Deep51 plain step 4 | `/checkpoints/exp21-deep51-plain-p8/step_4/model` | 6 | 0 | 25 | 4 | 0 | same |
| Deep51 plain step 8 | `/checkpoints/exp21-deep51-plain-p8/step_8/model` | 6 | 0 | 25 | 5 | 0 | same |
| M1 two-path tagweighted | `/work/exp21/models/m1-twopath-tagweighted` | 37 | 2 | 20 | 2 | 0 | `audit/m1_tagweighted_generated_{gsm,math}/verdicts.jsonl` and `EXPANDED_TH_RUN.md` |

### Normalization of early M1 tagweighted review

The early reports state 6/40 independent-useful path pairs, but that count
alone is weaker than the current strict criterion. Reading its row verdicts
shows that only `gsm8k-train/260` and `gsm8k-train/288` simultaneously have
independent useful paths, mathematically correct Paths and Conclusion, valid
structure, and a correct final answer. The MATH rows with independent paths
fail the Conclusion or final answer. Therefore the normalized strict count is
**2/40**, not 6/40. This prevents an inflated comparison with v4/v5 and
recovery checkpoints.

## Present but not comparable

| Checkpoint | Path | Known result on related fixed40 | Why outside rank |
|---|---|---|---|
| original M1 | `/work/runs/exp21-m1/model` | no current-schema semantic review | available BF16, but no complete comparable manual fixed40 result |
| Sol187 | `/work/runs/exp21-sol-th187/model` | masked pilot reports 39 complete blocks and 10 automatic correct answers | no full strict semantic block audit; cannot equate grammar to usefulness |
| Sol187 control | `/work/runs/exp21-sol-th187-control/model` | no paired current-schema fixed40 semantic audit | control checkpoint, not a ranked Multiverse model |
| deep75 | `/work/runs/exp21-sol-deep75/model` | masked pilot: 37 complete blocks, 6 automatic correct answers | no full manual strict-usefulness audit |
| deep75 control | `/work/runs/exp21-sol-deep75-control/model` | no matching complete semantic fixed40 audit | control checkpoint, not a ranked Multiverse model |

The automatic Sol187/deep75 figures are included only as provenance. They are
not comparable to `E` or `U`: later audits showed that syntactically complete
blocks can be mathematically false, duplicated, or pre-solved before the
block.

## Global TOP-5 under the rule

| Rank | Checkpoint | U/40 | E/40 | T/40 | O/40 | Selection reason |
|---:|---|---:|---:|---:|---:|---|
| 1 | v4 recovery8 step 8 | 2 | 29 | 2 | 0 | best external accuracy among all two-useful-block candidates; fewest truncations tied |
| 2 | selective v5 step 56 | 2 | 28 | 5 | 0 | second-highest external accuracy with two strict useful blocks |
| 3 | selective v4 step 56 | 2 | 27 | 4 | 0 | next external score, cleaner than v5 step 56 on truncation but external score is earlier tie-breaker |
| 4 | selective v4 step 64 | 2 | 26 | 2 | 1 | two useful blocks and low truncation; loses to step 56 on external score and has one outside-think tag |
| 5 | M1 two-path tagweighted | 2 | 20 | 2 | 0 | same normalized utility count; lowest external score in this group, but exceeds every one-useful-block candidate under rule |

The next candidates are selective v4 step 40 (U=1, E=28, T=3, O=0),
Deep51 tagged step 8 (U=1, E=28, T=5, O=0), then selective v4 step 48
(U=1, E=25, T=3, O=0). They are not in TOP-5 because usefulness is the first
post-eligibility metric.

## Reproducibility and limits

- Physical paths and BF16 dtype: read-only `kubectl exec` inspection of
  `config.json` and weight presence on 11 October.
- v4/v5/recovery8/Deep51 metrics: their paired JSON files named in the table.
- Early M1 normalization: full per-row verdict files named above.
- All comparisons are the same 20 GSM8K + 20 MATH prompts only. Full-dev,
  IFEval, frozen benchmarks, other decode modes, and temporary exports are not
  used to order this TOP-5.
- No checkpoint should be removed from this evidence: the report is a ranking,
  not an authorization to delete or overwrite any PVC data.
