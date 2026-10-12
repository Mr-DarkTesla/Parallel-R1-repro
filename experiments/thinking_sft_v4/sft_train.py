"""Thinking-SFT v4 trainer: graph-masked full-parameter SFT of Qwen3 on parallel and sequential thinking rows.

Target: Qwen/Qwen3-4B (common.BASE_MODEL, pinned revision) on ONE H100 NVL (94 GB), sequences up to 16384 tokens.
Exact VM commands are in README.md; the short form:

    python sft_train.py --data train.jsonl --val val.jsonl --out runs/sft_v4_4b --memory-report 3   # fit check
    python sft_train.py --data train.jsonl --val val.jsonl --out runs/sft_v4_4b                      # 3 epochs

Each sample is one sequence: parallel rows use contract.graph_positions and contract.graph_attention_mask (a
branch never sees its siblings), passed to the model as an additive 4D mask plus explicit position_ids;
sequential rows are plain causal. The loss is the mean over loss tokens of an optimizer step (micro-batches
accumulate until --grad-accum-tokens real tokens). The final checkpoint (bf16 safetensors by default) goes to
<out>/final with the tokenizer (tags added) and train_manifest.json; metrics go to <out>/metrics.jsonl.

Memory (4B = 4.02e9 params, tied embeddings; numbers for --optim adamw):
    fp32 weights 16.1 GB + fp32 grads 16.1 GB + fp32 AdamW exp_avg/exp_avg_sq 32.2 GB = 64.4 GB static
    (--optim adamw8bit, bitsandbytes when installed: states 8 GB -> 40 GB static). The rest (~25 GB) is for
    activations, so at 16k tokens:
  * gradient checkpointing per decoder layer (--grad-ckpt, default on when the longest training sample exceeds
    --grad-ckpt-min-len): keeps only each layer's fp32 input (T*2560*4 B = 168 MB at 16k, 6 GB for 36 layers)
    plus one recomputed layer (~3 GB) instead of ~2 GB per layer;
  * chunked LM loss (token_losses): the decoder runs to hidden states, only positions whose TARGET is in loss are
    gathered, and lm_head + fp32 cross entropy run on --loss-chunk rows at a time, each chunk checkpointed, so
    the [T, vocab] logits (16k x 151936 fp32 = 10 GB, plus as much for the softmax grad) never exist; a 2048-row
    chunk peaks at ~4 GB transient. Same loss and gradients as the full computation (tests/test_sft.py);
  * the additive mask is built directly in the compute dtype (bf16 under autocast: 0.5 GB at 16k), T rounded up
    to --pad-multiple (16 on CUDA) so SDPA's memory-efficient kernel needs no per-layer padded copy;
  * --sdpa-backend efficient (default on CUDA) allows only the memory-efficient SDPA kernel: the math fallback
    would materialize heads*T*T scores (17 GB per layer at 16k) and is turned into an error instead. --attn eager
    has the same problem and is for tests only;
  * with checkpointing, autocast runs with cache_enabled=False: the weight-cast cache would otherwise keep a bf16
    copy of all weights (7.5 GiB) through every forward;
  * expected peak ~70-75 GiB of the 93.6 GiB the H100 NVL reports, at 16k with adamw (estimate in README.md);
    --memory-report N runs N optimizer steps (two micro-batches each, so the second forward sees allocated
    grads) on the N longest training rows and prints torch.cuda.max_memory_allocated per phase.
Rows longer than --max-len (default 16384) are dropped and counted (reason too_long), never truncated.

Tag schedule (optional, README "Tag warmup"): --tag-warmup-steps K > 0 first runs K optimizer steps (stage=tag_warmup
in metrics.jsonl, not counted in the main schedule) in which only the eight tag rows of the tied embedding matrix
are trained: every other parameter has requires_grad=False, a gradient hook zeroes the other rows, and RowAdam
(Adam moments for the 8 rows only) runs at --tag-lr with a 10% warmup, then constant, no weight decay. Stage 2 is
the unchanged full run with a fresh optimizer; --tag-lr-mult M != 1 steps the tag rows there with a separate RowAdam
at M x the main lr (TagLrBoost: scaling their gradient would not change an Adam step). Every training record logs
tag_row_norm, tag_row_delta and loss_tag (CE on targets <Parallel>, count digit, </Plan>, </Path>, </Summary>).

transformers 4.51.3 / Qwen3: a 4D attention_mask is used as-is (assumed additive: _prepare_4d_causal_attention_
mask_with_cache_position returns it unchanged), AttentionMaskConverter._ignore_causal_mask_sdpa returns False for
any 4D mask (so SDPA never switches to is_causal), and _unmask_unattended (CUDA only) only touches fully masked
rows, of which collate() makes none; it compares against finfo(fp32).min (the embeddings are fp32) and leaves a
bf16 mask unchanged, at the cost of one extra mask-sized copy per forward. check_transformers() asserts these
facts on the installed version.
"""
import argparse
import hashlib
import inspect
import json
import math
import os
import random
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import BASE_MODEL, CONTRACT_PATH, KNOWN_REVISIONS, contract, default_revision  # noqa: E402
from sft_data import (CONTROL_KINDS, CONTROL_LOSS_KINDS, IGNORE, MODES, build_dataset, collate,  # noqa: E402
                      group_steps, id_in_val, read_jsonl, token_batches)
from tags import ensure_tags, tag_matrices, tag_row_ids  # noqa: E402


def check_transformers():
    """Assert the 4D-mask semantics this trainer relies on (see module docstring)."""
    import transformers
    from transformers.modeling_attn_mask_utils import AttentionMaskConverter
    from transformers.models.qwen3 import modeling_qwen3
    source = inspect.getsource(modeling_qwen3.Qwen3Model._prepare_4d_causal_attention_mask_with_cache_position)
    assert 'attention_mask.dim() == 4' in source and 'causal_mask = attention_mask' in source, \
        f'transformers {transformers.__version__}: Qwen3 no longer passes 4D masks through unchanged'
    embeds = torch.zeros(1, 3, 2)
    mask = torch.zeros(1, 1, 3, 3)
    for window in (None, 2):
        assert not AttentionMaskConverter._ignore_causal_mask_sdpa(mask, embeds, 0, window, is_training=True), \
            'SDPA would drop the 4D mask'
    # _unmask_unattended (applied on CUDA) must leave a collate()-style mask unchanged: no fully masked rows, in
    # the compute dtype, compared against the fp32 min (embeddings are fp32) or its own min
    source = inspect.getsource(modeling_qwen3.Qwen3Model._update_causal_mask)
    assert '_unmask_unattended(causal_mask, min_dtype)' in source and 'min_dtype = torch.finfo(dtype).min' in source
    for dtype in (torch.float32, torch.bfloat16):
        low = torch.finfo(dtype).min
        mask = torch.full((1, 1, 4, 4), low, dtype=dtype).triu(1)
        mask[0, 0, 3, :3] = low  # a padded query: sees itself only
        for reference in (torch.finfo(torch.float32).min, low):
            out = AttentionMaskConverter._unmask_unattended(mask, reference)
            assert out.dtype == dtype and torch.equal(out, mask), '_unmask_unattended changes the graph mask'
    return transformers.__version__


def configure_sdpa(choice, cuda):
    """'efficient': on CUDA allow only the memory-efficient SDPA kernel (it supports an additive mask in O(T)
    memory); a shape it cannot run raises instead of silently falling back to the math kernel, which stores
    heads*T*T scores. 'auto': PyTorch's own dispatch. Returns the enabled backends."""
    if not cuda or choice == 'auto':
        return 'auto'
    backends = torch.backends.cuda
    backends.enable_flash_sdp(False)  # flash takes no arbitrary mask; never chosen with one anyway
    backends.enable_math_sdp(False)
    if hasattr(backends, 'enable_cudnn_sdp'):
        backends.enable_cudnn_sdp(False)
    backends.enable_mem_efficient_sdp(True)
    return 'efficient'


def token_losses(model, batch, chunk=2048):
    """Per-token cross entropy of every loss target (the chunked LM loss). Returns (losses (N,), selection
    (B, T-1) bool): losses[i] is the loss of predicting token t+1 of row b for the i-th True entry (b, t) of the
    selection. The decoder runs to hidden states; only positions whose target token is in loss are gathered;
    lm_head + fp32 cross entropy run on `chunk` rows at a time, each chunk under activation checkpointing when
    grad is enabled, so neither the (B, T, vocab) logits nor their softmax grad is ever stored (peak ~ chunk *
    vocab * 8 bytes). Call it under autocast for a bf16 lm_head matmul. Equal to cross entropy on the full
    logits model(...).logits[:, :-1] at the labels[:, 1:] != IGNORE positions, gradients included."""
    out = model.get_decoder()(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'],
                      position_ids=batch['position_ids'], use_cache=False)
    hidden = out.last_hidden_state[:, :-1]
    target = batch['labels'][:, 1:]
    selection = target != IGNORE
    hidden, target = hidden[selection], target[selection]
    head = model.get_output_embeddings()

    def piece(h, y):
        return F.cross_entropy(head(h).float(), y, reduction='none')

    losses = []
    for begin in range(0, target.numel(), chunk):
        h, y = hidden[begin:begin + chunk], target[begin:begin + chunk]
        losses.append(checkpoint(piece, h, y, use_reentrant=False) if torch.is_grad_enabled() else piece(h, y))
    if not losses:
        return hidden.sum(-1) * 0.0, selection
    return torch.cat(losses), selection


def build_optimizer(params, args, cuda):
    """torch AdamW (fused on CUDA) or, with --optim adamw8bit, bitsandbytes AdamW8bit (8-bit states: 2 bytes per
    parameter instead of 8). bitsandbytes is optional: imported only here, with a clear error when missing."""
    kwargs = dict(lr=args.lr, betas=tuple(args.betas), weight_decay=args.weight_decay)
    if args.optim == 'adamw':
        return torch.optim.AdamW(params, fused=cuda, **kwargs)
    if args.optim == 'adamw8bit':
        try:
            import bitsandbytes
        except ImportError as error:
            raise SystemExit(f'--optim adamw8bit needs the optional package bitsandbytes, which is not importable '
                             f'({error}); install it on the VM (pip install bitsandbytes) or use --optim adamw') \
                from error
        if not cuda:
            raise SystemExit('--optim adamw8bit needs CUDA (bitsandbytes 8-bit optimizers run on GPU)')
        return bitsandbytes.optim.AdamW8bit(params, **kwargs)
    raise ValueError(f'unknown optimizer {args.optim}')


# Targets that are contract tags or the branch count (kinds 0..4 of CONTROL_KINDS): logged as loss_tag.
TAG_TARGET_KINDS = CONTROL_KINDS[:5]
assert TAG_TARGET_KINDS == ('<Parallel>', 'count', '</Plan>', '</Path>', '</Summary>'), TAG_TARGET_KINDS


class Meter:
    """Sums of per-token losses by mode and control kind; 'tag' = targets in TAG_TARGET_KINDS (loss_tag)."""

    def __init__(self):
        self.sum, self.count = defaultdict(float), defaultdict(int)

    def add(self, losses, selection, batch):
        losses = losses.detach().float()
        rows = selection.nonzero(as_tuple=True)[0]
        modes = batch['mode_index'][rows]
        control = batch['control'][:, 1:][selection]
        groups = {'all': torch.ones_like(modes, dtype=torch.bool)}
        for index, mode in enumerate(MODES):
            groups[mode] = modes == index
        groups['control'] = (control >= 0) & (control < len(CONTROL_LOSS_KINDS))
        groups['tag'] = (control >= 0) & (control < len(TAG_TARGET_KINDS))
        for index, kind in enumerate(CONTROL_KINDS):
            groups['ctrl:' + kind] = control == index
        for name, chosen in groups.items():
            count = int(chosen.sum())
            if count:
                self.sum[name] += losses[chosen].sum().item()
                self.count[name] += count

    def means(self, prefix='loss'):
        out = {}
        for name, total in self.sum.items():
            key = prefix if name == 'all' else f'{prefix}_{name}'
            out[key] = total / self.count[name]
        out[f'{prefix}_tokens'] = self.count.get('all', 0)
        out[f'{prefix}_tag_tokens'] = self.count.get('tag', 0)
        return out


# ------------------------------------------------------------------------------------- tag-row schedule

class RowAdam:
    """Adam without weight decay on a few rows of some matrices (the eight tag rows of the embedding matrix,
    and of lm_head when untied). Keeps its own fp32 moments of shape [len(rows), hidden] per matrix: 2 x 8 x 2560
    x 4 B = 160 KiB on the 4B model, instead of AdamW states for the whole 151936-row matrix (2.9 GiB). The update
    is torch.optim.AdamW(weight_decay=0)'s on those rows (tests/test_tag_warmup.py); other rows are never written.
    step(lr, grads) takes the rows' gradients ([len(rows), hidden] each, in self.weights order)."""

    def __init__(self, weights, rows, betas=(0.9, 0.95), eps=1e-8):
        self.weights = list(weights)
        self.rows = torch.as_tensor(list(rows), dtype=torch.long, device=self.weights[0].device)
        self.betas, self.eps, self.t = tuple(betas), eps, 0
        self.exp_avg = [torch.zeros(len(self.rows), w.size(1), dtype=torch.float32, device=w.device)
                        for w in self.weights]
        self.exp_avg_sq = [torch.zeros_like(m) for m in self.exp_avg]

    def state_bytes(self):
        return sum(m.numel() * m.element_size() for m in self.exp_avg + self.exp_avg_sq)

    @torch.no_grad()
    def step(self, lr, grads):
        self.t += 1
        beta1, beta2 = self.betas
        step_size = lr / (1 - beta1 ** self.t)
        correction2 = math.sqrt(1 - beta2 ** self.t)
        for weight, grad, m, v in zip(self.weights, grads, self.exp_avg, self.exp_avg_sq):
            grad = grad.float()
            m.lerp_(grad, 1 - beta1)
            v.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)
            denom = (v.sqrt() / correction2).add_(self.eps)
            rows = weight.index_select(0, self.rows).float().addcdiv_(m, denom, value=-step_size)
            weight.index_copy_(0, self.rows, rows.to(weight.dtype))


def row_grads(weights, rows):
    """[len(rows), hidden] gradient copies of the given rows (zeros when a matrix has no grad)."""
    index = torch.as_tensor(list(rows), dtype=torch.long, device=weights[0].device)
    return [w.grad.index_select(0, index) if w.grad is not None else
            torch.zeros(len(index), w.size(1), dtype=w.dtype, device=w.device) for w in weights]


def tag_row_stats(weights, rows, initial):
    """tag_row_norm: mean L2 norm of the tag rows of the input embedding; tag_row_delta: mean L2 distance of
    those rows from their values before training (after ensure_tags)."""
    with torch.no_grad():
        current = weights[0].detach()[list(rows)].float()
        return dict(tag_row_norm=current.norm(dim=-1).mean().item(),
                    tag_row_delta=(current - initial[0].float()).norm(dim=-1).mean().item())


def freeze_to_tag_rows(model, rows):
    """Stage 1: only the matrices holding the tag rows keep requires_grad (with tied embeddings: the one embedding
    matrix), and a post-accumulate hook zeroes every other row of their gradient in place (no gradient-sized
    copy). Returns undo(), which removes the hooks and restores every parameter's requires_grad."""
    weights = tag_matrices(model)
    previous = [(p, p.requires_grad) for p in model.parameters()]
    keep = {id(w) for w in weights}
    for p, _ in previous:
        p.requires_grad_(id(p) in keep)
    handles = []
    for weight in weights:
        mask = torch.zeros(weight.size(0), 1, dtype=weight.dtype, device=weight.device)
        mask[list(rows)] = 1

        def zero_other_rows(param, mask=mask):
            param.grad.mul_(mask)
        handles.append(weight.register_post_accumulate_grad_hook(zero_other_rows))

    def undo():
        for handle in handles:
            handle.remove()
        for p, flag in previous:
            p.requires_grad_(flag)
    return undo


def tag_warmup_plan(plans, lengths, args):
    """Stage-1 optimizer steps: the first --tag-warmup-steps steps of the main run's shuffled stream (epoch plans
    in order; further reshuffles if K exceeds the whole run). The main schedule is not changed by them."""
    stream = [step for plan in plans for step in plan]
    extra = 0
    while len(stream) < args.tag_warmup_steps:
        stream += group_steps(token_batches(lengths, args.micro_batch_tokens,
                                            seed=args.seed * 1000 + len(plans) + extra),
                              lengths, args.grad_accum_tokens)
        extra += 1
    return stream[:args.tag_warmup_steps]


def tag_lr_factor(step, total):
    """Stage-1 lr factor of 1-based step: linear warmup over ceil(10% of the steps), then constant."""
    warmup = max(1, math.ceil(0.1 * total))
    return min(1.0, step / warmup)


def run_tag_warmup(model, train, steps, rows, initial, args, device, dtype, autocast, pad_id, log):
    """Stage 1 (--tag-warmup-steps K > 0): K optimizer steps that update ONLY the eight tag rows. Same collate,
    chunked loss and per-step normalization as the main run; RowAdam at --tag-lr (own warmup, then constant),
    weight decay 0; gradients clipped to --grad-clip (the norm is that of the tag rows: the rest is zeroed).
    Logged as stage=tag_warmup with tag_step 1..K; the main run's step counter and schedule are unaffected.
    Memory: no gradient or optimizer state for anything but the embedding matrix (see README)."""
    weights = tag_matrices(model)
    undo = freeze_to_tag_rows(model, rows)
    adam = RowAdam(weights, rows, args.betas)
    start, first, last = time.time(), None, None
    try:
        for number, micro_batches in enumerate(steps, 1):
            step_start = time.time()
            n_loss = sum(train[i]['n_loss'] for batch in micro_batches for i in batch)
            n_tokens = sum(train[i]['length'] for batch in micro_batches for i in batch)
            meter = Meter()
            _reset_peak(device)
            for indices in micro_batches:
                batch = collate([train[i] for i in indices], pad_id, dtype=dtype, device=device,
                                pad_multiple=args.pad_multiple)
                with autocast():
                    losses, selection = token_losses(model, batch, args.loss_chunk)
                (losses.sum() / max(1, n_loss)).backward()
                meter.add(losses, selection, batch)
                del batch, losses, selection
            grad_norm = torch.nn.utils.clip_grad_norm_(weights, args.grad_clip).item()
            lr = args.tag_lr * tag_lr_factor(number, len(steps))
            adam.step(lr, row_grads(weights, rows))
            for weight in weights:
                weight.grad = None
            record = dict(stage='tag_warmup', tag_step=number, lr=lr, grad_norm=grad_norm, tokens=n_tokens,
                          loss_tokens_step=n_loss, micro_batches=len(micro_batches),
                          tokens_per_s=n_tokens / max(time.time() - step_start, 1e-9), elapsed=time.time() - start,
                          max_mem_gb=(_cuda_mem(device) or {}).get('peak_gb'),
                          **tag_row_stats(weights, rows, initial), **meter.means('loss'))
            first = first or record
            last = record
            if number % args.log_every == 0 or number == len(steps):
                log(record)
    finally:
        undo()
    keys = ('loss', 'loss_tag', 'tag_row_norm', 'tag_row_delta')
    return dict(steps_run=len(steps), seconds=time.time() - start, optimizer_state_bytes=adam.state_bytes(),
                first={k: first.get(k) for k in keys} if first else None,
                last={k: last.get(k) for k in keys} if last else None)


class TagLrBoost:
    """Stage 2 with --tag-lr-mult M != 1: the tag rows get M x the main lr. Scaling their gradient would not do it
    (Adam's step does not depend on the gradient scale), so the tag rows are taken out of the main optimizer and
    stepped by a RowAdam at M x the current main lr:
      before_step() (after clipping): copy the tag rows' gradients, zero them in .grad (the main AdamW's moments
        for these rows stay 0, so its update there is 0) and save the rows;
      after_step(lr) (after the main step): write the saved rows back (so the main optimizer's weight decay,
        or an 8-bit optimizer's quantization noise, never touches them), then RowAdam.step(M * lr).
    The tag rows thus get no weight decay. Memory: the 160 KiB moments plus two [8, hidden] copies per step."""

    def __init__(self, model, rows, mult, betas):
        self.weights, self.rows, self.mult = tag_matrices(model), list(rows), mult
        self.index = torch.as_tensor(self.rows, dtype=torch.long, device=self.weights[0].device)
        self.adam = RowAdam(self.weights, self.rows, betas)
        self.grads = self.saved = None

    @torch.no_grad()
    def before_step(self):
        self.grads = row_grads(self.weights, self.rows)
        for weight in self.weights:
            if weight.grad is not None:
                weight.grad.index_fill_(0, self.index, 0.0)
        self.saved = [weight.detach().index_select(0, self.index) for weight in self.weights]

    @torch.no_grad()
    def after_step(self, lr):
        for weight, saved in zip(self.weights, self.saved):
            weight.index_copy_(0, self.index, saved)
        self.adam.step(self.mult * lr, self.grads)
        self.grads = self.saved = None


def fingerprint(tensor):
    """Integer checksums of a tensor's bits, computed on its device in chunks (no full copy): (sum of the
    elements' bit patterns, position-weighted sum). Changing any single element changes the first sum."""
    bits = tensor.detach().contiguous().view(-1)
    bits = bits.view({8: torch.int64, 4: torch.int32, 2: torch.int16, 1: torch.uint8}[bits.element_size()])
    total = torch.zeros(2, dtype=torch.int64, device=bits.device)
    chunk = 1 << 24
    for begin in range(0, bits.numel(), chunk):
        part = bits[begin:begin + chunk].to(torch.int64)
        weight = torch.arange(begin, begin + part.numel(), dtype=torch.int64, device=bits.device) % 1000003 + 1
        total[0] += part.sum()
        total[1] += (part * weight).sum()
    return tuple(total.tolist())


def frozen_fingerprints(model, rows):
    """fingerprint() of every parameter, the matrices holding tag rows without those rows (they are consecutive)."""
    first, end = min(rows), max(rows) + 1
    assert list(rows) == list(range(first, end)), rows
    tagged = {id(w) for w in tag_matrices(model)}
    out = {}
    for name, p in model.named_parameters():
        if id(p) in tagged:
            out[name + '[:tags]'] = fingerprint(p[:first])
            out[name + '[tags:]'] = fingerprint(p[end:])
        else:
            out[name] = fingerprint(p)
    return out


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


HERE = Path(__file__).resolve().parent


def _git(*args):
    try:
        result = subprocess.run(['git', *args], cwd=HERE, capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else None
    except Exception:
        return None


def git_revision():
    return (_git('rev-parse', 'HEAD') or '').strip() or None


def code_state():
    """HEAD, whether this package differs from it (uncommitted or untracked files), and sha256 of its .py files:
    the code that trained a checkpoint, even from a dirty tree."""
    status = _git('status', '--porcelain', '--', '.')
    return dict(git=git_revision(), dirty=None if status is None else bool(status.strip()),
                dirty_files=None if status is None else status.splitlines(),
                package_sha256={path.name: sha256(path) for path in sorted(HERE.glob('*.py'))},
                contract_sha256=contract.SHA256)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--model', default=BASE_MODEL, help='HF id or local path (base model or SFT checkpoint)')
    parser.add_argument('--revision', default=None,
                        help=f'HF revision of --model (default: the pinned one for {sorted(KNOWN_REVISIONS)}, as '
                             f'vm_selftest)')
    parser.add_argument('--data', required=True, type=Path)
    parser.add_argument('--val', type=Path, default=None)
    parser.add_argument('--val-frac', type=float, default=0.02, help='id-hash split when --val is not given')
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--max-len', type=int, default=16384,
                        help='longer rows (prompt included) are dropped and counted as too_long, never truncated')
    parser.add_argument('--epochs', type=int, default=3)
    parser.add_argument('--lr', type=float, default=1e-5)
    parser.add_argument('--min-lr-ratio', type=float, default=0.1)
    parser.add_argument('--warmup-ratio', type=float, default=0.03)
    parser.add_argument('--weight-decay', type=float, default=0.0)
    parser.add_argument('--betas', type=float, nargs=2, default=(0.9, 0.95))
    parser.add_argument('--grad-clip', type=float, default=1.0)
    parser.add_argument('--micro-batch-tokens', type=int, default=16384, help='padded tokens per micro-batch')
    parser.add_argument('--grad-accum-tokens', type=int, default=393216,
                        help='real tokens per optimizer step (default ~54 rows of 7.2k: ~92 steps per epoch on '
                             '5k rows)')
    parser.add_argument('--target-steps-per-epoch', type=int, default=0,
                        help='if > 0, set --grad-accum-tokens = ceil(training tokens / this) (60-120 suggested)')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--bf16', action=argparse.BooleanOptionalAction, default=None,
                        help='bf16 autocast forward (default: on with CUDA)')
    parser.add_argument('--grad-ckpt', action=argparse.BooleanOptionalAction, default=None,
                        help='gradient checkpointing per decoder layer (default: on when the longest training '
                             'sample exceeds --grad-ckpt-min-len)')
    parser.add_argument('--grad-ckpt-min-len', type=int, default=2048)
    parser.add_argument('--loss-chunk', type=int, default=2048, help='rows per lm_head + cross-entropy chunk')
    parser.add_argument('--optim', choices=('adamw', 'adamw8bit'), default='adamw',
                        help='adamw: torch AdamW, fused on CUDA (fp32 states, 8 B/param); adamw8bit: bitsandbytes '
                             'AdamW8bit if importable (2 B/param)')
    parser.add_argument('--pad-multiple', type=int, default=None,
                        help='round micro-batch length up to this (default 16 on CUDA, 1 on CPU)')
    parser.add_argument('--sdpa-backend', choices=('efficient', 'auto'), default='efficient',
                        help='CUDA: efficient = memory-efficient SDPA kernel only (no T*T fallback); auto = torch')
    parser.add_argument('--memory-report', type=int, default=0, metavar='N',
                        help='run N optimizer steps on the N longest training rows, print '
                             'torch.cuda.max_memory_allocated per phase to stdout and <out>/memory_report.json, exit')
    parser.add_argument('--attn', choices=('sdpa', 'eager'), default='sdpa',
                        help='eager stores heads*T*T attention weights: tests and short rows only')
    parser.add_argument('--save-every-epoch', action='store_true')
    parser.add_argument('--save-dtype', choices=('bfloat16', 'float32'), default='bfloat16')
    parser.add_argument('--eval-every', type=int, default=0, help='also evaluate every N optimizer steps')
    parser.add_argument('--log-every', type=int, default=1)
    parser.add_argument('--max-invalid-frac', type=float, default=0.0,
                        help='abort if more invalid (not too-long) rows than this fraction')
    parser.add_argument('--init-existing-tags', action='store_true',
                        help='initialize tag rows even if the tokenizer already has the tags but no init marker')
    parser.add_argument('--max-steps', type=int, default=0, help='stop after N optimizer steps (debug)')
    parser.add_argument('--tag-warmup-steps', type=int, default=0, metavar='K',
                        help='stage 1: K optimizer steps that update ONLY the eight tag rows of the embedding '
                             'matrix (all else frozen), RowAdam at --tag-lr, before the full run; 0 = off. Not '
                             'counted in the main schedule (README: 60 for the 4B run)')
    parser.add_argument('--tag-lr', type=float, default=1e-3,
                        help='stage-1 lr: linear warmup over 10%% of --tag-warmup-steps, then constant; no weight '
                             'decay')
    parser.add_argument('--tag-lr-mult', type=float, default=1.0, metavar='M',
                        help='stage 2: the tag rows are stepped by a separate Adam at M x the main lr (taken out of '
                             'the main optimizer, no weight decay); 1 = off (they are ordinary AdamW rows)')
    parser.add_argument('--freeze-check', action='store_true',
                        help='after stage 1, assert every parameter except the tag rows is bit-identical to before '
                             '(on-device checksums) and the tag rows changed')
    return parser.parse_args(argv)


def load_samples(path, tokenizer, max_len, max_invalid_frac, name):
    samples, stats = build_dataset(read_jsonl(path), tokenizer, max_len)
    print(f'{name}: {json.dumps({k: v for k, v in stats.items() if k != "drop_examples"})}')
    for reason, example in stats['drop_examples'].items():
        print(f'  dropped {reason}: {example}')
    if stats['total'] and stats['invalid'] > max_invalid_frac * stats['total']:
        raise SystemExit(f'{name}: {stats["invalid"]} invalid rows of {stats["total"]} '
                         f'(> --max-invalid-frac {max_invalid_frac}): {stats["dropped"]}')
    return samples, stats


def evaluate(model, samples, pad_id, args, device, dtype, autocast):
    if not samples:
        return {}
    meter = Meter()
    was_training = model.training
    model.eval()
    lengths = [s['length'] for s in samples]
    with torch.no_grad():
        for indices in token_batches(lengths, args.micro_batch_tokens, shuffle=False):
            batch = collate([samples[i] for i in indices], pad_id, dtype=dtype, device=device,
                            pad_multiple=args.pad_multiple)
            with autocast():
                losses, selection = token_losses(model, batch, args.loss_chunk)
            meter.add(losses, selection, batch)
            del batch
    model.train(was_training)
    return meter.means('val_loss')


def save_checkpoint(model, tokenizer, path, save_dtype, manifest=None):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    dtype = getattr(torch, save_dtype)
    state = {key: value.detach().to('cpu', dtype).contiguous() for key, value in model.state_dict().items()}
    output, inputs = model.get_output_embeddings(), model.get_input_embeddings()
    if output is not None and output.weight.data_ptr() == inputs.weight.data_ptr():
        state = {key: value for key, value in state.items() if key != 'lm_head.weight'}
    model.save_pretrained(path, state_dict=state, safe_serialization=True)
    config = json.loads((path / 'config.json').read_text())
    config['torch_dtype'] = save_dtype  # save_pretrained writes the in-memory (fp32) dtype
    config['use_cache'] = True
    (path / 'config.json').write_text(json.dumps(config, indent=2, sort_keys=True) + '\n')
    tokenizer.save_pretrained(path)
    if manifest is not None:
        (path / 'train_manifest.json').write_text(json.dumps(manifest, indent=2, default=str) + '\n')


def lr_lambda(total, warmup, min_ratio):
    def factor(step):
        if step < warmup:
            return (step + 1) / warmup
        progress = (step - warmup) / max(1, total - warmup)
        return min_ratio + (1 - min_ratio) * 0.5 * (1 + math.cos(math.pi * min(1.0, progress)))
    return factor


GB = 1024 ** 3


def _cuda_mem(device):
    if device.type != 'cuda':
        return None
    return dict(peak_gb=torch.cuda.max_memory_allocated(device) / GB, now_gb=torch.cuda.memory_allocated(device) / GB,
                reserved_gb=torch.cuda.max_memory_reserved(device) / GB)


def _reset_peak(device):
    if device.type == 'cuda':
        torch.cuda.synchronize(device)
        torch.cuda.reset_peak_memory_stats(device)


def static_estimate(model, optim):
    """Bytes of weights, grads and optimizer states as allocated by this trainer (fp32 weights and grads)."""
    n = sum(p.numel() for p in model.parameters())
    per = dict(adamw=8, adamw8bit=2)[optim]
    return dict(params=n, weights_gb=4 * n / GB, grads_gb=4 * n / GB, optimizer_gb=per * n / GB,
                static_gb=(8 + per) * n / GB)


def static_estimate_tag_warmup(model, rows):
    """Stage 1 (--tag-warmup-steps): fp32 weights, a gradient only for the matrices holding tag rows (the one
    embedding matrix when tied), RowAdam moments for the tag rows only."""
    n = sum(p.numel() for p in model.parameters())
    grads = sum(w.numel() for w in tag_matrices(model))
    states = sum(2 * len(rows) * w.size(1) for w in tag_matrices(model))
    return dict(params=n, weights_gb=4 * n / GB, grads_gb=4 * grads / GB, optimizer_gb=4 * states / GB,
                static_gb=4 * (n + grads + states) / GB)


PHASES = ('forward1', 'backward1', 'forward2', 'backward2', 'optimizer')


def _memory_steps(model, step_fn, samples, order, pad_id, args, device, dtype, autocast, total, label):
    """Optimizer steps of two micro-batches each (the i-th longest sample twice); step_fn() clips, steps and
    clears the grads. Returns one record per step with torch.cuda peaks per phase."""
    records = []
    for number, index in enumerate(order, 1):
        sample = samples[index]
        record = dict(stage=label, step=number, id=sample['id'], mode=sample['mode'], length=sample['length'],
                      loss_tokens=sample['n_loss'])
        start = time.time()
        for micro in (1, 2):
            _reset_peak(device)
            batch = collate([sample], pad_id, dtype=dtype, device=device, pad_multiple=args.pad_multiple)
            record['mask_gb'] = batch['attention_mask'].numel() * batch['attention_mask'].element_size() / GB
            with autocast():
                losses, _ = token_losses(model, batch, args.loss_chunk)
            loss = losses.sum() / max(1, 2 * sample['n_loss'])
            record[f'forward{micro}'] = _cuda_mem(device)
            _reset_peak(device)
            loss.backward()
            del losses, loss, batch
            record[f'backward{micro}'] = _cuda_mem(device)
        _reset_peak(device)
        step_fn()
        record['optimizer'] = _cuda_mem(device)
        record['seconds'] = time.time() - start
        if device.type == 'cuda':
            record['peak_gb'] = max(record[phase]['peak_gb'] for phase in PHASES)
            record['headroom_gb'] = total - record['peak_gb']
        records.append(record)
        print('memory report:', json.dumps(record))
    return records


def memory_report(model, samples, rows, pad_id, args, device, dtype, autocast, cuda):
    """--memory-report N: N optimizer steps; step i accumulates two micro-batches, each the i-th longest sample
    alone, so the second forward/backward run with the fp32 grads already allocated (the worst case of the full
    run, where a 16k row can be any micro-batch of a step). Records torch.cuda.max_memory_allocated per phase:
    forward1/2 (incl. the chunked loss), backward1/2, optimizer (clip + step + zero_grad). Step 1 allocates the
    optimizer states, so steps >= 2 show the steady state. With --tag-warmup-steps > 0 the same N steps first run
    as stage 1 (tag rows only: report['tag_warmup']), then as the full run. Weights change: nothing is saved."""
    order = sorted(range(len(samples)), key=lambda i: -samples[i]['length'])[:args.memory_report]
    total = torch.cuda.get_device_properties(device).total_memory / GB if device.type == 'cuda' else None
    report = dict(device=str(device), total_gb=total, estimate=static_estimate(model, args.optim),
                  after_load=_cuda_mem(device), grad_ckpt=args.grad_ckpt, loss_chunk=args.loss_chunk,
                  optim=args.optim, sdpa=args.sdpa_backend, bf16=dtype == torch.bfloat16,
                  pad_multiple=args.pad_multiple, micro_batches_per_step=2, tag_lr_mult=args.tag_lr_mult, steps=[])
    model.train()
    stages = []
    if args.tag_warmup_steps > 0:
        weights = tag_matrices(model)
        undo = freeze_to_tag_rows(model, rows)
        adam = RowAdam(weights, rows, args.betas)

        def tag_step():
            torch.nn.utils.clip_grad_norm_(weights, args.grad_clip)
            adam.step(args.tag_lr, row_grads(weights, rows))
            for weight in weights:
                weight.grad = None
        estimate = static_estimate_tag_warmup(model, rows)
        print('memory report: stage 1 (tag rows only) static estimate (GiB)',
              json.dumps({k: round(v, 3) if isinstance(v, float) else v for k, v in estimate.items()}))
        report['tag_warmup'] = dict(estimate=estimate, steps=_memory_steps(
            model, tag_step, samples, order, pad_id, args, device, dtype, autocast, total, 'tag_warmup'))
        undo()
        stages.append(('stage 1 (tag rows only)', report['tag_warmup']))
    print('memory report: static estimate (GiB)', json.dumps({k: round(v, 2) if isinstance(v, float) else v
                                                              for k, v in report['estimate'].items()}))
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = build_optimizer(params, args, cuda)
    boost = TagLrBoost(model, rows, args.tag_lr_mult, args.betas) if args.tag_lr_mult != 1 else None

    def main_step():
        torch.nn.utils.clip_grad_norm_(params, args.grad_clip)
        if boost:
            boost.before_step()
        optimizer.step()
        if boost:
            boost.after_step(args.lr)
        optimizer.zero_grad(set_to_none=True)
    report['steps'] = _memory_steps(model, main_step, samples, order, pad_id, args, device, dtype, autocast, total,
                                    'main')
    stages.append(('full run', report))
    if device.type == 'cuda' and report['steps']:
        for name, part in stages:
            part['peak_gb'] = max(step['peak_gb'] for step in part['steps'])
            part['fits'] = part['peak_gb'] < 0.95 * total
            print(f'memory report, {name}: peak {part["peak_gb"]:.2f} GiB of {total:.2f} GiB '
                  f'({"fits" if part["fits"] else "DOES NOT FIT (or < 5% headroom)"}) on rows of '
                  f'{part["steps"][0]["length"]} tokens; peaks per phase (GiB):')
            for step in part['steps']:
                phases = '  '.join(f'{phase} {step[phase]["peak_gb"]:6.2f}' for phase in PHASES)
                print(f'  step {step["step"]} len {step["length"]:6d}: {phases}  ({step["seconds"]:.1f} s)')
    else:
        print('memory report: no CUDA device, phases ran but memory is not measured')
    (args.out / 'memory_report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main(argv=None):
    args = parse_args(argv)
    if args.tag_warmup_steps < 0 or args.tag_lr <= 0 or args.tag_lr_mult <= 0:
        raise SystemExit('--tag-warmup-steps must be >= 0, --tag-lr and --tag-lr-mult > 0')
    os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')  # before the first allocation
    from transformers import AutoModelForCausalLM, AutoTokenizer
    transformers_version = check_transformers()
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    cuda = torch.cuda.is_available()
    device = torch.device('cuda' if cuda else 'cpu')
    bf16 = cuda if args.bf16 is None else args.bf16
    dtype = torch.bfloat16 if bf16 else torch.float32  # compute dtype: the additive mask is built in it
    if args.pad_multiple is None:
        args.pad_multiple = 16 if cuda else 1
    args.sdpa_backend = configure_sdpa(args.sdpa_backend, cuda)

    def autocast():
        # With gradient checkpointing the autocast weight-cast cache would hold a bf16 copy of every weight
        # (8 GB for 4B) until the forward ends while nothing else keeps them; casting per use costs only time.
        return torch.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=bf16,
                              cache_enabled=not args.grad_ckpt)

    args.out.mkdir(parents=True, exist_ok=True)
    if args.revision is None:
        args.revision = default_revision(args.model)
    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=args.revision)
    model = AutoModelForCausalLM.from_pretrained(args.model, revision=args.revision, torch_dtype=torch.float32,
                                                 attn_implementation=args.attn)
    tag_report = ensure_tags(tokenizer, model, seed=args.seed, init_existing=args.init_existing_tags)
    print('tags:', json.dumps({k: v for k, v in tag_report.items() if k not in ('pieces', 'token_ids')}))
    model.to(device)
    rows = tag_row_ids(tokenizer)
    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id

    train, train_stats = load_samples(args.data, tokenizer, args.max_len, args.max_invalid_frac, 'train')
    if not train:
        raise SystemExit('no training samples')
    if args.grad_ckpt is None:
        args.grad_ckpt = max(s['length'] for s in train) > args.grad_ckpt_min_len
    print(f'gradient checkpointing: {args.grad_ckpt} (longest sample {max(s["length"] for s in train)} tokens); '
          f'loss chunk {args.loss_chunk}; optimizer {args.optim}; sdpa {args.sdpa_backend}; pad multiple '
          f'{args.pad_multiple}')
    if args.memory_report:
        if args.grad_ckpt:
            model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
        model.config.use_cache = False
        return memory_report(model, train, rows, pad_id, args, device, dtype, autocast, cuda)
    if args.val is not None:
        val, val_stats = load_samples(args.val, tokenizer, args.max_len, args.max_invalid_frac, 'val')
    else:
        # split by problem (sft_data.group_key), so sibling rows of one prompt never straddle train and val
        val = [s for s in train if id_in_val(s['group'], args.val_frac)]
        train = [s for s in train if not id_in_val(s['group'], args.val_frac)]
        val_stats = dict(split='group_hash', key='provenance.problem_id else task_id else sha256(prompt)',
                         frac=args.val_frac,
                         kept=len(val), groups=len({s['group'] for s in val}))
    if not train:
        raise SystemExit('no training samples')
    lengths = [s['length'] for s in train]
    if args.target_steps_per_epoch > 0:
        args.grad_accum_tokens = max(1, math.ceil(sum(lengths) / args.target_steps_per_epoch))
        print(f'--target-steps-per-epoch {args.target_steps_per_epoch}: {sum(lengths)} training tokens -> '
              f'--grad-accum-tokens {args.grad_accum_tokens}')
    if max(lengths) > args.micro_batch_tokens:
        print(f'warning: {sum(l > args.micro_batch_tokens for l in lengths)} samples exceed --micro-batch-tokens '
              f'and run alone in a micro-batch')
    plans = [group_steps(token_batches(lengths, args.micro_batch_tokens, seed=args.seed * 1000 + epoch), lengths,
                         args.grad_accum_tokens) for epoch in range(args.epochs)]
    total_steps = sum(len(plan) for plan in plans)
    if args.max_steps:
        total_steps = min(total_steps, args.max_steps)
    warmup = max(1, math.ceil(args.warmup_ratio * total_steps)) if args.warmup_ratio > 0 else 0
    print(f'train {len(train)} samples, val {len(val)}, {total_steps} optimizer steps, warmup {warmup}')

    if args.grad_ckpt:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
    model.config.use_cache = False
    model.train()

    metrics_path = args.out / 'metrics.jsonl'
    metrics = open(metrics_path, 'a')

    def log(record):
        metrics.write(json.dumps(record) + '\n')
        metrics.flush()
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in record.items()}))

    # Two-stage tag schedule: stage 1 (optional) trains only the eight tag rows; stage 2 is the full run below.
    tag_weights = tag_matrices(model)
    tag_initial = [w.detach()[rows].clone() for w in tag_weights]
    with torch.no_grad():
        base_row_norm = tag_weights[0][:rows[0]].float().norm(dim=-1).mean().item()
    tag_schedule = dict(
        rows=rows, matrices='embedding (tied lm_head)' if len(tag_weights) == 1 else 'embedding + lm_head',
        base_row_norm=base_row_norm, initial=tag_row_stats(tag_weights, rows, tag_initial),
        stage1=dict(steps=args.tag_warmup_steps, lr=args.tag_lr, enabled=args.tag_warmup_steps > 0,
                    lr_warmup_steps=max(1, math.ceil(0.1 * args.tag_warmup_steps)),
                    schedule='linear warmup over 10% of the steps, then constant', weight_decay=0.0,
                    betas=list(args.betas), grad_clip=args.grad_clip,
                    optimizer='RowAdam: Adam on the tag rows only, own fp32 moments',
                    trainable='only the tag rows (all other parameters requires_grad=False, other rows of the '
                              'tag matrices zeroed by a gradient hook)',
                    data='the first K optimizer steps of the main shuffled stream (same collate and loss); not '
                         'counted in the main schedule', freeze_check=args.freeze_check),
        stage2=dict(tag_lr_mult=args.tag_lr_mult, lr=args.lr,
                    tag_rows=('ordinary rows of the main optimizer' if args.tag_lr_mult == 1 else
                              f'excluded from the main optimizer (grads zeroed, rows restored after its step: no '
                              f'weight decay) and stepped by RowAdam at {args.tag_lr_mult} x the main lr')))
    if args.tag_warmup_steps > 0:
        before = evaluate(model, val, pad_id, args, device, dtype, autocast)
        if before:
            log(dict(stage='tag_warmup', tag_step=0, **before))
        prints = frozen_fingerprints(model, rows) if args.freeze_check else None
        summary = run_tag_warmup(model, train, tag_warmup_plan(plans, lengths, args), rows, tag_initial, args,
                                 device, dtype, autocast, pad_id, log)
        if args.freeze_check:
            after = frozen_fingerprints(model, rows)
            changed = sorted(name for name in prints if prints[name] != after[name])
            if changed:
                raise AssertionError(f'--freeze-check: stage 1 changed frozen parameters {changed}')
            moved = [not torch.equal(w.detach()[rows], initial) for w, initial in zip(tag_weights, tag_initial)]
            if not all(moved):
                raise AssertionError('--freeze-check: stage 1 did not change the tag rows')
            summary['freeze_check'] = f'passed ({len(prints)} tensors bit-identical, tag rows changed)'
            print('freeze check:', summary['freeze_check'])
        tag_schedule['stage1'].update(summary)
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = build_optimizer(params, args, cuda)  # fresh: stage 1 leaves no optimizer state behind
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda(total_steps, warmup, args.min_lr_ratio))
    boost = TagLrBoost(model, rows, args.tag_lr_mult, args.betas) if args.tag_lr_mult != 1 else None

    manifest = dict(
        contract=dict(path=str(CONTRACT_PATH), sha256=contract.SHA256, version=contract.CONTRACT_VERSION,
                      revision=contract.CONTRACT_REVISION),
        data=dict(train=str(args.data), train_sha256=sha256(args.data),
                  val=str(args.val) if args.val else None, val_sha256=sha256(args.val) if args.val else None),
        args={k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
        counts=dict(train=train_stats, val=val_stats, train_samples=len(train), val_samples=len(val)),
        base_model=dict(name=args.model, requested_revision=args.revision,
                        commit=getattr(model.config, '_commit_hash', None),
                        tokenizer_commit=tokenizer.init_kwargs.get('_commit_hash'),
                        local=Path(args.model).exists()),
        code=code_state(),
        tags={k: v for k, v in tag_report.items()}, git=git_revision(), torch=torch.__version__,
        transformers=transformers_version, bf16=bf16, device=str(device), total_steps=total_steps,
        memory=dict(estimate=static_estimate(model, args.optim), grad_ckpt=args.grad_ckpt, loss_chunk=args.loss_chunk,
                    optim=args.optim, sdpa=args.sdpa_backend, pad_multiple=args.pad_multiple,
                    tag_warmup_estimate=static_estimate_tag_warmup(model, rows)),
        tag_schedule=tag_schedule)
    val_epochs = []
    step, start = 0, time.time()
    initial = evaluate(model, val, pad_id, args, device, dtype, autocast)
    if initial:
        log(dict(step=0, epoch=0, stage='main', **initial))
    done = False
    for epoch, plan in enumerate(plans, 1):
        for micro_batches in plan:
            step_start = time.time()
            n_loss = sum(train[i]['n_loss'] for batch in micro_batches for i in batch)
            n_tokens = sum(train[i]['length'] for batch in micro_batches for i in batch)
            meter = Meter()
            _reset_peak(device)
            for indices in micro_batches:
                batch = collate([train[i] for i in indices], pad_id, dtype=dtype, device=device,
                                pad_multiple=args.pad_multiple)
                with autocast():
                    losses, selection = token_losses(model, batch, args.loss_chunk)
                (losses.sum() / max(1, n_loss)).backward()
                meter.add(losses, selection, batch)
                del batch, losses, selection
            grad_norm = torch.nn.utils.clip_grad_norm_(params, args.grad_clip).item()
            lr = scheduler.get_last_lr()[0]
            if boost:
                boost.before_step()
            optimizer.step()
            if boost:
                boost.after_step(lr)
            scheduler.step()
            optimizer.zero_grad(set_to_none=True)
            step += 1
            elapsed = time.time() - step_start
            if step % args.log_every == 0 or step == total_steps:
                log(dict(stage='main', step=step, epoch=epoch, lr=lr, grad_norm=grad_norm, tokens=n_tokens,
                         loss_tokens_step=n_loss, micro_batches=len(micro_batches),
                         tokens_per_s=n_tokens / max(elapsed, 1e-9), elapsed=time.time() - start,
                         max_mem_gb=(_cuda_mem(device) or {}).get('peak_gb'),
                         **tag_row_stats(tag_weights, rows, tag_initial), **meter.means('loss')))
            if args.eval_every and step % args.eval_every == 0:
                log(dict(stage='main', step=step, epoch=epoch,
                         **evaluate(model, val, pad_id, args, device, dtype, autocast)))
            if step >= total_steps:
                done = True
                break
        result = evaluate(model, val, pad_id, args, device, dtype, autocast)
        val_epochs.append(dict(epoch=epoch, step=step, **result))
        log(dict(stage='main', step=step, epoch=epoch, end_of_epoch=True, **result))
        (args.out / 'val_epochs.json').write_text(json.dumps(val_epochs, indent=2) + '\n')
        if args.save_every_epoch and not done and epoch < len(plans):
            save_checkpoint(model, tokenizer, args.out / f'epoch{epoch}', args.save_dtype,
                            dict(manifest, steps=step, epoch=epoch, val_epochs=val_epochs))
        if done:
            break
    tag_schedule['final'] = tag_row_stats(tag_weights, rows, tag_initial)
    manifest.update(steps=step, val_epochs=val_epochs, train_seconds=time.time() - start)
    save_checkpoint(model, tokenizer, args.out / 'final', args.save_dtype, manifest)
    (args.out / 'train_manifest.json').write_text(json.dumps(manifest, indent=2, default=str) + '\n')
    metrics.close()
    print('saved', args.out / 'final')
    return manifest


if __name__ == '__main__':
    main()
