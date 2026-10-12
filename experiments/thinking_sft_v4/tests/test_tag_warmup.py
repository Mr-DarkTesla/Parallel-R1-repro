"""Two-stage tag schedule (sft_train --tag-warmup-steps / --tag-lr / --tag-lr-mult / --freeze-check) on CPU with the
tiny random Qwen3 (tests/tiny.py, tied embeddings).

cd experiments/thinking_sft_v4 && python3 -m pytest -q tests/test_tag_warmup.py
"""
import copy
import json

import pytest
import torch
import torch.nn.functional as F

import sft_data as D
import sft_train
from common import contract
from tags import ensure_tags, tag_matrices, tag_row_ids
from test_sft import SEQUENTIAL, THREE, TWO, TWO_BLOCKS, make_rows, sample, tagged, write_jsonl
from tiny import build_tiny_model, build_tiny_tokenizer


def _base(tmp_path):
    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer)
    base = tmp_path / 'base'
    model.save_pretrained(base)
    tokenizer.save_pretrained(base)
    write_jsonl(tmp_path / 'train.jsonl', make_rows())
    write_jsonl(tmp_path / 'val.jsonl', make_rows()[:3])
    return base


def _run(tmp_path, name, *extra):
    return sft_train.main([
        '--model', str(tmp_path / 'base'), '--data', str(tmp_path / 'train.jsonl'), '--val',
        str(tmp_path / 'val.jsonl'), '--out', str(tmp_path / name), '--max-len', '400', '--micro-batch-tokens', '450',
        '--grad-accum-tokens', '300', '--no-bf16', '--save-dtype', 'float32', *extra])


def _initial_tagged_state(tmp_path):
    """The weights the trainer starts from: the saved base plus ensure_tags (deterministic for a seed)."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(tmp_path / 'base')
    model = AutoModelForCausalLM.from_pretrained(tmp_path / 'base', torch_dtype=torch.float32)
    ensure_tags(tokenizer, model, seed=0)
    return tokenizer, model


def _final_state(path):
    from transformers import AutoModelForCausalLM
    return AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float32)


def _args(tmp_path, *extra):
    return sft_train.parse_args(['--data', str(tmp_path / 'x.jsonl'), '--out', str(tmp_path / 'o'), *extra])


def _batch(tokenizer, texts=(TWO_BLOCKS, SEQUENTIAL, THREE)):
    return D.collate([sample(tokenizer, text, id=str(i)) for i, text in enumerate(texts)], tokenizer.pad_token_id)


# ------------------------------------------------------------------------------------------------ RowAdam

def test_row_adam_equals_torch_adamw_on_the_rows():
    torch.manual_seed(0)
    weight = torch.nn.Parameter(torch.randn(40, 6))
    rows = list(range(17, 25))
    before = weight.detach().clone()
    reference = torch.nn.Parameter(before[rows].clone())
    torch_adam = torch.optim.AdamW([reference], lr=3e-3, betas=(0.9, 0.95), eps=1e-8, weight_decay=0.0,
                                   foreach=False)
    mine = sft_train.RowAdam([weight], rows, betas=(0.9, 0.95))
    assert mine.state_bytes() == 2 * len(rows) * 6 * 4
    for step in range(7):
        grad = torch.randn(len(rows), 6) * (step + 1)
        reference.grad = grad.clone()
        torch_adam.step()
        mine.step(3e-3, [grad])
        torch.testing.assert_close(weight.detach()[rows], reference.detach(), atol=1e-7, rtol=1e-6)
    others = [r for r in range(40) if r not in rows]
    assert torch.equal(weight.detach()[others], before[others])  # never written


def test_tag_lr_factor_and_stage1_data_stream():
    assert [sft_train.tag_lr_factor(k, 60) for k in (1, 3, 6, 7, 60)] == [1 / 6, 0.5, 1.0, 1.0, 1.0]
    assert [sft_train.tag_lr_factor(k, 3) for k in (1, 2, 3)] == [1.0, 1.0, 1.0]  # warmup is at least one step
    lengths = [5, 17, 3, 40, 9, 9, 22, 1, 30, 12] * 3
    args = _args_namespace(tag_warmup_steps=0, micro_batch_tokens=64, grad_accum_tokens=60, seed=1)
    plans = [D.group_steps(D.token_batches(lengths, 64, seed=1000 + e), lengths, 60) for e in range(2)]
    stream = [step for plan in plans for step in plan]
    for k in (3, len(stream), len(stream) + 5):
        args.tag_warmup_steps = k
        steps = sft_train.tag_warmup_plan(plans, lengths, args)
        assert len(steps) == k and steps[:min(k, len(stream))] == stream[:k]
    args.tag_warmup_steps = 4
    assert len(sft_train.tag_warmup_plan([], lengths, args)) == 4  # --epochs 0: fresh shuffles


def _args_namespace(**kwargs):
    import argparse
    return argparse.Namespace(**kwargs)


# ---------------------------------------------------------------------------------------- stage 1: freezing

def test_stage1_updates_only_the_tag_rows_in_memory(tmp_path):
    tokenizer, model = tagged()
    rows = tag_row_ids(tokenizer)
    assert len(tag_matrices(model)) == 1  # tied
    before = {k: v.detach().clone() for k, v in model.state_dict().items()}
    flags = {n: p.requires_grad for n, p in model.named_parameters()}
    train = [sample(tokenizer, text, id=str(i)) for i, text in enumerate([TWO, THREE, TWO_BLOCKS, SEQUENTIAL])]
    steps = [[[0, 1]], [[2], [3]], [[1, 3]]]
    args = _args(tmp_path, '--tag-warmup-steps', '3', '--tag-lr', '1e-2', '--no-bf16')
    args.pad_multiple = 1
    initial = [w.detach()[rows].clone() for w in tag_matrices(model)]
    records = []
    model.train()
    prints = sft_train.frozen_fingerprints(model, rows)
    summary = sft_train.run_tag_warmup(model, train, steps, rows, initial, args, torch.device('cpu'), torch.float32,
                                       lambda: torch.autocast('cpu', enabled=False), tokenizer.pad_token_id,
                                       records.append)
    assert summary['steps_run'] == 3 and summary['optimizer_state_bytes'] == 2 * 8 * 64 * 4
    after = model.state_dict()
    embed = 'model.embed_tokens.weight'
    for key, value in before.items():
        if key in (embed, 'lm_head.weight'):
            others = [r for r in range(value.size(0)) if r not in rows]
            assert torch.equal(after[key][others], value[others]), key
            assert not torch.equal(after[key][rows], value[rows]), key
            assert (after[key][rows] != value[rows]).any(dim=-1).all(), 'every tag row moves'
        else:
            assert torch.equal(after[key], value), key
    assert sft_train.frozen_fingerprints(model, rows) == prints
    # requires_grad restored, hooks removed: a backward now reaches every row and every layer
    assert {n: p.requires_grad for n, p in model.named_parameters()} == flags
    losses, _ = sft_train.token_losses(model, _batch(tokenizer))
    losses.mean().backward()
    grad = model.get_input_embeddings().weight.grad
    others = [r for r in range(grad.size(0)) if r not in rows]
    assert grad[others].abs().sum() > 0 and all(p.grad is not None for p in model.parameters())
    assert [r['stage'] for r in records] == ['tag_warmup'] * 3 and [r['tag_step'] for r in records] == [1, 2, 3]


def test_stage1_untied_head_trains_both_tag_row_sets_only(tmp_path):
    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer)
    model.config.tie_word_embeddings = False
    model.lm_head.weight = torch.nn.Parameter(model.lm_head.weight.detach().clone() * 2)
    ensure_tags(tokenizer, model)
    rows = tag_row_ids(tokenizer)
    assert len(tag_matrices(model)) == 2
    before = {k: v.detach().clone() for k, v in model.state_dict().items()}
    train = [sample(tokenizer, text, id=str(i)) for i, text in enumerate([TWO, TWO_BLOCKS])]
    args = _args(tmp_path, '--tag-lr', '1e-2')
    args.pad_multiple = 1
    model.train()
    sft_train.run_tag_warmup(model, train, [[[0]], [[1]]], rows, [w.detach()[rows].clone() for w in tag_matrices(model)],
                             args, torch.device('cpu'), torch.float32, lambda: torch.autocast('cpu', enabled=False),
                             tokenizer.pad_token_id, lambda record: None)
    after = model.state_dict()
    for key in ('model.embed_tokens.weight', 'lm_head.weight'):
        others = [r for r in range(after[key].size(0)) if r not in rows]
        assert torch.equal(after[key][others], before[key][others]) and not torch.equal(after[key][rows],
                                                                                        before[key][rows])
    assert all(torch.equal(after[k], v) for k, v in before.items() if k not in ('model.embed_tokens.weight',
                                                                                 'lm_head.weight'))


def test_freeze_check_end_to_end_through_main(tmp_path):
    """--freeze-check: after stage 1 (here with no main steps: --epochs 0) every non-tag row and every other
    parameter of the saved checkpoint is bit-identical to the starting weights; the tag rows changed."""
    _base(tmp_path)
    manifest = _run(tmp_path, 'stage1', '--epochs', '0', '--tag-warmup-steps', '4', '--tag-lr', '1e-2',
                    '--freeze-check', '--grad-ckpt')
    assert manifest['steps'] == 0 and manifest['total_steps'] == 0
    stage1 = manifest['tag_schedule']['stage1']
    assert stage1['steps_run'] == 4 and stage1['freeze_check'].startswith('passed')
    tokenizer, start = _initial_tagged_state(tmp_path)
    rows = tag_row_ids(tokenizer)
    final = _final_state(tmp_path / 'stage1' / 'final')
    start_state, final_state = start.state_dict(), final.state_dict()
    others = [r for r in range(start_state['model.embed_tokens.weight'].size(0)) if r not in rows]
    for key, value in start_state.items():
        if key in ('model.embed_tokens.weight', 'lm_head.weight'):
            assert torch.equal(final_state[key][others], value[others]), key
            assert (final_state[key][rows] != value[rows]).any(dim=-1).all(), key
        else:
            assert torch.equal(final_state[key], value), key


def test_fingerprint_sees_a_one_ulp_change():
    torch.manual_seed(0)
    x = torch.randn(1000, 7)
    a = sft_train.fingerprint(x)
    y = x.clone()
    y[513, 3] = torch.nextafter(y[513, 3], torch.tensor(float('inf')))
    assert sft_train.fingerprint(x.clone()) == a and sft_train.fingerprint(y) != a
    z = x.clone()
    z[[1, 2]] = z[[2, 1]]  # swapped rows: the position-weighted sum differs
    assert sft_train.fingerprint(z) != a
    assert sft_train.fingerprint(x.bfloat16()) == sft_train.fingerprint(x.bfloat16().clone())


# --------------------------------------------------------------------------------------- stage 2: --tag-lr-mult

def _one_main_step(model, tokenizer, mult, weight_decay=0.0, force_boost=False, lr=1e-3):
    """One optimizer step of the main loop (clip, boost, AdamW) on a fixed batch."""
    rows = tag_row_ids(tokenizer)
    model.train()
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(params, lr=lr, betas=(0.9, 0.95), weight_decay=weight_decay)
    boost = sft_train.TagLrBoost(model, rows, mult, (0.9, 0.95)) if (mult != 1 or force_boost) else None
    losses, _ = sft_train.token_losses(model, _batch(tokenizer))
    losses.mean().backward()
    torch.nn.utils.clip_grad_norm_(params, 1.0)
    if boost:
        boost.before_step()
    optimizer.step()
    if boost:
        boost.after_step(lr)
    optimizer.zero_grad(set_to_none=True)
    return model.state_dict()


def test_tag_lr_mult_one_step_scales_tag_rows_and_leaves_the_rest_to_adamw():
    tokenizer, model = tagged()
    rows = tag_row_ids(tokenizer)
    start = {k: v.detach().clone() for k, v in model.state_dict().items()}
    plain = _one_main_step(copy.deepcopy(model), tokenizer, 1)
    boosted = _one_main_step(copy.deepcopy(model), tokenizer, 10)
    boost_one = _one_main_step(copy.deepcopy(model), tokenizer, 1, force_boost=True)
    embed = 'model.embed_tokens.weight'
    others = [r for r in range(start[embed].size(0)) if r not in rows]
    # everything but the tag rows: the same AdamW step, bit for bit (clipping saw the same total norm)
    for key in start:
        if key == embed or key == 'lm_head.weight':
            assert torch.equal(plain[key][others], boosted[key][others])
        else:
            assert torch.equal(plain[key], boosted[key]), key
            assert not torch.equal(plain[key], start[key]), key  # AdamW did move them
    # the tag rows: RowAdam at 10 x lr moves them 10 x as far (Adam's first step is ~lr * sign(grad))
    d_plain = (plain[embed][rows] - start[embed][rows]).norm()
    d_boost = (boosted[embed][rows] - start[embed][rows]).norm()
    assert 9.5 < (d_boost / d_plain).item() < 10.5, (d_boost, d_plain)
    # the boost path at M = 1 is the main AdamW on those rows
    torch.testing.assert_close(boost_one[embed][rows], plain[embed][rows], atol=1e-7, rtol=0)


def test_tag_lr_mult_keeps_main_weight_decay_off_the_tag_rows():
    tokenizer, model = tagged()
    rows = tag_row_ids(tokenizer)
    embed = 'model.embed_tokens.weight'
    no_decay = _one_main_step(copy.deepcopy(model), tokenizer, 10, weight_decay=0.0)
    decay = _one_main_step(copy.deepcopy(model), tokenizer, 10, weight_decay=0.5)
    assert torch.equal(no_decay[embed][rows], decay[embed][rows])
    others = [r for r in range(no_decay[embed].size(0)) if r not in rows]
    assert not torch.equal(no_decay[embed][others], decay[embed][others])  # decay does act on the rest


def test_tag_lr_mult_over_a_run_moves_tag_rows_further(tmp_path):
    _base(tmp_path)
    common = ('--epochs', '2', '--lr', '1e-4', '--warmup-ratio', '0')
    one = _run(tmp_path, 'm1', *common)
    ten = _run(tmp_path, 'm10', *common, '--tag-lr-mult', '10')
    assert one['steps'] == ten['steps'] >= 4
    d_one, d_ten = (m['tag_schedule']['final']['tag_row_delta'] for m in (one, ten))
    assert d_ten > 5 * d_one > 0, (d_one, d_ten)
    assert ten['tag_schedule']['stage2']['tag_lr_mult'] == 10 and 'RowAdam' in ten['tag_schedule']['stage2']['tag_rows']
    # the checkpoints agree with the manifest numbers
    tokenizer, start = _initial_tagged_state(tmp_path)
    rows = tag_row_ids(tokenizer)
    embed = 'model.embed_tokens.weight'
    for name, expected in (('m1', d_one), ('m10', d_ten)):
        final = _final_state(tmp_path / name / 'final').state_dict()[embed][rows]
        moved = (final - start.state_dict()[embed][rows]).norm(dim=-1).mean().item()
        assert abs(moved - expected) < 1e-6


# ------------------------------------------------------------------------------- logging, manifest, memory

def test_loss_tag_is_the_mean_over_tag_and_count_targets():
    tokenizer, model = tagged()
    batch = _batch(tokenizer, (TWO_BLOCKS, SEQUENTIAL, THREE, TWO))
    with torch.no_grad():
        losses, selection = sft_train.token_losses(model, batch, chunk=5)
        logits = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'],
                       position_ids=batch['position_ids'], use_cache=False).logits[:, :-1]
    meter = sft_train.Meter()
    meter.add(losses, selection, batch)
    means = meter.means('loss')
    target = batch['labels'][:, 1:]
    ids = [tokenizer.convert_tokens_to_ids(t) for t in ('<Parallel>', '</Plan>', '</Path>', '</Summary>')]
    is_count = batch['control'][:, 1:] == D.CONTROL_KINDS.index('count')
    chosen = (torch.isin(target, torch.tensor(ids)) | is_count) & (target != D.IGNORE)
    assert int(is_count.sum()) == 4 and int(chosen.sum()) == means['loss_tag_tokens'] > 10
    assert all(tokenizer.decode([t]) in contract.COUNTS for t in target[is_count].tolist())
    reference = F.cross_entropy(logits[chosen].float(), target[chosen])
    assert abs(means['loss_tag'] - reference.item()) < 1e-5
    assert means['loss_tag'] != means['loss_control']  # </think> is control but not a tag target


def test_two_stage_logs_and_manifest(tmp_path):
    _base(tmp_path)
    plain = _run(tmp_path, 'plain', '--epochs', '2', '--max-steps', '3')
    manifest = _run(tmp_path, 'two', '--epochs', '2', '--max-steps', '3', '--tag-warmup-steps', '5', '--tag-lr',
                    '1e-2', '--log-every', '1')
    assert manifest['total_steps'] == plain['total_steps'] == 3 and manifest['steps'] == 3  # K not counted
    records = [json.loads(line) for line in (tmp_path / 'two' / 'metrics.jsonl').read_text().splitlines()]
    warm = [r for r in records if r.get('stage') == 'tag_warmup' and 'grad_norm' in r]
    main = [r for r in records if r.get('stage') == 'main' and 'grad_norm' in r]
    assert [r['tag_step'] for r in warm] == [1, 2, 3, 4, 5] and all('step' not in r for r in warm)
    assert [r['step'] for r in main] == [1, 2, 3]
    for r in warm + main:
        for key in ('tag_row_norm', 'tag_row_delta', 'loss', 'loss_tag', 'loss_tag_tokens', 'lr'):
            assert key in r, (key, r)
    assert [r['lr'] for r in warm] == [1e-2] * 5  # warmup ceil(0.5) = 1 step, then constant
    assert main[0]['lr'] < 1e-5 + 1e-12  # the main schedule starts fresh (its own warmup)
    assert warm[-1]['tag_row_delta'] > warm[0]['tag_row_delta'] > 0
    # stage 1 lowers the validation loss on the tag targets
    before = next(r for r in records if r.get('stage') == 'tag_warmup' and r.get('tag_step') == 0)
    after = next(r for r in records if r.get('stage') == 'main' and r.get('step') == 0)
    assert after['val_loss_tag'] < before['val_loss_tag'] - 0.1
    saved = json.loads((tmp_path / 'two' / 'final' / 'train_manifest.json').read_text())
    schedule = saved['tag_schedule']
    assert schedule['stage1']['steps'] == 5 and schedule['stage1']['lr'] == 1e-2
    assert schedule['stage1']['weight_decay'] == 0.0 and schedule['stage1']['lr_warmup_steps'] == 1
    assert schedule['stage1']['steps_run'] == 5 and schedule['stage1']['last']['loss_tag'] is not None
    n = len(build_tiny_tokenizer())
    assert schedule['stage2']['tag_lr_mult'] == 1.0 and schedule['rows'] == list(range(n, n + 8))
    assert saved['args']['tag_warmup_steps'] == 5 and saved['args']['tag_lr_mult'] == 1.0
    assert plain['tag_schedule']['stage1']['enabled'] is False and 'steps_run' not in plain['tag_schedule']['stage1']


def test_memory_report_covers_stage1(tmp_path):
    _base(tmp_path)
    report = _run(tmp_path, 'mem', '--memory-report', '2', '--tag-warmup-steps', '60', '--grad-ckpt-min-len', '10',
                  '--tag-lr-mult', '10')
    assert [s['stage'] for s in report['tag_warmup']['steps']] == ['tag_warmup'] * 2
    assert [s['stage'] for s in report['steps']] == ['main'] * 2
    stage1, full = report['tag_warmup']['estimate'], report['estimate']
    assert stage1['weights_gb'] == full['weights_gb'] and stage1['static_gb'] < full['static_gb']
    assert not (tmp_path / 'mem' / 'final').exists()


def test_stage1_static_memory_on_the_4b_shape():
    """Static memory of stage 1 vs the full run on the 4B architecture (meta device: no allocation)."""
    from transformers import Qwen3Config, Qwen3ForCausalLM
    config = Qwen3Config(vocab_size=151936, hidden_size=2560, intermediate_size=9728, num_hidden_layers=36,
                         num_attention_heads=32, num_key_value_heads=8, head_dim=128, tie_word_embeddings=True)
    with torch.device('meta'):
        model = Qwen3ForCausalLM(config)
    rows = list(range(151669, 151677))
    stage1 = sft_train.static_estimate_tag_warmup(model, rows)
    full = sft_train.static_estimate(model, 'adamw')
    assert abs(stage1['params'] - 4.02e9) < 0.01e9 and abs(full['static_gb'] - 59.9) < 0.2
    assert abs(stage1['grads_gb'] - 151936 * 2560 * 4 / 2 ** 30) < 1e-9  # 1.45 GiB: the embedding matrix only
    assert stage1['optimizer_gb'] * 2 ** 30 == 2 * 8 * 2560 * 4  # 160 KiB of Adam moments
    assert abs(stage1['static_gb'] - 16.4) < 0.1 and stage1['static_gb'] < 0.3 * full['static_gb']


def test_bad_tag_arguments_are_rejected(tmp_path):
    _base(tmp_path)
    for extra in (('--tag-warmup-steps', '-1'), ('--tag-lr-mult', '0'), ('--tag-lr', '0')):
        with pytest.raises(SystemExit):
            _run(tmp_path, 'bad', *extra)
