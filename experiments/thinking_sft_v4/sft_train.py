"""Thinking-SFT v4 trainer: graph-masked SFT of Qwen3 on parallel and sequential thinking rows (single GPU).

    python sft_train.py --model Qwen/Qwen3-0.6B --data train.jsonl [--val val.jsonl] --out runs/sft_v4

Each sample is one sequence: parallel rows use contract.graph_positions and contract.graph_attention_mask (a
branch never sees its siblings), passed to the model as an additive 4D mask plus explicit position_ids;
sequential rows are plain causal. Weights and AdamW states are fp32; --bf16 (default on CUDA) runs the forward
under bf16 autocast. The loss is the mean over loss tokens of an optimizer step (micro-batches accumulate until
--grad-accum-tokens real tokens). The final checkpoint (bf16 safetensors by default) goes to <out>/final with the
tokenizer (tags added) and train_manifest.json; metrics go to <out>/metrics.jsonl.

transformers 4.51.3 / Qwen3: a 4D attention_mask is used as-is (assumed additive: _prepare_4d_causal_attention_
mask_with_cache_position returns it unchanged), AttentionMaskConverter._ignore_causal_mask_sdpa returns False for
any 4D mask (so SDPA never switches to is_causal), and _unmask_unattended only touches fully masked rows, of
which collate() makes none. check_transformers() asserts these facts on the installed version.
"""
import argparse
import hashlib
import inspect
import json
import math
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
from common import CONTRACT_PATH, contract  # noqa: E402
from sft_data import (CONTROL_KINDS, CONTROL_LOSS_KINDS, IGNORE, MODES, build_dataset, collate,  # noqa: E402
                      group_steps, id_in_val, read_jsonl, token_batches)
from tags import ensure_tags  # noqa: E402


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
    return transformers.__version__


def token_losses(model, batch, chunk=4096):
    """Per-token cross entropy of every loss target. Returns (losses (N,), selection (B, T-1) bool): losses[i]
    is the loss of predicting token t+1 of row b for the i-th True entry (b, t) of the selection. The lm_head
    runs only on selected positions, in checkpointed chunks, so (B, T, vocab) logits are never stored."""
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


class Meter:
    """Sums of per-token losses by mode and control kind."""

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
        return out


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def git_revision():
    try:
        return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=Path(__file__).parent, capture_output=True,
                              text=True, timeout=10).stdout.strip() or None
    except Exception:
        return None


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--model', required=True, help='HF id or local path (base model or SFT checkpoint)')
    parser.add_argument('--revision', default=None, help='HF revision of --model')
    parser.add_argument('--data', required=True, type=Path)
    parser.add_argument('--val', type=Path, default=None)
    parser.add_argument('--val-frac', type=float, default=0.02, help='id-hash split when --val is not given')
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--max-len', type=int, default=8192)
    parser.add_argument('--epochs', type=int, default=3)
    parser.add_argument('--lr', type=float, default=1e-5)
    parser.add_argument('--min-lr-ratio', type=float, default=0.1)
    parser.add_argument('--warmup-ratio', type=float, default=0.03)
    parser.add_argument('--weight-decay', type=float, default=0.0)
    parser.add_argument('--betas', type=float, nargs=2, default=(0.9, 0.95))
    parser.add_argument('--grad-clip', type=float, default=1.0)
    parser.add_argument('--micro-batch-tokens', type=int, default=16384, help='padded tokens per micro-batch')
    parser.add_argument('--grad-accum-tokens', type=int, default=65536, help='real tokens per optimizer step')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--bf16', action=argparse.BooleanOptionalAction, default=None,
                        help='bf16 autocast forward (default: on with CUDA)')
    parser.add_argument('--grad-ckpt', action='store_true')
    parser.add_argument('--attn', choices=('sdpa', 'eager'), default='sdpa')
    parser.add_argument('--save-every-epoch', action='store_true')
    parser.add_argument('--save-dtype', choices=('bfloat16', 'float32'), default='bfloat16')
    parser.add_argument('--eval-every', type=int, default=0, help='also evaluate every N optimizer steps')
    parser.add_argument('--log-every', type=int, default=1)
    parser.add_argument('--max-invalid-frac', type=float, default=0.0,
                        help='abort if more invalid (not too-long) rows than this fraction')
    parser.add_argument('--init-existing-tags', action='store_true',
                        help='initialize tag rows even if the tokenizer already has the tags but no init marker')
    parser.add_argument('--max-steps', type=int, default=0, help='stop after N optimizer steps (debug)')
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
            batch = collate([samples[i] for i in indices], pad_id, dtype=dtype, device=device)
            with autocast():
                losses, selection = token_losses(model, batch)
            meter.add(losses, selection, batch)
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


def main(argv=None):
    args = parse_args(argv)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    transformers_version = check_transformers()
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    cuda = torch.cuda.is_available()
    device = torch.device('cuda' if cuda else 'cpu')
    bf16 = cuda if args.bf16 is None else args.bf16
    dtype = torch.bfloat16 if bf16 else torch.float32  # compute dtype: the additive mask uses it

    def autocast():
        return torch.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=bf16)

    args.out.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=args.revision)
    model = AutoModelForCausalLM.from_pretrained(args.model, revision=args.revision, torch_dtype=torch.float32,
                                                 attn_implementation=args.attn)
    tag_report = ensure_tags(tokenizer, model, seed=args.seed, init_existing=args.init_existing_tags)
    print('tags:', json.dumps({k: v for k, v in tag_report.items() if k not in ('pieces', 'token_ids')}))
    model.to(device)
    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id

    train, train_stats = load_samples(args.data, tokenizer, args.max_len, args.max_invalid_frac, 'train')
    if args.val is not None:
        val, val_stats = load_samples(args.val, tokenizer, args.max_len, args.max_invalid_frac, 'val')
    else:
        val = [s for s in train if id_in_val(s['id'], args.val_frac)]
        train = [s for s in train if not id_in_val(s['id'], args.val_frac)]
        val_stats = dict(split='id_hash', frac=args.val_frac, kept=len(val))
    if not train:
        raise SystemExit('no training samples')
    lengths = [s['length'] for s in train]
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
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(params, lr=args.lr, betas=tuple(args.betas), weight_decay=args.weight_decay,
                                  fused=cuda)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda(total_steps, warmup, args.min_lr_ratio))

    metrics_path = args.out / 'metrics.jsonl'
    metrics = open(metrics_path, 'a')

    def log(record):
        metrics.write(json.dumps(record) + '\n')
        metrics.flush()
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in record.items()}))

    manifest = dict(
        contract=dict(path=str(CONTRACT_PATH), sha256=contract.SHA256, version=contract.CONTRACT_VERSION,
                      revision=contract.CONTRACT_REVISION),
        data=dict(train=str(args.data), train_sha256=sha256(args.data),
                  val=str(args.val) if args.val else None, val_sha256=sha256(args.val) if args.val else None),
        args={k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
        counts=dict(train=train_stats, val=val_stats, train_samples=len(train), val_samples=len(val)),
        tags={k: v for k, v in tag_report.items()}, git=git_revision(), torch=torch.__version__,
        transformers=transformers_version, bf16=bf16, device=str(device), total_steps=total_steps)
    val_epochs = []
    step, start = 0, time.time()
    initial = evaluate(model, val, pad_id, args, device, dtype, autocast)
    if initial:
        log(dict(step=0, epoch=0, **initial))
    done = False
    for epoch, plan in enumerate(plans, 1):
        for micro_batches in plan:
            step_start = time.time()
            n_loss = sum(train[i]['n_loss'] for batch in micro_batches for i in batch)
            n_tokens = sum(train[i]['length'] for batch in micro_batches for i in batch)
            meter = Meter()
            for indices in micro_batches:
                batch = collate([train[i] for i in indices], pad_id, dtype=dtype, device=device)
                with autocast():
                    losses, selection = token_losses(model, batch)
                (losses.sum() / max(1, n_loss)).backward()
                meter.add(losses, selection, batch)
            grad_norm = torch.nn.utils.clip_grad_norm_(params, args.grad_clip).item()
            optimizer.step()
            lr = scheduler.get_last_lr()[0]
            scheduler.step()
            optimizer.zero_grad(set_to_none=True)
            step += 1
            elapsed = time.time() - step_start
            if step % args.log_every == 0 or step == total_steps:
                log(dict(step=step, epoch=epoch, lr=lr, grad_norm=grad_norm, tokens=n_tokens, loss_tokens_step=n_loss,
                         micro_batches=len(micro_batches), tokens_per_s=n_tokens / max(elapsed, 1e-9),
                         elapsed=time.time() - start, **meter.means('loss')))
            if args.eval_every and step % args.eval_every == 0:
                log(dict(step=step, epoch=epoch, **evaluate(model, val, pad_id, args, device, dtype, autocast)))
            if step >= total_steps:
                done = True
                break
        result = evaluate(model, val, pad_id, args, device, dtype, autocast)
        val_epochs.append(dict(epoch=epoch, step=step, **result))
        log(dict(step=step, epoch=epoch, end_of_epoch=True, **result))
        (args.out / 'val_epochs.json').write_text(json.dumps(val_epochs, indent=2) + '\n')
        if args.save_every_epoch and not done and epoch < len(plans):
            save_checkpoint(model, tokenizer, args.out / f'epoch{epoch}', args.save_dtype,
                            dict(manifest, steps=step, epoch=epoch, val_epochs=val_epochs))
        if done:
            break
    manifest.update(steps=step, val_epochs=val_epochs, train_seconds=time.time() - start)
    save_checkpoint(model, tokenizer, args.out / 'final', args.save_dtype, manifest)
    (args.out / 'train_manifest.json').write_text(json.dumps(manifest, indent=2, default=str) + '\n')
    metrics.close()
    print('saved', args.out / 'final')
    return manifest


if __name__ == '__main__':
    main()
