"""Inspect/extract an SFT archive safely, then validate the HF contract."""
import argparse
import hashlib
import json
import tarfile
from pathlib import Path


def validate(path, plan=False):
    from transformers import AutoConfig, AutoTokenizer
    from safetensors import safe_open
    from verl.parallel_thinking_generation_v3.repro_trace import TOKENS
    from verl.parallel_thinking_generation_v3 import contract
    config = AutoConfig.from_pretrained(path, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
    if config.model_type != 'qwen3' or config.hidden_size != 1024 or config.num_hidden_layers != 28:
        raise ValueError('Expected Qwen3-0.6B architecture (1024 hidden, 28 layers)')
    ids = [tokenizer.encode(token, add_special_tokens=False) for token in TOKENS]
    if any(len(x) != 1 for x in ids) or len({x[0] for x in ids}) != 6:
        raise ValueError('Six distinct atomic Parallel/Path/Summary opening and closing tokens are required')
    if plan:  # protocol=plan also needs <Plan> and </Plan>, and the branch counts as single tokens
        ids = [[contract.tag_ids(tokenizer)[token]] for token in contract.TAGS]
        TOKENS = contract.TAGS
        contract.count_ids(tokenizer)
    if max(x[0] for x in ids) >= config.vocab_size:
        raise ValueError('Special-token IDs exceed model vocabulary')
    files = list(path.glob('*.safetensors'))
    if not files:
        raise ValueError('No HF safetensors weights found; trainer/LoRA checkpoints need conversion')
    embedding_shape = None
    for file in files:
        with safe_open(file, framework='pt', device='cpu') as weights:
            if 'model.embed_tokens.weight' in weights.keys():
                embedding_shape = weights.get_slice('model.embed_tokens.weight').get_shape()
    if embedding_shape != [config.vocab_size, config.hidden_size]:
        raise ValueError(f'Embedding shape {embedding_shape} does not match config')
    tokenizer.apply_chat_template([{'role': 'user', 'content': '2+2?'}], tokenize=True, add_generation_prompt=True)
    report = dict(model_path=str(path.resolve()), model_type=config.model_type, vocab_size=config.vocab_size,
                  tokenizer_size=len(tokenizer), special_tokens=dict(zip(TOKENS, ids)), embedding_shape=embedding_shape)
    print(json.dumps(report, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('checkpoint', type=Path)
    parser.add_argument('--plan', action='store_true', help='require the eight plan tags (contract.TAGS)')
    parser.add_argument('--extract-to', type=Path)
    args = parser.parse_args()
    path = args.checkpoint.resolve()
    if path.is_file():
        if args.extract_to is None:
            with tarfile.open(path) as archive:
                print('\n'.join(archive.getnames()[:120]))
            raise SystemExit('Archive inspected. Pass --extract-to /home/ubuntu/parallel-r1/models/sft for extraction and validation.')
        destination = args.extract_to.resolve()
        if destination.exists() and any(destination.iterdir()):
            raise ValueError('Extraction destination must be empty; existing checkpoints are preserved')
        with tarfile.open(path) as archive:
            members = archive.getmembers()
            for member in members:
                target = (destination / member.name).resolve()
                if not target.is_relative_to(destination) or not (member.isfile() or member.isdir()):
                    raise ValueError(f'Unsafe archive entry: {member.name}')
            destination.mkdir(parents=True, exist_ok=True)
            archive.extractall(destination, members=members)
        candidates = [p.parent for p in destination.rglob('config.json') if list(p.parent.glob('*.safetensors'))]
        if len(candidates) != 1:
            raise ValueError(f'Expected one HF model directory; found {candidates}')
        path = candidates[0]
        digest = hashlib.sha256()
        with args.checkpoint.open('rb') as stream:
            for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                digest.update(block)
        (destination / 'archive.sha256').write_text(digest.hexdigest() + '\n')
    report = validate(path, plan=args.plan)
    (path / 'checkpoint_validation.json').write_text(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
