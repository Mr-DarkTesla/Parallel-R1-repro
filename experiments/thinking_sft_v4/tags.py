"""Add the eight contract tags to a tokenizer + model and initialize their embedding rows.

The tags are added exactly as the RL side does (experiments/qwen06/prepare_think.py):
tokenizer.add_special_tokens({'additional_special_tokens': list(contract.TAGS)}), so on Qwen3-0.6B they become
151669..151676 in contract.TAGS order and fit into the padded embedding rows (151936) without a resize.

Each new tag row (input embedding, and lm_head when untied) starts at the mean of the rows of the tag's text
pieces ('<', 'Parallel', '>' encoded separately) plus seeded gaussian noise scaled to the mean row std, so tags
start near their spelling but are distinct. The model config records this in `parallel_thinking_tags`; a model
that carries the marker with matching ids (an SFT checkpoint) is left untouched.
"""
import re

import torch

from common import contract

MARKER = 'parallel_thinking_tags'


def tag_pieces(tag):
    """'</Path>' -> ['</', 'Path', '>']: the spelling of a tag, encoded piece by piece (never as the tag)."""
    return re.findall(r'</?|[A-Za-z]+|>', tag)


def piece_ids(tokenizer, tag):
    ids = []
    for piece in tag_pieces(tag):
        ids += tokenizer.encode(piece, add_special_tokens=False)
    return ids


def check_ids(tokenizer):
    """contract.tag_ids/token_ids/count_ids, plus the tags' ids increasing in contract.TAGS order."""
    tags = contract.tag_ids(tokenizer)
    tokens = contract.token_ids(tokenizer)
    counts = contract.count_ids(tokenizer)
    ordered = [tags[tag] for tag in contract.TAGS]
    if ordered != sorted(ordered) or ordered != list(range(ordered[0], ordered[0] + len(ordered))):
        raise ValueError(f'tag ids {ordered} are not consecutive in contract.TAGS order')
    return dict(tag_ids=tags, token_ids=tokens, count_ids=list(counts),
                branches_ids=contract.branches_ids(tokenizer))


def _cosines(rows):
    normed = torch.nn.functional.normalize(rows.float(), dim=-1)
    cos = normed @ normed.T
    cos.fill_diagonal_(-1.0)
    return cos.max().item()


def ensure_tags(tokenizer, model, seed=0, noise=0.5, init_existing=False):
    """Idempotently add and initialize the contract tags. Returns a report dict.

    status: 'initialized' (tags added now, rows initialized), 'present' (marker found: nothing done),
    'present_unmarked' (tags already in the tokenizer, no marker: rows left alone unless init_existing).
    """
    vocab = tokenizer.get_vocab()
    present = [tag for tag in contract.TAGS if tag in vocab]
    if present and len(present) != len(contract.TAGS):
        raise ValueError(f'tokenizer has only some contract tags: {present}')
    base_len = len(tokenizer) - (len(present) if present else 0)
    report = dict(contract_revision=contract.CONTRACT_REVISION, contract_sha256=contract.SHA256, seed=seed,
                  noise=noise, len_tokenizer_before=len(tokenizer), added=False, resized=False)
    if not present:
        tokenizer.add_special_tokens({'additional_special_tokens': list(contract.TAGS)})
        report['added'] = True
    ids = check_ids(tokenizer)
    report.update(ids)
    report['len_tokenizer'] = len(tokenizer)

    embeddings = model.get_input_embeddings()
    rows = embeddings.weight.size(0)
    report['rows_before'] = rows
    if len(tokenizer) > rows:
        model.resize_token_embeddings(len(tokenizer), mean_resizing=False)
        report['resized'] = True
        embeddings = model.get_input_embeddings()
    report['rows'] = embeddings.weight.size(0)
    tag_rows = [ids['tag_ids'][tag] for tag in contract.TAGS]

    marker = getattr(model.config, MARKER, None)
    if present and marker:
        if list(marker.get('ids', [])) != tag_rows:
            raise ValueError(f'model marker ids {marker.get("ids")} != tokenizer tag ids {tag_rows}')
        report['status'] = 'present'
        report['max_offdiag_cos'] = _cosines(embeddings.weight[tag_rows].detach())
        return report
    if present and not init_existing:
        report['status'] = 'present_unmarked'
        report['max_offdiag_cos'] = _cosines(embeddings.weight[tag_rows].detach())
        print('ensure_tags: tags present but the model has no init marker; rows left as they are '
              '(pass init_existing=True to initialize them)')
        return report

    output = model.get_output_embeddings()
    tied = output is None or output.weight.data_ptr() == embeddings.weight.data_ptr()
    report['tied'] = tied
    generator = torch.Generator().manual_seed(seed)
    pieces = {tag: piece_ids(tokenizer, tag) for tag in contract.TAGS}
    for tag, piece in pieces.items():
        if not piece or any(p >= base_len for p in piece):
            raise ValueError(f'pieces of {tag} {piece} are empty or not base tokens')
    report['pieces'] = pieces
    matrices = [embeddings.weight] + ([] if tied else [output.weight])
    with torch.no_grad():
        for weight in matrices:
            reference = weight[:base_len].float()
            scale = reference.std(dim=-1).mean().item()
            for tag, row in zip(contract.TAGS, tag_rows):
                mean = reference[pieces[tag]].mean(dim=0)
                jitter = torch.randn(weight.size(1), generator=generator) * noise * scale
                weight[row] = (mean + jitter.to(mean.device)).to(weight.dtype)
    report['row_std'] = embeddings.weight[:base_len].float().std(dim=-1).mean().item()
    report['max_offdiag_cos'] = _cosines(embeddings.weight[tag_rows].detach())
    report['status'] = 'initialized'
    setattr(model.config, MARKER, dict(tags=list(contract.TAGS), ids=tag_rows, init='mean_of_pieces+noise',
                                       noise=noise, seed=seed, contract_revision=contract.CONTRACT_REVISION))
    return report
