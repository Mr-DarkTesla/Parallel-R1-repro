"""Standardize group accuracy; center the auxiliary term without scaling it."""

from collections import defaultdict

import torch


@torch.no_grad()
def compute_split_advantage(accuracy, auxiliary, index, response_mask, epsilon=1e-6):
    """Preserve the auxiliary coefficient and give all-wrong groups zero signal.

    Accuracy uses the same unbiased sample standard deviation as ordinary GRPO.
    Singleton groups carry no learning signal. Both components are broadcast
    over retained response tokens; padding remains zero.
    """
    correct = torch.as_tensor(accuracy, dtype=torch.float32, device=response_mask.device)
    aux = torch.as_tensor(auxiliary, dtype=torch.float32, device=response_mask.device)
    if (response_mask.ndim != 2 or correct.ndim != 1 or aux.shape != correct.shape
            or not len(correct) or len(correct) != len(index) or len(correct) != len(response_mask)):
        raise ValueError('Expected nonempty aligned accuracy, auxiliary, uid and response-mask rows')
    if not torch.isfinite(correct).all() or not torch.isfinite(aux).all():
        raise ValueError('Reward components must be finite')
    if not ((correct == 0) | (correct == 1)).all() or not (aux[correct == 0] == 0).all():
        raise ValueError('Split GRPO requires binary accuracy and zero auxiliary reward for wrong answers')
    if epsilon <= 0:
        raise ValueError('epsilon must be positive')

    groups = defaultdict(list)
    for row, uid in enumerate(index):
        groups[uid].append(row)
    accuracy_advantage = torch.zeros_like(correct)
    auxiliary_advantage = torch.zeros_like(aux)
    mixed = 0
    for rows in groups.values():
        values, costs = correct[rows], aux[rows]
        if len(rows) > 1:
            accuracy_advantage[rows] = (values - values.mean()) / (values.std() + epsilon)
            auxiliary_advantage[rows] = costs - costs.mean()
        mixed += int(values.min() != values.max())
    combined = (accuracy_advantage + auxiliary_advantage).unsqueeze(-1) * response_mask
    metrics = {
        'reward/accuracy_mean': correct.mean().item(),
        'reward/aux_mean': aux.mean().item(),
        'reward/total_mean': (correct + aux).mean().item(),
        'advantage/accuracy_abs_mean': accuracy_advantage.abs().mean().item(),
        'advantage/aux_abs_mean': auxiliary_advantage.abs().mean().item(),
        'grpo/mixed_accuracy_group_fraction': mixed / len(groups),
    }
    return combined, combined, metrics
