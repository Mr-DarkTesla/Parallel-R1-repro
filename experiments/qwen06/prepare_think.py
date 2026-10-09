"""Thinking-mode RL inputs: the S1/S2 questions re-prompted for Qwen3 thinking, plus a calibration slice.

think_train / think_val keep the questions, answers and order of s1/s2 (DAPO train, APO validation);
only the instruction changes. The template must match the prompt the thinking SFT corpus used.
think_calib is a fixed sample of TRAIN questions for freezing the V2 cost scales.
"""
import argparse
import json
import random
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

DEFAULT_TEMPLATE = '{problem}\n\nPlease reason step by step, and put your final answer within \\boxed{{}}.'
MARKER = '\n\nProblem: '


def problem_text(prompt):
    """The problem from a prompt_v3 message (parallel-format instructions, then 'Problem: ...')."""
    content = prompt[0]['content']
    start = content.rfind(MARKER)
    if start < 0:
        raise ValueError(f'No {MARKER!r} in prompt: {content[:200]!r}')
    return content[start + len(MARKER):]


def convert(rows, template):
    converted = []
    for row in rows:
        row = dict(row)
        row['prompt'] = [{'role': 'user', 'content': template.format(problem=problem_text(row['prompt']))}]
        info = dict(row.get('extra_info') or {})
        info['reward_method'] = 'think_v0'  # run_rl.sh think overrides it with the chosen variant
        row['extra_info'] = info
        converted.append(row)
    return converted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(Path.home() / 'parallel-r1'))
    parser.add_argument('--template', default=DEFAULT_TEMPLATE, help='Python format string with {problem}')
    parser.add_argument('--calib-size', type=int, default=512)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--smoke-model', action='store_true',
                        help='write Qwen3-0.6B with the eight untrained contract tags for SMOKE=1 runs only')
    args = parser.parse_args()
    root = Path(args.root)
    source = root / 'repo/verl/data_preprocess_scripts/data'
    out = root / 'data'
    out.mkdir(exist_ok=True)
    sources = {
        'train': source / 'dapo/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_parallel_interv_reward/train.parquet',
        'val': source / 'APO_combine/adaptive_parallel_thinking_final_with_prompt_v3/rl_all_accuracy_parallel_interv_reward/test.parquet',
    }
    manifest = dict(template=args.template, calib_size=args.calib_size, seed=args.seed)
    for split, path in sources.items():
        rows = convert(pq.read_table(path).to_pylist(), args.template)
        table = pa.Table.from_pylist(rows)
        pq.write_table(table, out / f'think_{split}.parquet')
        pq.write_table(table.slice(0, 4 if split == 'train' else 2), out / f'think_smoke_{split}.parquet')
        manifest[split] = dict(source=str(path), rows=len(rows), first_prompt=rows[0]['prompt'][0]['content'])
        if split == 'train':
            calib = random.Random(args.seed).sample(rows, args.calib_size)
            pq.write_table(pa.Table.from_pylist(calib), out / 'think_calib.parquet')
            manifest['calib'] = dict(rows=len(calib), indices=[row['extra_info'].get('index') for row in calib])
    (out / 'think_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in manifest.items() if k != 'calib'}, indent=2, ensure_ascii=False))
    if args.smoke_model:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from verl.parallel_thinking_generation_v3.contract import TAGS
        model_id = 'Qwen/Qwen3-0.6B'
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        tokenizer.add_special_tokens({'additional_special_tokens': list(TAGS)})
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)
        if len(tokenizer) > model.get_input_embeddings().weight.size(0):
            model.resize_token_embeddings(len(tokenizer))
        target = root / 'models/smoke-qwen3-0.6b-think'
        target.mkdir(parents=True, exist_ok=True)
        tokenizer.save_pretrained(target)
        model.save_pretrained(target)
        (target / 'SMOKE_ONLY').write_text('Disposable untrained tag embeddings. Never use as SFT checkpoint.\n')
        print('Smoke model:', target)


if __name__ == '__main__':
    main()
