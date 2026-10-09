"""Local JSONL telemetry. No network logger or model-output alteration."""
import json
import os
import time
from pathlib import Path

TOKENS = ('<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>')


def write_record(kind, record):
    root = os.getenv('PARALLEL_R1_TRACE_DIR')
    if not root:
        return
    folder = Path(root)
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / f'{kind}-{os.getpid()}.jsonl').open('a') as stream:
        stream.write(json.dumps(record, ensure_ascii=False, default=str) + '\n')


class Trace:
    def __init__(self, trajectory, prompt_length):
        self.record = dict(schema_version=1, trajectory=trajectory, prompt_tokens=prompt_length,
                           calls=[], forks=[], started_at=time.time())

    async def generate(self, manager, phase, request_id, prompt_ids, sampling_params, **kwargs):
        started = time.time()
        output = await manager.generate(request_id=request_id, prompt_ids=prompt_ids,
                                        sampling_params=sampling_params, **kwargs)
        ids = output['token_ids'] if isinstance(output, dict) else output
        self.record['calls'].append(dict(phase=phase, request_id=request_id, prompt_tokens=len(prompt_ids),
                                        generated_tokens=len(ids), generated_ids=list(ids),
                                        started_at=started, duration_s=time.time()-started))
        return output

    def fork(self, index):
        event = dict(response_token_index=index, fork_index=len(self.record['forks']))
        self.record['forks'].append(event)
        write_record('events', dict(event='fork', trajectory=self.record['trajectory'], **event))

    def finish(self, tokenizer, response_ids, response_mask, position_ids, masks, untruncated_length):
        self.record.update(response_tokens=len(response_ids), untruncated_response_tokens=untruncated_length,
                           truncated=untruncated_length > len(response_ids), response_ids=response_ids,
                           response_mask=response_mask, position_ids=position_ids.tolist(), path_masks=masks,
                           text=tokenizer.decode(response_ids, skip_special_tokens=False), finished_at=time.time())
        # All actual retained opening tags, including a final tag without an executed fork.
        tag = tokenizer.encode('<Parallel>', add_special_tokens=False)[0]
        indices = [i for i, token in enumerate(response_ids) if token == tag]
        self.record['parallel_relative_positions'] = [i / len(response_ids) for i in indices] if response_ids else []
        self.record['executed_fork_count'] = len(self.record['forks'])
        self.record['generation_calls'] = len(self.record['calls'])
        self.record['generated_tokens_total'] = sum(call['generated_tokens'] for call in self.record['calls'])
        write_record('traces', self.record)


def install_forward_probe():
    """Count actual eager model forwards for each scheduled vLLM V1 request.

    Shared batches count once globally; each participating request receives one
    participation. These are different measures, and must not be conflated.
    """
    if not os.getenv('PARALLEL_R1_TRACE_DIR'):
        return
    from vllm.v1.worker.gpu_model_runner import GPUModelRunner
    from vllm.v1.worker.gpu_worker import Worker
    if getattr(GPUModelRunner, '_parallel_r1_probe', False):
        return
    GPUModelRunner._parallel_r1_probe = True
    original = GPUModelRunner.execute_model
    original_sleep = Worker.sleep

    def flush(runner, finished=None):
        counts = getattr(runner, '_parallel_r1_counts', {})
        for request in list(counts) if finished is None else finished:
            if request in counts:
                write_record('forwards', dict(request_id=request, **counts.pop(request)))

    def execute(runner, scheduler_output, *args, **kwargs):
        if not hasattr(runner, '_parallel_r1_counts'):
            runner._parallel_r1_counts = {}
        flush(runner, getattr(scheduler_output, 'finished_req_ids', ()))
        actual = 0
        def hook(module, inputs, output):
            nonlocal actual
            actual += 1
        handle = runner.model.register_forward_hook(hook)
        try:
            output = original(runner, scheduler_output, *args, **kwargs)
        finally:
            handle.remove()
        scheduled = scheduler_output.num_scheduled_tokens
        for request, tokens in scheduled.items():
            count = runner._parallel_r1_counts.setdefault(request, dict(forward_passes=0, scheduler_steps=0, scheduled_tokens=0))
            count['forward_passes'] += actual
            count['scheduler_steps'] += 1
            count['scheduled_tokens'] += tokens
        write_record('engine', dict(actual_forward_passes=actual, scheduled_requests=len(scheduled),
                                    scheduled_tokens=sum(scheduled.values())))
        return output

    def sleep(worker, *args, **kwargs):
        flush(worker.model_runner)
        return original_sleep(worker, *args, **kwargs)

    GPUModelRunner.execute_model = execute
    Worker.sleep = sleep
