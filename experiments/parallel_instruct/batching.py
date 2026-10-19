"""Keep prompt groups and effective batch fixed while changing GPU count."""
import math


def assignments(rank, world, prompts, responses_per_prompt):
    """Return (prompt index, sample index) pairs owned by this rank.

    Prefer keeping a prompt on one rank or a contiguous set of ranks. Uneven
    counts are allowed, e.g. batch32 on24 ranks gives 2/1/1 samples per prompt.
    """
    if any(type(x) is not int for x in (rank, world, prompts, responses_per_prompt)):
        raise ValueError('Batch dimensions must be integers')
    if world < 1 or prompts < 1 or responses_per_prompt < 2 or not 0 <= rank < world:
        raise ValueError('Invalid batch dimensions')
    if world > prompts * responses_per_prompt:
        raise ValueError('Choose at least one response per rank or reduce active ranks')
    if world <= prompts:
        return [(p, s) for p in range(rank, prompts, world) for s in range(responses_per_prompt)]
    base, extra = divmod(world, prompts)
    start = 0
    for prompt in range(prompts):
        count = base + int(prompt < extra)
        if start <= rank < start + count:
            return [(prompt, s) for s in range(rank - start, responses_per_prompt, count)]
        start += count
    raise AssertionError('Rank was not assigned a prompt')


def prompt_advantages(rank_records, prompts, responses_per_prompt):
    """Gathered per-rank records -> advantages keyed by prompt and sample.

    Center only within each prompt; no std division or whitening. Validate exact
    ownership and coverage before any response enters the optimizer.
    """
    groups = [[] for _ in range(prompts)]
    world = len(rank_records)
    for rank, records in enumerate(rank_records):
        expected = assignments(rank, world, prompts, responses_per_prompt)
        observed = [(r['prompt_index'], r['sample_index']) for r in records]
        if observed != expected:
            raise ValueError('Response ownership, ordering, or coverage mismatch')
        for record in records:
            if not math.isfinite(record['reward']):
                raise ValueError('Nonfinite reward')
            groups[record['prompt_index']].append(record)
    advantages = {}
    for prompt, records in enumerate(groups):
        if len(records) != responses_per_prompt or len({r['id'] for r in records}) != 1:
            raise ValueError('Incomplete or mixed prompt group')
        records.sort(key=lambda r: r['sample_index'])
        mean = sum(r['reward'] for r in records) / responses_per_prompt
        for record in records:
            advantages[prompt, record['sample_index']] = record['reward'] - mean
    return advantages


def ddp_loss_scale(world, prompts, responses_per_prompt):
    """DDP averages rank sums; turn that into a mean over the response batch."""
    assignments(0, world, prompts, responses_per_prompt)
    return world / (prompts * responses_per_prompt)


def rollout_seed(seed, step, prompt, sample):
    """Sampling seed is independent of rank ownership or GPU count."""
    import hashlib
    key = f"{seed}:{step}:{prompt}:{sample}".encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8], "little") % (2**63)
