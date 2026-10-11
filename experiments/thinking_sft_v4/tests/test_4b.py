"""4B / 16k-token trainer changes and record selection on CPU with the tiny Qwen3 (tests/tiny.py).

chunked LM loss == full-logits loss (values and gradients), mask dtype/padding, the generator's block annotation,
--optim adamw8bit error, --memory-report, select_records.py rules/split/stats, vm_selftest tag-id reporting.
"""
import json
import sys
from argparse import Namespace
from pathlib import Path

import pytest
import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import exactness  # noqa: E402
import select_records  # noqa: E402
import sft_data as D  # noqa: E402
import sft_train  # noqa: E402
from common import contract  # noqa: E402
from test_sft import PROMPT, SEQUENTIAL, THREE, TWO, TWO_BLOCKS, make_rows, sample, tagged, write_jsonl  # noqa: E402
from tiny import build_tiny_model, build_tiny_tokenizer  # noqa: E402

ATOL = 1e-5


def full_logits_losses(model, batch):
    """The old full computation: (B, T, vocab) logits, shift, cross entropy at the loss targets."""
    logits = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'],
                   position_ids=batch['position_ids'], use_cache=False).logits
    target = batch['labels'][:, 1:]
    selection = target != D.IGNORE
    return F.cross_entropy(logits[:, :-1][selection].float(), target[selection], reduction='none'), selection


def losses_and_grads(model, batch, fn):
    model.zero_grad(set_to_none=True)
    losses, selection = fn(model, batch)
    (losses.sum() / losses.numel()).backward()
    grads = {name: p.grad.detach().clone() for name, p in model.named_parameters() if p.grad is not None}
    return losses.detach(), selection, grads


# ----------------------------------------------------------------------------------------- chunked LM loss

@pytest.mark.parametrize('grad_ckpt', [False, True], ids=['plain', 'grad_ckpt'])
@pytest.mark.parametrize('chunk', [1, 7, 64, 2048])
def test_chunked_loss_equals_full_logits_loss_and_gradients(chunk, grad_ckpt):
    tokenizer, model = tagged()
    samples = [sample(tokenizer, text, id=str(i)) for i, text in enumerate([TWO_BLOCKS, SEQUENTIAL, THREE])]
    batch = D.collate(samples, tokenizer.pad_token_id, pad_multiple=16)
    model.train()
    reference, ref_selection, ref_grads = losses_and_grads(model, batch, full_logits_losses)
    if grad_ckpt:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
    losses, selection, grads = losses_and_grads(
        model, batch, lambda m, b: sft_train.token_losses(m, b, chunk=chunk))
    assert torch.equal(selection, ref_selection) and losses.numel() == sum(s['n_loss'] for s in samples)
    torch.testing.assert_close(losses, reference, atol=ATOL, rtol=0)
    assert grads.keys() == ref_grads.keys() and len(grads) > 10
    assert 'model.embed_tokens.weight' in grads  # tied lm_head: the head's gradient lands here too
    for name in grads:
        torch.testing.assert_close(grads[name], ref_grads[name], atol=1e-6, rtol=1e-4, msg=name)


def test_chunked_loss_under_bf16_autocast_matches_full_logits():
    tokenizer, model = tagged()
    samples = [sample(tokenizer, text, id=str(i)) for i, text in enumerate([TWO_BLOCKS, SEQUENTIAL])]
    batch = D.collate(samples, tokenizer.pad_token_id, dtype=torch.bfloat16)
    model.train()
    with torch.autocast('cpu', dtype=torch.bfloat16):
        reference, _, ref_grads = losses_and_grads(model, batch, full_logits_losses)
        losses, _, grads = losses_and_grads(model, batch, lambda m, b: sft_train.token_losses(m, b, chunk=5))
    assert torch.isfinite(losses).all()
    torch.testing.assert_close(losses, reference, atol=2e-2, rtol=0)
    for name in grads:
        assert grads[name].dtype == torch.float32  # fp32 weights keep fp32 grads under autocast
        torch.testing.assert_close(grads[name], ref_grads[name], atol=2e-2, rtol=5e-2, msg=name)


def test_chunked_loss_without_loss_tokens_is_zero_with_grad():
    tokenizer, model = tagged()
    s = sample(tokenizer, SEQUENTIAL)
    s = dict(s, labels=[D.IGNORE] * s['length'], n_loss=0)
    losses, _ = sft_train.token_losses(model, D.collate([s], tokenizer.pad_token_id))
    assert losses.numel() == 0 and losses.sum().item() == 0.0


# ------------------------------------------------------------------------------------------------ the mask

def test_pad_multiple_rounds_length_and_keeps_losses():
    tokenizer, model = tagged()
    samples = [sample(tokenizer, text, id=str(i)) for i, text in enumerate([TWO, SEQUENTIAL])]
    plain = D.collate(samples, tokenizer.pad_token_id)
    padded = D.collate(samples, tokenizer.pad_token_id, pad_multiple=16)
    T = plain['input_ids'].size(1)
    assert padded['input_ids'].size(1) % 16 == 0 and padded['input_ids'].size(1) >= T
    assert padded['attention_mask'].shape[-2:] == (padded['input_ids'].size(1),) * 2
    torch.testing.assert_close(padded['attention_mask'][..., :T, :T], plain['attention_mask'])
    with torch.no_grad():
        a, _ = sft_train.token_losses(model, plain)
        b, _ = sft_train.token_losses(model, padded)
    torch.testing.assert_close(a, b, atol=ATOL, rtol=0)


def test_bf16_mask_is_built_in_dtype_and_survives_unmask_unattended():
    from transformers.modeling_attn_mask_utils import AttentionMaskConverter
    tokenizer, _ = tagged()
    a, b = sample(tokenizer, TWO_BLOCKS), sample(tokenizer, SEQUENTIAL)
    batch = D.collate([a, b], tokenizer.pad_token_id, dtype=torch.bfloat16, pad_multiple=16)
    mask = batch['attention_mask']
    assert mask.dtype == torch.bfloat16
    assert set(mask.unique().tolist()) == {0.0, torch.finfo(torch.bfloat16).min}
    assert torch.equal(mask[0, 0, :a['length'], :a['length']] == 0, contract.graph_attention_mask(a['length'], a['spans']))
    assert (mask == 0).any(-1).all()  # no fully masked row
    for reference in (torch.finfo(torch.float32).min, torch.finfo(torch.bfloat16).min):
        assert torch.equal(AttentionMaskConverter._unmask_unattended(mask, reference), mask)


# ---------------------------------------------------------------------------- generator block annotation

def generator_style(row):
    """The 4B generator's convention: block-level segments of block b carry block=b (path stays None)."""
    row = json.loads(json.dumps(row))
    block, inside = 0, False
    for s in row['segments']:
        if s['text'] == '<Parallel>':
            block, inside = block + 1, True
        if inside and s['path'] is None:
            s['block'] = block
        if s['text'] == '</Summary>':
            inside = False
    return row


def test_generator_block_annotation_is_accepted_and_tokenizes_identically():
    tokenizer, _ = tagged()
    vocab = D.Vocab(tokenizer)
    row = D.make_row('x', 'test', PROMPT, TWO_BLOCKS)
    annotated = generator_style(row)
    assert annotated != row and any(s['block'] == 2 and s['path'] is None for s in annotated['segments'])
    D.validate_row(annotated)
    assert D.tokenize_row(annotated, vocab) == D.tokenize_row(row, vocab)
    for change in (lambda s: s.update(block=2), lambda s: s.update(path=1)):
        bad = json.loads(json.dumps(annotated))
        change(next(s for s in bad['segments'] if s['text'] == '</Plan>'))  # first block's </Plan>
        with pytest.raises(D.DataError) as error:
            D.validate_row(bad)
        assert error.value.reason == 'bad_block_path'
    outside = json.loads(json.dumps(annotated))
    outside['segments'][1]['block'] = 1  # main text before the block
    with pytest.raises(D.DataError):
        D.validate_row(outside)


# ------------------------------------------------------------------------------------- clipped exactness rows

def test_clip_sample_is_an_exact_prefix():
    tokenizer, model = tagged()
    s = sample(tokenizer, TWO_BLOCKS)
    first_end = s['spans'][2].end  # first block: three branches
    assert exactness.clip_sample(s, first_end) is None
    clipped = exactness.clip_sample(s, first_end + 6)
    assert clipped['length'] == first_end + 6 and len(clipped['spans']) == 3
    assert clipped['position_ids'] == contract.graph_positions(clipped['length'], clipped['spans'])
    report = exactness.check_sample(model, clipped, tokenizer.pad_token_id)
    assert max(report['path'], report['kv'], report['eager']) < ATOL and report['causal_control'] > 1e-2
    full = exactness.graph_logits(model, s)
    torch.testing.assert_close(exactness.graph_logits(model, clipped), full[:clipped['length']], atol=ATOL, rtol=0)
    second = exactness.clip_sample(s, 10 ** 6)
    assert second['length'] == s['spans'][3].start  # stops before the second block
    assert exactness.clip_sample(sample(tokenizer, SEQUENTIAL), 100) is None


# --------------------------------------------------------------------------------------- trainer options

def test_defaults_for_the_long_sequence_setup():
    args = sft_train.parse_args(['--data', 'x', '--out', 'y'])
    assert args.model == 'Qwen/Qwen3-4B' and args.max_len == 16384 and args.loss_chunk == 2048
    assert args.optim == 'adamw' and args.grad_ckpt is None and args.memory_report == 0
    assert args.sdpa_backend == 'efficient' and args.grad_accum_tokens == 393216
    assert sft_train.configure_sdpa('efficient', cuda=False) == 'auto'


def test_adamw8bit_needs_bitsandbytes():
    try:
        import bitsandbytes  # noqa: F401
        pytest.skip('bitsandbytes is installed here')
    except ImportError:
        pass
    params = [torch.nn.Parameter(torch.zeros(3))]
    args = Namespace(optim='adamw8bit', lr=1e-5, betas=(0.9, 0.95), weight_decay=0.0)
    with pytest.raises(SystemExit) as error:
        sft_train.build_optimizer(params, args, cuda=False)
    assert 'bitsandbytes' in str(error.value) and '--optim adamw' in str(error.value)
    optimizer = sft_train.build_optimizer(params, Namespace(**dict(vars(args), optim='adamw')), cuda=False)
    assert isinstance(optimizer, torch.optim.AdamW)


def _base(tmp_path):
    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer)
    base = tmp_path / 'base'
    model.save_pretrained(base)
    tokenizer.save_pretrained(base)
    return base


def test_memory_report_runs_steps_on_the_longest_rows(tmp_path, capsys):
    base = _base(tmp_path)
    rows = [generator_style(row) for row in make_rows()]
    write_jsonl(tmp_path / 'train.jsonl', rows)
    report = sft_train.main([
        '--model', str(base), '--data', str(tmp_path / 'train.jsonl'), '--out', str(tmp_path / 'run'),
        '--max-len', '400', '--memory-report', '2', '--no-bf16', '--grad-ckpt-min-len', '10'])
    assert [step['step'] for step in report['steps']] == [1, 2]
    lengths = [step['length'] for step in report['steps']]
    assert lengths == sorted(lengths, reverse=True) and report['grad_ckpt'] is True
    assert report['estimate']['params'] > 0 and report['estimate']['optimizer_gb'] == 2 * report['estimate']['weights_gb']
    saved = json.loads((tmp_path / 'run' / 'memory_report.json').read_text())
    assert saved['steps'][0]['id'] == report['steps'][0]['id']
    assert not (tmp_path / 'run' / 'final').exists()
    assert 'memory report' in capsys.readouterr().out


def test_grad_ckpt_auto_and_target_steps(tmp_path):
    base = _base(tmp_path)
    write_jsonl(tmp_path / 'train.jsonl', make_rows()[:6])
    common = ['--model', str(base), '--data', str(tmp_path / 'train.jsonl'), '--val-frac', '0', '--epochs', '1',
              '--micro-batch-tokens', '450', '--no-bf16', '--max-steps', '2']
    short = sft_train.main(common + ['--out', str(tmp_path / 'a')])
    assert short['memory']['grad_ckpt'] is False  # tiny rows are below --grad-ckpt-min-len
    long = sft_train.main(common + ['--out', str(tmp_path / 'b'), '--grad-ckpt-min-len', '10',
                                    '--target-steps-per-epoch', '3', '--optim', 'adamw'])
    assert long['memory']['grad_ckpt'] is True and long['memory']['loss_chunk'] == 2048
    tokens = long['counts']['train']['tokens']
    assert long['args']['grad_accum_tokens'] == -(-tokens // 3)


# --------------------------------------------------------------------------------------- select_records.py

def provenance(task, finished=True, correct=True, over=False, checks=('ok', 'ok'), plan='fork', n_tokens=1000):
    return dict(task_id=task, model_finished=finished, correct=correct, grade='correct' if correct else 'wrong',
                over_budget=over, branch_checks=[dict(ok=c.startswith('ok'), reason=c) for c in checks],
                plan_status=plan, n_tokens=n_tokens, raw_unreviewed=True)


def real_like(id, task, text=TWO, source='gsm', prompt=None, **kwargs):
    prompt = prompt or f'Problem {task}: compute it.'
    row = D.make_row(id, source, prompt, text, provenance(task, **kwargs))
    row['question'] = prompt
    return generator_style(row)


def synthetic_rows():
    seq = dict(text=SEQUENTIAL, checks=())
    return [
        real_like('a#raw', 'a'),
        real_like('b#raw', 'b', source='math', **seq),
        real_like('c#raw', 'c', finished=False, checks=('ok', 'branch_truncated')),
        real_like('d#raw', 'd', correct=False),
        real_like('e#raw', 'e', over=True),
        real_like('f#raw', 'f', checks=('ok', 'no_result_line')),
        real_like('g#raw', 'g', plan='gold_in_plan'),
        real_like('h#raw', 'h', checks=()),  # parallel row without branch checks
        dict(real_like('i#raw', 'i', source='math', **seq),
             segments=[dict(text='', loss=True, block=None, path=None)] + real_like('i', 'i', **seq)['segments']),
        real_like('j#raw', 'j', source='countdown', text=THREE, checks=('ok', 'ok', 'ok')),
        real_like('k#raw', 'k', source='math', text=TWO_BLOCKS, checks=('ok',) * 5, n_tokens=3000),
    ]


def run_select(tmp_path, rows, *flags, name='sel'):
    write_jsonl(tmp_path / 'in.jsonl', rows)
    out = tmp_path / name
    stats = select_records.main([str(tmp_path / 'in.jsonl'), '--out-dir', str(out), '--val-frac', '0', *flags])
    train = [json.loads(line) for line in (out / 'train.jsonl').read_text().splitlines()]
    return stats, train


def test_select_default_rules_and_stats(tmp_path):
    rows = synthetic_rows()
    stats, train = run_select(tmp_path, rows)
    assert sorted(r['id'] for r in train) == ['a#raw', 'b#raw', 'j#raw', 'k#raw']
    assert train == [r for r in rows if r['id'] in {'a#raw', 'b#raw', 'j#raw', 'k#raw'}]  # verbatim, input order
    first = stats['dropped_first_rule']
    assert first['model_finished'] == {'gsm': 1} and first['correct'] == {'gsm': 1}
    assert first['over_budget'] == {'gsm': 1} and first['branch_checks'] == {'gsm': 2}  # f and h
    assert first['plan_status'] == {'gsm': 1} and first['invalid:empty_segment'] == {'math': 1}
    assert stats['fails_by_rule']['branch_checks'] == {'gsm': 3}  # c fails it too (counted under model_finished)
    assert stats['dropped_branch_check_reasons'] == {'no_result_line': 1}
    assert stats['kept']['by_mode'] == {'parallel': 3, 'sequential': 1}
    assert stats['kept']['n_tokens']['max'] == 3000 and stats['kept']['n_tokens']['n'] == 4
    saved = json.loads((tmp_path / 'sel' / 'selection_stats.json').read_text())
    assert saved['kept'] == stats['kept'] and len(saved['config']['inputs'][0]['sha256']) == 64
    # every kept row passes the trainer's tokenization with the tiny tokenizer
    tokenizer, _ = tagged()
    samples, data_stats = D.build_dataset(train, tokenizer, max_len=10 ** 6, strict=True)
    assert data_stats['kept'] == 4


def test_select_relax_flags_dedup_caps_and_share(tmp_path):
    rows = synthetic_rows()
    stats, train = run_select(tmp_path, rows, '--allow-unfinished', '--allow-incorrect', '--allow-over-budget',
                              '--allow-failed-branch-checks', '--reject-plan-status', '', name='relaxed')
    assert len(train) == 10 and stats['dropped_total'] == {'invalid:empty_segment': 1}
    newer = json.loads(json.dumps(rows[0]))
    newer['provenance']['correct'] = False
    write_jsonl(tmp_path / 'repaired.jsonl', [newer])
    write_jsonl(tmp_path / 'in.jsonl', rows)
    last = select_records.main([str(tmp_path / 'in.jsonl'), str(tmp_path / 'repaired.jsonl'), '--dry-run'])
    assert last['dropped_first_rule']['duplicate_id'] == {'gsm': 1} and last['kept']['rows'] == 3  # a judged as repaired
    first = select_records.main([str(tmp_path / 'in.jsonl'), str(tmp_path / 'repaired.jsonl'), '--dry-run',
                                 '--on-duplicate', 'first'])
    assert first['kept']['rows'] == 4
    many = [real_like(f'p{i}', f'p{i}') for i in range(8)] + [real_like(f's{i}', f's{i}', text=SEQUENTIAL, checks=())
                                                               for i in range(8)]
    stats, train = run_select(tmp_path, many, '--seq-share', '0.2', name='share')
    assert sum(r['mode'] == 'sequential' for r in train) == 2 and len(train) == 10
    stats, train = run_select(tmp_path, many, '--seq-share', '0.75', name='share2')
    assert sum(r['mode'] == 'parallel' for r in train) == 2 and len(train) == 10
    stats, train = run_select(tmp_path, rows, '--source-cap', 'math=1', name='cap')
    assert sum(r['source'] == 'math' for r in train) == 1 and stats['dropped_first_rule']['source_cap'] == {'math': 1}


def test_select_split_groups_by_task_and_prompt(tmp_path):
    rows = []
    for i in range(40):
        rows += [real_like(f't{i}-par', f't{i}'), real_like(f't{i}-seq', f't{i}', text=SEQUENTIAL, checks=())]
    rows += [real_like('x1', 'x1', prompt='shared prompt'), real_like('x2', 'x2', prompt='shared prompt')]
    write_jsonl(tmp_path / 'in.jsonl', rows)
    out = tmp_path / 'split'
    stats = select_records.main([str(tmp_path / 'in.jsonl'), '--out-dir', str(out), '--val-frac', '0.3'])
    side = {}
    for part in ('train', 'val'):
        for line in (out / f'{part}.jsonl').read_text().splitlines():
            side[json.loads(line)['id']] = part
    assert all(side[f't{i}-par'] == side[f't{i}-seq'] for i in range(40))
    assert side['x1'] == side['x2']  # different task ids, same prompt: one group
    assert 0 < stats['val']['rows'] < len(rows) and stats['kept']['groups'] == 41
    assert stats['train']['groups'] + stats['val']['groups'] == 41


def test_select_with_a_tokenizer_applies_max_len(tmp_path):
    tokenizer = build_tiny_tokenizer()
    tokenizer.save_pretrained(tmp_path / 'tok')
    rows = synthetic_rows()
    write_jsonl(tmp_path / 'in.jsonl', rows)
    stats = select_records.main([str(tmp_path / 'in.jsonl'), '--dry-run', '--tokenizer', str(tmp_path / 'tok'),
                                 '--max-len', '120'])
    assert stats['config']['tag_ids'] == list(range(len(tokenizer), len(tokenizer) + 8))
    assert stats['dropped_first_rule']['too_long'] and stats['kept']['trainer_tokens']['max'] <= 120


# ------------------------------------------------------------------------------------------ vm_selftest ids

def test_vm_selftest_reports_actual_tag_ids_for_another_vocab(tmp_path, monkeypatch, capsys):
    import vm_selftest
    base = _base(tmp_path)
    data = tmp_path / 'data.jsonl'
    write_jsonl(data, [generator_style(row) for row in make_rows()])
    monkeypatch.setattr(sys, 'argv', ['vm_selftest.py', '--model', str(base), '--revision', '', '--data', str(data),
                                      '--max-exact-tokens', '120', '--max-len', '400'])
    with pytest.raises(SystemExit) as exit_:
        vm_selftest.main()
    out = capsys.readouterr().out
    n = len(build_tiny_tokenizer())
    assert f'[PASS] tag ids {n}..{n + 7}' in out and 'DIFFERENT' in out and 'NOT the Qwen3 vocabulary' in out
    assert '[PASS] tags added and initialized' in out and '[PASS] <|im_end|> single token' in out
    assert '[PASS] fp32 exactness builtin' in out and '[PASS] fp32 exactness r0[:' in out
    assert '[PASS] autocast + grad-ckpt train step' in out
    failed = out.split('FAILED: ')[-1]
    assert exit_.value.code == 1 and failed.strip() == "['cuda available']"  # CPU here: only the CUDA check fails
