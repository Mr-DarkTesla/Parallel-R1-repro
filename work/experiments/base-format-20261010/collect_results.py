"""Read immutable completed runs; write a separate verification report."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import math
import re

P = Path.cwd()
W = P / 'work/experiments'
B = W / 'base-format-20261010'
ARMS = {
    'original_instruct_native': 'instruct-token-warmup-20261010/evaluations/original-native-128',
    'base_full_sft_no_think': 'base-format-20261010/evaluations/base-no-think-unconstrained-128',
    'weighted_instruct_guard': 'format-loss-20261010/evaluations/weighted-format-constrained-128',
    'weighted_instruct_fewshot_guard': 'format-loss-20261010/evaluations/weighted-format-fewshot-128',
    'original_instruct_hf_diagnostic': 'format-diagnosis-20261010/evaluations/original-instruct-thinking-hf-128',
    'old_sft_instruct_guard': 'format-loss-20261010/evaluations/baseline-lr-5e-4-constrained-128',
}

def read(p):
    return json.loads(p.read_text())

def rows(p):
    return [json.loads(line) for line in p.open()]

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

all_scores = {}
report = dict(verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              original_baseline_unchanged=True, runs={}, source_sha256={},
              comparison_limit='Same fixed questions/scorer; model family, prompt and runtime differ. Accuracy delta is a target comparison, not a causal estimate of SFT degradation.',
              curriculum_selection_allowed=False, checkpoint_selection_allowed=False)
for name, rel in ARMS.items():
    root = W / rel
    summary = read(root / 'summary.json')
    scored = rows(root / 'scores.jsonl')
    assert summary['planned'] == summary['completed'] == len(scored) == 128
    assert read(root / 'worker-exits.json') == [0] * 8
    assert sum(bool(r['grade']['correct']) for r in scored) == summary['correct']
    assert len({r['id'] for r in scored}) == 128
    all_scores[name] = {r['id']:r for r in scored}
    widths = []
    for r in scored:
        current = 0
        groups = []
        for call in r.get('trace', {}).get('policy_calls', []):
            if call.get('phase') == 'path':
                current += 1
            elif current:
                groups.append(current)
                current = 0
        if current:
            groups.append(current)
        assert len(groups) == int(r.get('stats', {}).get('forks', 0))
        widths.extend(groups)
    fork_tasks = sum(r.get('stats', {}).get('forks', 0) > 0 for r in scored)
    assert fork_tasks == summary['executed_fork_samples']
    run = dict(accuracy_count=summary['correct'], accuracy=summary['correct']/128,
               basic_valid=summary['format_valid'], parallel_valid=summary['parallel_protocol_valid'],
               correct_and_parallel_valid=summary['correct_and_parallel_valid'],
               fork_tasks=fork_tasks, fork_task_fraction=fork_tasks/128,
               actual_rounds=len(widths), mean_rounds_per_task=len(widths)/128,
               actual_mean_width=sum(widths)/len(widths) if widths else None,
               actual_width_histogram=dict(sorted(collections.Counter(widths).items())),
               by_dataset={d:dict(n=v['completed'],correct=v['correct'],parallel_valid=v['parallel_valid'])
                           for d,v in summary['by_dataset'].items()},
               format_schema_version=summary['format_schema_version'],
               model=summary['model'], summary_path=str(root / 'summary.json'))
    report['runs'][name] = run
    for file in ['summary.json', 'scores.jsonl', 'worker-exits.json', 'manifest.json']:
        p = root / file
        report['source_sha256'][str(p.relative_to(P))] = sha(p)

baseline = all_scores['original_instruct_native']
assert sum(r['grade']['correct'] for r in baseline.values()) == 98
for name, scored in all_scores.items():
    assert scored.keys() == baseline.keys()
    assert all(r['problem'] == baseline[key]['problem'] and r['answer'] == baseline[key]['answer'] for key,r in scored.items())
    report['runs'][name]['delta_vs_fixed_original_baseline_pp'] = (report['runs'][name]['accuracy_count'] - 98) / 128 * 100

base = all_scores['base_full_sft_no_think']
report['paired_outcomes'] = dict(
    baseline_only_correct=sum(baseline[key]['grade']['correct'] and not r['grade']['correct'] for key,r in base.items()),
    base_only_correct=sum(not baseline[key]['grade']['correct'] and r['grade']['correct'] for key,r in base.items()),
    both_correct=sum(baseline[key]['grade']['correct'] and r['grade']['correct'] for key,r in base.items()),
    both_wrong=sum(not baseline[key]['grade']['correct'] and not r['grade']['correct'] for key,r in base.items()))
assert all(r['trace'].get('forced_think_prefix_tokens', 0) == 0 for r in base.values())
openings = sum(c.get('generated_ids', []).count(151671)
               for r in base.values() for c in r['trace']['policy_calls'] if c.get('phase') == 'main')
assert openings >= report['runs']['base_full_sft_no_think']['actual_rounds']
report['autonomy_proof'] = dict(forced_think_prefix_tokens=0,
    sampled_parallel_openers=openings, constrained_decoding=False,
    runtime_forced='Path IDs/headers and synchronization bridges; Plan, Parallel opener and width sampled')
m = rows(B / 'runs/production/metrics.jsonl')
assert len(m) == 126 and [r['step'] for r in m] == list(range(1, 127))
assert all(all(math.isfinite(r[k]) for k in ['loss','grad_norm','transformer_update_l2']) for r in m)
report['training'] = dict(**read(B / 'runs/production/result.json'),
    finite_optimizer_steps=126, sampled_backbone_positive_updates=sum(r['transformer_update_l2']>0 for r in m),
    initial_zero_update='First optimizer step has zero LR during warmup',
    validation_losses=[float(x) for x in re.findall(r'val/loss:([0-9.]+)', (B / 'logs/production.log').read_text())])
report['trace_observations'] = [
    dict(id='math_train/prealgebra/566',finding='Both paths compute correct GCD/factorizations; Summary incorrectly evaluates 8*9*37 as 2952 instead of 2664.'),
    dict(id='math_train/algebra/1558',finding='Plan asks for endpoint sum rather than decline; 450000+500 replaces required 450000-500.'),
    dict(id='gsm_infinite_ops4/ops4/510',finding='Path correctly computes 5-3=2, labels it non-owl; Summary subtracts 3 again and answers -1.'),
    dict(id='math_train/algebra/786',finding='Plan creates a trivial zero branch; another branch reverses the wrong interval endpoints under negation.'),
]
for item in report['trace_observations']:
    assert not base[item['id']]['grade']['correct']
    item['format_valid'] = base[item['id']]['format_valid']
    item['parallel_valid'] = base[item['id']]['parallel_protocol_valid']
    item['reference_answer'] = base[item['id']]['answer']
    item['extracted_answer'] = base[item['id']]['grade']['answer']
report['objective_assessment'] = dict(autonomous_format_learned=True,
    accuracy_retention_met=False, note='Base fork coverage 93.75%, but 84/128 vs original Instruct98/128; syntax validity does not prove useful independent computations.')
out = B / 'final-report.json'
assert not out.exists(), 'Preserve previous verification report'
out.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
print('FINAL_REPORT',out,'SHA256',sha(out))
print(json.dumps(dict(base=report['runs']['base_full_sft_no_think'],training=report['training'],paired=report['paired_outcomes']),ensure_ascii=False))
