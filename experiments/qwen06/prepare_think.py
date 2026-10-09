"""Thinking-mode RL data, split as agreed in the thinking-SFT debate (maxim, 2026-10-09, variant A).

Roles are frozen by the SFT side (Codex's dataset-plan.md / manifest.json, seed 20261009):

    role                 output                   use
    rl_train (1024)      think_train              RL rollouts
    rl_calibration (128) think_calib              difficulty check and V2 scales; never rolled out in RL
    dev (256)            think_val                validation during RL, choosing checkpoints and settings
    math_extra_test (512) think_math_test         final comparison only
    math500_test         think_math500 (+_pilot)  report only, never used to choose anything
    gsm_retention_test   think_gsm8k_test (+_pilot) check that grade-school math is not unlearned

rl_train, rl_calibration and dev are disjoint parts of the cleaned MATH train pool (algebra,
prealgebra, number theory, counting & probability, levels 2-4); math_train_reserve is never used.
GSM8K train and MATH geometry / intermediate algebra / precalculus belong to SFT only.

--roles DIR reads those files (<role>.jsonl, answers optionally in <role>.gold.jsonl) and
--manifest checks their sha256. A file larger than its role (math_extra_test given as the whole pool) and the
128-problem pilots are sampled with the seed; think_manifest.json lists every role's ids. Without --roles the same roles are built from the Hugging Face
datasets as a fallback: exact-duplicate and [asy] filtering only (no trigram near-duplicate
filter), so its ids differ from the frozen ones.
"""
import argparse
import hashlib
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
SEED = 20261009
SIZES = dict(rl_train=1024, rl_calibration=128, dev=256, math_extra_test=512, pilot=128)
# role -> (output name, data_source). Train-pool roles share one data_source so the V2 cost
# scales calibrated on rl_calibration apply to rl_train.
ROLES = dict(rl_train=('train', 'math'), rl_calibration=('calib', 'math'), dev=('val', 'math'),
             math_extra_test=('math_test', 'math_test'), math500_test=('math500', 'math500'),
             gsm_retention_test=('gsm8k_test', 'gsm8k'))


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
    if isinstance(text, int):
        return text
    match = re.fullmatch(r'(?:Level )?(\d)', str(text).strip())
    return int(match.group(1)) if match else -1


def subject_name(text):
    return str(text).strip().lower().replace(' & ', '_and_').replace(' ', '_')


def row(source, index, problem, answer, subject, difficulty, template):
    return dict(data_source=source, prompt=[{'role': 'user', 'content': template.format(problem=problem)}],
                ability='math', reward_model={'ground_truth': str(answer), 'style': 'rule'},
                # run_rl.sh think overrides reward_method with the chosen variant
                extra_info={'index': str(index), 'reward_method': 'think_v0', 'subject': subject,
                            'level': int(difficulty)},
                index=str(index))


def math_items(load, split, subjects, levels, exclude=frozenset()):
    """MATH problems of the given subjects and levels with a boxed answer, no [asy], no exact duplicates."""
    items, skipped, seen = [], Counter(), set(exclude)
    for subject in subjects:
        for i, item in enumerate(load(MATH, subject, split=split)):
            difficulty = level(item['level'])
            if difficulty not in levels:
                continue
            problem_key = key(item['problem'])
            if problem_key in seen:
                skipped['duplicate_or_math500'] += 1
                continue
            answer = last_boxed(item['solution'])
            if not answer or '[asy]' in item['problem']:
                skipped['no_boxed_answer_or_asy'] += 1
                continue
            seen.add(problem_key)
            items.append(dict(id=f'math_{split}/{subject}/{i}', problem=item['problem'], answer=answer,
                              subject=subject, level=difficulty))
    return items, dict(skipped)


def fallback_roles(load, levels, seed):
    """The frozen roles' structure rebuilt from Hugging Face (see module docstring)."""
    rng = random.Random(seed)
    math500 = [dict(id=item['unique_id'], problem=item['problem'], answer=item['answer'],
                    subject=subject_name(item['subject']), level=int(item['level']))
               for item in load('HuggingFaceH4/MATH-500', split='test')]
    pool, train_skipped = math_items(load, 'train', RL_SUBJECTS, levels)
    tests, test_skipped = math_items(load, 'test', RL_SUBJECTS, levels, {key(item['problem']) for item in math500})
    rng.shuffle(pool)
    cut = list(SIZES[name] for name in ('rl_train', 'rl_calibration', 'dev'))
    roles = dict(rl_train=pool[:cut[0]], rl_calibration=pool[cut[0]:sum(cut[:2])], dev=pool[sum(cut[:2]):sum(cut)],
                 math_extra_test=rng.sample(tests, min(SIZES['math_extra_test'], len(tests))), math500_test=math500,
                 gsm_retention_test=[dict(id=f'gsm8k_test/{i}', problem=item['question'], subject='gsm8k', level=-1,
                                          answer=item['answer'].split('####')[-1].strip().replace(',', ''))
                                     for i, item in enumerate(load('openai/gsm8k', 'main', split='test'))])
    return roles, dict(train=train_skipped, test=test_skipped, train_pool=len(pool), test_pool=len(tests),
                       reserve=len(pool) - sum(cut))


def read_role(directory, role):
    """Rows of <role>.jsonl, with answers from <role>.gold.jsonl when that file exists (joined by id)."""
    def rows(path):
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

    def pick(item, *names):
        return next((item[name] for name in names if item.get(name) not in (None, '')), None)

    path = directory / f'{role}.jsonl'
    items = rows(path)
    gold_path = directory / f'{role}.gold.jsonl'
    gold = {}
    if gold_path.exists():
        gold = {str(pick(item, 'id', 'uid', 'unique_id')): pick(item, 'gold', 'answer', 'ground_truth')
                for item in rows(gold_path)}
    out = []
    for number, item in enumerate(items):
        index = str(pick(item, 'id', 'uid', 'unique_id') or f'{role}/{number}')
        problem = pick(item, 'problem', 'question')
        answer = gold.get(index) or pick(item, 'gold', 'answer', 'ground_truth')
        if problem is None or answer is None:
            raise ValueError(f'{path} row {number} needs problem/question and an answer (or {gold_path.name}); '
                             f'keys: {sorted(item)}')
        out.append(dict(id=index, problem=problem, answer=answer, level=level(pick(item, 'level') or -1),
                        subject=subject_name(pick(item, 'subject', 'type') or role)))
    return out, hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_roles(directory, manifest, seed=SEED):
    """Role files as given. A role file larger than its size (math_extra_test may be the whole 1708-problem
    pool) is sampled down with the seed; the chosen ids go to think_manifest.json for comparison."""
    roles, hashes, sampled = {}, {}, {}
    for role in ROLES:
        roles[role], hashes[role] = read_role(directory, role)
        if len(roles[role]) > SIZES.get(role, len(roles[role])):
            sampled[role] = len(roles[role])
            roles[role] = random.Random(seed).sample(roles[role], SIZES[role])
    if manifest is not None:
        text = manifest.read_text()
        missing = [role for role, digest in hashes.items() if digest not in text]
        if missing:
            raise ValueError(f'sha256 of {missing} not found in {manifest}; the role files differ from the frozen ones')
    return roles, dict(sha256=hashes, sampled_from=sampled)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(Path.home() / 'parallel-r1'))
    parser.add_argument('--roles', type=Path, help='directory with the frozen <role>.jsonl files')
    parser.add_argument('--manifest', type=Path, help="Codex's manifest.json with the roles' sha256")
    parser.add_argument('--template', default=DEFAULT_TEMPLATE, help='Python format string with {problem}')
    parser.add_argument('--levels', type=int, nargs='+', default=list(RL_LEVELS), help='fallback only')
    parser.add_argument('--seed', type=int, default=SEED)
    parser.add_argument('--smoke-model', action='store_true',
                        help='write Qwen3-0.6B with the eight untrained contract tags for SMOKE=1 runs only')
    args = parser.parse_args()
    root = Path(args.root)
    out = root / 'data'
    out.mkdir(exist_ok=True)
    if args.roles:
        roles, provenance = frozen_roles(args.roles, args.manifest, args.seed)
        provenance['roles'] = str(args.roles)
    else:
        from datasets import load_dataset
        roles, provenance = fallback_roles(load_dataset, set(args.levels), args.seed)
        provenance['roles'] = 'fallback from Hugging Face'

    keys = {role: {key(item['problem']) for item in items} for role, items in roles.items()}
    for role in ('rl_train', 'rl_calibration', 'dev'):
        for other in ROLES:
            if other != role and keys[role] & keys[other]:
                raise ValueError(f'{role} shares {len(keys[role] & keys[other])} problems with {other}')

    manifest = dict(template=args.template, seed=args.seed, provenance=provenance)
    for role, (name, source) in ROLES.items():
        rows = [row(source, item['id'], item['problem'], item['answer'], item['subject'], item['level'], args.template)
                for item in roles[role]]
        pq.write_table(pa.Table.from_pylist(rows), out / f'think_{name}.parquet')
        manifest[name] = dict(role=role, rows=len(rows), by_subject=dict(Counter(r['extra_info']['subject'] for r in rows)),
                              by_level=dict(Counter(r['extra_info']['level'] for r in rows)),
                              ids=[r['index'] for r in rows])
        if role in ('math500_test', 'gsm_retention_test'):  # pilot subsets, fixed by the seed
            pilot = random.Random(args.seed).sample(rows, min(SIZES['pilot'], len(rows)))
            pq.write_table(pa.Table.from_pylist(pilot), out / f'think_{name}_pilot.parquet')
            manifest[name]['pilot_ids'] = [r['index'] for r in pilot]
        if role == 'rl_train':
            pq.write_table(pa.Table.from_pylist(rows[:4]), out / 'think_smoke_train.parquet')
        if role == 'dev':
            pq.write_table(pa.Table.from_pylist(rows[:2]), out / 'think_smoke_val.parquet')
    (out / 'think_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(json.dumps(manifest, indent=2, ensure_ascii=False)[:4000])

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
