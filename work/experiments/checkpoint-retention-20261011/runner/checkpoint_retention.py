"""Retention for newly managed checkpoints; legacy proof artifacts are untouched.

Consumers must call pin() before publishing a queue entry, and release() only
after every reader has finished. The registry lock serializes pins and cleanup.
"""
import contextlib
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import time


def atomic_json(path, value):
    path = Path(path)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    os.replace(temporary, path)


@contextlib.contextmanager
def registry(output):
    output = Path(output).resolve()
    with (output / 'artifact-leases.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        path = output / 'artifact-leases.json'
        data = json.loads(path.read_text()) if path.exists() else {'leases': {}}
        if not isinstance(data.get('leases'), dict):
            raise ValueError('Invalid artifact lease registry; cleanup refused')
        yield output, path, data


def pin(output, step, consumer):
    if not consumer or int(step) < 0:
        raise ValueError('A step and named consumer are required')
    with registry(output) as (_, path, data):
        data['leases'].setdefault(str(int(step)), {})[consumer] = {'state': 'active', 'created': time.time()}
        atomic_json(path, data)


def release(output, step, consumer):
    with registry(output) as (_, path, data):
        lease = data['leases'][str(int(step))][consumer]
        lease.update(state='completed', completed=time.time())
        atomic_json(path, data)


def should_save(step, total_steps, config):
    anchors = {int(s) for s in config.get('keep_steps', [32, 128, 256, 500])}
    every = int(config.get('resume_checkpoint_every', 16))
    if every < 1 or int(config.get('keep_count', 1)) < 1:
        raise ValueError('Resume interval and keep_count must be positive')
    return step == total_steps or step in anchors or step % every == 0


def prune(output, keep_steps=(32, 128, 256, 500), keep_count=1):
    """Keep pinned anchors and newest complete resumes; preserve all metadata."""
    if int(keep_count) < 1:
        raise ValueError('At least one rolling resume checkpoint is required')
    removed = []
    with registry(output) as (root, _, data):
        active = set()
        for step, leases in data['leases'].items():
            if not isinstance(leases, dict):
                raise ValueError('Invalid leases; cleanup refused')
            for lease in leases.values():
                if lease.get('state') not in ('active', 'completed'):
                    raise ValueError('Unknown lease state; cleanup refused')
                if lease['state'] == 'active':
                    active.add(int(step))
        complete = []
        for path in root.glob('checkpoint-*'):
            match = re.fullmatch(r'checkpoint-(\d+)', path.name)
            if not match or path.is_symlink() or not (path / 'complete.json').is_file():
                continue
            info = json.loads((path / 'complete.json').read_text())
            step = int(match[1])
            # Only this runner's artifacts are eligible, never legacy proofs.
            if not info.get('retention_managed'):
                continue
            world = int(info.get('world_size', 0))
            valid = info.get('step') == step and world > 0 and all(info.get(k) is True for k in ('model', 'optimizer', 'rng'))
            valid = valid and (path / 'hf' / 'config.json').is_file()
            valid = valid and any((path / 'hf').glob('*.safetensors'))
            valid = valid and all((path / f'rng-{rank}.pt').is_file() for rank in range(world))
            valid = valid and ((path / 'optimizer.pt').is_file() or all((path / f'optimizer-rank-{rank}.pt').is_file() for rank in range(world)))
            if valid:
                complete.append((step, path))
        complete.sort()
        protected = set(map(int, keep_steps)) | active | {s for s, _ in complete[-int(keep_count):]}
        history = root / 'checkpoint-history'
        for step, path in complete:
            if step in protected:
                continue
            # Refuse linked trees rather than following files outside this run.
            if any(p.is_symlink() for p in path.rglob('*')):
                continue
            metadata = {str(p.relative_to(path)): p.read_text() for p in path.rglob('*') if p.is_file() and p.suffix in ('.json', '.txt')}
            files = [p.stat() for p in path.rglob('*') if p.is_file()]
            event = dict(step=step, path=str(path), reason='obsolete managed resume; no active leases',
                         logical_bytes=sum(s.st_size for s in files),
                         exclusively_linked_allocated_bytes=sum(s.st_blocks * 512 for s in files if s.st_nlink == 1),
                         metadata=metadata, deleted_at=time.time())
            history.mkdir(exist_ok=True)
            atomic_json(history / f'{path.name}.json', event)
            shutil.rmtree(path)
            removed.append(event)
    return removed
