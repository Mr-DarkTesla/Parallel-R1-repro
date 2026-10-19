"""Scoped diagnostics: disjoint train phases and nested explanatory timers."""
import contextlib
import json
import os
from pathlib import Path
import time
import torch

CURRENT = None
KIND = 'other'

def category(value):
    global KIND
    KIND = value

class Profile:
    def __init__(self, output, rank, precision):
        global CURRENT
        self.output, self.rank, self.precision = Path(output), rank, precision
        self.output.mkdir(parents=True, exist_ok=True)
        self.step = None
        self.events = []
        self.host = {}
        self.counts = {}
        self.profiler = None
        self.profile_calls = 0
        self.profile_backward_done = False
        self.last_step_end = None
        CURRENT = self

    def start(self, step):
        self.step = step
        self.events = []
        self.host = {}
        self.counts = {}
        self.began = time.perf_counter()

    @contextlib.contextmanager
    def phase(self, name, cuda=True):
        start = time.perf_counter()
        begin = end = None
        if cuda:
            begin, end = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
            begin.record()
        scoped = self.rank == 0 and self.step == 51 and name == 'backward' and not self.profile_backward_done
        if scoped:
            self.profile_backward_done = True
            profiler = torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU, torch.profiler.ProfilerActivity.CUDA], record_shapes=True)
            profiler.__enter__()
        with torch.profiler.record_function(name):
            yield
        if end is not None:
            end.record()
            self.events.append((name, begin, end))
        self.host[name] = self.host.get(name, 0.) + time.perf_counter()-start
        self.counts[name] = self.counts.get(name, 0)+1
        if scoped:
            profiler.__exit__(None, None, None)
            profiler.export_chrome_trace(str(self.output/'rank0-first-backward.json'))
            (self.output/'rank0-first-backward-table.txt').write_text(profiler.key_averages().table(sort_by='self_cuda_time_total', row_limit=50))

    def finish(self, optimizer_step, metric):
        torch.cuda.synchronize()
        finished = time.perf_counter()
        durations = {}
        for name, begin, end in self.events:
            durations[name] = durations.get(name, 0.)+begin.elapsed_time(end)/1000
        value = dict(step=self.step, rank=self.rank, precision=self.precision,
                     wall_before_diagnostic_finish=finished-self.began,
                     phase_host_seconds=self.host, current_stream_event_seconds=durations,
                     counts=self.counts, optimizer_step=optimizer_step,
                     peak_gpu_bytes=metric['peak_gpu_bytes'],
                     warning='Nested detail timers overlap train phases; never add them to phase totals. Stream events include waits, not isolated GPU kernel durations; scoped Chrome trace gives kernel view. First step profiled, subsequent steps unprofiled.')
        with (self.output/f'phase-rank-{self.rank}.jsonl').open('a') as f:
            f.write(json.dumps(value)+'\n')
        self.last_step_end = finished

def phase(name, cuda=True):
    return CURRENT.phase(name, cuda) if CURRENT is not None and CURRENT.step is not None else contextlib.nullcontext()

def model_forward(fn, *args, **kwargs):
    owner = CURRENT
    kind = KIND
    scoped = owner is not None and owner.rank == 0 and owner.step == 51 and kind.startswith('generation') and owner.profile_calls < 9
    if scoped and owner.profiler is None:
        owner.profiler = torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU, torch.profiler.ProfilerActivity.CUDA], record_shapes=True)
        owner.profiler.__enter__()
    autocast = torch.autocast(device_type='cuda', dtype=torch.bfloat16) if owner is not None and owner.precision == 'bf16_autocast' else contextlib.nullcontext()
    with phase('detail.model.'+kind), autocast:
        result = fn(*args, **kwargs)
    if scoped:
        owner.profile_calls += 1
        if owner.profile_calls == 9:
            owner.profiler.__exit__(None, None, None)
            owner.profiler.export_chrome_trace(str(owner.output/'rank0-first-prefill-eight-decode.json'))
            (owner.output/'rank0-first-prefill-eight-decode-table.txt').write_text(owner.profiler.key_averages().table(sort_by='self_cuda_time_total', row_limit=50))
            owner.profiler = None
    return result
