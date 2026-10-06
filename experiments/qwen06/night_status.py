"""Read-only, bounded status inspection for the overnight queue."""
import json
import os
from pathlib import Path

root = Path(os.getenv('PARALLEL_R1_ROOT', str(Path.home() / 'parallel-r1')))
state = root / 'runs/night'
mode = (state / 'current_mode').read_text().strip() if (state / 'current_mode').exists() else None
report = dict(current_mode=mode, completed=[m for m in ('s1', 's2') if (state / f'{m}.done').exists()])
if mode in ('s1', 's2'):
    run = root / f'runs/qwen06-{mode}-seed1'
    tracker = run / 'checkpoints/latest_checkpointed_iteration.txt'
    report['last_saved_step'] = int(tracker.read_text()) if tracker.exists() else 0
    report['telemetry_bytes'] = {p.name: p.stat().st_size for p in (run / 'telemetry').glob('*.jsonl')}
    log = run / 'train.log'
    if log.exists():
        with log.open('rb') as stream:
            stream.seek(max(0, log.stat().st_size - 131072))
            lines = stream.read().decode('utf-8', errors='replace').splitlines()
        metric_lines = [line for line in lines if 'training/global_step:' in line]
        report['last_training_metrics'] = metric_lines[-1:] or []
        report['recent_log'] = lines[-5:]
    for kind in ('traces', 'forwards', 'events'):
        files = sorted((run / 'telemetry').glob(kind + '-*.jsonl'), key=lambda p: p.stat().st_mtime)
        if files:
            with files[-1].open('rb') as stream:
                stream.seek(max(0, files[-1].stat().st_size - 524288))
                lines = stream.read().splitlines()
            for line in reversed(lines):
                try:
                    row = json.loads(line)
                except (ValueError, UnicodeError):
                    continue
                if kind == 'traces':
                    report['trace_example'] = {key: row.get(key) for key in ('trajectory', 'prompt_tokens', 'response_tokens', 'executed_fork_count', 'truncated', 'generated_tokens_total')}
                    report['trace_example']['call_lengths'] = [{key: c[key] for key in ('phase', 'prompt_tokens', 'generated_tokens')} for c in row['calls']]
                    report['trace_example']['path_masks_present'] = bool(row.get('path_masks'))
                else:
                    report[kind + '_example'] = row
                break
print(json.dumps(report, indent=2, ensure_ascii=False))
