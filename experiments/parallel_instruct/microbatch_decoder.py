"""Fullwidth8 batching wrapper; each shared forward is charged once.

All 1..8 branches run in one subgroup. Invalid widths or a smaller path cap fail
before decoding; there is no fallback to sequential subgroups. The actual GPU
plus resident-Adam memory gate remains required before production.
"""
from decoder import BatchedHFDecoder


class MicrobatchedHFDecoder:
    def __init__(self, model, replay, device=None, max_paths=8):
        if not isinstance(max_paths, int) or max_paths < 1:
            raise ValueError('Positive integer max_paths required')
        self.core = BatchedHFDecoder(model, replay, device)
        self.max_paths = max_paths
        self.last_batch_stats = {}

    def __call__(self, call, budget, stops):
        return self.decode_many([call], budget, stops)[0]

    def decode_many(self, calls, budget, stops, *, target_sequences=None):
        if self.max_paths != 8 or not 1 <= len(calls) <= 8:
            raise ValueError('Fullwidth8 requires one complete group of 1..8 branches')
        budgets = [budget]*len(calls) if isinstance(budget, int) else list(budget)
        if len(budgets) != len(calls):
            raise ValueError('Per-row budgets must match calls')
        results, groups = [], []
        for begin in range(0, len(calls), self.max_paths):
            end = min(begin+self.max_paths, len(calls))
            options = {} if target_sequences is None else dict(target_sequences=target_sequences[begin:end])
            results.extend(self.core.decode_many(calls[begin:end], budgets[begin:end], stops, **options))
            group = dict(self.core.last_batch_stats, call_indices=list(range(begin,end)))
            groups.append(group)
        self.last_batch_stats = dict(
            physical_forward_calls=sum(g['physical_forward_calls'] for g in groups),
            prefill_forward_calls=sum(g['prefill_forward_calls'] for g in groups),
            decode_forward_calls=sum(g['decode_forward_calls'] for g in groups),
            active_row_forward_work=sum(g['active_row_forward_work'] for g in groups),
            microbatch_max_paths=self.max_paths, requested_rows=len(calls),
            sequential_subgroup_count=len(groups), sequential_subgroups=groups,
            reported_physical_cost_is_subgroup_sum=True,
            optimizer_memory_proof_still_required=True)
        return results
