"""Freeze the V2 cost scales s_D, s_T from the SFT checkpoint's correct answers on train calibration questions.

Input: validation dumps (<run>/validation/*.jsonl) of a validation-only run over think_calib.parquet
with REWARD=v0 and several samples per question. Output: JSON for COST_SCALES (REWARD=v2).
Each bucket (data source) gets the median D and T of its correct answers; a task gets its own
medians once it has at least --min-correct correct answers. RL samples never update the file.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import median


def scales(rows, min_correct):
    correct = [row for row in rows if row['acc'] == 1 and row['critical_depth'] > 0 and row['sampled_tokens'] > 0]
    if not correct:
        raise ValueError('No correct answers with D and T in the dumps')

    def summary(group):
        return dict(D=median(row['critical_depth'] for row in group), T=median(row['sampled_tokens'] for row in group),
                    correct=len(group))

    buckets, tasks = defaultdict(list), defaultdict(list)
    for row in correct:
        buckets[row['bucket']].append(row)
        if row['task']:
            tasks[row['task']].append(row)
    return dict(default=summary(correct), buckets={name: summary(group) for name, group in buckets.items()},
                tasks={name: summary(group) for name, group in tasks.items() if len(group) >= min_correct},
                rows=len(rows), correct=len(correct))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dumps', nargs='+', type=Path, help='validation JSONL files or directories')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--min-correct', type=int, default=3)
    args = parser.parse_args()
    files = [f for path in args.dumps for f in (sorted(path.glob('*.jsonl')) if path.is_dir() else [path])]
    rows = [json.loads(line) for f in files for line in f.read_text().splitlines() if line.strip()]
    result = dict(sources=[str(f) for f in files], **scales(rows, args.min_correct))
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({k: result[k] for k in ('rows', 'correct', 'default', 'buckets')}, indent=2))
    print(f'{len(result["tasks"])} tasks with their own scale; wrote {args.out}')


if __name__ == '__main__':
    main()
