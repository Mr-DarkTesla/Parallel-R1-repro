"""Render fresh forced-think metrics; never reuse old trace reviews."""
from pathlib import Path
import json,datetime as dt
from zoneinfo import ZoneInfo
W=Path(__file__).resolve().parent
s=json.loads((W/'summary.json').read_text())
previous=json.loads((W/'previous-comparison.json').read_text())
m=json.loads((W/'manifest.json').read_text())
review=json.loads((W/'trace-review.json').read_text()) if (W/'trace-review.json').exists() else {'reviewed':[]}
def pct(x):return f'{100*x:.1f}%' if x is not None else 'n/a'
def p(k):return f'{k}/{s["questions"]} ({100*k/s["questions"]:.1f}%)'
def ci(v):return f'{100*v[0]:.1f}–{100*v[1]:.1f}%' if v else 'n/a'
lines=['# Counted Unseen SFT: MATH-500 with automatic initial think', '',
 f'State: **{s["state"]}**, {s["questions"]}/500 answers. Generated '+dt.datetime.now(ZoneInfo('Europe/Moscow')).isoformat()+'.','',
 f'Checkpoint: {m["checkpoint"]}.','',
 'This fresh evaluation automatically inserts <think> and newline before the first sampled response token. The inserted prefix is exogenous, has action mask zero, counts toward the response budget, and enters every continuation context. The model still generates closing think and the final answer. No outputs from the previous partial evaluation are included.','',
 'One sample per question; temperature0.6, top-p0.95, top-k20, seed42. Response budget30720, path budget8192, context32768. Model-selected widths2..8 and no fixed round cap.','',
 '## Accuracy', '', f'Primary answer pass@1: **{p(s["final_answer_only_diagnostic"]["correct"])}**, Wilson95%CI {ci(s["final_answer_only_diagnostic"]["ci95"])}. Think-format compliance is measured separately. The historical extraction count is retained for compatibility.','',
 '| Run | Previous reference-blind metric | Answer pass@1 (think-independent) |','|---|---:|---:|']
for name,v in previous.items():
 lines.append(f'| {name} | {v["historical_correct"]}/500 ({pct(v["historical_pass_at_1"])}) | {v["final_answer_only_correct"]}/500 ({pct(v["final_answer_only_pass_at_1"])}) |')
f=s['final_answer_only_diagnostic']
lines.append(f'| New SFT with forced initial think, {s["questions"]} answers | {s["correct"]}/{s["questions"]} ({pct(s["pass_at_1"])}) | {f["correct"]}/{s["questions"]} ({pct(f["pass_at_1"])}) |')
lines += ['',f'Historical extraction Wilson95% interval: {ci(s["ci95"])}. Answer pass@1 interval: {ci(f["ci95"])}. Scorer errors: {len(s["scorer_errors"])}.','',
 'Historical extraction and Math-Verify0.8.0 are unchanged from previous runs. Its inherited think handling rejects opening think without any closing, but can accept a later opening after an earlier closing. Answer pass@1 removes think tags before the same reference-blind extraction; it does not establish valid reasoning or format. Previous saved rescores reproduce84/79/61correct under both methods.','',
 'This is an end-to-end comparison: model/data, system prompt, genuine Unseen masks/positions, model-selected width, numerical backend and now forced initial think differ from historical runs. It does not isolate an SFT data effect.','',
 '## Runtime and format','',
 f'Parallel questions: {s["parallel_questions"]}; multi-round questions: {s["multi_round_questions"]}. Fork distribution: {s["forks"]}. Widths: {s["widths"]}.',
 f'Invalid width: {s["invalid_width_questions"]}; invalid assembled parallel structure: {s["format_invalid_questions"]}. Budget exhausted: {s["budget_exhausted_questions"]}.',
 f'Think structure: {s["think_structure"]}. Tag counts: {s["think_markup"]}.',
 f'Final-answer format: {s.get("answer_format",{})}.',
 f'Runtime closing-label replacements: {s["runtime_closure_label_replacements"]}. Accounting/context audit: {s["context_audit"]}.','',
 'The opening think, numbered path prefixes and some structural closures are runtime injected. Assembled-format compliance is therefore distinct from raw sampled-format compliance. Original sampled labels and masks remain in traces.','',
 '| Metric | Mean | Median | p90 | Max |','|---|---:|---:|---:|---:|']
for name in ['response_tokens','sampled_tokens','forced_tokens','critical_depth','sampled_work_over_critical_depth','elapsed_seconds_per_question','generation_calls']:
 v=s[name]
 if v.get('n'):lines.append(f'| {name} | {v["mean"]:.2f} | {v["median"]:.2f} | {v["p90"]:.2f} | {v["max"]:.2f} |')
lines += ['','Paths execute sequentially within each GPU worker; eight workers handle different questions. Work/depth is a theoretical sampled-token ratio, not measured wall-clock speedup.','',
 '## SFT dataset quality','',
 'Full audit: ../data-quality-audit/report.txt and report.json. All5145 examples have canonical think/Plan/counted paths/boxed final structure and all gold answers match. This does not prove useful scheduling or global consistency of the source problem.',
 'Old2145:3852/11970 paths contain no detected numeric operation; new3000:0/11475. These are syntactic heuristics, not semantic error rates. Manual32purposefully selected cases found given/alias-only and unused old branches plus negative-count contexts in both sources.35concrete findings for23rows are preserved in high-confidence-issues.jsonl.',
 'Independent random manual cross-check (seed20261009,15old+15new, no overlap with purposeful32; see ../data-quality-audit/random-review/report.txt) found given/alias-only paths in14/15old versus0/15new. Three new examples use weak same-chain verification and one nests prefix computations. The sample is small and source identity was visible; selection and judgment did not use heuristic flags.',
 'This random review also confirmed four additional new source contradictions: elephant count<=-14, cartoon count<=-4, tiger count=-24, nomination average<=-22. Exact original constraints and arithmetic witnesses are preserved; this was incidental detection, not exhaustive consistency validation.',
 'The full conservative source-condition scan found negative-count/average witnesses in667/3000new(22.23%) and332/2145old(15.48%), under ordinary ordered arithmetic and nonnegative quantity domains. All1483serialized premise subsets replay;10random proofs were independently manually confirmed. This is a lower bound, not a teacher-answer error rate; remaining rows are unresolved. Official generation has optional modulo, so intended arithmetic must be fixed before filtering. See ../data-quality-audit/final-report.txt and local-context-validator/report.txt.',
 'Arithmetic provenance recovered all5145original target solutions:19513recognized numeric equalities match ordinary arithmetic and no explicit modulo instructions were found. None of the1483negative quantities exactly matches a Define-quantity in those target chains; this is text matching, not a full dependency graph proof. Thus source contradictions do not establish999bad teacher solutions or justify blind deletion. For the next controlled baseline, omit old2145 and assess new target-chain quality; preserve the possibility of repairing irrelevant context instead of deleting whole tasks. All current width7/8 examples are old, so useful coverage needs replacement. No causal effect on MATH accuracy has been established.', '',
 '## Fresh semantic review','']
if review['reviewed']:
 lines.append('Deliberately selected diagnostic cases; this is not a random quality-rate estimate.')
 for note in review['reviewed']:lines.append(f'- Question index {note["index"]}, **{note["assessment"]}**: {note["note"]}')
else:lines.append('A semantic review of this fresh run has not yet been performed. Reviews from the prior partial run are not reused.')
lines += ['','## Artifacts','',
 '- manifest.json: exact protocol, immutable checkpoint and question hashes.',
 '- traces-0.jsonl through traces-7.jsonl: only this fresh run.',
 '- scores.jsonl, trace-statistics.jsonl, summary.json: reference-blind grades and runtime statistics.',
 '- previous-comparison.json and previous-*-scores.jsonl: copied read-only historical rescores.',
 '- preflight.json: CPU import, forced-prefix and sampling-guard checks.','',
 'CPU finalization from project root:','',
 '    .venv/bin/python '+str(W.relative_to(W.parents[3]))+'/score.py --final',
 '    .venv/bin/python '+str(W.relative_to(W.parents[3]))+'/report.py','']
(W/'REPORT.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'state':s['state'],'questions':s['questions'],'primary_pass_at_1':f['pass_at_1'],'report':str(W/'REPORT.md')}))
