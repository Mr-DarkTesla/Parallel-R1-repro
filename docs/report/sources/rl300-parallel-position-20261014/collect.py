"""Read-only extraction from saved updates 1-300; stdout is compact JSON."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json

ROOT = Path('${PROJECT_ROOT}/work/experiments')
RUNS = {
    'steps1_50': ROOT / 'rl-r2-24gpu-20261012/recovery-20261012-global-parity/production',
    'steps51_300': ROOT / 'rl-vllm-32gpu-batch64-20261012/repair-01-refresh-memory/production',
}
result = dict(collected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              formula='zero-based <Parallel> token index / len(response_ids), excluding prompt',
              averaging='pool all blocks in a committed update; no correctness/format filter; absent blocks excluded',
              paper='https://arxiv.org/html/2509.07980#S4.SS4', runs={})
for name, root in RUNS.items():
    metric_bytes = (root / 'metrics.jsonl').read_bytes()
    commits = {d['step']: d for d in map(json.loads, metric_bytes.splitlines()) if (1 <= d['step'] <= 50 if name == 'steps1_50' else 51 <= d['step'] <= 300)}
    rows, sources = [], []
    records = {s: [] for s in commits}
    for file in sorted(root.glob('traces-rank-*.jsonl')):
        digest = hashlib.sha256()
        with file.open('rb') as inp:
            for line in inp:
                digest.update(line)
                if not line.endswith(b'\n'):
                    continue
                d = json.loads(line)
                if d['step'] not in commits:
                    continue
                ids = d['response_ids']
                tag = d['policy_calls'][0]['structure_tags'][0]
                indices = [i for i, token in enumerate(ids) if token == tag]
                records[d['step']].append(dict(
                    rank=d['rank'], prompt=d.get('prompt_index', d['id']), sample=d['sample'],
                    n_tokens=len(ids), starts=indices,
                    positions=[i / len(ids) for i in indices],
                    completed_forks=d['stats']['forks'],
                    truncated=d['stats']['truncated'],
                    format_valid=d['format_valid'],
                ))
        sources.append(dict(path=str(file), sha256=digest.hexdigest()))
    for step, responses in sorted(records.items()):
        ranks = commits[step]['ranks']
        expected = sum(r['group'] for r in ranks)
        assert len(responses) == expected == (96 if name == 'steps1_50' else 64), (name, step, len(responses), expected)
        assert len({(r['rank'], r['prompt'], r['sample']) for r in responses}) == expected
        assert Counter(r['rank'] for r in responses) == Counter({r['rank']: r['group'] for r in ranks})
        positions = [p for r in responses for p in r['positions']]
        first = [r['positions'][0] for r in responses if r['positions']]
        row = dict(step=step, phase_iteration=step, responses=expected,
                   blocks=len(positions), responses_with_parallel=len(first),
                   mean_relative_position=sum(positions)/len(positions) if positions else None,
                   mean_first_relative_position=sum(first)/len(first) if first else None,
                   mean_start_token=sum(i for r in responses for i in r['starts'])/len(positions) if positions else None,
                   truncated_responses=sum(r['truncated'] for r in responses),
                   invalid_format_responses=sum(not r['format_valid'] for r in responses),
                   optimizer_step=all(r['optimizer_step'] for r in ranks),
                   positive_update=all(r['backbone_update_l2'] > 0 for r in ranks))
        assert all(0 <= p < 1 for p in positions)
        rows.append(row)
    config = json.loads((root / 'config.json').read_text())
    result['runs'][name] = dict(root=str(root),
        config={k: config.get(k) for k in ['initial_step','steps','response_budget','path_budget','reward_mode','initial_checkpoint','model','optimizer_reset']},
        metric_sha256=hashlib.sha256(metric_bytes).hexdigest(), sources=sources,
        rows=rows, responses=records)
assert set(s for v in result['runs'].values() for s in v['responses']) == set(range(1,301))
print('RL300_POSITION_JSON_BEGIN')
print(json.dumps(result, ensure_ascii=False))
