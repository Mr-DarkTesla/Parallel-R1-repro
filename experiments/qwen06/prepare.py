"""Prepare identical S1/S2 inputs, provenance and a disposable GPU smoke model."""
import argparse
import hashlib
import json
from pathlib import Path

import pyarrow.parquet as pq


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(Path.home() / 'parallel-r1'))
    parser.add_argument('--smoke-model', action='store_true')
    args = parser.parse_args()
    root = Path(args.root)
    source = root / 'repo/verl/data_preprocess_scripts/data'
    out = root / 'data'
    out.mkdir(exist_ok=True)
    sources = {
        'train': source / 'dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_parallel_interv_reward/train.parquet',
        'val': source / 'APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_parallel_interv_reward/test.parquet',
        'sft': source / 'gsm8k/adaptive_parallel_thinking_no_prompt_filtered/sft_all/train.parquet',
    }
    manifest = {}
    for split, path in sources.items():
        table = pq.read_table(path)
        rows = table.to_pylist()
        manifest[split] = dict(source=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                               rows=len(rows), schema=str(table.schema))
        if split == 'sft':
            pq.write_table(table, out / 'sft_reference.parquet')
            continue
        for mode in ('s1', 's2'):
            copied = []
            for row in rows:
                row = dict(row)
                info = dict(row.get('extra_info') or {})
                info['reward_method'] = 'accuracy_parallel_interv_reward' if mode == 's2' and split == 'train' else 'accuracy_reward'
                row['extra_info'] = info
                copied.append(row)
            from pyarrow import Table
            prepared = Table.from_pylist(copied)
            pq.write_table(prepared, out / f'{mode}_{split}.parquet')
            pq.write_table(prepared.slice(0, 4 if split == 'train' else 2), out / f'{mode}_smoke_{split}.parquet')
        manifest[split]['data_sources'] = sorted(set(str(r['data_source']) for r in rows))
        manifest[split]['first_extra_info'] = rows[0]['extra_info']
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    if args.smoke_model:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from verl.parallel_thinking_generation_v3.repro_trace import TOKENS
        model_id = 'Qwen/Qwen3-0.6B'
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        tokenizer.add_special_tokens({'additional_special_tokens': list(TOKENS)})
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)
        model.resize_token_embeddings(len(tokenizer))
        target = root / 'models/smoke-qwen3-0.6b-special'
        target.mkdir(parents=True, exist_ok=True)
        tokenizer.save_pretrained(target)
        model.save_pretrained(target)
        (target / 'SMOKE_ONLY').write_text('Disposable untrained special-token embeddings. Never use as SFT checkpoint.\n')
        print('Smoke model:', target)


if __name__ == '__main__':
    main()
