"""Opt-in coarse phase timing for a separate runner; no per-token synchronization.

Record boundaries around rollout, replay/backward, optimizer, cleanup, metrics
collectives, validation and checkpoint. Final-backward walltime includes DDP
communication overlap; this timer cannot isolate NCCL compute from backward.
"""
import time


class PhaseTimer:
    def __init__(self, device=None):
        self.device = device
        self.boundaries = []

    def mark(self, name):
        if self.boundaries and name == self.boundaries[-1][0]:
            raise ValueError('Adjacent timing boundaries need distinct names')
        event = None
        if self.device is not None:
            import torch
            event = torch.cuda.Event(enable_timing=True)
            event.record(torch.cuda.current_stream(self.device))
        self.boundaries.append((name,time.perf_counter(),event))

    def finish(self):
        if self.device is not None:
            import torch
            torch.cuda.synchronize(self.device)
        phases = []
        for before,after in zip(self.boundaries,self.boundaries[1:]):
            phases.append(dict(begin=before[0],end=after[0],host_seconds=after[1]-before[1],
                               device_stream_seconds=None if before[2] is None else before[2].elapsed_time(after[2])/1000))
        return dict(phases=phases,host_total_seconds=sum(p['host_seconds'] for p in phases),
                    final_profiling_synchronize_excluded=True,
                    device_events_cover_current_stream_only=True,
                    backward_and_ddp_communication_not_separated=True)
