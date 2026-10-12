"""Experimental CPU-proven cohort serving; frozen rollout/reward unchanged.

Only the owner thread invokes the model. Each episode gets a separate Client.
Episode cost remains sum(max generated subgroup lengths), as in max_paths=2
serial microbatch serving; server-global shared calls are separate telemetry.
"""
import copy
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor


class CohortDecoder:
    def __init__(self, core, max_rows=8, max_paths=2, gather_seconds=.002):
        if max_rows < max_paths or max_paths < 1:
            raise ValueError('Require max_rows >= max_paths >= 1')
        self.core, self.max_rows, self.max_paths = core, max_rows, max_paths
        self.gather_seconds = gather_seconds
        self.pending = queue.Queue()
        self.server_batches = []

    def run(self, jobs):
        """jobs are functions accepting a private episode decoder adapter."""
        self.server_batches = []
        with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            futures = [pool.submit(job, Client(self, i)) for i, job in enumerate(jobs)]
            carry = None
            while not all(f.done() for f in futures) or carry is not None or not self.pending.empty():
                try:
                    request = carry or self.pending.get(timeout=.01)
                except queue.Empty:
                    continue
                carry = None
                cohort, rows = [request], len(request['calls'])
                deadline = time.monotonic() + self.gather_seconds
                while rows < self.max_rows:
                    try:
                        other = self.pending.get(timeout=max(0., deadline-time.monotonic()))
                    except queue.Empty:
                        break
                    # Existing decode API shares stop IDs; incompatible requests
                    # are left intact for the next batch, never approximated.
                    if rows+len(other['calls']) > self.max_rows or other['stops'] != request['stops']:
                        carry = other
                        break
                    cohort.append(other)
                    rows += len(other['calls'])
                try:
                    calls = [c for r in cohort for c in r['calls']]
                    budgets = [b for r in cohort for b in r['budgets']]
                    targets = [t for r in cohort for t in r['targets']] if request['targets'] is not None else None
                    if any((r['targets'] is None) != (targets is None) for r in cohort):
                        raise ValueError('Do not mix forced and sampled requests')
                    options = {} if targets is None else dict(target_sequences=targets)
                    results = self.core.decode_many(calls, budgets, request['stops'], **options)
                    self.server_batches.append(dict(episode_ids=[r['episode'] for r in cohort],
                                                    **copy.deepcopy(self.core.last_batch_stats)))
                    offset = 0
                    for r in cohort:
                        r['result'] = results[offset:offset+len(r['calls'])]
                        offset += len(r['calls'])
                except BaseException as error:
                    for r in cohort:
                        r['error'] = error
                finally:
                    for r in cohort:
                        r['ready'].set()
            return [f.result() for f in futures]


class Client:
    def __init__(self, owner, episode):
        self.owner, self.episode = owner, episode
        self.last_batch_stats = {}

    def __call__(self, call, budget, stops):
        return self.decode_many([call], budget, stops)[0]

    def decode_many(self, calls, budget, stops, *, target_sequences=None):
        budgets = [budget]*len(calls) if isinstance(budget, int) else list(budget)
        if len(budgets) != len(calls):
            raise ValueError('Per-row budgets must match calls')
        outputs, groups = [], []
        for start in range(0, len(calls), self.owner.max_paths):
            end = start+self.owner.max_paths
            request = dict(calls=calls[start:end], budgets=budgets[start:end], stops=tuple(sorted(set(stops))),
                           targets=None if target_sequences is None else target_sequences[start:end],
                           episode=self.episode, ready=threading.Event())
            self.owner.pending.put(request)
            request['ready'].wait()
            if 'error' in request:
                raise request['error']
            values = request['result']
            outputs.extend(values)
            lengths = [len(v[0]) for v in values]
            physical = max(lengths, default=0)
            groups.append(dict(physical_forward_calls=physical, prefill_forward_calls=int(physical > 0),
                               decode_forward_calls=max(0, physical-1), active_row_forward_work=sum(lengths),
                               call_indices=list(range(start, min(end, len(calls))))))
        self.last_batch_stats = dict(
            **{key: sum(g[key] for g in groups) for key in ('physical_forward_calls', 'prefill_forward_calls',
                                                          'decode_forward_calls', 'active_row_forward_work')},
            sequential_subgroups=groups, microbatch_max_paths=self.owner.max_paths,
            episode_cost_is_unbatched_server_counterfactual=True,
            cross_episode_server_cost_not_used_for_reward=True)
        return outputs
