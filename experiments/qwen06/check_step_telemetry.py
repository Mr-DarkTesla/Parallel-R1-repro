"""Check real rollout telemetry and phase coverage without touching training."""
import argparse
import json
from collections import defaultdict
from pathlib import Path
from analyze import runtime_segments

parser = argparse.ArgumentParser()
parser.add_argument('run', type=Path)
parser.add_argument('--step', type=int, required=True)
args = parser.parse_args()
token_ids = json.loads((args.run / 'checkpoint.json').read_text())['special_tokens']
counts = defaultdict(int)
for file in (args.run / 'telemetry').glob('forwards-*.jsonl'):
    for line in file.read_text().splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue  # A currently appended last record is not part of the snapshot.
        counts[row['request_id']] += row['forward_passes']
report = dict(step=args.step, samples=0, executed_forks=0, retained_tokens=0,
              request_forward_participations=0, missing_forward_calls=0,
              segment_coverage_errors=0, phase_tokens=defaultdict(int))
for file in (args.run / 'telemetry').glob('traces-*.jsonl'):
    for line in file.read_text().splitlines():
        try:
            trace = json.loads(line)
        except ValueError:
            continue
        if trace['trajectory']['step'] != args.step or trace['trajectory'].get('validate'):
            continue
        report['samples'] += 1
        report['executed_forks'] += trace['executed_fork_count']
        report['retained_tokens'] += trace['response_tokens']
        cursor = 0
        for part in runtime_segments(trace, token_ids):
            report['segment_coverage_errors'] += int(part['start'] != cursor)
            report['phase_tokens'][part['phase']] += part['tokens']
            cursor = part['end']
        report['segment_coverage_errors'] += int(cursor != trace['response_tokens'])
        for call in trace['calls']:
            keys = [key for key in counts if key == call['request_id'] or key.startswith(call['request_id'] + '-')]
            report['missing_forward_calls'] += int(not keys)
            report['request_forward_participations'] += sum(counts[key] for key in keys)
print(json.dumps(report, indent=2))
if report['segment_coverage_errors'] or report['missing_forward_calls']:
    raise SystemExit(1)
