"""Thinking-SFT v4 data + trainer on CPU with a tiny random Qwen3 (tests/tiny.py).

cd experiments/thinking_sft_v4 && python3 -m pytest -q tests/test_sft.py
"""
import json
import sys
from pathlib import Path

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import exactness  # noqa: E402
import sft_data as D  # noqa: E402
import sft_train  # noqa: E402
from common import contract  # noqa: E402
from tags import MARKER, ensure_tags, tag_pieces  # noqa: E402
from tiny import build_tiny_model, build_tiny_tokenizer  # noqa: E402

ATOL = 1e-5
PROMPT = 'Solve x + 2 = 5. Put the final answer in \\boxed{}.'
TWO = ('<think>\nLet x be a real number.\n\n<Parallel>branches=2<Plan>decompose\n1: a\n2: b\n</Plan>'
       '<Path>1: body one is longer than two</Path><Path>2: body two</Path></Parallel>'
       '<Summary>summary</Summary></think>\n\nanswer<|im_end|>')
THREE = ('<think>\nLet x be 2.\n\n<Parallel>branches=3<Plan>cases\n1: x > 0\n2: x < 0\n3: x = 0\n</Plan>'
         '<Path>1: if x > 0 then f(x) = x</Path><Path>2: otherwise -x and more text here</Path><Path>3: zero</Path>'
         '</Parallel><Summary> Both branches agree.</Summary>So the answer is 3.</think>\n\nThe answer is 3.<|im_end|>')
TWO_BLOCKS = ('<think>\nWe check.\n\n<Parallel>branches=3<Plan>cases\n1: x > 0\n2: x < 0\n3: x = 0\n</Plan>'
              '<Path>1: if x > 0 then f(x) = x</Path><Path>2: otherwise -x</Path><Path>3: zero case here</Path>'
              '</Parallel><Summary> Both agree.</Summary>Hmm, wait. <Parallel>branches=2<Plan>verify\n'
              '1: check sum\n2: check product\n</Plan><Path>1: 1 + 2 = 3</Path><Path>2: 3 * 4 = 12 ok</Path>'
              '</Parallel><Summary>fine</Summary></think>\n\nThe answer is \\boxed{3}.<|im_end|>')
SEQUENTIAL = ('<think>\nOkay, let me think step by step. 3 * 4 = 12 and 12 / 2 = 6.\n</think>\n\n'
              'The final answer is \\boxed{6}.<|im_end|>')


def tagged(attn='sdpa'):
    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer, attn=attn)
    ensure_tags(tokenizer, model)
    return tokenizer, model


def sample(tokenizer, text, id='x', prompt=PROMPT):
    return D.tokenize_row(D.make_row(id, 'test', prompt, text), D.Vocab(tokenizer))


def span_logits(logits, span):
    return logits[span.start:span.end]


# ------------------------------------------------------------------------------- (a) exactness of the forward

@pytest.mark.parametrize('attn', ['sdpa', 'eager'])
@pytest.mark.parametrize('text', [TWO, THREE, TWO_BLOCKS], ids=['two', 'three', 'two_blocks'])
def test_graph_forward_matches_independent_references(attn, text):
    tokenizer, model = tagged(attn)
    s = sample(tokenizer, text)
    report = exactness.check_sample(model, s, tokenizer.pad_token_id)
    assert report['path'] < ATOL, report      # branch k == causal [prefix .. </Plan>, branch k], positions 0..n-1
    assert report['kv'] < ATOL, report        # everything == runtime decode with concatenated branch KV caches
    assert report['eager'] < ATOL, report     # everything == from-scratch forward with explicit visibility
    assert report['causal_control'] > 1e-2, report  # the references would catch a plain causal forward
    assert exactness.runtime_positions(s) == s['position_ids']


def test_path_reference_is_literally_prefix_plus_branch():
    tokenizer, model = tagged()
    s = sample(tokenizer, THREE)
    logits = exactness.graph_logits(model, s)
    first = s['spans'][0].start
    assert s['input_ids'][first - 1] == tokenizer.convert_tokens_to_ids('</Plan>')
    for span in s['spans']:
        ids = s['input_ids'][:first] + s['input_ids'][span.start:span.end]
        reference = exactness.forward_logits(model, ids)  # default positions, no mask
        torch.testing.assert_close(span_logits(logits, span), reference[first:], atol=ATOL, rtol=0)


@pytest.mark.parametrize('replacement', [' body ONE is a different text', ' x'], ids=['other', 'shorter'])
def test_sibling_invariance(replacement):
    tokenizer, model = tagged()
    base = sample(tokenizer, TWO)
    other = sample(tokenizer, TWO.replace(' body one is longer than two', replacement))
    a, b = exactness.graph_logits(model, base), exactness.graph_logits(model, other)
    assert base['input_ids'][base['spans'][0].start:base['spans'][0].end] != \
        other['input_ids'][other['spans'][0].start:other['spans'][0].end]
    torch.testing.assert_close(span_logits(a, base['spans'][1]), span_logits(b, other['spans'][1]), atol=ATOL, rtol=0)
    assert base['position_ids'][base['spans'][1].start] == other['position_ids'][other['spans'][1].start]
    # the summary reads both branches, so it does change
    assert (a[base['spans'][1].end:].mean(0) - b[other['spans'][1].end:].mean(0)).abs().max() > 1e-4


# ------------------------------------------------------------------------------------------- (b) loss ownership

def test_labels_follow_the_agreed_ownership():
    tokenizer, _ = tagged()
    row = D.make_row('x', 'test', PROMPT, TWO_BLOCKS)
    s = D.tokenize_row(row, D.Vocab(tokenizer))
    prompt = tokenizer.encode(D.prompt_text(tokenizer, PROMPT), add_special_tokens=False)
    assert s['input_ids'][:len(prompt)] == prompt and s['prompt_length'] == len(prompt)
    assert all(label == D.IGNORE for label in s['labels'][:len(prompt)])
    cursor = len(prompt)
    inserted = {'branches=', '<Plan>', '<Path>', '</Parallel>', '<Summary>'} | {f'{k}:' for k in range(1, 5)}
    in_loss = {'<think>', '<Parallel>', '2', '3', '</Plan>', '</Path>', '</Summary>', '</think>', '<|im_end|>'}
    seen = set()
    for seg in row['segments']:
        ids = tokenizer.encode(seg['text'], add_special_tokens=False)
        labels = s['labels'][cursor:cursor + len(ids)]
        assert s['input_ids'][cursor:cursor + len(ids)] == ids
        if seg['text'] in inserted:
            assert not seg['loss'] and all(label == D.IGNORE for label in labels), seg
            seen.add(seg['text'])
        else:
            assert seg['loss'] and labels == ids, seg
            if seg['text'] in in_loss:
                seen.add(seg['text'])
        cursor += len(ids)
    assert cursor == s['length'] and s['input_ids'][-1] == tokenizer.convert_tokens_to_ids('<|im_end|>')
    assert seen >= inserted - {'4:'} | in_loss
    # control kinds point at the right tokens
    kinds = {D.CONTROL_KINDS[k] for k in s['control'] if k >= 0}
    assert kinds == set(D.CONTROL_KINDS)
    count_positions = [t for t, k in enumerate(s['control']) if k == D.CONTROL_KINDS.index('count')]
    assert [tokenizer.decode([s['input_ids'][t]]) for t in count_positions] == ['3', '2']
    assert all(s['labels'][t] != D.IGNORE for t, k in enumerate(s['control']) if k >= 0)
    # spans are <Path> .. </Path>, siblings adjacent, the first after </Plan>
    path_open, path_close = (tokenizer.convert_tokens_to_ids(t) for t in ('<Path>', '</Path>'))
    for span in s['spans']:
        assert s['input_ids'][span.start] == path_open and s['input_ids'][span.end - 1] == path_close


def test_sequential_rows_are_plain_causal():
    tokenizer, _ = tagged()
    s = sample(tokenizer, SEQUENTIAL)
    assert s['mode'] == 'sequential' and s['spans'] == [] and s['position_ids'] == list(range(s['length']))
    batch = D.collate([s], tokenizer.pad_token_id)
    assert torch.equal(batch['attention_mask'][0, 0] == 0, torch.ones(s['length'], s['length']).tril().bool())


def test_segment_text_matches_format_block():
    block = contract.format_block('cases', ['x > 0', 'x <= 0'], [' if x > 0 then 1', ' else 0'], ' 1 or 0')
    segments = D.segment_text('<think>\n' + block + '</think>\n\nok<|im_end|>')
    assert ''.join(s['text'] for s in segments) == '<think>\n' + block + '</think>\n\nok<|im_end|>'
    assert [s['text'] for s in segments if not s['loss']] == [
        'branches=', '<Plan>', '<Path>', '1:', '<Path>', '2:', '</Parallel>', '<Summary>']


def bad_rows():
    good = D.make_row('g', 'test', PROMPT, TWO)

    def edit(change):
        row = json.loads(json.dumps(good))
        change(row)
        return row

    def flip(text, loss):
        return lambda row: [seg.update(loss=loss) for seg in row['segments'] if seg['text'] == text]

    return {
        'bad_loss': edit(flip('<Path>', True)),
        'bad_loss ': edit(flip('</Path>', False)),
        'tag_not_own_segment': edit(lambda row: row['segments'][1].update(text='x </think> y')),
        'invalid_plan': edit(lambda row: [seg.update(text='decompose\n1: a\n3: b\n') for seg in row['segments']
                                          if seg['text'].startswith('decompose')]),
        'bad_block_path': edit(lambda row: row['segments'][9].update(path=2)),
        'mode_mismatch': edit(lambda row: row.update(mode='sequential')),
        'unexpected_segment': edit(lambda row: row['segments'].pop(-1)),
        'bad_count': edit(lambda row: [seg.update(text='5') for seg in row['segments'] if seg['text'] == '2']),
        'unexpected_segment ': edit(lambda row: row['segments'].pop(13)),  # path prefix '2:' missing
    }


def test_invalid_and_too_long_rows_are_dropped_with_reasons():
    tokenizer, _ = tagged()
    rows = list(bad_rows().items())
    long_row = D.make_row('long', 'test', PROMPT, SEQUENTIAL.replace('step by step.', 'step by step. ' * 80))
    data = [row for _, row in rows] + [long_row, D.make_row('ok', 'test', PROMPT, TWO)]
    samples, stats = D.build_dataset(data, tokenizer, max_len=300)
    assert [s['id'] for s in samples] == ['ok']
    expected = {}
    for reason, _ in rows:
        expected[reason.strip()] = expected.get(reason.strip(), 0) + 1
    expected['too_long'] = 1
    assert stats['dropped'] == expected, stats['drop_examples']
    assert stats['invalid'] == len(rows)
    with pytest.raises(D.DataError):
        D.build_dataset(data, tokenizer, max_len=300, strict=True)


# --------------------------------------------------------------------------------------- (c) batch == single

@pytest.mark.parametrize('attn', ['sdpa', 'eager'])
def test_padded_mixed_batch_equals_single(attn):
    tokenizer, model = tagged(attn)
    samples = [sample(tokenizer, text, id=str(i)) for i, text in enumerate([TWO_BLOCKS, SEQUENTIAL, THREE, TWO])]
    assert len({s['length'] for s in samples}) == len(samples)

    def per_sample(batch_samples):
        batch = D.collate(batch_samples, tokenizer.pad_token_id)
        with torch.no_grad():
            losses, selection = sft_train.token_losses(model, batch, chunk=7)
        rows = selection.nonzero(as_tuple=True)[0]
        assert torch.isfinite(losses).all()
        return [losses[rows == b] for b in range(len(batch_samples))]

    together = per_sample(samples)
    for s, mine in zip(samples, together):
        alone = per_sample([s])[0]
        assert mine.numel() == alone.numel() == s['n_loss']
        torch.testing.assert_close(mine, alone, atol=ATOL, rtol=0)
    # HF's own logits on the padded batch are finite everywhere (padded queries attend to themselves)
    batch = D.collate(samples, tokenizer.pad_token_id)
    with torch.no_grad():
        logits = model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'],
                       position_ids=batch['position_ids'], use_cache=False).logits
    assert torch.isfinite(logits).all()


def test_collate_mask_layout():
    tokenizer, _ = tagged()
    a, b = sample(tokenizer, TWO), sample(tokenizer, SEQUENTIAL)
    batch = D.collate([a, b], tokenizer.pad_token_id)
    T = max(a['length'], b['length'])
    mask = batch['attention_mask']
    assert mask.shape == (2, 1, T, T) and mask.dtype == torch.float32
    allowed = mask == 0
    short = min((a, b), key=lambda s: s['length'])
    row = [a, b].index(short)
    L = short['length']
    assert not allowed[row, 0, :L, L:].any()
    assert torch.equal(allowed[row, 0, L:, L:], torch.eye(T - L, dtype=torch.bool))
    assert torch.equal(allowed[0, 0, :a['length'], :a['length']],
                       contract.graph_attention_mask(a['length'], a['spans']))
    assert (batch['labels'][row, L:] == D.IGNORE).all() and (batch['input_ids'][row, L:] == tokenizer.pad_token_id).all()
    assert batch['position_ids'][row, L] == short['position_ids'][-1] + 1
    bf16 = D.collate([a], tokenizer.pad_token_id, dtype=torch.bfloat16)['attention_mask']
    assert bf16.dtype == torch.bfloat16 and bf16.min() == torch.finfo(torch.bfloat16).min


def test_token_batches_respect_the_budget():
    lengths = [5, 17, 3, 40, 9, 9, 22, 1, 30, 12] * 7
    batches = D.token_batches(lengths, 64, seed=3)
    assert sorted(i for batch in batches for i in batch) == list(range(len(lengths)))
    assert all(len(batch) * max(lengths[i] for i in batch) <= 64 for batch in batches)
    steps = D.group_steps(batches, lengths, 100)
    assert [b for step in steps for b in step] == batches
    assert all(sum(lengths[i] for b in step for i in b) >= 100 for step in steps[:-1])
    assert D.token_batches([100, 3], 64, shuffle=False) == [[0], [1]]


# ------------------------------------------------------------------------------------- (d) end-to-end training

def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows))


def make_rows():
    texts = [TWO, THREE, TWO_BLOCKS, SEQUENTIAL, SEQUENTIAL.replace('6', '8'), TWO.replace('body two', 'body 2')]
    rows = [D.make_row(f'r{i}', 'test', PROMPT if i % 2 else 'Compute 3 * 4 / 2.', text) for i, text in enumerate(texts)]
    rows.append(D.make_row('long', 'test', PROMPT, SEQUENTIAL.replace('step by step.', 'step by step. ' * 150)))
    return rows


def test_train_end_to_end_and_reload(tmp_path):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer)
    base = tmp_path / 'base'
    model.save_pretrained(base)
    tokenizer.save_pretrained(base)
    rows = make_rows()
    write_jsonl(tmp_path / 'train.jsonl', rows)
    write_jsonl(tmp_path / 'val.jsonl', rows[:3])
    out = tmp_path / 'run'
    manifest = sft_train.main([
        '--model', str(base), '--data', str(tmp_path / 'train.jsonl'), '--val', str(tmp_path / 'val.jsonl'),
        '--out', str(out), '--max-len', '400', '--epochs', '2', '--lr', '1e-3', '--micro-batch-tokens', '450',
        '--grad-accum-tokens', '300', '--save-every-epoch', '--eval-every', '2', '--grad-ckpt', '--no-bf16',
        '--save-dtype', 'float32'])
    final = out / 'final'
    for name in ('config.json', 'model.safetensors', 'tokenizer.json', 'tokenizer_config.json', 'train_manifest.json'):
        assert (final / name).exists(), name
    assert (out / 'epoch1' / 'model.safetensors').exists() and not (out / 'epoch2').exists()
    saved = json.loads((final / 'train_manifest.json').read_text())
    assert saved['contract']['sha256'] == contract.SHA256 and saved['contract']['revision'] == contract.CONTRACT_REVISION
    assert saved['counts']['train']['dropped'] == {'too_long': 1} and saved['counts']['train']['kept'] == 6
    assert len(saved['data']['train_sha256']) == 64 and saved['steps'] == manifest['steps'] >= 2
    assert [e['epoch'] for e in saved['val_epochs']] == [1, 2]
    records = [json.loads(line) for line in (out / 'metrics.jsonl').read_text().splitlines()]
    train_records = [r for r in records if 'grad_norm' in r]
    for key in ('loss', 'loss_parallel', 'loss_sequential', 'loss_control', 'loss_ctrl:</Path>', 'lr',
                'tokens_per_s', 'grad_norm'):
        assert any(key in r for r in train_records), key
    assert all(torch.isfinite(torch.tensor(r['loss'])) for r in train_records)
    val = [r['val_loss'] for r in records if 'val_loss' in r]
    assert val[-1] < val[0]  # lr 1e-3 on six rows: it learns
    # reload: tags present with the init marker, ensure_tags is a no-op
    reloaded_tok = AutoTokenizer.from_pretrained(final)
    reloaded = AutoModelForCausalLM.from_pretrained(final, torch_dtype=torch.float32)
    assert getattr(reloaded.config, MARKER)['ids'] == list(range(len(tokenizer), len(tokenizer) + 8))
    before = {k: v.clone() for k, v in reloaded.state_dict().items()}
    report = ensure_tags(reloaded_tok, reloaded)
    assert report['status'] == 'present' and not report['added'] and not report['resized']
    assert len(reloaded_tok) == len(tokenizer) + 8
    assert all(torch.equal(before[k], v) for k, v in reloaded.state_dict().items())
    assert reloaded_tok.apply_chat_template([{'role': 'user', 'content': 'q'}], tokenize=False,
                                            add_generation_prompt=True, enable_thinking=True).endswith(D.ASSISTANT_PREFIX)
    # the reloaded weights are the trained ones (float32 save): same loss as at the end of training
    s = D.tokenize_row(rows[0], D.Vocab(reloaded_tok))
    reloaded.eval()
    report = exactness.check_sample(reloaded, s, reloaded_tok.pad_token_id, brute_force=False)
    assert report['kv'] < ATOL and report['path'] < ATOL


def test_train_bf16_autocast_smoke(tmp_path):
    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer)
    base = tmp_path / 'base'
    model.save_pretrained(base)
    tokenizer.save_pretrained(base)
    write_jsonl(tmp_path / 'train.jsonl', make_rows()[:6])
    manifest = sft_train.main([
        '--model', str(base), '--data', str(tmp_path / 'train.jsonl'), '--val-frac', '0.3', '--out',
        str(tmp_path / 'run'), '--epochs', '1', '--micro-batch-tokens', '450', '--grad-accum-tokens', '300',
        '--bf16', '--attn', 'eager'])
    config = json.loads((tmp_path / 'run' / 'final' / 'config.json').read_text())
    assert config['torch_dtype'] == 'bfloat16' and manifest['bf16']
    assert manifest['counts']['train_samples'] + manifest['counts']['val_samples'] == 6


def test_check_transformers_semantics():
    sft_train.check_transformers()


# ------------------------------------------------------------------------------------------------ (e) tags

def test_ensure_tags_order_ids_and_idempotence():
    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer)
    n = len(tokenizer)
    for tag in contract.TAGS:
        assert len(tokenizer.encode(tag, add_special_tokens=False)) > 1
    report = ensure_tags(tokenizer, model)
    assert report['status'] == 'initialized' and report['added'] and not report['resized']
    assert [report['tag_ids'][tag] for tag in contract.TAGS] == list(range(n, n + 8))
    assert tokenizer.additional_special_tokens == list(contract.TAGS)
    assert contract.tag_ids(tokenizer) == report['tag_ids']
    contract.token_ids(tokenizer)
    assert len(contract.count_ids(tokenizer)) == 3
    assert len(contract.branches_ids(tokenizer)) >= 1
    assert all(len(contract.path_prefix_ids(tokenizer, k)) == 2 for k in range(1, 5))
    assert report['max_offdiag_cos'] < 0.95
    weight = model.get_input_embeddings().weight
    # each tag row is near the mean of its pieces' rows and different from every other tag
    for tag in contract.TAGS:
        pieces = [i for piece in tag_pieces(tag) for i in tokenizer.encode(piece, add_special_tokens=False)]
        assert pieces == report['pieces'][tag]
        mean = weight[pieces].mean(0)
        cos = torch.nn.functional.cosine_similarity(weight[report['tag_ids'][tag]], mean, dim=0)
        assert cos > 0.5, (tag, cos)
    snapshot = weight.detach().clone()
    again = ensure_tags(tokenizer, model)
    assert again['status'] == 'present' and len(tokenizer) == n + 8
    assert torch.equal(snapshot, model.get_input_embeddings().weight)
    # same seed -> same rows
    tokenizer2 = build_tiny_tokenizer()
    model2 = build_tiny_model(tokenizer2)
    ensure_tags(tokenizer2, model2)
    assert torch.equal(snapshot, model2.get_input_embeddings().weight)


def test_ensure_tags_resizes_and_handles_untied_heads():
    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer, rows=len(tokenizer))
    report = ensure_tags(tokenizer, model)
    assert report['resized'] and report['rows'] == len(tokenizer) == report['rows_before'] + 8
    assert model.get_output_embeddings().weight.data_ptr() == model.get_input_embeddings().weight.data_ptr()

    tokenizer = build_tiny_tokenizer()
    model = build_tiny_model(tokenizer)
    model.config.tie_word_embeddings = False
    model.lm_head.weight = torch.nn.Parameter(model.lm_head.weight.detach().clone() * 2)
    report = ensure_tags(tokenizer, model)
    assert not report['tied']
    ids = [report['tag_ids'][tag] for tag in contract.TAGS]
    pieces = report['pieces']['<Parallel>']
    head = model.lm_head.weight
    assert torch.nn.functional.cosine_similarity(head[ids[0]], head[pieces].mean(0), dim=0) > 0.5
    assert not torch.equal(head[ids], model.get_input_embeddings().weight[ids])


def test_ensure_tags_unmarked_existing_tags_are_left_alone():
    tokenizer = build_tiny_tokenizer()
    tokenizer.add_special_tokens({'additional_special_tokens': list(contract.TAGS)})  # prepare_think --smoke-model
    model = build_tiny_model(tokenizer)
    snapshot = model.get_input_embeddings().weight.detach().clone()
    report = ensure_tags(tokenizer, model)
    assert report['status'] == 'present_unmarked'
    assert torch.equal(snapshot, model.get_input_embeddings().weight)
    report = ensure_tags(tokenizer, model, init_existing=True)
    assert report['status'] == 'initialized'
    partial = build_tiny_tokenizer()
    partial.add_special_tokens({'additional_special_tokens': ['<Parallel>']})
    with pytest.raises(ValueError):
        ensure_tags(partial, build_tiny_model(partial))


@pytest.mark.parametrize('attn', ['sdpa', 'eager'])
def test_gradient_checkpointing_gives_the_same_gradients(attn):
    tokenizer, model = tagged(attn)
    samples = [sample(tokenizer, text, id=str(i)) for i, text in enumerate([TWO_BLOCKS, SEQUENTIAL])]
    batch = D.collate(samples, tokenizer.pad_token_id)
    model.train()
    grads = []
    for enable in (False, True):
        if enable:
            model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
        model.zero_grad()
        losses, _ = sft_train.token_losses(model, batch)
        losses.mean().backward()
        grads.append({n: p.grad.clone() for n, p in model.named_parameters() if p.grad is not None})
    assert grads[0].keys() == grads[1].keys() and len(grads[0]) > 10
    for name in grads[0]:
        torch.testing.assert_close(grads[0][name], grads[1][name], atol=1e-5, rtol=1e-4)


def test_bf16_autocast_graph_forward_close_to_fp32():
    tokenizer, model = tagged('sdpa')
    s = sample(tokenizer, TWO_BLOCKS)
    reference = D.collate([s], tokenizer.pad_token_id)
    low = D.collate([s], tokenizer.pad_token_id, dtype=torch.bfloat16)
    with torch.no_grad():
        exact, _ = sft_train.token_losses(model, reference)
        with torch.autocast('cpu', dtype=torch.bfloat16):
            approx, _ = sft_train.token_losses(model, low)
    assert torch.isfinite(approx).all()
    assert (exact - approx).abs().max() < 0.1
