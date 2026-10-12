import hashlib
import json
from pathlib import Path
import time

R = Path.cwd()
B = R / 'work/experiments/rl-instruct-20261011/eval24-joint'
def read(p):
    return json.loads(Path(p).read_text())
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
while not all((B / lane / 'result.json').exists() for lane in ['main', 'tmp2', 'tmp3']):
    if any((B / lane / 'status.json').exists() and read(B / lane / 'status.json')['state'] == 'failed' for lane in ['main', 'tmp2', 'tmp3']):
        raise RuntimeError('Lane failure; no complete benchmark result')
    time.sleep(15)
lanes = [read(B / lane / 'result.json') for lane in ['main', 'tmp2', 'tmp3']]
assert all(x['passed'] and x['exit_codes'] == [0] * 8 for x in lanes)
assert all(x['protocol'] == lanes[0]['protocol'] and x['model_manifest'] == lanes[0]['model_manifest'] and x['source_manifest'] == lanes[0]['source_manifest'] for x in lanes)
paths = {p: h for x in lanes for p, h in x['traces'].items()}
assert len(paths) == 24 and all(sha(p) == h for p, h in paths.items())
rows = [json.loads(l) for p in paths for l in Path(p).read_text().splitlines()]
assert len(rows) == 500 and {r['index'] for r in rows} == set(range(500)) and len({r['id'] for r in rows}) == 500
plan = read(B / 'main/plan.json')
questions = [json.loads(l) for l in Path(plan['questions']).read_text().splitlines()]
assert all(r['id'] == questions[r['index']]['id'] and not r['grade'].get('error') for r in rows)
baseline_dir = R / 'work/experiments/rl-instruct-20261011/math500-fullwidth8'
audit = read(baseline_dir / 'baseline-native500-audit.json')
assert audit['passed'] and audit['completed'] == 500 and audit['technical_unknowns'] == 0 and audit['all8worker_exit_zero']
assert audit['protocol'] == lanes[0]['protocol']
basefiles = sorted((baseline_dir / 'runs/001-fullSFT-baseline').glob('rank-*.jsonl'))
assert len(basefiles) == 8 and all(sha(p) == audit['trace_sha256'][p.name] for p in basefiles)
base = {r['id']: r for p in basefiles for r in [json.loads(l) for l in p.read_text().splitlines()]}
assert len(base) == 500 and all(base[r['id']]['index'] == r['index'] for r in rows)
correct = [bool(r['grade']['correct']) for r in rows]
widths = [w for r in rows for w in r['widths']]
improved = sum(c and not base[r['id']]['grade']['correct'] for r, c in zip(rows, correct))
regressed = sum(not c and base[r['id']]['grade']['correct'] for r, c in zip(rows, correct))
result = dict(passed=True, checkpoint=32, arm='R2', completed=500, missing=0, technical_unknowns=0, correct=sum(correct), accuracy=sum(correct)/500, format_valid=sum(r['format_valid'] for r in rows), parallel_valid=sum(r['parallel_valid'] for r in rows), correct_parallel=sum(c and r['parallel_valid'] for r,c in zip(rows,correct)), fork_samples=sum(r['stats']['forks']>0 for r in rows), rounds=sum(r['stats']['forks'] for r in rows), mean_width=sum(widths)/len(widths) if widths else None, mean_actual_F=sum(r['instrumented_forward_calls'] for r in rows)/500, mean_sampled_T=sum(r['stats']['sampled_tokens'] for r in rows)/500, paired=dict(improved=improved, regressed=regressed, accuracy_difference=(improved-regressed)/500), protocol=lanes[0]['protocol'], traces=paths, model_manifest=lanes[0]['model_manifest'], selection_allowed=False)
tmp=B/'result.tmp';tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(B/'result.json')
