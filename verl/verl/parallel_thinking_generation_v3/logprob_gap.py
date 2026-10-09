"""Compare vLLM's sampled-token log-probs with the actor's old_log_probs per trajectory segment.

Block-1 paths are scored in the rollout's own context by both the tree and the
flat_packed actor, so their gap is the bf16 noise floor; a larger gap elsewhere
is a rollout/actor context mismatch. Valid for temperature 1 without top-p/top-k
truncation, because vLLM V1 reports log-probs of the raw logits. For the same reason,
with protocol=plan_v1 the gap also contains the mass of the tags each node suppresses
(the actor scores the suppressed distribution that was actually sampled).
"""
import torch

SEGMENTS = ('main_before_fork', 'path_block1', 'path_later', 'summary_block1', 'summary_later', 'main_after_fork',
            'plan_block1', 'plan_later')
MAIN_BEFORE, PATH_FIRST, PATH_LATER, SUMMARY_FIRST, SUMMARY_LATER, MAIN_AFTER, PLAN_FIRST, PLAN_LATER = range(
    len(SEGMENTS))


def gap_metrics(rollout_log_probs, actor_log_probs, segments, prefix='rollout_gap'):
    """Mean/max |rollout - actor| log-prob and token counts for each segment and overall."""
    gap = (rollout_log_probs.float() - actor_log_probs.float()).abs()
    metrics = {}
    for name, selected in [(name, segments == code) for code, name in enumerate(SEGMENTS)] + [('all', segments >= 0)]:
        values = gap[selected]
        metrics[f'{prefix}/{name}_tokens'] = int(values.numel())
        if values.numel():
            metrics[f'{prefix}/{name}_abs_mean'] = values.mean().item()
            metrics[f'{prefix}/{name}_abs_max'] = values.max().item()
    return metrics
