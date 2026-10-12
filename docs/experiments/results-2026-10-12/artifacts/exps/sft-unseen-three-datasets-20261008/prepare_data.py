"""Lossless source conversion and exact tokenizer preflight; no trace rewriting."""
import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent
MODEL = Path('${MODEL_ROOT}/Qwen3-0.6B-Base-special-v2')
TAGS = ['<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(text):
    def block(m):
        body = m.group(1)
        paths = re.findall(r'<Path>.*?</Path>', body, flags=re.S)
        assert len(paths) >= 2
        assert not re.sub(r'<Path>.*?</Path>', '', body, flags=re.S).strip()
        return '<Parallel>' + ''.join(paths) + '</Parallel>'
    result = re.sub(r'<Parallel>(.*?)</Parallel>', block, text, flags=re.S)
    assert re.findall(r'<Path>(.*?)</Path>', result, re.S) == re.findall(r'<Path>(.*?)</Path>', text, re.S)
    return result


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    tag_ids = {t: tokenizer.encode(t, add_special_tokens=False) for t in TAGS}
    assert all(len(v) == 1 for v in tag_ids.values())
    assert len({v[0] for v in tag_ids.values()}) == 6
    datasets = []
    for name, filename in [('gsm_infinite', 'gsm_infinite_adaptive_parallel_5k.jsonl'), ('sft_messages', 'sft_messages_5000.jsonl')]:
        source = ROOT / 'input' / filename
        rows = []
        for index, line in enumerate(source.read_text().splitlines()):
            obj = json.loads(line)
            messages = obj['messages']
            assert messages[-1]['role'] == 'assistant'
            assert [m['role'] for m in messages] == ['system', 'user', 'assistant']
            rows.append({'sample_id': f'{name}:{index}', 'source_row_index': index,
                         'problem': messages[-2]['content'], 'prompt_messages': json.dumps(messages[:-1], ensure_ascii=False),
                         'response': compact(messages[-1]['content']), 'source_sha256': sha(source) if index == 0 else ''})
        order = sorted(range(len(rows)), key=lambda i: hashlib.sha256(('split-seed-1:' + rows[i]['problem']).encode()).hexdigest())
        validation = set(order[:500])
        datasets.append((name, {'train': [r for i,r in enumerate(rows) if i not in validation],
                                'val': [r for i,r in enumerate(rows) if i in validation]}, {filename: sha(source)}))
    mixed = {}
    for split in ('train', 'val'):
        df = pd.read_parquet(ROOT / 'input' / f'{split}.parquet')
        mixed[split] = [{'sample_id': str(row['id']), 'problem': row['problem'],
                         'prompt_messages': json.dumps([{'role':'user', 'content':row['problem']}], ensure_ascii=False),
                         'response': compact(row['response'])} for row in df.to_dict('records')]
    datasets.append(('mixed', mixed, {f'{s}.parquet': sha(ROOT / 'input' / f'{s}.parquet') for s in ('train','val')}))
    report = {'base_source': json.loads((MODEL / 'source.json').read_text()), 'tag_ids': tag_ids,
              'split_policy': 'Adaptive corpora: deterministic SHA256(problem, split-seed-1), 4500/500. Mixed: original splits.',
              'transformation': 'Only whitespace outside sibling Path spans is removed; system/user roles preserved.', 'datasets': []}
    for name, splits, sources in datasets:
        dest = ROOT / 'data' / name
        dest.mkdir(parents=True, exist_ok=True)
        record = {'name': name, 'sources': sources, 'splits': {}}
        for split, rows in splits.items():
            for row in rows:
                prompt = tokenizer.apply_chat_template(json.loads(row['prompt_messages']), tokenize=False, add_generation_prompt=True)
                row['prompt_tokens'] = len(tokenizer.encode(prompt, add_special_tokens=False))
                row['response_tokens'] = len(tokenizer.encode(row['response'] + tokenizer.eos_token, add_special_tokens=False))
                row['total_tokens'] = row['prompt_tokens'] + row['response_tokens']
            df = pd.DataFrame(rows)
            path = dest / f'{split}.parquet'
            df.to_parquet(path, index=False)
            lengths = sorted(df.total_tokens.tolist())
            record['splits'][split] = {'rows': len(rows), 'sha256': sha(path), 'min':min(lengths), 'max':max(lengths),
                'quantiles': {str(p): lengths[min(len(lengths)-1, int(len(lengths)*p))] for p in (0.5,0.9,0.95,0.99)},
                'over': {str(n):sum(x>n for x in lengths) for n in (3072,4096,8192,16384,32768,40960)}}
        assert not (set(r['problem'] for r in splits['train']) & set(r['problem'] for r in splits['val']))
        report['datasets'].append(record)
        print(json.dumps(record), flush=True)
    (ROOT / 'data-report.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
