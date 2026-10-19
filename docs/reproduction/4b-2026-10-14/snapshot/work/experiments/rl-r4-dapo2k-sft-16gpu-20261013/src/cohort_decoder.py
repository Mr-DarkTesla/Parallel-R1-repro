"""Phase-boundary cohort batching with one model owner and exact episode F.

A request is an indivisible complete sibling group (1..8). Different episodes
can share a 16/32-row backend batch. A phase is completed before scheduling the
next cohort: continuous admission within an in-flight KV cache is not implemented.
Every real semantic row participates in exactly len(generated_ids) physical
calls; its episode is charged once for the union of its branch participation.
Dummy inactive rows do not count. Global backend calls never enter R2 rewards.
"""
import copy
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor


class CohortDecoder:
    def __init__(self, core, max_rows=32, gather_seconds=.003):
        if not isinstance(max_rows, int) or max_rows < 8:
            raise ValueError('Aggregate capacity must fit an intact width8 fork')
        self.core, self.max_rows, self.gather_seconds = core, max_rows, gather_seconds
        self.pending = queue.Queue()
        self.server_batches = []

    def run(self, jobs):
        self.server_batches = []
        if not jobs:
            return []
        with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            futures = [pool.submit(job, Client(self, i)) for i, job in enumerate(jobs)]
            deferred = []
            while not all(f.done() for f in futures) or deferred or not self.pending.empty():
                try:
                    request = deferred.pop(0) if deferred else self.pending.get(timeout=.01)
                except queue.Empty:
                    continue
                cohort, rows = [request], len(request['calls'])
                deadline = time.monotonic()+self.gather_seconds
                while rows < self.max_rows:
                    try:
                        other = self.pending.get(timeout=max(0.,deadline-time.monotonic()))
                    except queue.Empty:
                        break
                    if rows+len(other['calls']) > self.max_rows or other['stops'] != request['stops'] or (other['targets'] is None) != (request['targets'] is None):
                        deferred.append(other)
                        continue
                    cohort.append(other)
                    rows += len(other['calls'])
                try:
                    calls = [dict(c,episode_id=str(r['episode'])) for r in cohort for c in r['calls']]
                    budgets = [b for r in cohort for b in r['budgets']]
                    targets = None if request['targets'] is None else [t for r in cohort for t in r['targets']]
                    options = {} if targets is None else dict(target_sequences=targets)
                    values = self.core.decode_many(calls,budgets,request['stops'],**options)
                    stats = copy.deepcopy(self.core.last_batch_stats)
                    self.server_batches.append(dict(episode_ids=[r['episode'] for r in cohort],
                        phase_names=[r['calls'][0].get('phase') for r in cohort],
                        episode_row_counts=[len(r['calls']) for r in cohort],**stats))
                    offset=0
                    for r in cohort:
                        r['result']=values[offset:offset+len(r['calls'])]
                        offset+=len(r['calls'])
                except BaseException as error:
                    for r in cohort:
                        r['error']=error
                finally:
                    for r in cohort:
                        r['ready'].set()
            return [f.result() for f in futures]


class Client:
    def __init__(self, owner, episode):
        self.owner,self.episode=owner,episode
        self.last_batch_stats={}

    def __call__(self,call,budget,stops):
        return self.decode_many([call],budget,stops)[0]

    def decode_many(self,calls,budget,stops,*,target_sequences=None):
        if not 1 <= len(calls) <= 8:
            raise ValueError('Episode requests must be one intact 1..8 sibling group')
        budgets=[budget]*len(calls) if isinstance(budget,int) else list(budget)
        if len(budgets)!=len(calls) or any(n<0 for n in budgets):
            raise ValueError('Invalid per-row budgets')
        if target_sequences is not None and len(target_sequences)!=len(calls):
            raise ValueError('Invalid forced targets')
        request=dict(calls=calls,budgets=budgets,stops=tuple(sorted(set(stops))),
            targets=target_sequences,episode=self.episode,ready=threading.Event())
        self.owner.pending.put(request)
        request['ready'].wait()
        if 'error' in request:
            raise request['error']
        outputs=request['result']
        lengths=[len(v[0]) for v in outputs]
        # All branch rows start together in a backend batch. Their union of
        # actual participation is sampling steps [0,max(lengths)).
        physical=max(lengths,default=0)
        stats=dict(physical_forward_calls=physical,prefill_forward_calls=int(physical>0),
            decode_forward_calls=max(0,physical-1),active_row_forward_work=sum(lengths),
            call_indices=list(range(len(calls))))
        self.last_batch_stats=dict(**stats,requested_rows=len(calls),microbatch_max_paths=8,
            sequential_subgroup_count=1,sequential_subgroups=[dict(stats)],
            episode_cost_is_actual_backend_participation=True,
            cross_episode_server_cost_not_used_for_reward=True)
        return outputs
