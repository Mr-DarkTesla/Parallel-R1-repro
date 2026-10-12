"""fast_repair.py on CPU: Codex rule copies, triage on the real pool (when reachable), merger and branch repair round
trips through a fake LLM backend, assembly/validation/byte identity, resume, and selection with repaired rows.

cd experiments/thinking_sft_v4 && python3 -m pytest -q tests/test_fast_repair.py
"""
import ast
import hashlib
import json
import os
import sys
import types
from collections import Counter
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import codex_rules as C  # noqa: E402
import fast_repair as F  # noqa: E402
import select_records  # noqa: E402
import sft_data as D  # noqa: E402
from tiny import build_tiny_tokenizer  # noqa: E402

POOL = Path(os.environ.get('FAST_REPAIR_POOL', '/mnt/project-files/thinking-sft-4b/pool-20261012'))
CODEX = Path(os.environ.get('CODEX_CODE_DIR', POOL / 'codex-code'))
REAL = (POOL / 'all.raw.jsonl').exists() and (POOL / 'details.jsonl').exists()
BOX = '\n\nPlease reason step by step, and put your final answer within \\boxed{}.'
FILL = ' I check each quantity carefully and write every step out in full so that nothing is skipped here.' * 3


@pytest.fixture(autouse=True)
def fake_math_verify(monkeypatch):
    """gen.grade imports math_verify (not installed on CPU); exec/gsm are decided by the Decimal check anyway."""
    module = types.ModuleType('math_verify')
    module.parse = lambda text: text.replace('\\boxed{', '').rstrip('}').strip()
    module.verify = lambda a, b: a == b
    monkeypatch.setitem(sys.modules, 'math_verify', module)


# ------------------------------------------------------------------------------------------- Codex copies

COPIED = {
    'countdown_directions.py': ['parse_direction', 'has_literal_pair', 'attainable', 'direction_has_solution'],
    'quality_checks.py': ['meaningful_result', 'expression_key'],
    'gen.py': ['STUDENT_SAMPLING', 'seed_of', 'last_boxed', 'gold_answer', 'final_boxed_answer', 'grade',
               'norm_math', 'NUMBER', 'numbers_in', 'contains_answer', 'answer_in_question', 'patch_sampler',
               'split_think', 'RESULT', 'component_for', 'last_number', 'countdown_expr', 'countdown_branch',
               'check_branch', 'executor_prompt_d', 'executor_prompt_e', 'merger_prompt', 'seg', 'parallel_segments'],
    'raw_acquisition.py': ['RESERVE', 'ntok', 'overhead'],
    'audit_repair.py': ['MERGE_NOTE', 'numeric', 'final_grade', 'repair_merger_prompt'],
}


def top_level(source):
    out = {}
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[node.name] = ast.dump(node)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                for name in ([target] if isinstance(target, ast.Name) else getattr(target, 'elts', [])):
                    out[name.id] = ast.dump(node)
    return out


@pytest.mark.skipif(not CODEX.exists(), reason='codex-code folder not reachable')
def test_codex_copies_verbatim():
    mine = top_level(Path(C.__file__).read_text())
    for name, names in COPIED.items():
        theirs = top_level((CODEX / name).read_text())
        for item in names:
            assert mine[item] == theirs[item], f'{item} differs from codex-code/{name}'
    literals = {node.value for node in ast.walk(ast.parse((CODEX / 'raw_acquisition.py').read_text()))
                if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    assert C.COUNTDOWN_BRANCH_SUFFIX in literals  # the string raw_work appends to Countdown branch requests


def test_countdown_verify_reasons():
    assert C.countdown_verify('3*4+5', [3, 4, 5], 17) == dict(correct=True, reason='correct')
    assert C.countdown_verify('3*4+5', [3, 4, 4], 17)['reason'] == 'wrong_multiset'
    assert C.countdown_verify('3*4-5', [3, 4, 5], 17)['reason'] == 'wrong_value'
    assert C.countdown_verify('3/4+5', [3, 4, 5], 17)['reason'] == 'invalid_characters'
    assert C.countdown_verify('3*(4+', [3, 4], 17)['reason'] == 'invalid_grammar'


# --------------------------------------------------------------------------------------- real pool checks

@pytest.fixture(scope='module')
def real_plan():
    cfg = dict(F.DEFAULTS)
    return F.plan_records(POOL / 'all.raw.jsonl', POOL / 'details.jsonl', cfg)


@pytest.mark.skipif(not REAL, reason='pool-20261012 not reachable')
def test_real_triage_counts(real_plan):
    jobs, stats, _ = real_plan
    assert all(check['match'] for check in stats['triage_check'].values()), stats['triage_check']
    assert sum(stats['triage'].values()) == 5000
    assert stats['buckets'] == {F.EXEC: 605, F.TRUNC: 416, F.LONG: 614}
    assert stats['long_summary_par_clean']['gsm/>ratio'] == 359 and stats['long_summary_par_clean']['math/>ratio'] == 255
    # no raw run requests file here: every truncated record is skipped and counted
    assert stats['skipped'][F.TRUNC] == {'branch_request_unavailable': 413, 'plan_status_gold_in_plan': 3}
    assert stats['jobs'] == {F.EXEC: 605, F.LONG: 609}


@pytest.mark.skipif(not REAL, reason='pool-20261012 not reachable')
def test_real_input_products_and_countdown_scorer(real_plan):
    _, _, entries = real_plan
    details = {d['id']: d for _, d in F.raw_lines(POOL / 'details.jsonl')}
    agree, n = Counter(), 0
    for _, row in entries:
        d = details[row['id']]
        if row['source'] == 'exec' and row['mode'] == 'parallel':
            parsed = F.parse_parallel(row)
            spec = F.workshop_spec(row['question'])
            assert F.count_input_products(parsed['summary'], spec) == d['exec_summary_input_products']
            assert F.count_input_products(parsed['answer'], spec) == d['exec_answer_input_products']
            n += 1
        if row['source'] == 'countdown':
            q = F.build_q(row, d)
            after = ''.join(s['text'] for s in row['segments']).split('</think>', 1)
            ok, _ = C.grade(q['task'], q['gold'], after[1][:-len('<|im_end|>')] if len(after) == 2 else None)
            agree[ok == row['provenance']['correct']] += 1
    assert n == 1329 and agree == Counter({True: 1015})


@pytest.mark.skipif(not REAL, reason='pool-20261012 not reachable')
def test_real_recheck_of_kept_branches_matches_raw(real_plan):
    _, _, entries = real_plan
    details = {d['id']: d for _, d in F.raw_lines(POOL / 'details.jsonl')}
    seen = Counter()
    for _, row in entries:
        if row['mode'] != 'parallel' or row['provenance'].get('plan_status') != 'fork':
            continue
        try:
            parsed = F.parse_parallel(row)
        except ValueError:
            continue
        q = F.build_q(row, details[row['id']])
        for i, (body, check) in enumerate(zip(parsed['bodies'], row['provenance']['branch_checks'])):
            if check['ok']:
                again = F.recheck_kept_branch(q, parsed['plan'], i, body)
                seen[again == check] += 1
    assert seen[False] == 0 and seen[True] > 8000


# ------------------------------------------------------------------------------------------ fixtures

def workshop_question():
    rows = [(1, 10, 8, 5, 1, 2, 3), (2, 12, 10, 4, 2, 1, 5), (3, 20, 9, 6, 0, 1, 4)]
    text = ' '.join(f'Workshop {i} produces {p} units and initially sells {s} units for ${c} each. {r} of the sold '
                    f'units are returned for a full refund. Materials cost ${m} for EVERY produced unit, including '
                    f'unsold and returned units. Fixed expenses are ${f}. Unsold stock earns nothing.'
                    for i, p, s, c, r, m, f in rows)
    return text + ' What is the total net profit across the three workshops?'


def make_row(rid, source, question, prompt, prefix, kind, items, bodies, summary, answer, checks, n_tokens=900):
    plan = dict(kind=kind, items=items, branches=len(items),
                plan_text=kind + '\n' + ''.join(f'{i}: {x}\n' for i, x in enumerate(items, 1)))
    segs, _ = C.parallel_segments(prefix, plan, bodies, summary, answer)
    return dict(id=rid, source=source, mode='parallel', question=question, prompt=prompt, segments=segs,
                provenance=dict(task_id=rid.split('#')[0], n_tokens=n_tokens, raw_unreviewed=True,
                                model_finished=all(c[0] for c in checks), correct=True, grade='correct',
                                over_budget=False, branch_checks=[dict(ok=ok, reason=r) for ok, r in checks],
                                plan_status='fork'))


def detail_of(row, oracle, bad=(), products=(0, 0)):
    return dict(id=row['id'], source=row['source'], mode='parallel', correct=True, actual_finished=not bad,
                final_finish_reason='stop', branch_bad=list(bad), oracle=oracle,
                exec_summary_input_products=products[0], exec_answer_input_products=products[1])


def fixture_pool(tmp_path):
    q_exec = workshop_question()
    exec_bodies = [' Revenue is (8 - 1) times 5 = 35 and materials are 20, minus fixed 3.' + FILL + '\n\nResult: 12',
                   ' Revenue is (10 - 2) times 4 = 32, materials 12, fixed 5.' + FILL + '\n\nResult: 15',
                   ' Revenue is 9 times 6 = 54, materials 20, fixed 4.' + FILL + '\n\nResult: 30']
    exec_row = make_row('exec-x#raw', 'exec', q_exec, q_exec + BOX, 'Let me compute each workshop.\n\n', 'decompose',
                        [f'Compute the net profit for Workshop {i}.' for i in (1, 2, 3)], exec_bodies,
                        'Check: 7 * 5 = 35, 10 * 2 = 20, 8 * 4 = 32, 12 * 1 = 12, so 12 + 15 + 30 = 57.',
                        '\n\nWorkshop 1: 7 * 5 = 35 and 10 * 2 = 20. Total \\boxed{57}.',
                        [(True, 'ok_oracle_verified')] * 3)
    exec_failing = json.loads(json.dumps(exec_row))
    exec_failing['id'], exec_failing['provenance']['task_id'] = 'exec-y#raw', 'exec-y'
    q_gsm = 'Tom has 3 boxes with 4 apples each and 2 bags with 5 apples each. How many apples does he have?'
    gsm_bodies = [' Three boxes with four apples each give 3 times 4 = 12.' + FILL + '\n\nResult: 12',
                  ' Two bags hold five apples each, so I start with 2 times' + FILL]
    gsm_row = make_row('gsm-t#raw', 'gsm', q_gsm, q_gsm + BOX, 'He has boxes and bags.\n\n', 'decompose',
                       ['Compute the apples in the boxes.', 'Compute the apples in the bags.'], gsm_bodies,
                       'Boxes 12, bags 10, total 22.', '\n\n\\boxed{22}', [(True, 'ok'), (False, 'branch_truncated')])
    long_bodies = [' The boxes give 3 times 4 = 12 apples.' + FILL + '\n\nResult: 12',
                   ' The bags give 2 times 5 = 10 apples.' + FILL + '\n\nResult: 10']
    long_row = make_row('gsm-l#raw', 'gsm', q_gsm, q_gsm + BOX, 'He has boxes and bags.\n\n', 'decompose',
                        ['Compute the apples in the boxes.', 'Compute the apples in the bags.'], long_bodies,
                        'Let me redo everything. ' + 'Boxes: 3 * 4 = 12. Bags: 2 * 5 = 10. ' * 12 + 'Total 22.',
                        '\n\nThe answer is \\boxed{22}.', [(True, 'ok'), (True, 'ok')])
    q_cd = ('Find an arithmetic expression that equals 17, using these numbers: 3, 4, 5. Use every given number '
            'exactly once, including duplicates.')
    cd_bodies = [' Multiplying 3 and 4 gives 12 and adding 5 gives 17.' + FILL + '\n\nResult: 3*4+5',
                 ' Adding 4 and 5 gives 9, then with 3 I can try' + FILL]
    cd_row = make_row('countdown-c#raw', 'countdown', q_cd, q_cd, 'I need 17.\n\n', 'candidates',
                      ['Try multiplying 3 and 4 first, then combine with 5.',
                       'Try adding 4 and 5 first, then combine with 3.'], cd_bodies, 'Branch 1 found it.',
                      '\n\nFinal Answer: 3*4+5', [(True, 'ok_countdown_valid'), (False, 'branch_truncated')])
    clean_row = make_row('gsm-c#raw', 'gsm', q_gsm, q_gsm + BOX, 'He has boxes and bags.\n\n', 'decompose',
                         ['Compute the apples in the boxes.', 'Compute the apples in the bags.'], long_bodies,
                         'Results 12 and 10 give 22.', '\n\n\\boxed{22}', [(True, 'ok'), (True, 'ok')])
    rows = [exec_row, exec_failing, gsm_row, long_row, cd_row, clean_row]
    details = [detail_of(exec_row, '57', products=(4, 2)), detail_of(exec_failing, '57', products=(4, 2)),
               detail_of(gsm_row, '22', bad=['branch_truncated']), detail_of(long_row, '22'),
               detail_of(cd_row, '((3*4)+5)', bad=['branch_truncated']), detail_of(clean_row, '22')]
    for row in rows:
        D.validate_row(row)
    raw, det, req = tmp_path / 'all.raw.jsonl', tmp_path / 'details.jsonl', tmp_path / 'branch_requests.jsonl'
    F.write_jsonl(raw, rows)
    F.write_jsonl(det, details)
    F.write_jsonl(req, [
        dict(task_id='gsm-t', index=1, request='Two bags hold 5 apples each. How many apples are in the bags?\n\n'
             "Think it through step by step. End with one line 'Result: ...' that gives the answer.",
             body_sha256=F.sha256_text(gsm_bodies[1])),
        dict(task_id='countdown-c', index=1, request='Using 3, 4 and 5, make 17 by adding 4 and 5 first.',
             body_sha256=F.sha256_text(cd_bodies[1]))])
    return raw, det, req, rows


def plan(tmp_path, *extra):
    raw, det, req, rows = fixture_pool(tmp_path)
    work = tmp_path / 'work'
    args = F.parse_args(['plan', '--raw', str(raw), '--details', str(det), '--work-dir', str(work),
                         '--branch-requests', str(req), '--expect-sha256', '', *extra])
    jobs, stats = F.cmd_plan(args)
    return work, jobs, stats, rows


# ------------------------------------------------------------------------------------------ fake backend

class FakeBackend:
    def __init__(self, tokenizer, fn, fail_after=None):
        self.tokenizer, self.fn, self.fail_after = tokenizer, fn, fail_after
        self.queue, self.requested, self.done = [], [], 0

    def add(self, request):
        self.queue.append(request)
        self.requested.append(request['key'])

    def has_unfinished(self):
        return bool(self.queue)

    def step(self):
        if self.fail_after is not None and self.done >= self.fail_after:
            raise KeyboardInterrupt('simulated stop')
        request = self.queue.pop(0)
        self.done += 1
        outputs = [dict(o, n_tokens=len(self.tokenizer.encode(o['text'], add_special_tokens=False)))
                   for o in self.fn(request)]
        assert len(outputs) == request['params']['n']
        return [(request['key'], outputs)]


def stop(text):
    return dict(text=text, finish_reason='stop')


def fake_llm(request):
    """Deterministic outputs per request key; asserts the request shapes."""
    key, content = request['key'], request['content']
    job = key.split('|')[0]
    if '|branch' in key:
        assert request['thinking'] and request['params']['n'] == 2 and request['params']['max_tokens'] > 1000
        assert request['params']['temperature'] == 0.6 and 'seed' in request['params']
        if job.startswith('gsm'):
            assert content.startswith('Two bags hold 5 apples')
            return [dict(text='Two bags of five' + FILL, finish_reason='length'),
                    stop('Two bags with five apples each give 2 times 5 = 10.' + FILL + '\n</think>\n\nResult: 10')]
        assert content.endswith(C.COUNTDOWN_BRANCH_SUFFIX)  # added: the raw request lacked "ANY SUBSET"
        return [stop('I try 4 + 5 = 9 first.' + FILL + '\n</think>\n\nResult: 3*4+5'),           # off direction
                stop('4 + 5 = 9; 9*3, 9+3, 9-3 never give 17.' + FILL + '\n</think>\n\nResult: no expression '
                     'works this way')]
    if key.endswith('|summary'):
        assert not request['thinking'] and request['prompt'].endswith('<think>\n\n</think>\n\n')
        assert request['params']['n'] == 4 and request['params']['max_tokens'] <= 1024
        assert 'Result:' in content and 'verified' in content
        if job.startswith('exec'):
            assert 'produces' not in content and content.startswith('Find the total net profit')
            if job == 'exec-y#raw':
                return [stop('7 * 5 = 35 and 10 * 2 = 20 so 57.')] * 4
            return [stop('Recomputing: 7 * 5 = 35, 10 * 2 = 20, 8 * 4 = 32, total 57.'),   # input products
                    stop('The Results are 12, 15 and 30. ' * 20),                          # too long
                    stop('The Results are 12, 15 and 30, and 12 + 15 + 30 = 57.'),         # accepted
                    stop('So 12 + 15 + 30 = 57.')]                                         # wrong answer below
        if job.startswith('countdown'):
            assert 'equals 17' in content
            return [stop('Branch 1 gives 3*4+5, which uses 3, 4 and 5 and equals 17.')] * 4
        return [dict(text='The boxes give 12 and', finish_reason='length'),
                stop('The boxes give 12 and the bags give 10, so 12 + 10 = 22.'),
                stop('<Summary> 22'), stop('12 + 10 = 22.')]
    assert '|answer' in key and not request['thinking'] and request['params']['n'] == 1
    assert 'Reasoning summary:' in content
    if job.startswith('countdown'):
        return [stop('Branch 1 works.\nFinal Answer: 3*4+5')]
    if job == 'exec-x#raw' and key.endswith('answer4'):
        return [stop('The total is \\boxed{58}.')]
    return [stop('The total is \\boxed{57}.' if job.startswith('exec') else 'He has \\boxed{22} apples.')]


def run(work, backend):
    return F.cmd_run(F.parse_args(['run', '--work-dir', str(work), '--checkpoint-every', '2']), backend=backend)


def assemble(work, tokenizer):
    return F.cmd_assemble(F.parse_args(['assemble', '--work-dir', str(work)]), tokenizer=tokenizer)


# ------------------------------------------------------------------------------------------------- tests

def test_plan_buckets_and_requests(tmp_path):
    work, jobs, stats, _ = plan(tmp_path)
    assert stats['triage'] == {'exec_summary_resolves': 2, 'branch_truncated_only': 2, 'par_clean': 2}
    assert {j['id']: j['kind'] for j in jobs} == {'exec-x#raw': F.EXEC, 'exec-y#raw': F.EXEC,
                                                  'gsm-t#raw': F.TRUNC, 'countdown-c#raw': F.TRUNC,
                                                  'gsm-l#raw': F.LONG}  # gsm-c: summary short enough
    cd = next(j for j in jobs if j['id'] == 'countdown-c#raw')
    assert cd['branch_requests']['1']['countdown_suffix_added'] and cd['truncated'] == [1]
    assert (work / 'jobs.jsonl').exists() and json.loads((work / 'plan.json').read_text())['config']['summary_ratio'] == 0.5
    # without the exact request the truncated records are skipped and counted; arm_d is an explicit opt-in
    raw, det, _, _ = fixture_pool(tmp_path / 'b')
    jobs2, stats2, _ = F.plan_records(raw, det, dict(F.DEFAULTS), {}, 'none', '')
    assert stats2['skipped'][F.TRUNC] == {'branch_request_unavailable': 2}
    jobs3, _, _ = F.plan_records(raw, det, dict(F.DEFAULTS), {}, 'arm_d', '')
    assert {j['branch_requests']['1']['source'] for j in jobs3 if j['truncated']} == {'fallback_arm_d'}
    assert estimate_keys(F.estimate(jobs, F.raw_lines(raw), dict(F.DEFAULTS)))


def estimate_keys(est):
    return est['requests']['branch'] == 2 and est['requests']['summary'] == 5 and 'H100 NVL' in est['minutes']


def test_round_trip_merger_and_branch_repairs(tmp_path):
    work, jobs, _, rows = plan(tmp_path)
    tokenizer = build_tiny_tokenizer()
    backend = FakeBackend(tokenizer, fake_llm)
    manifest = run(work, backend)
    assert manifest['job_states'] == {'accepted': 4, 'failed': 1}
    repaired, stats = assemble(work, tokenizer)
    by_id = {r['id']: r for r in repaired}
    originals = {r['id']: r for r in rows}
    assert stats['accepted'] == {F.EXEC: 1, F.TRUNC: 2, F.LONG: 1} and stats['repair_failed'] == {F.EXEC: 1}

    # exec: shortest passing pair is sample 3 (sample 4's answer is wrong); only summary + answer changed
    ex = by_id['exec-x#raw']
    rep = ex['provenance']['repair']
    assert rep['kind'] == F.EXEC and rep['accepted_index'] == 2 and rep['node'] == 'summary+answer'
    assert [s['reason'] for s in rep['attempts']['summary']['samples']] == [
        'summary_input_products', 'summary_too_long', 'ok', 'ok']
    assert rep['attempts']['answers'][3]['reason'] == 'wrong:wrong_numeric'
    assert rep['exec_input_products']['summary'] == 0 and rep['exec_input_products']['summary_before'] == 4
    job = next(j for j in jobs if j['id'] == 'exec-x#raw')
    changed = {job['idx']['summary'], job['idx']['answer']}
    for i, (new, old) in enumerate(zip(ex['segments'], originals['exec-x#raw']['segments'])):
        if i in changed:
            assert new['loss'] == old['loss'] and new['block'] == old['block'] and new['path'] == old['path']
        else:
            assert json.dumps(new) == json.dumps(old)  # byte-identical
    assert ex['segments'][job['idx']['summary']]['text'] == 'The Results are 12, 15 and 30, and 12 + 15 + 30 = 57.'
    assert ex['segments'][job['idx']['answer']]['text'] == '\n\nThe total is \\boxed{57}.'
    p = ex['provenance']
    assert p['model_finished'] and p['correct'] and p['grade'] == 'correct_numeric' and not p['repair_failed']
    assert p['branch_checks'] == [dict(ok=True, reason='ok_oracle_verified')] * 3  # re-checked, not copied
    assert p['n_tokens'] == len(tokenizer.encode(''.join(s['text'] for s in ex['segments']), add_special_tokens=False))
    assert rep['original_sha256'] == job['original']['line_sha256'] and len(rep['prompt_sha256']) == 2

    # exec-y: every summary recomputes -> original row flagged repair_failed, segments untouched
    failed = by_id['exec-y#raw']
    assert failed['provenance']['repair_failed'] and failed['segments'] == originals['exec-y#raw']['segments']
    assert failed['provenance']['repair']['reason'] == 'summary:summary_input_products'

    # truncated gsm: branch 2 regenerated (sample 2 finished), then the merger; branch 1 untouched
    gsm = by_id['gsm-t#raw']
    job = next(j for j in jobs if j['id'] == 'gsm-t#raw')
    assert gsm['segments'][job['idx']['bodies'][0]] == originals['gsm-t#raw']['segments'][job['idx']['bodies'][0]]
    body = gsm['segments'][job['idx']['bodies'][1]]['text']
    assert body.startswith(' Two bags with five apples') and body.endswith('\n\nResult: 10')
    p = gsm['provenance']
    assert p['model_finished'] and p['correct'] and [c['ok'] for c in p['branch_checks']] == [True, True]
    assert p['repair']['attempts']['branches'][1]['accepted_index'] == 1
    assert p['repair']['branch_request_sources'] == {1: 'raw_run_request'}
    assert p['repair']['node'] == 'branch2+summary+answer'
    # gsm summary samples: truncated, ok, tags, ok(shorter) -> the shorter one wins
    assert [s['reason'] for s in p['repair']['attempts']['summary']['samples']] == [
        'summary_truncated', 'ok', 'summary_tags', 'ok']
    assert gsm['segments'][job['idx']['summary']]['text'] == '12 + 10 = 22.'

    # countdown: the off-direction sample is rejected, the sound no-solution claim accepted
    cd = by_id['countdown-c#raw']
    assert cd['provenance']['branch_checks'][1] == dict(ok=True, reason='ok_countdown_none')
    assert cd['provenance']['repair']['attempts']['branches'][1]['samples'][0]['reason'] == 'countdown_off_direction'
    assert cd['segments'][-2]['text'] == '\n\nBranch 1 works.\nFinal Answer: 3*4+5'

    # long summary gsm: shorter summary, branches/plan/prefix identical
    long = by_id['gsm-l#raw']
    assert long['provenance']['repair']['lengths']['summary_chars_after'] < \
        0.5 * long['provenance']['repair']['lengths']['longest_branch_chars']
    for row in repaired:
        D.validate_row(row)
        assert row['provenance']['n_tokens'] <= 16384

    # export + selection: repaired rows replace raw ones by id; repair_failed dropped unless --keep-repair-failed
    out = tmp_path / 'repaired.jsonl'
    F.cmd_export(F.parse_args(['export', '--work-dir', str(work), '--out', str(out)]))
    raw = tmp_path / 'all.raw.jsonl'
    stats = select_records.main([str(raw), str(out), '--dry-run'])
    assert stats['dropped_first_rule']['replaced_by_repair'] == {'exec': 2, 'gsm': 2, 'countdown': 1}
    assert stats['dropped_first_rule']['repair_failed'] == {'exec': 1}
    assert stats['kept']['rows'] == 5  # 4 repaired + gsm-c clean raw
    kept = select_records.main([str(raw), str(out), '--dry-run', '--keep-repair-failed'])
    assert kept['kept']['rows'] == 6
    sel = select_records.main([str(raw), str(out), '--out-dir', str(tmp_path / 'sel'), '--val-frac', '0'])
    train = [json.loads(x) for x in (tmp_path / 'sel' / 'train.jsonl').read_text().splitlines()]
    assert {r['id']: bool(r['provenance'].get('repair')) for r in train} == {
        'exec-x#raw': True, 'gsm-t#raw': True, 'gsm-l#raw': True, 'countdown-c#raw': True, 'gsm-c#raw': False}
    assert sel['kept']['rows'] == 5


def test_resume_after_partial_results(tmp_path):
    work, jobs, _, _ = plan(tmp_path)
    tokenizer = build_tiny_tokenizer()
    full = FakeBackend(tokenizer, fake_llm)
    run(work, full)
    complete = F.read_results(work / 'results.jsonl')
    reference = {k: v['outputs'] for k, v in complete.items()}
    # fresh work dir, stop after 5 requests (with a torn last line), then resume
    work2, _, _, _ = plan(tmp_path / 'second')
    first = FakeBackend(tokenizer, fake_llm, fail_after=5)
    with pytest.raises(KeyboardInterrupt):
        run(work2, first)
    partial = F.read_results(work2 / 'results.jsonl')
    assert len(partial) == 5
    with open(work2 / 'results.jsonl', 'a') as handle:
        handle.write('{"key": "torn')
    second = FakeBackend(tokenizer, fake_llm)
    run(work2, second)
    assert not set(second.requested) & set(partial)  # nothing re-generated
    resumed = F.read_results(work2 / 'results.jsonl')
    assert {k: v['outputs'] for k, v in resumed.items()} == reference
    assert {k: v['params'] for k, v in resumed.items()} == {k: v['params'] for k, v in complete.items()}
    rows_a, _ = assemble(work, tokenizer)
    rows_b, _ = assemble(work2, tokenizer)
    strip = lambda rows: [json.dumps(dict(r, provenance={k: v for k, v in r['provenance'].items()  # noqa: E731
                                                          if k != 'repair'}), sort_keys=True) for r in rows]
    assert strip(rows_a) == strip(rows_b)
    # a second run on a finished work dir issues nothing
    idle = FakeBackend(tokenizer, fake_llm)
    run(work2, idle)
    assert idle.requested == []


def test_seeds_and_budgets_are_deterministic(tmp_path):
    work, jobs, _, _ = plan(tmp_path)
    tokenizer = build_tiny_tokenizer()
    plan_cfg = json.loads((work / 'plan.json').read_text())['config']
    ctx = F.Ctx(tokenizer, plan_cfg)
    job = next(j for j in jobs if j['id'] == 'gsm-t#raw')
    a, b = F.evaluate(job, {}, ctx), F.evaluate(job, {}, F.Ctx(tokenizer, plan_cfg))
    assert a['pending'][0]['params'] == b['pending'][0]['params']
    params = a['pending'][0]['params']
    assert params['seed'] == C.seed_of('fast-repair', F.REVISION, 'gsm-t#raw|branch2')
    kept = len(tokenizer.encode(job['bodies'][0], add_special_tokens=False))
    assert params['max_tokens'] == 16384 - 2048 - C.overhead(ctx, job['prefix'], job['plan']) - kept
    assert hashlib.sha256(a['pending'][0]['prompt'].encode()).hexdigest()


# ------------------------------------------------------------------------- second pass (prompt v2, retry)

def job_of(source, oracle='57', task=None):
    task = dict(task or {}, src=source, question='q')
    return dict(source=source, q=dict(task=task, gold=dict(oracle=oracle)))


def test_rule_b_final_marker():
    assert F.has_final_marker('Branch 1 gives 3*4+5.\nFinal Answer: 3*4+5')
    assert F.has_final_marker('so the total is \\boxed{57}')
    assert F.has_final_marker('FINAL ANSWER: 22') and F.has_final_marker('my final answer : 22')
    assert not F.has_final_marker('The final answer is the sum of these three numbers.')  # left to rule (a)
    assert not F.has_final_marker('12 + 10 = 22, so he has 22 apples.')


def test_rule_a_numeric_values():
    exec_job = job_of('exec', '-252')
    summary = 'The Results are -255, -137 and 140. (-255) + (-137) = -392; -392 + 140 = -252. The total is -252.'
    assert F.final_value_check(exec_job, summary, 'The total is \\boxed{-252}.') == (True, 'numeric')
    # the smoke failure: the summary leaves the arithmetic to the answer call
    lazy = 'The Results are -255, -137 and 140. The final answer is the sum of these three numbers.'
    assert F.final_value_check(exec_job, lazy, 'The total is \\boxed{-252}.') == (False, 'numeric')
    assert not F.final_value_check(exec_job, 'They add up to 252.', 'So \\boxed{-252}.')[0]   # sign matters
    assert F.final_value_check(exec_job, 'That is a loss of $252.', 'So \\boxed{-252}.')[0]
    assert not F.final_value_check(exec_job, '-392 + 140 = -152', 'So \\boxed{-252}.')[0]
    assert not F.final_value_check(job_of('exec', '-5'), 'I compute 12-5 = 7.', 'So \\boxed{-5}.')[0]  # a minus
    assert F.final_value_check(job_of('exec', '-5'), 'I compute 7 - 12 = -5.', 'So \\boxed{-5}.')[0]  # a sign
    gsm = job_of('gsm', '1234.5')
    assert F.final_value_check(gsm, 'Adding gives $1,234.50 in total.', 'He pays \\boxed{1234.5}.')[0]
    assert F.final_value_check(gsm, 'Adding gives 1,234.5.', 'He pays \\boxed{\\$1,234.50}.')[0]  # gold fallback
    assert F.final_value_check(job_of('gsm', '22'), '12 + 10 = 22 apples', '\\boxed{22}')[0]
    assert F.final_value_check(job_of('gsm', '22'), 'x', 'no box') == (False, 'no_boxed')


def test_rule_a_countdown_and_math():
    cd = job_of('countdown', '((3*4)+5)')
    answer = 'Branch 1 works.\nFinal Answer: 3*4+5'
    assert F.final_value_check(cd, 'Branch 1 gives 3 * 4 + 5, which uses 3, 4 and 5.', answer)[0]
    assert F.final_value_check(cd, 'I take (4 x 3) + 5: 4*3 = 12; 12 + 5 = 17.', answer)[0]  # same expression key
    assert not F.final_value_check(cd, '3*4 = 12; 12 + 5 = 17.', answer)[0]               # steps only
    assert not F.final_value_check(cd, 'Branch 1 reaches 17.', answer)[0]
    math = job_of('math', '\\boxed{\\frac{3}{4}}')
    assert F.final_value_check(math, 'So the ratio is 3/4.', 'It is \\boxed{\\dfrac{3}{4}}.') == (True, 'math_string')
    assert F.final_value_check(math, 'so x = \\frac{3}{4}', 'It is \\boxed{\\frac34}.')[0]
    assert F.final_value_check(math, 'so x is three quarters', 'It is \\boxed{\\frac{3}{4}}.') == (False,
                                                                                               'math_string')
    assert F.final_value_check(math, 'three quarters', '\\boxed{\\frac{3}{4}}', 'skip') == (True, 'skipped')
    assert F.final_value_check(math, 'the side is 5 cm', 'It is \\boxed{5}.') == (True, 'numeric')
    assert F.final_value_check(math, 'none', 'It is \\boxed{\\sqrt{2}}.')[0] is False
    assert F.final_value_check(math, 'r = \\sqrt{2}', 'It is \\boxed{\\sqrt{2}}.')[0]
    assert F.final_value_check(math, 'anything', 'It is \\boxed{x}.') == (True, 'skipped_short')
    assert F.final_value_check(math, 'x = 1, 2, 10', 'So \\boxed{1,2,10}.') == (True, 'math_string')  # not 1210
    assert F.final_value_check(math, 'x = 1 and 10', 'So \\boxed{1,2,10}.') == (False, 'math_string')
    assert F.final_value_check(math, 'so it is (-∞, 2) ∪ (2, 4)', '\\boxed{(-\\infty, 2) \\cup (2, 4)}')[0]
    assert F.final_value_check(math, 'p(x) = x² + 1', '\\boxed{x^2 + 1}')[0]
    assert F.final_value_check(math, 'r = 2√6 / 3', '\\boxed{\\dfrac{2\\sqrt{6}}{3}}')[0]
    assert F.final_value_check(math, '(6, 235°)', '\\boxed{(6, 235^\\circ)}')[0]
    matrix = '\\boxed{\\begin{pmatrix} 1 & 0 \\\\ 0 & 1 \\end{pmatrix}}'
    assert F.final_value_check(math, '[[1, 0], [0, 1]]', matrix) == (True, 'skipped_matrix')
    assert F.strict_reason(math, 'Final Answer: 5', '\\boxed{5}') == 'summary_final_marker'
    assert F.strict_reason(math, 'the side is 4', '\\boxed{5}') == 'summary_missing_value'
    assert F.strict_reason(math, 'the side is 5', '\\boxed{5}') is None


def test_retry_cause():
    trunc, exec_ = dict(kind=F.TRUNC), dict(kind=F.EXEC)
    failed = lambda reason: dict(status='failed', reason=reason)  # noqa: E731
    assert F.retry_cause(exec_, failed('summary:summary_input_products')) == 'merger'
    assert F.retry_cause(exec_, failed('answer:wrong:wrong_numeric')) == 'merger'
    assert F.retry_cause(exec_, failed('answer:v2:summary_missing_value')) == 'merger'
    assert F.retry_cause(exec_, failed('summary_budget')) is None
    assert F.retry_cause(trunc, failed('branch:branch_truncated')) == 'branch'
    assert F.retry_cause(trunc, failed('branch_budget')) == 'branch'
    assert F.retry_cause(exec_, dict(status='accepted')) is None
    assert F.retry_cause(trunc, dict(status='waiting')) is None


def first_pass_llm(request):
    """fake_llm with three first-pass changes: the truncated GSM branch never finishes (branch failure), the Countdown
    summaries carry their own Final Answer line (rule b) and the long-summary GSM summaries never state 22 (rule a)."""
    key = request['key']
    if key == 'gsm-t#raw|branch2':
        return [dict(text='Two bags of five' + FILL, finish_reason='length')] * 2
    if key == 'countdown-c#raw|summary':
        return [stop('Branch 1 gives 3*4+5.\nFinal Answer: 3*4+5')] * 4
    if key == 'gsm-l#raw|summary':
        return [stop('The boxes give 12 and the bags give 10; I add them.')] * 4
    return fake_llm(request)


def retry_llm(request):
    """Outputs of the v2 (retry) requests; asserts their shapes."""
    key, content = request['key'], request['content']
    job = key.split('|')[0]
    assert '|v2|' in key and request['prompt_version'] == 'v2' and 'seed' in request['params']
    if '|branch' in key:
        assert job == 'gsm-t#raw' and request['thinking'] and request['params']['n'] == 4
        return [dict(text='Two bags of five' + FILL, finish_reason='length'),
                stop('Two bags with five apples each give 2 times 5 = 10, as I check slowly.' + FILL +
                     '\n</think>\n\nResult: 10'),
                stop('Two bags with five apples each give 2 times 5 = 10.' + FILL + '\n</think>\n\nResult: 10'),
                stop('no')]
    if key.endswith('|summary'):
        assert not request['thinking'] and request['params']['n'] == 8 and request['params']['max_tokens'] <= 1024
        assert 'one operation per step' in content and 'Final Answer" line' in content
        if job.startswith('exec'):
            assert 'produces' not in content and '(-25) + 40 = 15' in content
            return [stop('The Results are 12, 15 and 30.\nFinal Answer: 57'),                       # rule (b)
                    stop('The Results are 12, 15 and 30; the total is their sum.'),                 # rule (a)
                    stop('The Results are 12, 15 and 30. 12 + 15 = 27; 27 + 30 = 57. The total is 57.'),
                    stop('Recomputing 7 * 5 = 35 and 10 * 2 = 20: 12 + 15 = 27; 27 + 30 = 57.')] * 2
        if job.startswith('countdown'):
            assert 'names the chosen expression' in content
            return [stop('Branch 1 found a valid expression and branch 2 found none, so I use it.')] * 8
        if job == 'gsm-l#raw':
            return [stop('Boxes 12, bags 10. 12 + 10 = 22.\nFinal Answer: 22')] * 8
        return [stop('The boxes give 12 and the bags give 10. 12 + 10 = 22. He has 22 apples.')] * 8
    assert '|answer' in key and request['params']['n'] == 1
    assert ('value the reasoning summary reached' in content or 'expression the reasoning summary chose' in content)
    if job.startswith('countdown'):
        return [stop('Branch 1 works.\nFinal Answer: 3*4+5')]
    return [stop('The total is \\boxed{57}.' if job.startswith('exec') else 'He has \\boxed{22} apples.')]


def retry(work, backend, *extra):
    return F.cmd_run(F.parse_args(['run', '--work-dir', str(work), '--retry-failed', '--checkpoint-every', '2',
                                   *extra]), backend=backend)


def test_retry_pass_and_assemble_merge(tmp_path):
    work, jobs, _, rows = plan(tmp_path)
    tokenizer = build_tiny_tokenizer()
    manifest = run(work, FakeBackend(tokenizer, first_pass_llm))
    assert manifest['job_states'] == {'accepted': 3, 'failed': 2}
    first_sha = F.sha256_file(work / 'results.jsonl')

    # 1. assemble --strict-v2 (default) on the first pass: two v1-accepted pairs are demoted
    _, stats = assemble(work, tokenizer)
    sv = stats['strict_v2']
    assert sv['enabled'] and sv['first_pass_accepted_v1'] == {F.EXEC: 1, F.TRUNC: 1, F.LONG: 1}
    assert sv['demoted_reasons'] == {f'{F.TRUNC}/answer:v2:summary_final_marker': 1,
                                     f'{F.LONG}/answer:v2:summary_missing_value': 1}
    assert sv['retry_candidates'] == {f'{F.EXEC}/merger': 1, f'{F.TRUNC}/merger': 1, f'{F.TRUNC}/branch': 1,
                                      f'{F.LONG}/merger': 1}
    assert sv['retry_outcomes'] == {f'{k}/not_run': n for k, n in ((F.EXEC, 1), (F.TRUNC, 2), (F.LONG, 1))}
    assert stats['accepted'] == {F.EXEC: 1} and stats['repair_failed'] == {F.EXEC: 1, F.LONG: 1}
    _, loose = F.cmd_assemble(F.parse_args(['assemble', '--work-dir', str(work), '--no-strict-v2']),
                              tokenizer=tokenizer)
    assert loose['accepted'] == {F.EXEC: 1, F.TRUNC: 1, F.LONG: 1} and 'demoted_by_strict_v2' not in loose['strict_v2']

    # 2. run --retry-failed: only the candidates' v2 requests, into results.retry.jsonl
    backend = FakeBackend(tokenizer, retry_llm)
    manifest = retry(work, backend)
    assert F.sha256_file(work / 'results.jsonl') == first_sha  # the first pass is untouched
    assert manifest['selection']['candidates'] == sv['retry_candidates'] and manifest['jobs'] == 4
    assert manifest['selection']['demoted_by_strict_v2'] == sv['demoted_reasons']
    assert not any(k.startswith('exec-x#raw') for k in backend.requested)  # first-pass accepted: never retried
    assert {k for k in backend.requested if not k.split('|')[-1].startswith('answer')} == {
        'exec-y#raw|v2|summary', 'gsm-t#raw|v2|branch2', 'gsm-t#raw|v2|summary', 'countdown-c#raw|v2|summary',
        'gsm-l#raw|v2|summary'}  # countdown keeps its accepted first-pass branch: no new branch request
    retry_rows = F.read_results(work / F.RETRY_RESULTS)
    assert set(retry_rows) == set(backend.requested) and all(r['prompt_version'] == 'v2' for r in retry_rows.values())
    assert {r['job_id'] for r in retry_rows.values()} == {'exec-y#raw', 'gsm-t#raw', 'countdown-c#raw', 'gsm-l#raw'}
    # the retried branch budget uses the 1,536-token reserve instead of 2,048
    ctx = F.Ctx(tokenizer, json.loads((work / 'plan.json').read_text())['config'])
    job = next(j for j in jobs if j['id'] == 'gsm-t#raw')
    first_budget = F.read_results(work / 'results.jsonl')['gsm-t#raw|branch2']['params']['max_tokens']
    assert retry_rows['gsm-t#raw|v2|branch2']['params']['max_tokens'] == first_budget + C.RESERVE - 1536
    assert F.evaluate_v2(job, {**F.read_results(work / 'results.jsonl'), **retry_rows}, ctx)['status'] == 'accepted'

    # resumable: a second retry run issues nothing; the first pass issues nothing either
    idle = FakeBackend(tokenizer, retry_llm)
    retry(work, idle)
    assert idle.requested == []
    idle = FakeBackend(tokenizer, first_pass_llm)
    run(work, idle)
    assert idle.requested == [] and F.sha256_file(work / 'results.jsonl') == first_sha

    # 3. assemble merges: accepted first pass > accepted retry > repair_failed
    merged, stats = assemble(work, tokenizer)
    by_id = {r['id']: r for r in merged}
    assert stats['accepted_by_pass'] == {f'{F.EXEC}/first': 1, f'{F.EXEC}/retry': 1, f'{F.TRUNC}/retry': 1}
    assert stats['repair_failed'] == {F.LONG: 1}
    assert stats['strict_v2']['retry_outcomes'] == {
        f'{F.EXEC}/accepted': 1, f'{F.TRUNC}/accepted': 1,
        f'{F.TRUNC}/failed:answer:summary_missing_value': 1, f'{F.LONG}/failed:summary:summary_final_marker': 1}
    assert 'countdown-c#raw' not in by_id  # demoted, retry failed: branch_truncated rows are not exported

    first = by_id['exec-x#raw']['provenance']['repair']
    assert first['prompt_version'] == 'v1' and first['repair_pass'] == 'first' and first['strict_v2']

    ey = by_id['exec-y#raw']
    rep = ey['provenance']['repair']
    assert rep['prompt_version'] == 'v2' and rep['repair_pass'] == 'retry' and not ey['provenance']['repair_failed']
    assert rep['first_pass'] == dict(status='failed', reason='summary:summary_input_products',
                                     demoted_by_strict_v2=False)
    assert [s['reason'] for s in rep['attempts']['summary']['samples']][:4] == [
        'summary_final_marker', 'ok', 'ok', 'summary_input_products']
    assert rep['attempts']['answers'][1]['reason'] == 'summary_missing_value'
    assert rep['attempts']['answers'][2]['reason'] == 'ok' and rep['accepted_index'] == 2
    job = next(j for j in jobs if j['id'] == 'exec-y#raw')
    assert ey['segments'][job['idx']['summary']]['text'] == \
        'The Results are 12, 15 and 30. 12 + 15 = 27; 27 + 30 = 57. The total is 57.'
    assert set(rep['prompt_sha256']) == {'exec-y#raw|v2|summary', 'exec-y#raw|v2|answer3'}
    assert all(rep['seeds'].values()) and ey['provenance']['correct']
    original = next(r for r in rows if r['id'] == 'exec-y#raw')
    for i, (new, old) in enumerate(zip(ey['segments'], original['segments'])):
        if i not in (job['idx']['summary'], job['idx']['answer']):
            assert json.dumps(new) == json.dumps(old)

    gt = by_id['gsm-t#raw']
    rep = gt['provenance']['repair']
    assert rep['repair_pass'] == 'retry' and rep['first_pass']['reason'] == 'branch:branch_truncated'
    branch = rep['attempts']['branches'][1]
    assert branch['retried'] and branch['accepted_key'] == 'gsm-t#raw|v2|branch2' and branch['accepted_index'] == 2
    assert gt['provenance']['branch_checks'] == [dict(ok=True, reason='ok'), dict(ok=True, reason='ok')]
    assert rep['node'] == 'branch2+summary+answer' and 'gsm-t#raw|v2|branch2' in rep['prompt_sha256']

    gl = by_id['gsm-l#raw']
    assert gl['provenance']['repair_failed'] and gl['segments'] == next(r for r in rows if r['id'] == 'gsm-l#raw')[
        'segments']
    rep = gl['provenance']['repair']
    assert rep['reason'] == 'answer:v2:summary_missing_value' and rep['demoted_by_strict_v2']
    assert rep['retry']['status'] == 'failed' and rep['retry']['reason'] == 'summary:summary_final_marker'

    # --no-strict-v2: the v1-accepted pairs come back, retry results are used only for real first-pass failures
    loose_rows, loose = F.cmd_assemble(F.parse_args(['assemble', '--work-dir', str(work), '--no-strict-v2']),
                                       tokenizer=tokenizer)
    assert loose['accepted_by_pass'] == {f'{F.EXEC}/first': 1, f'{F.EXEC}/retry': 1, f'{F.TRUNC}/first': 1,
                                         f'{F.TRUNC}/retry': 1, f'{F.LONG}/first': 1}
    assert loose['repair_failed'] == {}

    # export + selection read the merged rows
    out = tmp_path / 'repaired.jsonl'
    assemble(work, tokenizer)
    stats = F.cmd_export(F.parse_args(['export', '--work-dir', str(work), '--out', str(out)]))
    assert stats['by_kind'] == {f'{F.EXEC}/repaired': 2, f'{F.TRUNC}/repaired': 1, f'{F.LONG}/failed': 1}
    sel = select_records.main([str(tmp_path / 'all.raw.jsonl'), str(out), '--dry-run'])
    assert sel['kept']['rows'] == 3 + 1 + 0  # exec-x, exec-y, gsm-t repaired + gsm-c clean; countdown raw dropped


def test_retry_does_not_rewrite_first_pass_with_torn_line(tmp_path):
    work, _, _, _ = plan(tmp_path)
    tokenizer = build_tiny_tokenizer()
    run(work, FakeBackend(tokenizer, first_pass_llm))
    with open(work / 'results.jsonl', 'a') as handle:
        handle.write('{"key": "torn')  # as if the first pass were still writing
    sha = F.sha256_file(work / 'results.jsonl')
    retry(work, FakeBackend(tokenizer, retry_llm), '--no-retry-branches')
    assemble(work, tokenizer)
    assert F.sha256_file(work / 'results.jsonl') == sha
    manifest = [json.loads(x) for x in (work / F.RETRY_MANIFEST).read_text().splitlines()][-1]
    assert manifest['selection']['branch_retry_disabled'] == {F.TRUNC: 1} and manifest['jobs'] == 3
