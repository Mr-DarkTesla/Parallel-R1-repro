"""Freeze representative trace groups and atomically submit bounded owned audit203."""
import hashlib
import json
import os
from pathlib import Path

P = Path('${PROJECT_ROOT}')
HERE = P/'work/experiments/rl-readiness-20261010/batched'
TRACE = P/'work/experiments/base-format-20261010/evaluations/base-no-think-unconstrained-128'
HOST = P/'work/experiments/night-20261010/cloud-continued/tmp2'
OUTPUT = HERE/'frozen-trace-cases.json'
QUEUE = HOST/'queue/203-batched-base-fp32-gpu.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if Path.cwd() != P:
        raise RuntimeError('Explicit project root cwd required')
    if OUTPUT.exists() or QUEUE.exists():
        raise RuntimeError('Immutable proof inputs/queue already exist; no overwrite')
    status = json.loads((HOST/'status.json').read_text())
    if status.get('state') not in ['idle', None] or status.get('pending', 0):
        raise RuntimeError('Host must still be idle: '+str(status))
    groups = []
    sources = {}
    for path in sorted(TRACE.glob('traces-*.jsonl')):
        sources[str(path.relative_to(P))] = sha(path)
        for line in path.open():
            trajectory = json.loads(line)
            call_group = []
            round_index = 0
            for call in trajectory['trace']['policy_calls'] + [{'phase':'end'}]:
                if call['phase'] == 'path':
                    call_group.append(call)
                elif call_group:
                    round_index += 1
                    width = len(call_group)
                    if width in [2, 4, 6]:
                        groups.append(dict(kind='frozen_real_base_trace', width=width,
                                           task_id=trajectory['id'], round=round_index,
                                           source_trace=str(path.relative_to(P)),
                                           calls=call_group))
                    call_group = []
    cases = []
    for width in [2, 4, 6]:
        # Preserve the real prefix with most prior context, and actual raw
        # actions capped at128 solely to bound this diagnostic's runtime.
        choices = [g for g in groups if g['width']==width]
        group = max(choices, key=lambda g:max(len(c['prompt_ids']) for c in g['calls']))
        group['original_target_lengths'] = [len(c['generated_ids']) for c in group['calls']]
        group['target_cap'] = 128
        for call in group['calls']:
            call['generated_ids'] = call['generated_ids'][:128]
        cases.append(group)
    OUTPUT.write_text(json.dumps(dict(source_sha256=sources, cases=cases), indent=2)+'\n')
    files = [HERE/'decoder.py', HERE/'gpu_perf.py', OUTPUT, *(HERE/'frozen').rglob('*.py')]
    source = {str(p):sha(p) for p in files}
    python = P/'work/experiments/night-20261010/cloud/tmp2/runtime/bin/python'
    task = dict(argv=['env','NVIDIA_TF32_OVERRIDE=0','CUDA_VISIBLE_DEVICES=0',
                      'OMP_NUM_THREADS=2','PYTHONDONTWRITEBYTECODE=1', str(python), '-B',
                      str(HERE/'gpu_perf.py'), '--model',
                      str(P/'work/experiments/base-format-20261010/runs/production/final'),
                      '--device','cuda','--output',str(HERE/'gpu-proof.json')],
                cwd=str(P), timeout_seconds=1800, wait_for=[],
                scope='Bounded one-GPU frozen Base FP32 batched decoder audit; no optimizer or training',
                source_sha256=source)
    temporary = QUEUE.with_suffix('.new')
    temporary.write_text(json.dumps(task, indent=2)+'\n')
    os.replace(temporary, QUEUE)
    (HERE/'gpu-launch-receipt.json').write_text(json.dumps(dict(queue=str(QUEUE), task=task,
               cases=[{k:v for k,v in c.items() if k!='calls'} for c in cases]), indent=2)+'\n')
    print(json.dumps(dict(queued=str(QUEUE), case_count=len(cases), source_file_count=len(source))))


if __name__=='__main__':
    main()
