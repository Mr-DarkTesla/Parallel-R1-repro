"""Thinking-mode RL data, split as agreed in the thinking-SFT debate (maxim, 2026-10-09, variant A).

RL train: MATH train, subjects algebra, prealgebra, number theory, counting & probability, levels 2-4.
Evaluation: MATH-500; TEST = MATH test outside MATH-500, same subjects and levels as RL train;
GSM8K test, to check the model did not unlearn grade-school math.
The SFT corpus uses GSM8K train and MATH geometry, intermediate algebra and precalculus; none of
them goes into RL.

Writes to <root>/data: think_train (RL), think_val (MATH-500, validation during RL),
think_math_test, think_gsm8k_test, think_calib (fixed sample of RL train questions for the V2
cost scales), think_smoke_{train,val} and think_manifest.json. The prompt template must match
the one the thinking SFT corpus used. Needs the Hugging Face Hub (datasets).
"""
import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

DEFAULT_TEMPLATE = '{problem}\n\nPlease reason step by step, and put your final answer within \\boxed{{}}.'
MATH = 'EleutherAI/hendrycks_math'
RL_SUBJECTS = ('algebra', 'prealgebra', 'number_theory', 'counting_and_probability')
SFT_SUBJECTS = ('geometry', 'intermediate_algebra', 'precalculus')  # never used here
RL_LEVELS = (2, 3, 4)


def last_boxed(text):
    """Content of the last \\boxed{...} (or \\fbox{...}) with balanced braces, or None."""
    start = max(text.rfind('\\boxed{'), text.rfind('\\fbox{'))
    if start < 0:
        return None
    index = text.index('{', start)
    depth = 0
    for end in range(index, len(text)):
        depth += {'{': 1, '}': -1}.get(text[end], 0)
        if depth == 0:
            return text[index + 1:end].strip()
    return None


def key(problem):
    """Problem identity across MATH copies: whitespace-insensitive."""
    return re.sub(r'\s+', ' ', problem).strip()


def level(text):
    match = re.fullmatch(r'Level (\d)', str(text).strip())
    return int(match.group(1)) if match else -1


def row(source, index, problem, answer, subject, difficulty, template):
    return dict(data_source=source, prompt=[{'role': 'user', 'content': template.format(problem=problem)}],
                ability='math', reward_model={'ground_truth': answer, 'style': 'rule'},
                # run_rl.sh think overrides reward_method with the chosen variant
                extra_info={'index': index, 'reward_method': 'think_v0', 'subject': subject, 'level': difficulty},
                index=index)


def math_rows(load, split, source, subjects, levels, template, exclude=frozenset()):
    rows, skipped = [], Counter()
    for subject in subjects:
        for i, item in enumerate(load(MATH, subject, split=split)):
            difficulty = level(item['level'])
            if difficulty not in levels:
                continue
            if key(item['problem']) in exclude:
                skipped['math500'] += 1
                continue
            answer = last_boxed(item['solution'])
            if not answer:
                skipped['no_boxed_answer'] += 1
                continue
            rows.append(row(source, f'math_{split}/{subject}/{i}', item['problem'], answer, subject, difficulty, template))
    return rows, dict(skipped)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(Path.home() / 'parallel-r1'))
    parser.add_argument('--template', default=DEFAULT_TEMPLATE, help='Python format string with {problem}')
    parser.add_argument('--levels', type=int, nargs='+', default=list(RL_LEVELS))
    parser.add_argument('--calib-size', type=int, default=512)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--smoke-model', action='store_true',
                        help='write Qwen3-0.6B with the eight untrained contract tags for SMOKE=1 runs only')
    args = parser.parse_args()
    from datasets import load_dataset
    root = Path(args.root)
    out = root / 'data'
    out.mkdir(exist_ok=True)
    levels = set(args.levels)

    math500 = list(load_dataset('HuggingFaceH4/MATH-500', split='test'))
    excluded = {key(item['problem']) for item in math500}
    train, train_skipped = math_rows(load_dataset, 'train', 'math_train', RL_SUBJECTS, levels, args.template)
    test, test_skipped = math_rows(load_dataset, 'test', 'math_test', RL_SUBJECTS, levels, args.template, excluded)
    if test_skipped.get('math500', 0) < sum(item['subject'].lower().replace(' & ', '_and_').replace(' ', '_')
                                            in RL_SUBJECTS and item['level'] in levels for item in math500):
        print('Warning: fewer MATH-500 problems matched in MATH test than expected; check whitespace/text drift')
    val = [row('math500', item['unique_id'], item['problem'], item['answer'],
               item['subject'].lower().replace(' & ', '_and_').replace(' ', '_'), int(item['level']), args.template)
           for item in math500]
    gsm8k = [row('gsm8k_test', f'gsm8k_test/{i}', item['question'],
                 item['answer'].split('####')[-1].strip().replace(',', ''), 'gsm8k', -1, args.template)
             for i, item in enumerate(load_dataset('openai/gsm8k', 'main', split='test'))]
    overlap = {key(r['prompt'][0]['content']) for r in train} & {key(r['prompt'][0]['content']) for r in val + test}
    if overlap:
        raise ValueError(f'{len(overlap)} RL train problems also appear in evaluation sets')

    tables = dict(train=train, val=val, math_test=test, gsm8k_test=gsm8k)
    for name, rows in tables.items():
        pq.write_table(pa.Table.from_pylist(rows), out / f'think_{name}.parquet')
    pq.write_table(pa.Table.from_pylist(train[:4]), out / 'think_smoke_train.parquet')
    pq.write_table(pa.Table.from_pylist(val[:2]), out / 'think_smoke_val.parquet')
    calib = random.Random(args.seed).sample(train, min(args.calib_size, len(train)))
    pq.write_table(pa.Table.from_pylist(calib), out / 'think_calib.parquet')

    manifest = dict(template=args.template, rl_subjects=RL_SUBJECTS, levels=sorted(levels), seed=args.seed,
                    sources=dict(math=MATH, math500='HuggingFaceH4/MATH-500', gsm8k='openai/gsm8k main'),
                    skipped=dict(train=train_skipped, math_test=test_skipped),
                    calib=dict(rows=len(calib), indices=[r['index'] for r in calib]))
    for name, rows in tables.items():
        manifest[name] = dict(rows=len(rows), by_subject=dict(Counter(r['extra_info']['subject'] for r in rows)),
                              by_level=dict(Counter(r['extra_info']['level'] for r in rows)),
                              first_prompt=rows[0]['prompt'][0]['content'])
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
