"""Select generator records for thinking-SFT v4: explicit, logged keep rules, dedup, optional caps, a grouped split.

    python select_records.py all.raw.jsonl [repaired.jsonl ...] --out-dir data/sft_v4_4b [--val-frac 0.05]
    python select_records.py all.raw.jsonl --dry-run --stats selection-dryrun.json
    python select_records.py all.raw.jsonl --out-dir data/sft_v4_4b --tokenizer Qwen/Qwen3-4B   # on the VM

Input rows already follow the trainer schema (sft_data.py): id, source, mode, prompt, segments, provenance
{model_finished, correct, grade, over_budget, branch_checks [{ok, reason}], plan_status, n_tokens, task_id, ...}.
Rows are never modified; kept rows are written verbatim.

Rules, applied in this order; a dropped row is counted under the FIRST rule it fails (per source), and every
quality rule is also counted independently (`fails`) to show overlaps:
    malformed        not a JSON object with string id/source/mode and a provenance object
    duplicate_id     an id seen before (--on-duplicate first|last decides which copy is judged; default last, so
                     pass the raw file first and a repaired file after it)
    model_finished   provenance.model_finished is True             (--allow-unfinished skips it)
    correct          provenance.correct is True                    (--allow-incorrect)
    over_budget      provenance.over_budget is False               (--allow-over-budget)
    branch_checks    every provenance.branch_checks[i].ok is True, and a parallel row has at least one check
                                                                   (--allow-failed-branch-checks)
    plan_status      provenance.plan_status not in --reject-plan-status (default gold_in_plan: the plan states
                     the gold answer, a label leak; --reject-plan-status '' turns the rule off)
    invalid:<reason> sft_data.validate_row (schema + contract grammar, no tokenizer)   (--no-validate)
    tokenize:<reason>, too_long
                     only with --tokenizer: sft_data.tokenize_row with the eight tags added as tags.py does,
                     and the trainer's length (prompt included) <= --max-len
    source_cap       --source-cap SOURCE=N keeps N rows of that source (seeded hash order)
    seq_share        --seq-share F drops sequential or parallel rows (seeded hash order) until sequential rows are
                     a fraction F of the kept rows (default: keep all)

Split: rows are grouped by provenance.task_id, falling back to sha256(prompt), and groups sharing a task id or a
prompt are merged, so no problem straddles train and val; a group is in val when sha256 of its key falls in
--val-frac (sft_data.id_in_val). Outputs: <out-dir>/train.jsonl, val.jsonl and the stats JSON (--stats, default
<out-dir>/selection_stats.json): config, input sha256, kept/dropped per rule per source, branch-check reasons of
dropped rows, token lengths (provenance.n_tokens: the generator's count with the real tokenizer; the trainer's own
count when --tokenizer is given).
"""
import argparse
import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sft_data as D  # noqa: E402
from common import contract, default_revision  # noqa: E402

QUALITY_RULES = ('model_finished', 'correct', 'over_budget', 'branch_checks', 'plan_status')


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def rank(seed, row_id):
    return hashlib.sha256(f'{seed}:{row_id}'.encode()).hexdigest()


def read_rows(paths):
    """[(path, line, row or DataError)] in file order."""
    out = []
    for path in paths:
        for number, row in enumerate(D.read_jsonl(path), 1):
            out.append((str(path), number, row))
    return out


def quality_failures(row, allow, reject_plan=()):
    """Names of the quality rules this row fails (rules in `allow` are skipped)."""
    p = row['provenance']
    failed = []
    if 'model_finished' not in allow and p.get('model_finished') is not True:
        failed.append('model_finished')
    if 'correct' not in allow and p.get('correct') is not True:
        failed.append('correct')
    if 'over_budget' not in allow and p.get('over_budget') is not False:
        failed.append('over_budget')
    if 'branch_checks' not in allow:
        checks = p.get('branch_checks')
        ok = isinstance(checks, list) and all(isinstance(c, dict) and c.get('ok') is True for c in checks)
        if not ok or (row['mode'] == 'parallel' and not checks):
            failed.append('branch_checks')
    if str(p.get('plan_status')) in reject_plan:
        failed.append('plan_status')
    return failed


def is_malformed(row):
    if not isinstance(row, dict):
        return True
    if not all(isinstance(row.get(key), str) for key in ('id', 'source', 'mode')):
        return True
    return not isinstance(row.get('provenance'), dict)


class Groups:
    """Union-find over split keys: rows sharing a task id or a prompt end up in one group."""

    def __init__(self):
        self.parent = {}

    def find(self, key):
        self.parent.setdefault(key, key)
        while self.parent[key] != key:
            self.parent[key] = self.parent[self.parent[key]]
            key = self.parent[key]
        return key

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def split_keys(row):
    keys = ['prompt:' + hashlib.sha256(str(row.get('prompt', '')).encode()).hexdigest()]
    task = row['provenance'].get('task_id')
    if task not in (None, ''):
        keys.insert(0, f'task:{task}')
    return keys


def length_stats(values):
    if not values:
        return dict(n=0)
    ordered = sorted(values)
    pick = lambda q: ordered[min(len(ordered) - 1, int(q * len(ordered)))]  # noqa: E731
    return dict(n=len(values), total=sum(values), mean=round(statistics.fmean(values), 1),
                p50=pick(0.5), p90=pick(0.9), p95=pick(0.95), max=ordered[-1], min=ordered[0])


def load_tokenizer(name, revision):
    """Tokenizer with the eight tags added exactly as tags.ensure_tags does (no model needed)."""
    from transformers import AutoTokenizer
    from tags import check_ids
    tokenizer = AutoTokenizer.from_pretrained(name, revision=revision)
    present = [tag for tag in contract.TAGS if tag in tokenizer.get_vocab()]
    if not present:
        tokenizer.add_special_tokens({'additional_special_tokens': list(contract.TAGS)})
    elif len(present) != len(contract.TAGS):
        raise SystemExit(f'tokenizer has only some contract tags: {present}')
    return tokenizer, check_ids(tokenizer)


def parse_caps(items):
    caps = {}
    for item in items or ():
        source, _, number = item.partition('=')
        if not source or not number.isdigit():
            raise SystemExit(f'--source-cap wants SOURCE=N, got {item!r}')
        caps[source] = int(number)
    return caps


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('inputs', nargs='+', type=Path, help='raw and/or repaired JSONL files')
    parser.add_argument('--out-dir', type=Path, default=None)
    parser.add_argument('--stats', type=Path, default=None, help='stats JSON (default <out-dir>/selection_stats.json)')
    parser.add_argument('--dry-run', action='store_true', help='only count and write the stats JSON')
    parser.add_argument('--val-frac', type=float, default=0.05)
    parser.add_argument('--seed', type=int, default=0, help='hash seed for caps and the share (not the split)')
    parser.add_argument('--on-duplicate', choices=('first', 'last'), default='last')
    parser.add_argument('--allow-unfinished', action='store_true', help='skip the model_finished rule')
    parser.add_argument('--allow-incorrect', action='store_true', help='skip the correct rule')
    parser.add_argument('--allow-over-budget', action='store_true', help='skip the over_budget rule')
    parser.add_argument('--allow-failed-branch-checks', action='store_true', help='skip the branch_checks rule')
    parser.add_argument('--reject-plan-status', default='gold_in_plan',
                        help="comma list of provenance.plan_status values to drop ('' = none)")
    parser.add_argument('--no-validate', action='store_true', help='skip sft_data.validate_row')
    parser.add_argument('--source-cap', action='append', metavar='SOURCE=N')
    parser.add_argument('--seq-share', type=float, default=None, help='target fraction of sequential rows')
    parser.add_argument('--tokenizer', default=None, help='HF id or path: tokenize like the trainer, apply --max-len')
    parser.add_argument('--revision', default=None, help='tokenizer revision (default: pinned for known ids)')
    parser.add_argument('--max-len', type=int, default=16384, help='with --tokenizer: drop longer rows (too_long)')
    args = parser.parse_args(argv)
    if not args.dry_run and args.out_dir is None:
        parser.error('--out-dir is required unless --dry-run')
    if args.seq_share is not None and not 0 <= args.seq_share <= 1:
        parser.error('--seq-share must be in [0, 1]')
    return args


def select(args):
    allow = set()
    for flag, rule in (('allow_unfinished', 'model_finished'), ('allow_incorrect', 'correct'),
                       ('allow_over_budget', 'over_budget'), ('allow_failed_branch_checks', 'branch_checks')):
        if getattr(args, flag):
            allow.add(rule)
    caps = parse_caps(args.source_cap)
    reject_plan = tuple(status for status in args.reject_plan_status.split(',') if status)
    entries = read_rows(args.inputs)
    dropped = defaultdict(Counter)       # rule -> source -> count (first failing rule)
    fails = defaultdict(Counter)         # quality rule -> source -> count (independently)
    examples = {}
    seen_by_source = Counter()
    check_reasons = Counter()

    def drop(rule, row, detail=''):
        source = row.get('source', '?') if isinstance(row, dict) else '?'
        dropped[rule][source] += 1
        row_id = row.get('id', '?') if isinstance(row, dict) else '?'
        examples.setdefault(rule, f'{row_id}: {detail}'[:300])

    # 1. malformed + dedup (the judged copy of an id is its first or last occurrence)
    rows, positions = [], {}
    for path, number, row in entries:
        if isinstance(row, D.DataError) or is_malformed(row):
            drop('malformed', row if isinstance(row, dict) else {}, f'{path}:{number}')
            continue
        seen_by_source[row['source']] += 1
        if row['id'] in positions:
            index = positions[row['id']]
            if args.on_duplicate == 'last':
                drop('duplicate_id', rows[index], f'replaced by {path}:{number}')
                rows[index] = row
            else:
                drop('duplicate_id', row, f'{path}:{number}')
            continue
        positions[row['id']] = len(rows)
        rows.append(row)

    tokenizer = None
    tag_ids = None
    if args.tokenizer:
        revision = default_revision(args.tokenizer) if args.revision is None else (args.revision or None)
        tokenizer, ids = load_tokenizer(args.tokenizer, revision)
        tag_ids = [ids['tag_ids'][tag] for tag in contract.TAGS]
        vocab = D.Vocab(tokenizer)

    # 2. quality rules, validation, tokenization
    kept, lengths = [], {}
    for row in rows:
        failed = quality_failures(row, allow, reject_plan)
        for rule in failed:
            fails[rule][row['source']] += 1
        if failed:
            if failed[0] == 'branch_checks':
                check_reasons.update(c.get('reason') for c in row['provenance'].get('branch_checks') or []
                                     if isinstance(c, dict) and c.get('ok') is not True)
            drop(failed[0], row, str({k: row['provenance'].get(k) for k in ('model_finished', 'correct', 'grade',
                                                                            'over_budget')}))
            continue
        if not args.no_validate:
            try:
                D.validate_row(row)
            except D.DataError as error:
                drop(f'invalid:{error.reason}', row, str(error))
                continue
        if tokenizer is not None:
            try:
                sample = D.tokenize_row(row, vocab)
            except D.DataError as error:
                drop(f'tokenize:{error.reason}', row, str(error))
                continue
            if sample['length'] > args.max_len:
                drop('too_long', row, f'{sample["length"]} > {args.max_len}')
                continue
            lengths[row['id']] = sample['length']
        kept.append(row)

    # 3. per-source caps, then the sequential share (seeded hash order: stable under reordering of the inputs)
    if caps:
        by_source = defaultdict(list)
        for row in kept:
            by_source[row['source']].append(row)
        keep_ids = set()
        for source, group in by_source.items():
            group.sort(key=lambda r: rank(args.seed, r['id']))
            limit = caps.get(source, len(group))
            keep_ids.update(r['id'] for r in group[:limit])
            for row in group[limit:]:
                drop('source_cap', row, f'{source} cap {limit}')
        kept = [row for row in kept if row['id'] in keep_ids]
    if args.seq_share is not None and kept:
        seq = sorted((r for r in kept if r['mode'] == 'sequential'), key=lambda r: rank(args.seed, r['id']))
        par = sorted((r for r in kept if r['mode'] == 'parallel'), key=lambda r: rank(args.seed, r['id']))
        share = args.seq_share
        if len(seq) > share * (len(seq) + len(par)):
            n_seq = len(seq) if share >= 1 else int(share * len(par) / (1 - share))
            surplus = seq[n_seq:]
        else:
            n_par = len(par) if share <= 0 else int(len(seq) * (1 - share) / share)
            surplus = par[n_par:]
        for row in surplus:
            drop('seq_share', row, f'target {share}')
        gone = {r['id'] for r in surplus}
        kept = [row for row in kept if row['id'] not in gone]

    # 4. grouped split
    groups = Groups()
    for row in kept:
        keys = split_keys(row)
        for key in keys[1:]:
            groups.union(keys[0], key)
    train, val = [], []
    for row in kept:
        group = groups.find(split_keys(row)[0])
        (val if D.id_in_val(group, args.val_frac) else train).append(row)

    def summary(part):
        n_tokens = [r['provenance'].get('n_tokens') for r in part if isinstance(r['provenance'].get('n_tokens'), int)]
        out = dict(rows=len(part), by_source=dict(Counter(r['source'] for r in part)),
                   by_mode=dict(Counter(r['mode'] for r in part)),
                   by_source_mode=dict(Counter(f'{r["source"]}/{r["mode"]}' for r in part)),
                   groups=len({groups.find(split_keys(r)[0]) for r in part}),
                   n_tokens=length_stats(n_tokens),
                   n_tokens_by_mode={mode: length_stats([r['provenance']['n_tokens'] for r in part
                                                         if r['mode'] == mode and
                                                         isinstance(r['provenance'].get('n_tokens'), int)])
                                     for mode in D.MODES},
                   n_tokens_over_max_len=sum(n > args.max_len for n in n_tokens),
                   plan_status=dict(Counter(str(r['provenance'].get('plan_status')) for r in part)))
        if lengths:
            out['trainer_tokens'] = length_stats([lengths[r['id']] for r in part])
        return out

    rule_order = ['malformed', 'duplicate_id', *QUALITY_RULES]
    ordered = {rule: dict(dropped[rule]) for rule in rule_order if rule in dropped}
    ordered.update({rule: dict(counts) for rule, counts in sorted(dropped.items()) if rule not in ordered})
    stats = dict(
        config=dict(inputs=[dict(path=str(p), sha256=sha256_file(p)) for p in args.inputs],
                    rules=[rule for rule in QUALITY_RULES[:4] if rule not in allow] +
                          ([f'plan_status not in {list(reject_plan)}'] if reject_plan else []) +
                          ([] if args.no_validate else ['validate_row']) +
                          (['tokenize_row', f'max_len={args.max_len}'] if tokenizer is not None else []),
                    relaxed=sorted(allow), reject_plan_status=list(reject_plan), on_duplicate=args.on_duplicate,
                    source_caps=caps,
                    seq_share=args.seq_share, val_frac=args.val_frac, seed=args.seed, tokenizer=args.tokenizer,
                    tag_ids=tag_ids, contract_sha256=contract.SHA256,
                    split_key='provenance.task_id else sha256(prompt), merged when sharing either'),
        lines=len(entries), rows_by_source=dict(seen_by_source), unique_rows=len(rows),
        kept=summary(kept), train=summary(train), val=summary(val),
        dropped_first_rule=ordered,
        dropped_total={rule: sum(counts.values()) for rule, counts in ordered.items()},
        fails_by_rule={rule: dict(fails[rule]) for rule in QUALITY_RULES if rule in fails},
        dropped_branch_check_reasons=dict(check_reasons), drop_examples=examples)
    return train, val, stats


def write_jsonl(path, rows):
    with open(path, 'w') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')
    return sha256_file(path)


def main(argv=None):
    args = parse_args(argv)
    train, val, stats = select(args)
    if not args.dry_run:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        stats['outputs'] = dict(train=dict(path=str(args.out_dir / 'train.jsonl'),
                                           sha256=write_jsonl(args.out_dir / 'train.jsonl', train)),
                                val=dict(path=str(args.out_dir / 'val.jsonl'),
                                         sha256=write_jsonl(args.out_dir / 'val.jsonl', val)))
    stats_path = args.stats or (args.out_dir / 'selection_stats.json' if args.out_dir else None)
    if stats_path is not None:
        stats_path.parent.mkdir(parents=True, exist_ok=True)
        stats_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + '\n')
    print(f'{stats["lines"]} lines, {stats["unique_rows"]} unique ids -> kept {stats["kept"]["rows"]} '
          f'(train {stats["train"]["rows"]}, val {stats["val"]["rows"]} in {stats["val"]["groups"]} groups)')
    print('kept by source/mode:', json.dumps(stats['kept']['by_source_mode'], sort_keys=True))
    print('dropped (first failing rule, by source):')
    for rule, counts in stats['dropped_first_rule'].items():
        print(f'  {rule:24s} {sum(counts.values()):5d}  {json.dumps(counts, sort_keys=True)}')
    print('fails by rule (independent):', json.dumps(stats['fails_by_rule'], sort_keys=True))
    print('kept n_tokens:', json.dumps(stats['kept']['n_tokens']))
    if stats_path is not None:
        print('stats ->', stats_path)
    return stats


if __name__ == '__main__':
    main()
