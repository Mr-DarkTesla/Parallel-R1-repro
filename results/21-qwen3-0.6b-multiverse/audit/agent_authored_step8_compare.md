# Agent-authored tagged/plain fixed40 sweep

`raw_acc_robust` is parser output. Manual external accuracy and strictly useful blocks remain null until the complete review manifest is present.

| Variant | Raw correct /40 | Numbered /40 | Truncated /40 | Manual correct /40 | Strict useful /40 |
|---|---:|---:|---:|---:|---:|
| plain_step8 | 22 | 14 | 5 | 22 | 1 |
| tagged_step8 | 23 | 19 | 2 | 23 | 2 |

## Paired CIs

All reported binary deltas are candidate minus reference in percentage points. CI is a deterministic 10,000-resample paired bootstrap over the identical 40 prompts.

- `plain_step8` vs `c0_corrected` raw accuracy: -25.00 pp, 95% CI [-42.50, -7.50].
  Manual external: -30.00 pp [-45.00, -15.00]; strict useful: +2.50 pp [0.00, 7.50].
- `plain_step8` vs `tagged_step8` raw accuracy: -2.50 pp, 95% CI [-17.50, 12.50].
  Manual external: -2.50 pp [-17.50, 12.50]; strict useful: -2.50 pp [-7.50, 0.00].
- `tagged_step8` vs `c0_corrected` raw accuracy: -22.50 pp, 95% CI [-40.00, -5.00].
  Manual external: -27.50 pp [-45.00, -10.00]; strict useful: +5.00 pp [0.00, 12.50].
- `tagged_step8` vs `plain_step8` raw accuracy: +2.50 pp, 95% CI [-12.50, 17.50].
  Manual external: +2.50 pp [-12.50, 17.50]; strict useful: +2.50 pp [0.00, 7.50].
