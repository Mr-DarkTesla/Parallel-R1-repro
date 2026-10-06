"""Read-only checks of accepted ParaThinker rows. Lexical flags require manual review.
Usage (from verl/): python ../scripts/audit_sft_overlap.py /work/assets/parathinker/train_mix.parquet <output.json>
"""
import collections
import json
import re
import sys
import unicodedata

import pandas as pd

DATA = 'data_preprocess_scripts/data'
FORMAT = 'adaptive_parallel_thinking_final_with_prompt_v3'
EVAL = [f'{DATA}/APO_combine/{FORMAT}/rl_all_accuracy_reward/test.parquet',
        f'{DATA}/APO_combine/{FORMAT}/rl_all_accuracy_reward/math300_x8.parquet',
        f'{DATA}/limo/test.parquet',
        f'{DATA}/gsm8k/{FORMAT}/rl_all_accuracy_times_parallel_reward/test.parquet']


def problem(prompt):
    return prompt[0]['content'].split('Problem: ', 1)[-1]


def normalized(text):
    return ' '.join(unicodedata.normalize('NFKC', text).lower().split())


def words(text):
    return re.findall(r'[a-z0-9]+', text.lower())


def spans(tokens, size):
    return {' '.join(tokens[i:i + size]) for i in range(len(tokens) - size + 1)}


mix = pd.read_parquet(sys.argv[1])
rows = mix[mix.data_source == 'Leslie04/parathinker-math-6K']
eval_rows = [problem(p) for filename in EVAL for p in pd.read_parquet(filename).prompt]
eval_exact = {normalized(p) for p in eval_rows}
eval_spans = {n: set().union(*(spans(words(p), n) for p in eval_rows)) for n in (8, 13)}
counts = collections.Counter()
flags = []
seen = set()
similarities = []
for mix_index, row in rows.iterrows():
    question = problem(row.prompt)
    normal = normalized(question)
    tokens = words(question)
    response = row.extra_info['answer']
    paths = re.findall(r'<Path>(.*?)</Path>', response, re.S)
    found = []
    if normal in eval_exact:
        counts['exact_eval_match'] += 1
        found.append('exact_eval_match')
    for n in (8, 13):
        if spans(tokens, n) & eval_spans[n]:
            counts[f'eval_{n}gram_flag'] += 1
            found.append(f'eval_{n}gram_flag')
    if len(tokens) < 13:
        counts['question_under_13_words'] += 1
    if normal in seen:
        counts['duplicate_question_after_first'] += 1
    seen.add(normal)
    if len(paths) == 2:
        a, b = (normalized(p) for p in paths)
        if a == b:
            counts['identical_paths'] += 1
        sa, sb = (spans(words(p), 4) for p in paths)
        similarity = len(sa & sb) / len(sa | sb) if sa | sb else 1
        similarities.append(similarity)
        if similarity >= .8:
            counts['path_4gram_jaccard_ge_0_8'] += 1
    if found:
        flags.append({'mix_index': int(mix_index), 'source_index': int(row['index']), 'flags': found})
summary = {'accepted_rows': len(rows), 'counts': dict(counts), 'flags': flags,
           'mean_path_4gram_jaccard': sum(similarities) / len(similarities) if similarities else None,
           'note': '8-gram matches are review candidates, not confirmed contamination. No filtering or dataset edits.'}
with open(sys.argv[2], 'w') as output:
    json.dump(summary, output, indent=2)
print(json.dumps({k:v for k,v in summary.items() if k != 'flags'}, indent=2))
