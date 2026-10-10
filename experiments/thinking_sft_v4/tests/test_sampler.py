"""Graph sampler on CPU with a tiny random Qwen3 and a char-level tokenizer (HFBackend only).

cd experiments/thinking_sft_v4 && python3 -m pytest -q tests/test_sampler.py
"""
import string
import sys
from pathlib import Path

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import contract  # noqa: E402
import graph_sampler as gs  # noqa: E402

CHAT_TEMPLATE = (
    "{% for m in messages %}<|im_start|>{{ m['role'] }}\n{{ m['content'] }}<|im_end|>\n{% endfor %}"
    "{% if add_generation_prompt %}<|im_start|>assistant\n"
    "{% if enable_thinking is defined and enable_thinking is false %}<think>\n\n</think>\n\n{% endif %}{% endif %}")


def build_tokenizer():
    """Char-level tokenizer with Qwen3's control tokens (and <think>/</think> as non-special added tokens), then
    the eight tags added as Qwen3 gets them (prepare_think.py: add_special_tokens in contract.TAGS order)."""
    from tokenizers import Tokenizer, decoders, models
    from transformers import PreTrainedTokenizerFast
    chars = sorted(set(string.printable) - set('\x0b\x0c\r'))
    vocab = {'<unk>': 0, **{c: i + 1 for i, c in enumerate(chars)}}
    core = Tokenizer(models.BPE(vocab=vocab, merges=[], unk_token='<unk>'))
    core.decoder = decoders.Fuse()
    tokenizer = PreTrainedTokenizerFast(tokenizer_object=core, unk_token='<unk>', eos_token='<|im_end|>',
                                        pad_token='<|endoftext|>')
    tokenizer.add_special_tokens({'additional_special_tokens': ['<|im_start|>', '<|im_end|>']})
    tokenizer.add_tokens(['<think>', '</think>'])
    tokenizer.add_special_tokens({'additional_special_tokens': list(contract.TAGS)})
    tokenizer.chat_template = CHAT_TEMPLATE
    return tokenizer


def build_model(tokenizer, seed=0):
    from transformers import Qwen3Config, Qwen3ForCausalLM
    torch.manual_seed(seed)
    config = Qwen3Config(vocab_size=len(tokenizer) + 7, hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                         num_attention_heads=4, num_key_value_heads=2, head_dim=16, max_position_embeddings=1024,
                         tie_word_embeddings=True, sliding_window=None, attn_implementation='sdpa')
    model = Qwen3ForCausalLM(config).eval()
    with torch.no_grad():  # larger logits than the 0.02 init so greedy choices are not near-ties
        model.model.embed_tokens.weight.normal_(0, 0.3)
    return model


class Boosted(torch.nn.Module):
    """A model whose logits get a fixed additive vector (to make tags attractive)."""

    def __init__(self, model, boost):
        super().__init__()
        self.inner, self.boost = model, boost
        self.config = model.config

    def forward(self, **kwargs):
        out = self.inner(**kwargs)
        out.logits = out.logits + self.boost.to(out.logits.dtype)
        return out


class Recording:
    """Backend wrapper that keeps every (request, result)."""
    graph = True

    def __init__(self, backend):
        self.backend, self.log = backend, []

    def generate(self, requests, sampling):
        results = self.backend.generate(requests, sampling)
        self.log.extend(zip(requests, results))
        return results


GREEDY = gs.Sampling(temperature=0.0)


@pytest.fixture(scope='module')
def tok():
    return build_tokenizer()


@pytest.fixture(scope='module')
def model(tok):
    return build_model(tok)


def enc(tok, text):
    return tok.encode(text, add_special_tokens=False)


def tid(tok, token):
    ids = enc(tok, token)
    assert len(ids) == 1, token
    return ids[0]


def summary_boost(tok, model, value=50.0):
    boost = torch.zeros(model.config.vocab_size)
    boost[tid(tok, '</Summary>')] = value  # summary closes at once; every other node suppresses it (-100)
    return Boosted(model, boost)


def brute_logits(net, ids, spans):
    """Full-sequence graph forward of serialized ids with the contract mask and positions."""
    length = len(ids)
    allowed = contract.graph_attention_mask(length, spans)
    mask = torch.zeros(1, 1, length, length).masked_fill(~allowed, torch.finfo(torch.float32).min)
    positions = torch.tensor([contract.graph_positions(length, spans)])
    with torch.no_grad():
        return net(input_ids=torch.tensor([ids]), attention_mask=mask, position_ids=positions).logits[0].float()


def causal_logits(net, ids):
    with torch.no_grad():
        return net(input_ids=torch.tensor([ids])).logits[0].float()


def forcing(tok, table):
    """force hook from {(stage, block, path): text or ids}; texts are encoded, tags in them become their ids."""
    def force(index, stage, block, path):
        value = table.get((index, stage, block, path), table.get((stage, block, path)))
        if value is None:
            return None
        return enc(tok, value) if isinstance(value, str) else list(value)
    return force


def test_tiny_tokenizer_matches_contract(tok):
    ids = contract.token_ids(tok)
    assert len(set(ids.values())) == len(contract.TAGS) + len(contract.NODE_CONTROL)
    assert contract.count_ids(tok) == tuple(tid(tok, c) for c in '234')
    assert enc(tok, '<Path>1: x</Path>') == [ids['<Path>'], *enc(tok, '1:'), *enc(tok, ' x'), ids['</Path>']]
    prompt = tok.apply_chat_template([{'role': 'user', 'content': 'q'}], tokenize=False, add_generation_prompt=True,
                                     enable_thinking=True)
    assert prompt == '<|im_start|>user\nq<|im_end|>\n<|im_start|>assistant\n'
    assert gs.eos_ids(tok) == tuple(sorted({tid(tok, '<|im_end|>'), tid(tok, '<|endoftext|>')}))


# ------------------------------------------------------------------------------------------------ a) exactness

def run_exact(tok, net, table, prompts, max_blocks=1, budget=90):
    backend = Recording(gs.HFBackend(net, record_logits=True))
    sampler = gs.GraphSampler(tok, backend, sampling=GREEDY, max_blocks=max_blocks, budget=budget, branch_cap=9,
                              force=forcing(tok, table))
    return sampler.generate(prompts), backend.log


FORK = {('main', 1, None): '<think>\nLet x.<Parallel>', ('count', 1, None): '2',
        ('plan', 1, None): 'decompose\n1: a\n2: b\n</Plan>'}


def check_against_brute(tok, net, reports, log):
    """Every sampled token's recorded logits equal the full graph forward of the final serialization."""
    full = {}
    for report in reports:
        ids = report_ids(tok, report)
        full[tuple(ids)] = brute_logits(net, ids, gs.serialized_spans(report))
    checked = {'graph': 0, 'causal': 0}
    for request, result in log:
        # find the report containing this call: its context (minus a branch prefix) is a prefix of the ids
        for ids, logits in full.items():
            position = locate(list(ids), request, result)
            if position is None:
                continue
            got = result.logits
            want = logits[position - 1:position - 1 + len(result.tokens)]
            torch.testing.assert_close(got, want, atol=1e-5, rtol=0)
            checked['graph' if request.spans else 'causal'] += 1
            if not request.spans:  # a causal call also equals an independent plain causal forward
                own = causal_logits(net, request.context + result.tokens[:-1])[len(request.context) - 1:]
                torch.testing.assert_close(got, own, atol=1e-5, rtol=0)
            break
        else:
            raise AssertionError(f'call not found in any serialization: node {request.node}')
    return checked


def report_ids(tok, report):
    return report['prompt_ids'] + report['token_ids']


def locate(ids, request, result):
    """Index in ids of the call's first sampled token, or None. A branch call's context is the shared prefix +
    its own <Path> i: (the other branches sit in between in the serialization)."""
    tokens = result.tokens
    if request.node == contract.PATH:
        prefix, own = request.context[:-3], request.context[-3:]
        if ids[:len(prefix)] != prefix:
            return None
        index = len(prefix)
        while index < len(ids):
            if ids[index:index + 3] == own:
                start = index + 3
                body = ids[start:start + len(tokens)]
                if body[:len(tokens) - 1] == tokens[:-1]:
                    return start
            index += 1
        return None
    if ids[:len(request.context)] != request.context:
        return None
    start = len(request.context)
    if ids[start:start + len(tokens) - 1] != tokens[:-1]:
        return None
    return start


@pytest.fixture(scope='module')
def exact_run(tok, model):
    net = summary_boost(tok, model)
    reports, log = run_exact(tok, net, FORK, ['What is 2+2?', 'Find the sum of the first ten primes, please.'])
    return net, reports, log


def test_exact_graph_logits_match_brute_force(tok, exact_run):
    net, reports, log = exact_run
    for report in reports:
        assert report['forked'] and report['blocks'][0]['plan_status'] == contract.VALID
        assert len(report['spans']) == 2
        assert report['blocks'][0]['summary_stop'] == 'close'
    checked = check_against_brute(tok, net, reports, log)
    # per sample: 2 branches (causal) + summary + main after it (graph)
    assert checked == {'causal': 4, 'graph': 4}


def test_exact_second_block_runs_on_the_graph(tok, model):
    net = summary_boost(tok, model)
    table = dict(FORK)
    table.update({('main', 2, None): ' so<Parallel>', ('count', 2, None): '3',
                  ('plan', 2, None): 'cases\n1: p\n2: q\n3: r\n</Plan>'})
    reports, log = run_exact(tok, net, table, ['Solve x^2=4.'], max_blocks=2, budget=150)
    report = reports[0]
    assert [b['N'] for b in report['blocks']] == [2, 3]
    assert [s[2:] for s in report['spans']] == [[1, 1], [1, 2], [2, 1], [2, 2], [2, 3]]
    checked = check_against_brute(tok, net, reports, log)
    # block 1 branches causal; summary 1, block-2 branches (prefix holds block 1), summary 2, final main: graph
    assert checked == {'causal': 2, 'graph': 1 + 3 + 1 + 1}
    assert all(r.spans for r, _ in log if r.node == contract.PATH and r.context.count(tid(tok, '<Plan>')) == 2)


def test_branches_are_independent(tok, model):
    net = summary_boost(tok, model)
    base, log = run_exact(tok, net, FORK, ['What is 2+2?'])
    other = dict(FORK)
    other[('path', 1, 1)] = ' totally different branch one</Path>'
    changed, log2 = run_exact(tok, net, other, ['What is 2+2?'])

    def branch(log, path):
        return [(r, res) for r, res in log if r.node == contract.PATH and r.context[-2:] == enc(tok, f'{path}:')]

    (r2, res2), = branch(log, 2)
    (r2b, res2b), = branch(log2, 2)
    assert res2.tokens == res2b.tokens
    torch.testing.assert_close(res2.logits, res2b.logits, atol=1e-5, rtol=0)  # batch shapes differ
    assert base[0]['token_ids'] != changed[0]['token_ids']
    # the summary does see branch 1
    s1 = [res for r, res in log if r.node == contract.SUMMARY][0]
    s2 = [res for r, res in log2 if r.node == contract.SUMMARY][0]
    assert not torch.allclose(s1.logits[0], s2.logits[0])


# ------------------------------------------------------------------------------------------------ b) suppression

def all_boost(tok, model, value=30.0, extra=None):
    boost = torch.zeros(model.config.vocab_size)
    for token in contract.TAGS + contract.NODE_CONTROL:
        boost[tid(tok, token)] = value
    for token, add in (extra or {}).items():
        boost[tid(tok, token)] += add
    return Boosted(model, boost)


@pytest.mark.parametrize('node', [contract.MAIN_OPEN, contract.MAIN_CLOSED, contract.PLAN, contract.PATH,
                                  contract.SUMMARY])
def test_nodes_never_sample_suppressed_tokens(tok, model, node):
    ids, counts = contract.token_ids(tok), contract.count_ids(tok)
    backend = gs.HFBackend(all_boost(tok, model))
    context = gs.chat_prompt_ids(tok, 'q') + enc(tok, '<think>\nhm')
    requests = [gs.Request(context, node, (), 40, seed, contract.sampling_constraint(node, ids, counts))
                for seed in range(4)]
    sampled = [t for r in backend.generate(requests, gs.Sampling(temperature=1.0, top_p=1.0, top_k=0))
               for t in r.tokens]
    suppressed = {ids[t] for t in contract.suppressed_tokens(node)}
    assert not suppressed & set(sampled)
    closer = contract.SAMPLED_TAG[node]
    if closer is not None:  # the boost works: the node's own tag is sampled
        assert ids[closer] in sampled
    if node in (contract.MAIN_OPEN, contract.MAIN_CLOSED):  # main may write <think>/</think>
        assert {ids['<think>'], ids['</think>']} & set(sampled)


def test_count_samples_only_counts(tok, model):
    ids, counts = contract.token_ids(tok), contract.count_ids(tok)
    backend = gs.HFBackend(all_boost(tok, model))
    context = gs.chat_prompt_ids(tok, 'q') + enc(tok, '<think>\n<Parallel>branches=')
    requests = [gs.Request(context, contract.COUNT, (), 1, seed, contract.sampling_constraint(contract.COUNT, ids,
                                                                                               counts))
                for seed in range(60)]
    sampled = [t for r in backend.generate(requests, gs.Sampling(temperature=1.0, top_p=1.0, top_k=0))
               for t in r.tokens]
    assert len(sampled) == 60 and set(sampled) <= set(counts) and len(set(sampled)) >= 2
    # end to end: a boosted model forks at once and COUNT still picks a digit
    sampler = gs.GraphSampler(tok, gs.HFBackend(all_boost(tok, model, extra={'<Parallel>': 10})),
                              sampling=gs.Sampling(1.0, 1.0, 0), budget=40, branch_cap=5)
    for report in sampler.generate(['a', 'b', 'c'], seeds=[1, 2, 3]):
        assert report['blocks'] and report['blocks'][0]['N'] in (2, 3, 4)
        assert report['calls'][1]['node'] == contract.COUNT and report['calls'][1]['sampled'] == 1


def test_sequential_mode_never_forks(tok, model):
    sampler = gs.GraphSampler(tok, gs.HFBackend(all_boost(tok, model)), sampling=gs.Sampling(1.0, 1.0, 0),
                              budget=30)
    ids = contract.token_ids(tok)
    for report in sampler.generate(['a', 'b'], allow_parallel=False):
        assert not report['forked'] and not set(report['token_ids']) & {ids[t] for t in contract.TAGS}
        assert report['status'] == gs.TRAJECTORY_BUDGET and report['T'] == 30 == report['D']


# ------------------------------------------------------------------------------------------------ c) statuses

def forced_sampler(tok, model, table, **kwargs):
    kwargs.setdefault('budget', 80)
    return gs.GraphSampler(tok, gs.HFBackend(model), sampling=GREEDY, force=forcing(tok, table), **kwargs)


def test_invalid_plan_ends_the_trajectory(tok, model):
    table = dict(FORK)
    table[('count', 1, None)] = '3'  # plan has 2 lines
    report = forced_sampler(tok, model, table).generate(['q'])[0]
    assert report['status'] == contract.INVALID_PLAN == report['blocks'][0]['plan_status']
    assert report['text'].endswith('<Parallel>branches=3<Plan>decompose\n1: a\n2: b\n</Plan>')
    assert not report['spans']


def test_plan_eos_and_budget(tok, model):
    table = dict(FORK)
    table[('plan', 1, None)] = 'decompose\n1: a<|im_end|>'
    assert forced_sampler(tok, model, table).generate(['q'])[0]['status'] == contract.PLAN_INCOMPLETE
    table = {k: v for k, v in FORK.items() if k[0] != 'plan'}  # sampled plan of a random model never closes
    report = forced_sampler(tok, model, table, plan_cap=7).generate(['q'])[0]
    assert report['status'] == contract.PLAN_BUDGET_EXHAUSTED and report['blocks'][0]['plan_tokens'] == 7


def test_eos_in_branch_is_written_as_close(tok, model):
    table = dict(FORK)
    table[('path', 1, 1)] = ' first<|im_end|>'
    table[('path', 1, 2)] = ' second</Path>'
    report = forced_sampler(tok, model, summary_boost_table(table)).generate(['q'])[0]
    assert '<Path>1: first</Path><Path>2: second</Path></Parallel><Summary>' in report['text']
    assert [b['stop'] for b in report['blocks'][0]['branches']] == ['eos', 'close']
    assert '<|im_end|>' not in report['text'].split('<Summary>')[0]


def summary_boost_table(table):
    table = dict(table)
    table[('summary', 1, None)] = ' ok</Summary>'
    return table


def test_branch_cap_appends_close(tok, model):
    report = forced_sampler(tok, model, summary_boost_table(FORK), branch_cap=4).generate(['q'])[0]
    block = report['blocks'][0]
    assert [b['stop'] for b in block['branches']] == ['cap', 'cap'] and [b['sampled'] for b in block['branches']] == [4, 4]
    for start, end, _, _ in report['spans']:
        assert end - start == 1 + 2 + 4 + 1  # <Path> i: 4 sampled </Path>(inserted)


# ------------------------------------------------------------------------------------------------ d) serialization

def test_forced_trajectory_serializes_like_format_block(tok, model):
    table = {('main', 1, None): '<think>\nhi\n\n<Parallel>', ('count', 1, None): '2',
             ('plan', 1, None): 'cases\n1: x\n2: y\n</Plan>', ('path', 1, 1): ' one</Path>',
             ('path', 1, 2): ' two<|im_end|>', ('summary', 1, None): ' sum</Summary>',
             ('main', 2, None): '</think>\n\nThe answer is \\boxed{4}.<|im_end|>'}
    report = forced_sampler(tok, model, table, budget=200).generate(['q'])[0]
    block = contract.format_block('cases', ['x', 'y'], [' one', ' two'], ' sum')
    assert report['text'] == '<think>\nhi\n\n' + block + '</think>\n\nThe answer is \\boxed{4}.<|im_end|>'
    assert report['status'] == gs.COMPLETE and report['answer'] == 'The answer is \\boxed{4}.'
    # ids are the segment-wise encoding SFT uses (tags single ids, inserted pieces encoded on their own)
    segments = ['<think>', '\nhi\n\n', '<Parallel>', 'branches=', '2', '<Plan>', 'cases\n1: x\n2: y\n', '</Plan>',
                '<Path>', '1:', ' one', '</Path>', '<Path>', '2:', ' two', '</Path>', '</Parallel>', '<Summary>',
                ' sum', '</Summary>', '</think>', '\n\nThe answer is \\boxed{4}.', '<|im_end|>']
    assert report['token_ids'] == [t for s in segments for t in enc(tok, s)]
    lengths = dict(main1=len(enc(tok, '<think>\nhi\n\n<Parallel>')), plan=len(enc(tok, 'cases\n1: x\n2: y\n</Plan>')),
                   p1=len(enc(tok, ' one</Path>')), p2=len(enc(tok, ' two<|im_end|>')),
                   summary=len(enc(tok, ' sum</Summary>')),
                   main2=len(enc(tok, '</think>\n\nThe answer is \\boxed{4}.<|im_end|>')))
    assert report['T'] == sum(lengths.values()) + 1
    assert report['D'] == report['T'] - min(lengths['p1'], lengths['p2'])
    assert report['blocks'][0]['kind'] == 'cases' and report['blocks'][0]['items'] == ['x', 'y']


# ------------------------------------------------------------------------------------------------ e) batching

def test_batched_equals_batch_size_one(tok, model):
    net = summary_boost(tok, model)
    prompts = ['a', 'What is the remainder of 7^100 mod 5?', 'Compute 12*13.']
    outputs = []
    for max_batch in (1, 8):
        sampler = gs.GraphSampler(tok, gs.HFBackend(net, max_batch=max_batch), sampling=GREEDY, budget=70,
                                  branch_cap=8, force=forcing(tok, {
                                      (0, 'main', 1, None): '<think>\nok<Parallel>', (1, 'main', 1, None): '<think>\nhm',
                                      ('count', 1, None): '2', ('plan', 1, None): 'methods\n1: u\n2: v\n</Plan>'}))
        outputs.append([(r['token_ids'], r['status']) for r in sampler.generate(prompts)]
                       + [(r['token_ids'], r['status']) for r in sampler.generate(prompts, allow_parallel=False)])
    assert outputs[0] == outputs[1]
    assert outputs[0][0][0] != outputs[0][2][0]


# ------------------------------------------------------------------------------------------------ eval CLI

def test_eval_cli_end_to_end(tok, model, tmp_path):
    import json
    import eval_graph
    ckpt = tmp_path / 'ckpt'
    tok.save_pretrained(ckpt)
    model.save_pretrained(ckpt)
    tasks, gold = tmp_path / 'tasks.jsonl', tmp_path / 'gold.jsonl'
    tasks.write_text('\n'.join(json.dumps(r) for r in [dict(id='a', problem='1+1?'), dict(id='b', question='2+2?'),
                                                        dict(id='c', prompt=[{'role': 'user', 'content': '3+3?'}])]))
    gold.write_text('\n'.join(json.dumps(r) for r in [dict(id='a', answer='2'),
                                                       dict(id='b', oracle='So it is $\\boxed{4}$.'),
                                                       dict(id='c', final='6')]))
    out = tmp_path / 'out'
    reports = eval_graph.main(['--model', str(ckpt), '--tasks', str(tasks), '--gold', str(gold), '--backend', 'hf',
                               '--mode', 'both', '--budget', '24', '--branch-cap', '6', '--out', str(out)])
    assert reports['graph']['n'] == reports['sequential']['n'] == 3
    assert {'accuracy', 'fork_rate', 'valid_plan_rate', 'N_histogram', 'kind_histogram', 'mean_T', 'mean_D',
            'D_over_T', 'branch_length', 'status', 'truncation_rate'} <= set(reports['graph'])
    rows = [json.loads(line) for line in (out / 'samples_graph.jsonl').read_text().splitlines()]
    assert [r['gold'] for r in rows] == ['2', '4', '6']
    assert json.loads((out / 'report.json').read_text())['sequential']['fork_rate'] == 0
    assert (out / 'samples.md').read_text().startswith('# eval_graph')


def test_grading_helpers():
    import eval_graph as ev
    assert ev.gold_of({'oracle': 'Thus \\boxed{\\frac{1}{2}} and \\boxed{3}.'}) == '3'
    assert ev.gold_of({'reward_model': {'ground_truth': '7'}}) == '7'
    text = '<think>\n<Parallel>branches=2<Plan>x</Plan><Path>1: \\boxed{9}</Path></Parallel>' \
           '<Summary>s</Summary> ok</think>\n\nSo \\boxed{\\dfrac{1}{2}}.<|im_end|>'
    pred = ev.extract_answer(ev.answer_region(text))
    assert pred == '\\dfrac{1}{2}' and ev.equivalent(pred, '\\dfrac{1}{2}') and ev.equivalent('4', ' 4 ')
    if ev.mv_verify is not None:  # symbolic equivalence on the VM, as in the RL reward
        assert ev.equivalent(pred, '\\frac{1}{2}') and ev.equivalent('0.5', '\\frac12')
    assert ev.answer_region('<think> unfinished') is None and not ev.equivalent(None, '1')
    assert ev.extract_answer(ev.answer_region('</think>\n<Parallel> \\boxed{5}')) is None


# ------------------------------------------------------------------------------------------------ shared fixtures

def test_with_shared_bpe_fixtures():
    """Same exactness and serialization checks on the byte-level BPE tokenizer of tests/tiny.py with the tags
    added by tags.ensure_tags (skipped if implementer A's modules are absent)."""
    tiny = pytest.importorskip('tiny')
    tags = pytest.importorskip('tags')
    tokenizer = tiny.build_tiny_tokenizer()
    model = tiny.build_tiny_model(tokenizer)
    tags.ensure_tags(tokenizer, model)
    net = summary_boost(tokenizer, model)
    reports, log = run_exact(tokenizer, net, FORK, ['What is 2+2?', 'Let x + 2 = 5. Find x, please.'])
    assert all(r['blocks'][0]['plan_status'] == contract.VALID for r in reports)
    checked = check_against_brute(tokenizer, net, reports, log)
    assert checked == {'causal': 4, 'graph': 4}
    table = {('main', 1, None): '<think>\nOkay, cases.\n\n<Parallel>', ('count', 1, None): '2',
             ('plan', 1, None): 'cases\n1: x > 0\n2: x <= 0\n</Plan>', ('path', 1, 1): ' then f(x) = x</Path>',
             ('path', 1, 2): ' then f(x) = -x<|im_end|>', ('summary', 1, None): ' Both agree.</Summary>',
             ('main', 2, None): '</think>\n\nThe answer is \\boxed{3}.<|im_end|>'}
    report = forced_sampler(tokenizer, model, table, budget=300).generate(['q'])[0]
    block = contract.format_block('cases', ['x > 0', 'x <= 0'], [' then f(x) = x', ' then f(x) = -x'], ' Both agree.')
    assert report['text'] == '<think>\nOkay, cases.\n\n' + block + '</think>\n\nThe answer is \\boxed{3}.<|im_end|>'
    assert report['status'] == gs.COMPLETE


# ------------------------------------------------------------------------------------------------ review fixes

def test_budget_counts_inserted_tokens_like_the_rl_loop(tok, model):
    """room = budget - len(response), inserted tokens included (parallel_thinking_loop_v3: remaining / room -
    len(out['ids'])); each branch gets min(branch_cap, left - len(<Path> i:) - 1)."""
    main, plan = '<think>\nLet x.<Parallel>', 'decompose\n1: a\n2: b\n</Plan>'
    head = len(enc(tok, main)) + len(enc(tok, 'branches=')) + 1 + 1  # main, branches=, count, <Plan>
    # the plan gets exactly the 5 response tokens left after the inserted branches= and <Plan>
    table = {k: v for k, v in FORK.items() if k[0] != 'plan'}
    table[('plan', 1, None)] = plan
    report = forced_sampler(tok, model, table, budget=head + 5).generate(['q'])[0]
    assert report['status'] == contract.PLAN_BUDGET_EXHAUSTED and report['blocks'][0]['plan_tokens'] == 5
    assert len(report['token_ids']) == head + 5
    # 6 tokens left after </Plan>: every branch gets 6 - len(<Path>i:) - 1 = 2 (RL: left - len(prefix) - 1)
    prefix_len = len(enc(tok, '<Path>1:'))
    table = dict(FORK)
    table.update({('path', 1, 1): ' a long first branch</Path>', ('path', 1, 2): ' a long second branch</Path>'})
    budget = head + len(enc(tok, plan)) + 6
    report = forced_sampler(tok, model, table, budget=budget, branch_cap=50).generate(['q'])[0]
    block = report['blocks'][0]
    assert [b['sampled'] for b in block['branches']] == [6 - prefix_len - 1] * 2
    assert [b['stop'] for b in block['branches']] == ['budget', 'budget']
    for start, end, _, _ in report['spans']:
        assert end - start == 6  # <Path> i: 2 sampled </Path>(inserted): fits the room exactly
    assert report['status'] == gs.TRAJECTORY_BUDGET and block['summary_tokens'] is None  # no room for a summary
    # a main call is capped by the response length (inserted tokens of the block included)
    table = summary_boost_table(FORK)
    table[('main', 2, None)] = ' and then a very long continuation of the main chain'
    report = forced_sampler(tok, model, table, budget=80, branch_cap=4).generate(['q'])[0]
    assert report['status'] == gs.TRAJECTORY_BUDGET and len(report['token_ids']) == 80


class EmptyCount:
    """Backend that returns no tokens for COUNT, as VLLMBackend does when the context fills max_model_len."""
    graph = True

    def __init__(self, backend):
        self.backend = backend

    def generate(self, requests, sampling):
        results = self.backend.generate(requests, sampling)
        return [gs.Result([]) if r.node == contract.COUNT else res for r, res in zip(requests, results)]


def test_count_without_room_in_the_backend_ends_the_trajectory(tok, model):
    table = {('main', 1, None): FORK[('main', 1, None)]}
    sampler = gs.GraphSampler(tok, EmptyCount(gs.HFBackend(model)), sampling=GREEDY, budget=80,
                              force=forcing(tok, table))
    report = sampler.generate(['q', 'r'])
    assert [r['status'] for r in report] == [contract.PLAN_BUDGET_EXHAUSTED] * 2
    assert all(r['blocks'][0]['plan_status'] == contract.PLAN_BUDGET_EXHAUSTED for r in report)


def test_grading_matches_the_rl_reward():
    import eval_graph as ev
    region = ev.answer_region
    # extraction: last '\boxed{' with matched braces, as math_dapo.last_boxed_only_string + remove_boxed
    assert ev.extract_answer(region('</think>\\boxed{5} then \\fbox{6}')) == '5'
    assert ev.extract_answer(region('</think>answer \\boxed{12}. Note: \\boxed is a macro')) == '12'
    assert ev.extract_answer(region('</think>\\boxed 5 and {x}')) is None
    assert ev.extract_answer(region('</think>Final Answer: 7 ')) == '7 '
    if ev.MATH_DAPO is not None:
        for text in ('\\boxed{a{b}c} and \\boxed{\\frac{1}{2}}', 'x', '\\boxed{unclosed', '\\boxed{}'):
            boxed = ev.MATH_DAPO.last_boxed_only_string(text)
            want = None if boxed is None else ev.MATH_DAPO.remove_boxed(boxed)
            assert ev.reward_boxed(text) == want
            saved, ev.MATH_DAPO = ev.MATH_DAPO, None
            try:
                assert ev.reward_boxed(text) == want  # the fallback copy agrees
            finally:
                ev.MATH_DAPO = saved
    # a plan failure gives c = 0 (parallel_think_cost: trajectory_status != 'ok'), trajectory_budget stays gradable
    text = '<think>\nx\n</think>\n\nSo \\boxed{4}<Parallel>branches=2<Plan>decompose\n1: a\n</Plan>'
    pred = ev.extract_answer(region(text))
    assert pred == '4'
    for status in ev.ENDED:
        assert ev.graded(dict(status=status), pred, '4') == (False, True)
    for status in (gs.COMPLETE, gs.TRAJECTORY_BUDGET):
        assert ev.graded(dict(status=status), pred, '4') == (True, True)


def test_gold_pairing_by_id(tmp_path):
    import json
    import eval_graph as ev

    def write(name, rows):
        path = tmp_path / name
        path.write_text('\n'.join(json.dumps(r) for r in rows))
        return path

    tasks = write('t.jsonl', [dict(unique_id='test/a/1.json', problem='p', answer='1'),
                              dict(unique_id='test/a/2.json', problem='q', answer='2')])
    gold = write('g.jsonl', [dict(unique_id='test/a/2.json', answer='2'), dict(unique_id='test/a/1.json', answer='1')])
    items = ev.load_items(tasks, gold)
    assert [(i['id'], i['question'], i['gold']) for i in items] == [('test/a/1.json', 'p', '1'),
                                                                     ('test/a/2.json', 'q', '2')]
    with pytest.raises(ValueError):  # ids on one side only: no silent pairing by order
        ev.load_items(tasks, write('g2.jsonl', [dict(answer='1'), dict(answer='2')]))
    with pytest.raises(ValueError):
        ev.load_items(tasks, write('g3.jsonl', [dict(unique_id='test/a/1.json', answer='1'),
                                                dict(unique_id='test/a/1.json', answer='2')]))
    plain = ev.load_items(write('t4.jsonl', [dict(problem='p'), dict(problem='q')]),
                          write('g4.jsonl', [dict(answer='1'), dict(answer='2')]))
    assert [i['gold'] for i in plain] == ['1', '2']  # neither file has ids: by order, announced


def test_rl_parquet_rows_are_used_verbatim(tmp_path):
    """prepare_think.py rows: templated chat prompt, reward_model.ground_truth, index (read as jsonl here; the VM
    reads the .parquet files with pyarrow)."""
    import json
    import eval_graph as ev
    templated = gs.DEFAULT_TEMPLATE.format(problem='What is 1+1?')
    row = dict(data_source='math500', prompt=[{'role': 'user', 'content': templated}], ability='math',
               reward_model={'ground_truth': '2', 'style': 'rule'}, extra_info={'index': 'test/a/1.json'},
               index='test/a/1.json')
    path = tmp_path / 'rl.jsonl'
    path.write_text(json.dumps(row))
    item, = ev.load_items(path)
    assert item == dict(id='test/a/1.json', question=templated, message=True, gold='2')
    bare, = ev.load_items(_write(tmp_path, [dict(id='q', problem='What is 1+1?', answer='2')]))
    assert not bare['message'] and bare['question'] == 'What is 1+1?'


def _write(tmp_path, rows):
    import json
    path = tmp_path / 'bare.jsonl'
    path.write_text('\n'.join(json.dumps(r) for r in rows))
    return path
