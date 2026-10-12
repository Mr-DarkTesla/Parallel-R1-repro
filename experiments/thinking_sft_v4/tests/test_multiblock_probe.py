"""multiblock_probe.py on CPU with a fake backend: Codex planner copies, select / block-1 reuse rules, the planner-2
prompt (contents, no gold), every stage through assembly of a 2-block record (validator, tokenization, loss flags,
markdown, stats) and a NO_FORK single-block record.

cd experiments/thinking_sft_v4 && CUDA_VISIBLE_DEVICES= python -m pytest -q tests/test_multiblock_probe.py
"""
import ast
import json
import os
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import codex_rules as C  # noqa: E402
import multiblock_probe as M  # noqa: E402
import sft_data as D  # noqa: E402
from common import contract  # noqa: E402
from tags import ensure_tags  # noqa: E402
from tiny import build_tiny_model, build_tiny_tokenizer  # noqa: E402

POOL = Path(os.environ.get('FAST_REPAIR_POOL', '/mnt/project-files/thinking-sft-4b/pool-20261012'))
CODEX = Path(os.environ.get('CODEX_CODE_DIR', POOL / 'codex-code'))
BOX = '\n\nPlease reason step by step, and put your final answer within \\boxed{}.'
Q1130 = 'How many integers $-11 \\leq n \\leq 11$ satisfy $(n-2)(n+4)(n + 8)<0$?'
QB = 'A crate holds 9 boxes and each box holds 7 widgets. Some crates are unusual. How many widgets are in all crates?'
QD = 'How many ways can a committee of 3 be chosen from 6 people?'
ORACLE = {'1130': 'GOLDSENTINEL1130 the negative intervals hold 3 and 5 integers, so $\\boxed{8}$.',
          'B': 'GOLDSENTINELB so the total is $\\boxed{4173}$.',
          'D': 'GOLDSENTINELD $\\binom{6}{3} = \\boxed{20}$.'}
IDS = ['math-intermediate_algebra-train-1130', 'math-test-B', 'math-test-D']
BODY_ONLY = 'BODYONLY detailed branch reasoning that planner 2 must not see'


@pytest.fixture(autouse=True)
def fake_math_verify(monkeypatch):
    """gen.grade imports math_verify (VM venv only): compare the last boxed contents."""
    module = types.ModuleType('math_verify')
    module.parse = lambda text: (C.last_boxed(text) or text).strip()
    module.verify = lambda a, b: a == b
    monkeypatch.setitem(sys.modules, 'math_verify', module)


# ------------------------------------------------------------------------------------------- Codex copies

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
def test_codex_planner_copies_verbatim():
    mine = top_level(Path(M.__file__).read_text())
    theirs = top_level((CODEX / 'gen.py').read_text())
    for name in ('TEACHER_SAMPLING', 'PLANNER_SYS', 'parse_json_obj', 'plan_text', 'validate_plan'):
        assert mine[name] == theirs[name], f'{name} differs from codex-code/gen.py'
    teacher = [node.value for node in ast.parse((CODEX / 'gen.py').read_text()).body
               if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', None) == 'TEACHER']
    assert M.PLANNER == ast.literal_eval(teacher[0])
    literals = {node.value for node in ast.walk(ast.parse((CODEX / 'raw_acquisition.py').read_text()))
                if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    assert M.RAW_PLANNER_RULES in literals  # the rules raw_plan appends to gen.PLANNER_SYS


# ------------------------------------------------------------------------------------------- synthetic pool

def body(text, result):
    return ' ' + text + '\n\n' + f'Result: {result}'


def pool_row(task_id, question, plan_kind, items, results, checks_ok=True):
    prefix = f'Okay, so I need to solve this: {question[:40]}\n\n'
    plan = dict(kind=plan_kind, items=items, branches=len(items), plan_text=M.plan_text(plan_kind, items))
    bodies = [body(f'{BODY_ONLY} {i}.', r) for i, r in enumerate(results, 1)]
    segs, text = C.parallel_segments(prefix, plan, bodies, 'Pool summary that ends the problem.', '\n\nPool answer.')
    return dict(id=task_id + '#raw', source='math', mode='parallel', question=question, prompt=question + BOX,
                segments=segs, provenance=dict(task_id=task_id, n_tokens=999, plan_status='fork', branch_checks=[
                    dict(ok=checks_ok or i > 0, reason='ok' if checks_ok or i > 0 else 'branch_truncated')
                    for i in range(len(items))]))


@pytest.fixture
def pool(tmp_path):
    rows = [
        pool_row(IDS[0], Q1130, 'cases', ['Determine the sign of the product for n < -8.',
                                          'Determine the sign of the product for -8 < n < -4.',
                                          'Determine the sign of the product for -4 < n < 2.'],
                 ['negative', 'positive', 'negative']),
        pool_row(IDS[1], QB, 'decompose', ['Count the widgets in the ordinary crates.',
                                           'Count the widgets in the unusual crates.'], ['63', '4110']),
        pool_row(IDS[2], QD, 'methods', ['Count with the binomial formula.', 'Count by listing.'], ['x', 'y'],
                 checks_ok=False),
    ]
    details = [dict(id=r['id'], oracle=ORACLE[key], correct=True) for r, key in zip(rows, ('1130', 'B', 'D'))]
    folder = tmp_path / 'pool'
    folder.mkdir()
    (folder / 'all.raw.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
    (folder / 'details.jsonl').write_text(''.join(json.dumps(d) + '\n' for d in details))
    return folder


# ------------------------------------------------------------------------------------------- fake backend

PLAN1_1130 = dict(analysis='Four intervals.', decision='FORK', branches=4, kind='cases', assignments=[
    'Determine the sign of (n-2)(n+4)(n+8) for n < -8.', 'Determine the sign of (n-2)(n+4)(n+8) for -8 < n < -4.',
    'Determine the sign of (n-2)(n+4)(n+8) for -4 < n < 2.', 'Determine the sign of (n-2)(n+4)(n+8) for n > 2.'],
    subproblems=[f'What is the sign of (n-2)(n+4)(n+8) when {r}?' for r in
                 ('n < -8', '-8 < n < -4', '-4 < n < 2', 'n > 2')])
PLAN2_1130 = dict(analysis='Two counts.', decision='FORK', branches=2, kind='decompose', assignments=[
    'Count the integers n with -11 <= n < -8.', 'Count the integers n with -4 < n < 2.'],
    subproblems=['How many integers n satisfy -11 <= n < -8?', 'How many integers n satisfy -4 < n < 2?'])


def out(text, finish='stop'):
    return dict(text=text, finish_reason=finish, n_tokens=max(1, len(text) // 4), stop_reason=None)


class FakeBackend:
    def __init__(self, which, tok):
        self.which, self.tok, self.requests = which, tok, []

    def generate(self, requests):
        self.requests += requests
        return [[out(t) for t in self.answer(r)] for r in requests]

    def answer(self, r):
        kind, task_id = r['key'].split('|')[:2]
        n = r['params'].get('n', 1)
        short = task_id.split('-')[-1]
        if kind == 'coverage':
            return ['{"evidence": "every part is assigned", "covers": true}']
        if kind == 'plan1':
            if short == '1130':
                return ['not json at all'] if r['key'].endswith('a0') else [json.dumps(PLAN1_1130)]
            return ['{"analysis": "single chain", "decision": "NO_FORK"}']
        if kind == 'plan2':
            return [json.dumps(PLAN2_1130)] if short == '1130' else ['{"analysis": "chain", "decision": "NO_FORK"}']
        if kind.startswith('branch'):
            index = int(r['key'].split('|')[2])
            value = dict(branch1={1: 'negative', 2: 'positive', 3: 'negative', 4: 'positive'},
                         branch2={1: '3', 2: '5'})[kind][index]
            return [f'I work on part {index} step by step.\n</think>\n\nResult: {value}'] * n
        if kind.startswith('summary'):
            good = ('The product is negative for n < -8 and for -4 < n < 2, positive elsewhere.' if kind == 'summary1'
                    else 'The counts are 3 and 5, and 3 + 5 = 8, so these intervals hold 8 integers.')
            return ['Final Answer: \\boxed{1}'] + [good] * (n - 1)
        if kind == 'continuation':
            return ['Now I need to count the integers in each negative interval within the range.\n\n'] * n
        if kind == 'final':
            if short == '1130':
                return ['\n\nSo the count is 8.\n</think>\n\nThere are \\boxed{8} such integers.'] * n
            return ['\n\nAdding 63 and 4110 gives 4173.\n</think>\n\nThe total is \\boxed{4173}.'] * n
        raise AssertionError(r['key'])


def run_all(pool, out_dir):
    tok = build_tiny_tokenizer()
    cfg = dict(M.DEFAULTS)
    M.select(pool, out_dir, IDS, list(M.FORCE_REGENERATE), cfg)
    backends = {}
    for name in M.STAGES:
        backend = FakeBackend(M.MODEL_OF[name], tok)
        backends[name] = backend
        M.STAGE_FUNCS[name](out_dir, backend, cfg)
    records, stats = M.assemble(out_dir, tok)
    return records, stats, backends


# ------------------------------------------------------------------------------------------- tests

def test_select_reuse_rules(pool, tmp_path):
    items = {i['id']: i for i in M.select(pool, tmp_path / 'o', IDS, list(M.FORCE_REGENERATE), dict(M.DEFAULTS))}
    assert items[IDS[0]]['reuse_candidate'] is False and 'forced_regenerate' in items[IDS[0]]['pool_reject']
    assert items[IDS[1]]['reuse_candidate'] is True
    assert items[IDS[2]]['reuse_candidate'] is False
    assert items[IDS[2]]['pool_reject'][0].startswith('pool_branch_checks_failed')
    assert items[IDS[1]]['prefix'].endswith('\n\n') and items[IDS[1]]['pool_block']['results'] == [
        'Result: 63', 'Result: 4110']
    config = json.loads((tmp_path / 'o' / 'config.json').read_text())
    assert config['ids'] == IDS and 'causal' in config['context']


def test_default_ids_listed():
    assert list(M.DEFAULT_IDS)[0] == 'math-intermediate_algebra-train-1130' and len(M.DEFAULT_IDS) == 12
    assert M.FORCE_REGENERATE == ('math-intermediate_algebra-train-1130',)


def test_two_block_record_end_to_end(pool, tmp_path):
    out_dir = tmp_path / 'probe'
    records, stats, backends = run_all(pool, out_dir)
    by_id = {r['provenance']['task_id']: r for r in records}
    assert set(by_id) == {IDS[0], IDS[1]}
    assert stats['per_id'][IDS[2]]['status'] == 'no_block1_plan'

    # 1130: regenerated block 1 (4 cases), block 2 forked, two blocks in the contract format
    row = by_id[IDS[0]]
    assert row['provenance']['block1_source'] == 'regenerated' and row['provenance']['blocks'] == 2
    summary = D.validate_row(row)
    assert [b['branches'] for b in summary['blocks']] == [4, 2]
    inserted = {'branches=', '<Plan>', '<Path>', '</Parallel>', '<Summary>'}
    for s in row['segments']:
        is_prefix = s['path'] is not None and s['text'] == contract.path_prefix(s['path']) and not s['loss']
        assert s['loss'] is not (s['text'] in inserted or is_prefix), s
    for number in (1, 2):
        block = [s for s in row['segments'] if s['block'] == number]
        assert block[0]['text'] == '<Parallel>' and block[-1]['text'] == '</Summary>'
        assert [s['text'] for s in block if s['path'] is None][:6] == [
            '<Parallel>', 'branches=', str(summary['blocks'][number - 1]['branches']), '<Plan>',
            block[4]['text'], '</Plan>']
    text = ''.join(s['text'] for s in row['segments'])
    assert text.count('<Parallel>') == 2 and text.index('</Summary>') < text.rindex('<Parallel>')
    assert '\n\nNow I need to count the integers in each negative interval within the range.\n\n<Parallel>' in text
    assert text.endswith('</think>\n\nThere are \\boxed{8} such integers.<|im_end|>')
    assert row['provenance']['correct'] is True and stats['per_id'][IDS[0]]['correct'] is True
    assert row['provenance']['plan2']['decision'] == 'FORK'
    # the summary sample carrying a Final Answer marker was rejected
    assert row['provenance']['summary_samples']['1'][0]['reason'] == 'summary_final_marker'

    # tokenizes with the tags added (the trainer's view): graph spans for both blocks
    tok = build_tiny_tokenizer()
    ensure_tags(tok, build_tiny_model(tok))
    sample = D.tokenize_row(row, D.Vocab(tok))
    assert sorted({s.block for s in sample['spans']}) == [1, 2]

    # B: pool block reused after the coverage audit, planner 2 said NO_FORK -> single block
    single = by_id[IDS[1]]
    assert single['provenance']['block1_source'] == 'pool' and single['provenance']['blocks'] == 1
    assert len(D.validate_row(single)['blocks']) == 1 and single['provenance']['plan2']['decision'] == 'NO_FORK'
    assert single['provenance']['correct'] is True

    # stats, traces
    info = stats['per_id'][IDS[0]]
    assert info['blocks'] == 2 and info['block2_decision'] == 'FORK' and info['n_tokens'] > 0
    assert 0 < info['critical_path_tokens'] < info['sampled_tokens']
    assert len(info['lengths']['branches1']) == 4 and len(info['lengths']['branches2']) == 2
    assert stats['two_block_records'] == 1 and stats['block2'] == {'FORK': 1, 'NO_FORK': 1, 'no_block1_plan': 1}
    assert stats['gold_in_prompts']['oracle'] == [] and stats['gold_oracle_in_any_prompt'] is False
    md = (out_dir / 'traces' / f'{IDS[0]}.md').read_text()
    assert '[[branches=]]4[[<Plan>]]' in md and '[[<Path>]][[1:]]' in md and '[[</Parallel>]][[<Summary>]]' in md
    assert md.count('[[branches=]]') == 2 and '`````text' in md
    assert IDS[0] in (out_dir / 'traces.md').read_text()
    saved = [json.loads(line) for line in (out_dir / 'records.jsonl').read_text().splitlines()]
    assert [r['id'] for r in saved] == [f'{IDS[0]}#multiblock', f'{IDS[1]}#multiblock']


def test_no_gold_in_any_prompt(pool, tmp_path):
    _, _, backends = run_all(pool, tmp_path / 'probe')
    prompts = [r['prompt'] for b in backends.values() for r in b.requests]
    calls = [json.loads(line) for line in (tmp_path / 'probe' / 'calls.jsonl').read_text().splitlines()]
    assert len(calls) == len(prompts) and prompts
    for prompt in prompts:
        assert 'GOLDSENTINEL' not in prompt
    assert not any('4173' in p for p in prompts)  # B's gold answer (not in its question)


def test_planner2_prompt_contents(pool, tmp_path):
    _, _, backends = run_all(pool, tmp_path / 'probe')
    plan2 = [r for r in backends['plan2'].requests if r['key'].startswith(f'plan2|{IDS[0]}|')]
    assert len(plan2) == 1
    prompt = plan2[0]['prompt']
    assert M.SECOND_BLOCK_NOTE in prompt and M.PLANNER_SYS in prompt and M.RAW_PLANNER_RULES in prompt
    assert 'Do not redo, repeat, re-check or extend the work of the first step' in prompt
    user = prompt.split('Problem:\n', 1)[1]
    assert user.startswith(Q1130)  # question only, no instruction suffix
    assert 'Okay, so I need to solve this' in user  # prefix
    assert 'First parallel step (cases)' in user
    for item in PLAN1_1130['assignments']:
        assert item in user
    for result in ('Result: negative', 'Result: positive'):
        assert result in user
    assert 'The product is negative for n < -8 and for -4 < n < 2, positive elsewhere.' in user  # summary 1
    assert 'Now I need to count the integers in each negative interval within the range.' in user  # paragraph
    assert 'I work on part' not in user and BODY_ONLY not in user  # no branch bodies
    assert '<Parallel>' not in user and '<Summary>' not in user and '\\boxed' not in user
    assert 'GOLDSENTINEL' not in prompt
    # the block-1 planner prompt has no second-block note
    plan1 = [r for r in backends['plan1'].requests if r['key'].startswith('plan1|')]
    assert plan1 and all(M.SECOND_BLOCK_NOTE not in r['prompt'] for r in plan1)
    # block-2 branches got the standalone mini-problems
    branch2 = [r for r in backends['student2'].requests if r['key'].startswith('branch2|')]
    assert [PLAN2_1130['subproblems'][0] in branch2[0]['prompt'], PLAN2_1130['subproblems'][1] in branch2[1]['prompt']
            ] == [True, True]
    # the final call of a forked item continues the causal serialized text through block 2's </Summary>
    final = [r for r in backends['student2'].requests if r['key'] == f'final|{IDS[0]}'][0]
    assert final['prompt'].endswith('8 integers.</Summary>') and final['prompt'].count('<Parallel>') == 2
    cont = [r for r in backends['student1'].requests if r['key'].startswith('continuation|')][0]
    assert cont['prompt'].endswith('</Summary>\n\n') and cont['params']['stop'] == ['\n\n', '</think>']
    assert cont['params']['max_tokens'] == 400


def test_merger_and_continuation_requests(pool, tmp_path):
    _, _, backends = run_all(pool, tmp_path / 'probe')
    merger = [r for r in backends['student1'].requests if r['key'].startswith('summary1|')]
    for r in merger:
        assert M.BLOCK_SUMMARY_NOTE[1] in r['prompt'] and r['params']['max_tokens'] == 1024
        assert BODY_ONLY not in r['prompt'] and 'Result:' in r['prompt']
        assert r['prompt'].endswith('<think>\n\n</think>\n\n')  # non-thinking
    merger2 = [r for r in backends['student2'].requests if r['key'].startswith('summary2|')]
    assert len(merger2) == 1 and M.BLOCK_SUMMARY_NOTE[2] in merger2[0]['prompt']
    assert 'Result: 3' in merger2[0]['prompt'] and 'Result: 5' in merger2[0]['prompt']


def test_resume_skips_finished_stages(pool, tmp_path, monkeypatch):
    out_dir = tmp_path / 'probe'
    run_all(pool, out_dir)
    calls = []
    monkeypatch.setattr(M.subprocess, 'run', lambda *a, **k: calls.append(a))
    monkeypatch.setattr(M, 'load_tokenizer', build_tiny_tokenizer)
    args = M.parse_args(['run', '--pool', str(pool), '--out', str(out_dir)])
    records, stats = M.cmd_run(args)
    assert calls == [] and len(records) == 2


@pytest.mark.skipif(not (POOL / 'all.raw.jsonl').exists(), reason='pool not reachable')
def test_default_ids_in_real_pool(tmp_path):
    items = {i['id']: i for i in M.select(POOL, tmp_path / 'o', list(M.DEFAULT_IDS), list(M.FORCE_REGENERATE),
                                          dict(M.DEFAULTS))}
    assert list(items) == list(M.DEFAULT_IDS)
    assert items['math-intermediate_algebra-train-1130']['pool_reject'] == ['forced_regenerate']
    assert items['math-intermediate_algebra-train-1130']['pool_block']['plan']['branches'] == 3  # misses (2, oo)
    for item in items.values():
        assert item['prefix'].endswith('\n\n') and contract.plain_text(item['prefix'])
        assert item['q']['src'] in ('math', 'countdown')
        if item['reuse_candidate']:
            assert all(r and r.startswith('Result: ') for r in item['pool_block']['results'])
