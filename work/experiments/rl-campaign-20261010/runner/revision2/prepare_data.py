"""Pinned GSM only; train, selection validation and sealed final are disjoint."""
from pathlib import Path
import collections
import hashlib
import json
import random
import re
import unicodedata

HERE = Path(__file__).resolve().parent
P = next(p for p in HERE.parents if (p/'verl').is_dir() and (p/'exps').is_dir())
CONVENTIONS = 'GSM-Infinite dataset conventions: For this self-contained problem, an unmentioned category at a location contributes zero. A total includes all relevant categories mentioned at that location. Total nominations or newborn children are sums of (number of films or adult animals) times (average nominations or children per member); totals of schools or adult animals sum the category counts.\n\n'


def norm(text):
    return ' '.join(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',text).lower()))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def core_text(text):
    text=text.split(CONVENTIONS,1)[-1].split('\n\nProblem: ',1)[-1]
    if text.startswith('Answer the questions below.') and '\n\n' in text:
        text=text.split('\n\n',1)[-1]
    if '<context>' in text:
        text=text.split('<context>',1)[-1]
    return re.sub(r'</?context>', '', text, flags=re.I).strip()


def family(text):
    return re.sub(r'\d+', 'NUM', norm(core_text(text)))


def main():
    import pandas as pd
    out = HERE/'data'
    if out.exists():
        raise FileExistsError(out)
    excluded_ids, excluded_questions, excluded_cores, excluded_families = set(),set(),set(),set()
    exclude_sources = {}
    files = sorted(set(P.glob('work/experiments/*/evaluations/questions*.jsonl')))
    files += [P/'exps/deepseek-gsm-wide3000-v2-20261009/production/train.jsonl',
              P/'exps/deepseek-gsm-wide3000-v2-20261009/production/val.jsonl']
    for f in files:
        if not f.exists():
            continue
        exclude_sources[str(f.relative_to(P))] = digest(f)
        for line in f.read_text().splitlines():
            r = json.loads(line)
            excluded_ids.add(str(r['id']))
            q = r.get('problem',r.get('question',''))
            excluded_questions.add(norm(q))
            core = core_text(q)
            excluded_cores.add(norm(core))
            if f.name.startswith('questions'):
                excluded_families.update([family(q),re.sub(r'\d+','NUM',norm(q))])
    old_eval = P/'exps/rl-dataset-screen-20261007/gsm_infinite.parquet'
    if old_eval.exists():
        exclude_sources[str(old_eval.relative_to(P))] = digest(old_eval)
        for r in pd.read_parquet(old_eval).to_dict('records'):
            for m in r['prompt']:
                q = m['content']
                excluded_questions.add(norm(q))
                excluded_cores.add(norm(q.split('\n\nProblem: ',1)[-1]))
                excluded_families.update([family(q),re.sub(r'\d+','NUM',norm(q))])
    for f in (P/'cache/screen-hf/datasets--EleutherAI--hendrycks_math/snapshots').glob('*/*/*.parquet'):
        exclude_sources[str(f.relative_to(P))] = digest(f)
        d = pd.read_parquet(f)
        if 'problem' in d.columns:
            excluded_cores.update(norm(str(x)) for x in d.problem)
    models = [('medium_0','c6c5ab433565ddfe3e38e22be165b5c40e6bd576'),
              ('hard_0','49b0c72bca4c257a378d07da41561fe081ec5ad5')]
    seen, candidates, sources, reject = set(), [], {}, collections.Counter()
    for config, rev in models:
        directory = P/f'cache/screen-hf/datasets--InfiniAILab--gsm_infinite_{config}/snapshots/{rev}/data'
        for op in range(2,16):
            f = directory/f'ops_{op}-00000-of-00001.parquet'
            if not f.exists():
                continue
            sources[str(f.relative_to(P))] = digest(f)
            for index,r in enumerate(pd.read_parquet(f).to_dict('records')):
                if r['mode'] != 'normalforward' or r['length'] != 'zero_context':
                    reject['wrong_mode_or_context'] += 1
                    continue
                answer = re.findall(r'Answer:\s*(-?\d+(?:\.\d+)?)',r['solution'])
                if len(answer) != 1:
                    reject['invalid_answer'] += 1
                    continue
                core = r['problem']+'\n'+r['question']
                question = CONVENTIONS+core
                key = norm(core)
                id_ = f'gsm_infinite_{config}/ops_{op}-00000-of-00001/{index}'
                if key in seen:
                    reject['duplicate'] += 1
                    continue
                if family(core) in excluded_families:
                    reject['benchmark_number_masked_family_overlap'] += 1
                    continue
                if id_ in excluded_ids or key in excluded_cores or norm(question) in excluded_questions:
                    reject['historical_train_or_eval_overlap'] += 1
                    continue
                seen.add(key)
                family_sha = hashlib.sha256(family(core).encode()).hexdigest()
                bucket = int(family_sha[:8],16)%20
                split = 'final' if bucket<5 else 'val' if bucket<7 else 'train'
                candidates.append(dict(id=id_,problem=question,answer=answer[0],source='GSM_Infinite',
                    source_dataset=f'InfiniAILab/gsm_infinite_{config}',source_revision=rev,
                    source_file=str(f.relative_to(P)),source_row_index=index,op=op,
                    normalized_core_sha256=hashlib.sha256(key.encode()).hexdigest(),
                    split_group=family_sha, proposed_split=split))
    random.Random(20261010).shuffle(candidates)
    quota = dict(train=[512,307,205],val=[64,38,26],final=[256,154,102])
    selected = {split:[] for split in quota}
    counts = {split:[0,0,0] for split in quota}
    available = collections.Counter()
    for r in candidates:
        split = r['proposed_split']
        category = 0 if r['op']<=4 else 1 if r['op']<=8 else 2
        available[(split,category)] += 1
        if counts[split][category] < quota[split][category]:
            r.pop('proposed_split')
            selected[split].append(r)
            counts[split][category] += 1
    for split in selected:
        if counts[split] != quota[split]:
            raise ValueError(f'Insufficient disjoint source rows {split}: selected={counts[split]}, required={quota[split]}, available={dict(available)}')
    out.mkdir(exist_ok=False)
    for split in selected:
        random.Random(20261010).shuffle(selected[split])
        (out/f'{split}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in selected[split]))
    for a,b in [('train','val'),('train','final'),('val','final')]:
        for key in ['id','normalized_core_sha256','split_group']:
            assert {r[key] for r in selected[a]}.isdisjoint({r[key] for r in selected[b]})
    smoke = []
    for low,high in [(2,4),(5,8),(9,15)]:
        smoke.extend(next(r for r in selected['train'] if low<=r['op']<=high) for _ in range(1))
    smoke.extend(r for r in selected['train'] if r not in smoke)
    (out/'smoke.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in smoke[:8]))
    report = dict(passed=True,train=1024,val=128,sealed_final=512,ratios='50% ops2-4,30%ops5-8,20%ops9-15',
        actual_bucket_counts=counts,source='Pinned official GSM only, no MATH-derived training',
        excluded_id_count=len(excluded_ids),excluded_normalized_question_count=len(excluded_questions),
        excluded_normalized_core_count=len(excluded_cores),excluded_benchmark_family_count=len(excluded_families),
        source_sha256=sources,excluded_source_sha256=exclude_sources,rejections=dict(reject),
        split_rules='Number-masked normalized core family hash; all exact IDs and cores disjoint; all current SFT3000 excluded',
        decontamination_limit='Source, exact, normalized and number-masked family disjointness; not proof against all semantic overlap',
        file_sha256={f.name:digest(f) for f in out.glob('*.jsonl')})
    (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    main()
