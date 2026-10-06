"""Synthetic alternating rewards ONLY to check a nonzero GRPO optimizer step.

Not a math metric. Production runs never load this file.
"""
import itertools

_counter = itertools.count()


def compute_score(**kwargs):
    return {'score': 1.0 if next(_counter) % 2 else -1.0, 'synthetic_smoke_reward': True}
