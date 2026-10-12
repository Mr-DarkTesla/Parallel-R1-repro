"""Fast deterministic repair pass for the 5k parallel-thinking pool (pool-20261012): plan (CPU), run (one GPU,
vLLM offline), assemble (CPU), export. The raw pool is never modified; repaired rows keep the raw id and replace
the raw row in select_records.py (raw file first, repaired file second).

    python fast_repair.py requests --raw-run-root RUNS/raw-full --out W/branch_requests.jsonl   # optional, exact
    python fast_repair.py plan --raw all.raw.jsonl --details details.jsonl --work-dir W [--branch-requests ...]
    python fast_repair.py run --work-dir W                 # GPU; resumable, checkpoints W/results.jsonl
    python fast_repair.py assemble --work-dir W            # CPU; W/assembled.jsonl + W/assemble_stats.json
    python fast_repair.py export --work-dir W --out W/repaired.jsonl

Triage (`triage`, from Codex's per-record audit details.jsonl; reproduces the counts agreed with the user):
    seq_clean, par_clean                kept as they are (not in the repair file)
    exec_summary_resolves               exec parallel, all branches workshop-oracle verified, the Summary repeats
                                        >= 2 original input products -> merger repair (kind exec_merger)
    branch_truncated_only               the only branch defect is truncation, final correct -> regenerate the
                                        truncated branches (same request as the raw run), then the merger
                                        (kind branch_truncated)
    par_clean, GSM/MATH, Summary longer than --summary-ratio x the longest branch body (characters)
                                        -> merger repair (kind long_summary_merger)
    wrong_final, plan_or_branch_solves_whole, branch_wrong_other, unfinished_final_or_mixed, seq_unfinished
                                        dropped in v1 (counted)

Merger repair (all three kinds; Branches, plan and prefix stay byte-identical when only the merger changes):
  * Summary call: chat template with enable_thinking=False (the text IS the summary inside <think>), max_tokens
    --summary-max-tokens (1024), n=4. The request gets the plan items and each branch's Result line only: exec gets
    Codex's Results-only workshop header and no production inputs (audit_repair.repair_merger_prompt); GSM/MATH/
    Countdown get the question plus an explicit "these Results are verified; state and combine them, do not
    re-derive" instruction (SUMMARY_NOTE).
  * Answer call (text after </think>): one short non-thinking call per surviving summary sample, from the Results
    and that summary, max_tokens --answer-max-tokens (512).
  * Accept a (summary, answer) pair only if both calls stopped by themselves, the final is correct by Codex's scorer
    (audit_repair.final_grade = gen.grade + the Decimal check for exec/gsm), the summary is <= --summary-ratio x
    the longest branch body (characters), exec summary and answer each repeat <= --max-input-products (1) input
    products (Codex's signal, reproduced exactly on all 1,329 exec records), no tag/control token in either text
    (contract.plain_text), the record is <= 16,384 generator tokens and passes sft_data.validate_row. The shortest
    accepted pair (summary + answer tokens) wins.
  * Nothing accepted: exec/long-summary rows are exported unchanged with provenance.repair_failed=true (dropped by
    select_records unless --keep-repair-failed); branch_truncated rows are not exported (the raw row already
    fails the default rules).

Branch repair: the SAME request as the raw run (verbatim from the raw run's raw_branches.jsonl via `requests`;
the 4B pool used the planner's standalone mini-problems, which the records do not store), thinking mode, n=2,
max_tokens = (16384 - 2048 summary reserve - the record's other parts) / number of truncated branches (Codex's
raw_acquisition.overhead), accepted if Codex's gen.check_branch passes (finished, Result line, workshop oracle,
Countdown exact checks, decompose final-answer rule) and, for Countdown, its expression differs from the
siblings' (gen.stage_branch rule); oracle/valid first, then shortest. Countdown requests get raw_acquisition's
"ANY SUBSET" sentence when they lack it (the 1,536 older records). Without an exact request the record is skipped
and counted (or, with --branch-request-fallback arm_d, Codex's in-context executor_prompt_d is used and marked).

Sampling is the raw run's (gen.STUDENT_SAMPLING: temperature 0.6, top_p 0.95, top_k 20) with a per-request seed
gen.seed_of('fast-repair', REVISION, key), recorded with every result; vLLM is built like gen.Engine (bf16,
prefix caching, engine seed 0, Codex's exact top-k/top-p sampler patch). Every decision is a pure function of
jobs.jsonl + results.jsonl (`evaluate`), so `run` resumes exactly and `assemble` reproduces the run's choices.
"""
import argparse
import copy
import hashlib
import json
import os
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codex_rules as C  # noqa: E402
import sft_data as D  # noqa: E402
from common import BASE_MODEL, BASE_REVISION, contract  # noqa: E402

REVISION = 'fast-repair-20261012-v1'
RAW_SHA256 = '5b48bda734214f7dfb42886a7ad2f3fa08e6b8f0c477b4a2fd5aad03c9ae222d'
TOTAL = C.MAX_TOTAL_TOKENS
EXEC, TRUNC, LONG = 'exec_merger', 'branch_truncated', 'long_summary_merger'
KINDS = (EXEC, TRUNC, LONG)
# Counts the user computed from details.jsonl (the other categories were not given).
EXPECTED_TRIAGE = dict(seq_clean=1199, par_clean=1924, exec_summary_resolves=605, branch_truncated_only=416)
SUMMARY_NOTE = (
    '\n\nThe Results above are verified and final. Write the summary step of the reasoning that follows these '
    'independent tasks: state the Results you use and perform only the remaining combination, comparison or '
    'deduction that reaches the final answer. Do not re-derive, recompute or re-check any Result from the original '
    'data, and do not restate how the tasks were solved. If a Result is missing or the Results conflict, say so '
    'instead of solving that task yourself. Write brief plain prose in the first person, as part of your own '
    'reasoning. Do not write a final response, \\boxed{}, or any markup.')
ANSWER_NOTE = {
    'boxed': ('\n\nNow write the final response to the user: at most two sentences that state the result, ending '
              'with the final answer in \\boxed{}. Do not repeat the calculations.'),
    'countdown': ('\n\nNow write the final response to the user: one sentence, then a separate line beginning '
                  'Final Answer: followed by the expression. Use every given number exactly once, explicit * for '
                  'multiplication, plain ASCII, no equals sign. Do not repeat the search.'),
}
DEFAULTS = dict(summary_ratio=0.5, summary_max_tokens=1024, answer_max_tokens=512, branch_samples=2,
                merger_samples=4, max_input_products=1, long_summary_sources=('gsm', 'math'))


# ------------------------------------------------------------------------------------------------- small io

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_text(text):
    return sha256_bytes(text.encode('utf-8'))


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def raw_lines(path):
    """[(line bytes without newline, parsed row)] of a JSONL file."""
    out = []
    with open(path, 'rb') as handle:
        for line in handle:
            line = line.rstrip(b'\n')
            if line.strip():
                out.append((line, json.loads(line)))
    return out


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    tmp.replace(path)


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w', encoding='utf-8') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')
    tmp.replace(path)
    return sha256_file(path)


def read_results(path):
    """{key: result}; a torn last line (a stop mid-write) is dropped and the file rewritten without it."""
    path = Path(path)
    if not path.exists():
        return {}
    lines = path.read_bytes().split(b'\n')
    results, good = {}, []
    for number, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            if any(rest.strip() for rest in lines[number + 1:]):
                raise
            tmp = path.with_name(path.name + '.tmp')
            tmp.write_bytes(b''.join(item + b'\n' for item in good))
            tmp.replace(path)
            break
        good.append(line)
        results[row['key']] = row
    return results


class ResultWriter:
    """Appends each finished request at once (flushed); fsync every `every` requests and on close."""

    def __init__(self, path, every=64):
        self.handle = open(path, 'a', encoding='utf-8')
        self.every, self.count = every, 0

    def write(self, row):
        self.handle.write(json.dumps(row, ensure_ascii=False) + '\n')
        self.handle.flush()
        self.count += 1
        if self.count % self.every == 0:
            os.fsync(self.handle.fileno())

    def close(self):
        self.handle.flush()
        os.fsync(self.handle.fileno())
        self.handle.close()


# ----------------------------------------------------------------------------------------- record structure

def parse_parallel(row):
    """Exact structure of a one-block raw parallel row; raises ValueError if it is not the generator's layout.

    Returns prefix, plan dict (kind/items/branches/plan_text as gen.validate_plan), bodies, summary, answer and the
    segment index of each replaceable text (bodies, summary, answer)."""
    segs = row['segments']
    texts = [s['text'] for s in segs]
    if texts[0] != '<think>' or texts.count('<Parallel>') != 1 or texts[-1] != '<|im_end|>':
        raise ValueError('not a one-block parallel row')
    p = texts.index('<Parallel>')
    if p > 2:
        raise ValueError('prefix in several segments')
    prefix = texts[1] if p == 2 else ''
    if texts[p + 1] != contract.BRANCHES or texts[p + 3] != '<Plan>' or texts[p + 5] != '</Plan>':
        raise ValueError('block head')
    n = int(texts[p + 2])
    parsed = contract.parse_plan(texts[p + 4], n)
    if parsed is None:
        raise ValueError('invalid plan')
    pos, bodies, body_idx = p + 6, [], []
    for i in range(1, n + 1):
        if texts[pos:pos + 2] != ['<Path>', contract.path_prefix(i)] or texts[pos + 3] != '</Path>':
            raise ValueError(f'path {i}')
        bodies.append(texts[pos + 2])
        body_idx.append(pos + 2)
        pos += 4
    if texts[pos:pos + 2] != ['</Parallel>', '<Summary>'] or texts[pos + 3:pos + 5] != ['</Summary>', '</think>']:
        raise ValueError('block tail')
    if len(texts) != pos + 7:
        raise ValueError('extra segments')
    summary, answer = texts[pos + 2], texts[pos + 5]
    plan = dict(kind=parsed.kind, items=list(parsed.items), branches=n, plan_text=texts[p + 4], status='fork')
    rebuilt = '<think>' + prefix + contract.format_block(parsed.kind, list(parsed.items), bodies, summary) + \
        '</think>' + answer + '<|im_end|>'
    if rebuilt != ''.join(texts):
        raise ValueError('serialization differs')
    return dict(prefix=prefix, plan=plan, bodies=bodies, summary=summary, answer=answer,
                idx=dict(bodies=body_idx, summary=pos + 2, answer=pos + 5))


def rebuild_segments(segments, idx, bodies, summary, answer):
    """Copy of the original segments with only the given texts replaced (loss/block/path untouched)."""
    segs = copy.deepcopy(segments)
    for index, body in zip(idx['bodies'], bodies):
        segs[index]['text'] = body
    segs[idx['summary']]['text'] = summary
    segs[idx['answer']]['text'] = answer
    return segs


def result_line_of(body):
    """The Result line gen.check_branch appended to an accepted branch body (' ' + core + '\\n\\n' + line)."""
    head, sep, line = body.rpartition('\n\n')
    return line if sep and line.startswith('Result: ') and C.meaningful_result(line[len('Result: '):]) else None


# --------------------------------------------------------------------------------------------- task / gold

WORKSHOP = re.compile(
    r'Workshop (\d+) produces (\d+) units and initially sells (\d+) units for \$(\d+) each\. (\d+) of the sold units '
    r'are returned for a full refund\. Materials cost \$(\d+) for EVERY produced unit, including unsold and returned '
    r'units\. Fixed expenses are \$(\d+)\.')
COUNTDOWN_Q = re.compile(r'equals (-?\d+), using these numbers: ([\d, ]+?)\. ')
MUL = r'\s*(?:\*|×|\\times|\\cdot|x|·)\s*'


def workshop_spec(question):
    keys = ('index', 'produced', 'sold', 'price', 'returned', 'material', 'fixed')
    return [dict(zip(keys, map(int, match))) for match in WORKSHOP.findall(question)]


def input_product_pairs(spec):
    """Distinct unordered operand pairs of the products an exec solution computes from the inputs: sold*price,
    returned*price, (sold-returned)*price, produced*material."""
    pairs = set()
    for w in spec:
        for a, b in ((w['sold'], w['price']), (w['returned'], w['price']), (w['sold'] - w['returned'], w['price']),
                     (w['produced'], w['material'])):
            pairs.add(tuple(sorted((a, b))))
    return pairs


def count_input_products(text, spec):
    """Codex's exec re-solving signal (details.jsonl exec_summary_input_products / exec_answer_input_products):
    how many distinct input-product pairs appear written as a multiplication ('a * b', '$a x b', 'a \\times b', ...)
    in either order. Reproduces both stored fields exactly on all 1,329 raw exec records."""
    flat = (text or '').replace(',', '')
    count = 0
    for a, b in input_product_pairs(spec):
        for x, y in ((a, b), (b, a)):
            if re.search(rf'(?<![\d.])\$?{x}{MUL}\$?{y}(?![\d.])', flat):
                count += 1
                break
    return count


def build_q(row, detail):
    """gen.py's question dict (src, task, gold) rebuilt from the record + details.jsonl (gold only for scoring)."""
    src = row['source']
    task = dict(src=src, question=row['question'])
    gold = dict(oracle=detail['oracle'])
    if src == 'countdown':
        match = COUNTDOWN_Q.search(row['question'])
        if match is None:
            raise ValueError('countdown question')
        task['target'] = int(match.group(1))
        task['numbers'] = [int(x) for x in match.group(2).split(',')]
    if src == 'exec':
        spec = workshop_spec(row['question'])
        if len(spec) != 3 or [w['index'] for w in spec] != [1, 2, 3]:
            raise ValueError('workshop spec')
        task['spec'] = spec
        comp = {f'Workshop {w["index"]}': (w['sold'] - w['returned']) * w['price'] - w['produced'] * w['material']
                - w['fixed'] for w in spec}
        if C.numeric(str(detail['oracle'])) != sum(comp.values()):
            raise ValueError('workshop oracle mismatch')
        gold['component_oracles'] = comp
    return dict(id=row['provenance']['task_id'], src=src, task=task, gold=gold, prompt=row['prompt'])


# ------------------------------------------------------------------------------------------------- triage

def triage(detail):
    """Category of one details.jsonl row (first matching rule)."""
    if detail['mode'] == 'sequential':
        if not detail['actual_finished']:
            return 'seq_unfinished'
        return 'seq_clean' if detail['correct'] else 'wrong_final'
    if not detail['correct']:
        return 'wrong_final'
    if detail['final_finish_reason'] != 'stop':
        return 'unfinished_final_or_mixed'
    bad = set(detail['branch_bad'])
    if 'decompose_branch_reports_final_answer' in bad:
        return 'plan_or_branch_solves_whole'
    if bad == {'branch_truncated'}:
        return 'branch_truncated_only'
    if bad:
        return 'unfinished_final_or_mixed' if 'branch_truncated' in bad else 'branch_wrong_other'
    if not detail['actual_finished']:
        return 'unfinished_final_or_mixed'
    if detail['source'] == 'exec' and detail.get('exec_summary_input_products', 0) >= 2:
        return 'exec_summary_resolves'
    return 'par_clean'


def repair_kind(category, row, parsed, cfg):
    if category == 'exec_summary_resolves':
        return EXEC
    if category == 'branch_truncated_only':
        return TRUNC
    if category == 'par_clean' and row['source'] in cfg['long_summary_sources'] and parsed is not None:
        if len(parsed['summary']) > cfg['summary_ratio'] * max(map(len, parsed['bodies'])):
            return LONG
    return None


# --------------------------------------------------------------------------------------------------- prompts

def results_block(job, results):
    return '\n'.join(f'{i}. {item}\n{result}' for i, (item, result) in enumerate(zip(job['plan']['items'], results), 1))


def merger_context(job, results):
    """Plan items + Result lines. exec: Codex's Results-only workshop header (audit_repair.repair_merger_prompt),
    no production inputs; other sources: the question, which is needed to know how to combine."""
    if job['source'] == 'exec':
        return 'Find the total net profit across the workshops.\n\nCompleted independent calculations:\n' + \
            results_block(job, results)
    return job['q']['task']['question'] + '\n\nCompleted independent tasks:\n' + results_block(job, results)


def summary_request(job, results):
    return merger_context(job, results) + SUMMARY_NOTE


def answer_request(job, results, summary):
    note = ANSWER_NOTE['countdown' if job['source'] == 'countdown' else 'boxed']
    return merger_context(job, results) + '\n\nReasoning summary:\n' + summary + note


def branch_request(job, index):
    return job['branch_requests'][str(index)]['text']


# ------------------------------------------------------------------------------------------------- evaluate

class Ctx:
    """Tokenizer-dependent helpers shared by run and assemble (the generator's tokenizer: no tags added)."""

    def __init__(self, tokenizer, cfg, max_model_len=18432, request_seeds=True):
        self.tok, self.cfg, self.max_model_len, self.request_seeds = tokenizer, cfg, max_model_len, request_seeds
        self._cache = {}

    def ntok(self, text):
        if text not in self._cache:
            if len(self._cache) > 200000:
                self._cache.clear()
            self._cache[text] = len(self.tok.encode(text, add_special_tokens=False))
        return self._cache[text]

    def prompt(self, content, thinking):
        return self.tok.apply_chat_template([{'role': 'user', 'content': content}], tokenize=False,
                                            add_generation_prompt=True, enable_thinking=thinking)

    def request(self, key, node, content, thinking, n, budget):
        prompt = self.prompt(content, thinking)
        prompt_ids = self.tok.encode(prompt, add_special_tokens=False)
        max_tokens = min(budget, self.max_model_len - len(prompt_ids) - 8)
        params = dict(n=n, max_tokens=max_tokens, **C.STUDENT_SAMPLING)
        if self.request_seeds:
            params['seed'] = C.seed_of('fast-repair', REVISION, key)
        return dict(key=key, node=node, content=content, thinking=thinking, prompt=prompt, prompt_ids=prompt_ids,
                    params=params)


def expression_key_of(line):
    try:
        return repr(C.expression_key(C.countdown_expr(line[len('Result: '):]) or ''))
    except (ValueError, SyntaxError):
        return None


def evaluate(job, results, ctx):
    """Pure decision for one job given the finished results so far.

    Returns dict(status='waiting', pending=[request...]) | dict(status='failed', reason, ...) |
    dict(status='accepted', bodies, summary, answer, segments, n_tokens, ...)."""
    cfg, q, plan = ctx.cfg, job['q'], job['plan']
    jid = job['id']
    bodies, lines = list(job['bodies']), list(job['results'])
    nodes = dict(branches={}, summary=None, answers={})
    # 1. truncated branches
    if job['truncated']:
        kept = sum(ctx.ntok(b) for i, b in enumerate(bodies) if i not in job['truncated'])
        budget = (TOTAL - C.RESERVE - C.overhead(ctx, job['prefix'], plan) - kept) // len(job['truncated'])
        pending = []
        for i in job['truncated']:
            key = f'{jid}|branch{i + 1}'
            if key not in results:
                req = ctx.request(key, f'branch{i + 1}', branch_request(job, i), True, cfg['branch_samples'], budget)
                if req['params']['max_tokens'] < 64:
                    return dict(status='failed', reason='branch_budget', nodes=nodes)
                pending.append(req)
        if pending:
            return dict(status='waiting', pending=pending, nodes=nodes)
        used = {expression_key_of(line) for i, line in enumerate(lines)
                if i not in job['truncated'] and job['source'] == 'countdown' and line and C.countdown_expr(line)}
        for i in job['truncated']:
            key = f'{jid}|branch{i + 1}'
            samples = []
            for k, out in enumerate(results[key]['outputs']):
                ok, reason, body, line = C.check_branch(q, plan, i, out)
                if ok and reason == 'ok_countdown_valid' and expression_key_of(line) in used:
                    ok, reason = False, 'countdown_duplicate_expression'
                samples.append(dict(index=k, ok=ok, reason=reason, body=body, line=line,
                                    finish_reason=out['finish_reason'], n_tokens=out['n_tokens']))
            good = sorted((s for s in samples if s['ok']),
                          key=lambda s: (s['reason'] not in ('ok_oracle_verified', 'ok_countdown_valid'),
                                         s['n_tokens'], s['index']))
            nodes['branches'][i] = dict(key=key, samples=[{k: v for k, v in s.items() if k not in ('body', 'line')}
                                                          for s in samples],
                                        accepted_index=good[0]['index'] if good else None,
                                        reason=good[0]['reason'] if good else None)
            if not good:
                worst = Counter(s['reason'] for s in samples).most_common(1)[0][0]
                return dict(status='failed', reason=f'branch:{worst}', nodes=nodes)
            bodies[i], lines[i] = good[0]['body'], good[0]['line']
            if good[0]['reason'] == 'ok_countdown_valid':
                used.add(expression_key_of(lines[i]))
    # 2. summary (non-thinking), n samples
    longest = max(map(len, bodies))
    _, empty = C.parallel_segments(job['prefix'], plan, bodies, '', '\n\n')
    remaining = TOTAL - ctx.ntok(empty) - C.MARGIN
    key = f'{jid}|summary'
    budget = min(cfg['summary_max_tokens'], remaining - cfg['answer_max_tokens'])
    if key not in results:
        req = ctx.request(key, 'summary', summary_request(job, lines), False, cfg['merger_samples'], budget)
        if req['params']['max_tokens'] < 32:
            return dict(status='failed', reason='summary_budget', nodes=nodes)
        return dict(status='waiting', pending=[req], nodes=nodes)
    spec = q['task'].get('spec')
    candidates, pending = [], []
    summary_samples = []
    for k, out in enumerate(results[key]['outputs']):
        text = out['text'].strip()
        reason = None
        if out['finish_reason'] != 'stop':
            reason = 'summary_truncated'
        elif not text:
            reason = 'summary_empty'
        elif not contract.plain_text(text):
            reason = 'summary_tags'
        elif len(text) > cfg['summary_ratio'] * longest:
            reason = 'summary_too_long'
        elif spec and count_input_products(text, spec) > cfg['max_input_products']:
            reason = 'summary_input_products'
        summary_samples.append(dict(index=k, finish_reason=out['finish_reason'], n_tokens=out['n_tokens'],
                                    chars=len(text), reason=reason or 'ok'))
        if reason is None:
            candidates.append((k, text))
    nodes['summary'] = dict(key=key, samples=summary_samples)
    if not candidates:
        return dict(status='failed', reason='summary:' + Counter(s['reason'] for s in summary_samples)
                    .most_common(1)[0][0], nodes=nodes)
    # 3. answer (non-thinking) per surviving summary
    for k, summary in candidates:
        akey = f'{jid}|answer{k + 1}'
        if akey not in results:
            budget = min(cfg['answer_max_tokens'], remaining - ctx.ntok(summary))
            req = ctx.request(akey, f'answer{k + 1}', answer_request(job, lines, summary), False, 1, budget)
            if req['params']['max_tokens'] >= 16:
                pending.append(req)
            else:
                nodes['answers'][k] = dict(key=akey, reason='answer_budget')
    if pending:
        return dict(status='waiting', pending=pending, nodes=nodes)
    accepted = []
    for k, summary in candidates:
        akey = f'{jid}|answer{k + 1}'
        if akey not in results:
            continue
        out = results[akey]['outputs'][0]
        answer = out['text'].strip()
        reason, grade, n_tokens, segs = None, None, None, None
        if out['finish_reason'] != 'stop':
            reason = 'answer_truncated'
        elif not answer:
            reason = 'answer_empty'
        elif not contract.plain_text(answer):
            reason = 'answer_tags'
        elif spec and count_input_products(answer, spec) > cfg['max_input_products']:
            reason = 'answer_input_products'
        else:
            correct, grade = C.final_grade(dict(q=q, final=dict(text=summary + '\n</think>\n\n' + answer)))
            if not correct:
                reason = 'wrong:' + grade
        if reason is None:
            segs = rebuild_segments(job['segments'], job['idx'], bodies, summary, '\n\n' + answer)
            n_tokens = ctx.ntok(''.join(s['text'] for s in segs))
            if n_tokens > TOTAL:
                reason = 'over_budget'
            else:
                try:
                    D.validate_row(dict(id=jid, source=job['source'], mode='parallel', prompt=job['q']['prompt'],
                                        segments=segs, provenance={}))
                except D.DataError as error:
                    reason = 'invalid:' + error.reason
        nodes['answers'][k] = dict(key=akey, finish_reason=out['finish_reason'], n_tokens=out['n_tokens'],
                                   chars=len(answer), reason=reason or 'ok', grade=grade)
        if reason is None:
            accepted.append(dict(index=k, summary=summary, answer='\n\n' + answer, segments=segs, n_tokens=n_tokens,
                                 grade=grade, cost=ctx.ntok(summary) + out['n_tokens']))
    if not accepted:
        reasons = Counter(a['reason'] for a in nodes['answers'].values())
        return dict(status='failed', reason='answer:' + reasons.most_common(1)[0][0], nodes=nodes)
    best = min(accepted, key=lambda a: (a['cost'], a['index']))
    nodes['summary']['accepted_index'] = best['index']
    return dict(status='accepted', bodies=bodies, results=lines, summary=best['summary'], answer=best['answer'],
                segments=best['segments'], n_tokens=best['n_tokens'], grade=best['grade'], nodes=nodes,
                longest_branch_chars=longest)


# ------------------------------------------------------------------------------------------------------ plan

def load_branch_requests(path):
    table = {}
    if path:
        for row in D.read_jsonl(path):
            if isinstance(row, D.DataError):
                raise SystemExit(f'{path}: {row}')
            table[(row['task_id'], int(row['index']))] = row
    return table


def plan_records(raw_path, details_path, cfg, branch_requests=None, fallback='none', expect_sha256=RAW_SHA256):
    """(jobs, stats) for the raw pool; pure CPU, no tokenizer."""
    raw_sha = sha256_file(raw_path)
    if expect_sha256 and raw_sha != expect_sha256:
        raise SystemExit(f'{raw_path} sha256 {raw_sha} != expected {expect_sha256}')
    entries = raw_lines(raw_path)
    details = {d['id']: d for _, d in raw_lines(details_path)}
    branch_requests = branch_requests or {}
    categories, by_source = Counter(), defaultdict(Counter)
    jobs, skipped, bucket = [], defaultdict(Counter), Counter()
    long_ratio = Counter()
    for line, row in entries:
        detail = details.get(row['id'])
        if detail is None:
            raise SystemExit(f'{row["id"]} missing in details')
        category = triage(detail)
        categories[category] += 1
        by_source[category][row['source']] += 1
        parsed = None
        if row['mode'] == 'parallel':
            try:
                parsed = parse_parallel(row)
            except ValueError:
                parsed = None
        kind = repair_kind(category, row, parsed, cfg)
        if category == 'par_clean' and row['source'] in cfg['long_summary_sources'] and parsed is not None:
            longest = max(map(len, parsed['bodies']))
            long_ratio[(row['source'], '>ratio' if len(parsed['summary']) > cfg['summary_ratio'] * longest
                        else '<=ratio')] += 1
            long_ratio[(row['source'], '>1.0x' if len(parsed['summary']) > longest else '<=1.0x')] += 1
        if kind is None:
            continue
        bucket[kind] += 1

        def skip(reason):
            skipped[kind][reason] += 1

        if parsed is None:
            skip('unparsed_structure')
            continue
        if row['provenance'].get('plan_status') == 'gold_in_plan':
            skip('plan_status_gold_in_plan')
            continue
        try:
            D.validate_row(row)
        except D.DataError as error:
            skip('original_invalid:' + error.reason)
            continue
        try:
            q = build_q(row, detail)
        except ValueError as error:
            skip(f'task:{error}')
            continue
        checks = row['provenance']['branch_checks']
        truncated = [i for i, c in enumerate(checks) if c['reason'] == 'branch_truncated'] if kind == TRUNC else []
        if kind == TRUNC and (not truncated or len(truncated) != detail['branch_bad'].count('branch_truncated')):
            skip('truncated_flags_disagree')
            continue
        results = [None if i in truncated else result_line_of(b) for i, b in enumerate(parsed['bodies'])]
        if any(r is None for i, r in enumerate(results) if i not in truncated):
            skip('kept_branch_without_result_line')
            continue
        requests = {}
        if truncated:
            missing = None
            for i in truncated:
                found = branch_requests.get((q['id'], i))
                if found is not None and found.get('body_sha256') == sha256_text(parsed['bodies'][i]):
                    text, source = found['request'], 'raw_run_request'
                elif fallback == 'arm_d':
                    text, source = C.executor_prompt_d(q, parsed['prefix'], parsed['plan'], i), 'fallback_arm_d'
                else:
                    missing = 'branch_request_body_mismatch' if found is not None else 'branch_request_unavailable'
                    break
                suffix = ''
                if q['src'] == 'countdown' and 'ANY SUBSET' not in text:
                    suffix = C.COUNTDOWN_BRANCH_SUFFIX
                requests[str(i)] = dict(text=text + suffix, source=source, countdown_suffix_added=bool(suffix))
            if missing:
                skip(missing)
                continue
        jobs.append(dict(
            id=row['id'], task_id=q['id'], kind=kind, source=row['source'], category=category, q=q,
            prefix=parsed['prefix'], plan=parsed['plan'], bodies=parsed['bodies'], results=results,
            truncated=truncated, branch_requests=requests, segments=row['segments'], idx=parsed['idx'],
            original=dict(line_sha256=sha256_bytes(line), n_tokens=row['provenance'].get('n_tokens'),
                          summary_chars=len(parsed['summary']), answer_chars=len(parsed['answer']),
                          longest_branch_chars=max(map(len, parsed['bodies'])),
                          branch_checks=checks,
                          exec_summary_input_products=detail.get('exec_summary_input_products'),
                          exec_answer_input_products=detail.get('exec_answer_input_products'))))
    jobs.sort(key=lambda j: (KINDS.index(j['kind']), j['id']))
    triage_check = {name: dict(expected=want, got=categories.get(name, 0), match=categories.get(name, 0) == want)
                    for name, want in EXPECTED_TRIAGE.items()}
    stats = dict(
        revision=REVISION, raw=dict(path=str(raw_path), sha256=raw_sha, rows=len(entries)),
        details=dict(path=str(details_path), sha256=sha256_file(details_path)), config=cfg,
        branch_request_fallback=fallback, branch_requests_loaded=len(branch_requests),
        triage=dict(categories), triage_by_source={k: dict(v) for k, v in by_source.items()},
        triage_check=triage_check,
        long_summary_par_clean={f'{s}/{r}': c for (s, r), c in sorted(long_ratio.items())},
        buckets=dict(bucket), skipped={k: dict(v) for k, v in skipped.items()},
        jobs=dict(Counter(j['kind'] for j in jobs)),
        jobs_by_source={kind: dict(Counter(j['source'] for j in jobs if j['kind'] == kind)) for kind in KINDS},
        truncated_branches=sum(len(j['truncated']) for j in jobs))
    return jobs, stats, entries


def estimate(jobs, entries, cfg):
    """Request/token/time estimate without the tokenizer: generator tokens from characters per token measured on the
    raw pool (assistant text characters / provenance.n_tokens, per source)."""
    chars, tokens = Counter(), Counter()
    finished_branch = defaultdict(list)
    for _, row in entries:
        chars[row['source']] += sum(len(s['text']) for s in row['segments'])
        tokens[row['source']] += row['provenance']['n_tokens']
        if row['mode'] == 'parallel':
            for s, check in zip([s for s in row['segments'] if s['path'] and s['loss'] and s['text'] != '</Path>'],
                                row['provenance']['branch_checks']):
                if check['ok']:
                    finished_branch[row['source']].append(len(s['text']))
    cpt = {s: chars[s] / tokens[s] for s in chars}
    out = dict(chars_per_token={s: round(v, 3) for s, v in cpt.items()}, requests=Counter(), sequences=Counter(),
               max_tokens=Counter(), expected_tokens=Counter())
    for job in jobs:
        rate = cpt[job['source']]
        est = lambda text: len(text) / rate  # noqa: E731
        bodies = job['bodies']
        if job['truncated']:
            empty = '<think>' + job['prefix'] + contract.format_block(job['plan']['kind'], job['plan']['items'],
                                                                       [''] * len(bodies), '') + '</think>\n\n<|im_end|>'
            kept = sum(est(b) for i, b in enumerate(bodies) if i not in job['truncated'])
            cap = max(0, int((TOTAL - C.RESERVE - est(empty) - C.MARGIN - kept) // len(job['truncated'])))
            typical = statistics.fmean(finished_branch[job['source']]) / rate
            for i in job['truncated']:
                # a new sample is assumed at least as long as the truncated raw attempt (the hard tail)
                expect = min(cap, max(est(bodies[i]), typical))
                out['requests']['branch'] += 1
                out['sequences']['branch'] += cfg['branch_samples']
                out['max_tokens']['branch'] += cfg['branch_samples'] * cap
                out['expected_tokens']['branch'] += cfg['branch_samples'] * expect
        n = cfg['merger_samples']
        out['requests']['summary'] += 1
        out['sequences']['summary'] += n
        out['max_tokens']['summary'] += n * cfg['summary_max_tokens']
        out['expected_tokens']['summary'] += n * 350
        out['requests']['answer'] += n
        out['sequences']['answer'] += n
        out['max_tokens']['answer'] += n * cfg['answer_max_tokens']
        out['expected_tokens']['answer'] += n * 80
    for key in ('max_tokens', 'expected_tokens'):
        out[key] = {k: int(v) for k, v in out[key].items()}
    # Decode throughput assumptions (vLLM 0.8.5, bf16 4B, prefix caching): long branch contexts (8-14k tokens) are
    # KV-bandwidth bound, ~80-120 running sequences on 94 GB; short non-thinking merger calls run ~256 sequences.
    tps = {'H100 NVL': dict(branch=5000, merger=15000), 'A100 80GB': dict(branch=2800, merger=8000)}
    out['minutes'] = {}
    for gpu, rate in tps.items():
        def minutes(tokens):
            return round((tokens.get('branch', 0) / rate['branch'] +
                          (tokens.get('summary', 0) + tokens.get('answer', 0)) / rate['merger']) / 60 + 3, 1)
        out['minutes'][gpu] = dict(expected=minutes(out['expected_tokens']), upper_bound=minutes(out['max_tokens']),
                                   assumed_decode_tokens_per_s=rate, model_load_minutes=3)
    out['requests'], out['sequences'] = dict(out['requests']), dict(out['sequences'])
    out['note'] = ('answer requests are an upper bound (one per summary sample that passes the summary checks); '
                   'expected summary/answer lengths 350/80 tokens are assumptions; branch expectation = max(raw '
                   'truncated attempt, mean finished branch of the source), capped by the new budget.')
    return out


def cmd_plan(args):
    cfg = dict(DEFAULTS, summary_ratio=args.summary_ratio, summary_max_tokens=args.summary_max_tokens,
               answer_max_tokens=args.answer_max_tokens, max_input_products=args.max_input_products,
               long_summary_sources=tuple(args.long_summary_sources.split(',')))
    jobs, stats, entries = plan_records(args.raw, args.details, cfg, load_branch_requests(args.branch_requests),
                                        args.branch_request_fallback, args.expect_sha256)
    stats['estimate'] = estimate(jobs, entries, cfg)
    if stats['skipped'].get(TRUNC, {}).get('branch_request_unavailable'):
        # what the run costs once the exact raw requests are supplied (same budgets; request texts do not matter)
        hypo, _, _ = plan_records(args.raw, args.details, cfg, {}, 'arm_d', args.expect_sha256)
        stats['estimate_with_branch_requests'] = dict(jobs=dict(Counter(j['kind'] for j in hypo)),
                                                      truncated_branches=sum(len(j['truncated']) for j in hypo),
                                                      **estimate(hypo, entries, cfg))
    stats['notes'] = [
        'Every raw branch request was the planner\'s standalone mini-problem (gen.executor_prompt_e: no branch '
        'mentions a sub-task), and the records do not store it: exact branch repair needs '
        'wave-*/raw_branches.jsonl from the raw run (`fast_repair.py requests`). Without it branch_truncated '
        'records are skipped (or use --branch-request-fallback arm_d, a different request).',
        'countdown_core.verify was not shipped; codex_rules.countdown_verify agrees with every stored Countdown '
        'verdict. math_verify (in the VM venv) is required by gen.grade for run/assemble.',
        'par_clean includes 5 gold_in_plan records (select_records drops them by default); they and 3 gold_in_plan '
        'truncated records are not repaired.',
        'Triage categories without user counts (wrong_final, plan_or_branch_solves_whole, branch_wrong_other, '
        'unfinished_final_or_mixed, seq_unfinished) follow the first-matching rule in fast_repair.triage.']
    if args.work_dir:
        args.work_dir.mkdir(parents=True, exist_ok=True)
        stats['jobs_file'] = dict(path=str(args.work_dir / 'jobs.jsonl'), sha256=write_jsonl(args.work_dir /
                                                                                              'jobs.jsonl', jobs))
        write_json(args.work_dir / 'plan.json', stats)
    if args.stats:
        write_json(args.stats, stats)
    print(json.dumps(dict(triage=stats['triage'], triage_check=stats['triage_check'], buckets=stats['buckets'],
                          jobs=stats['jobs'], skipped=stats['skipped'], requests=stats['estimate']['requests'],
                          minutes=stats['estimate']['minutes']), indent=1))
    return jobs, stats


# ------------------------------------------------------------------------------------------- branch requests

def cmd_requests(args):
    """Exact raw branch requests from the raw run directory (wave-*/raw_branches.jsonl: 'request' per branch)."""
    rows, files = [], sorted(Path(args.raw_run_root).glob('wave-*/raw_branches.jsonl'))
    if not files:
        raise SystemExit(f'no wave-*/raw_branches.jsonl under {args.raw_run_root}')
    for path in files:
        for item in D.read_jsonl(path):
            for branch in item['branches']:
                rows.append(dict(task_id=item['id'], index=branch['index'], request=branch['request'],
                                 request_sha256=sha256_text(branch['request']), raw_limit=branch.get('limit'),
                                 raw_finish_reason=branch.get('finish_reason'),
                                 body_sha256=sha256_text(branch['body']), source_file=str(path)))
    sha = write_jsonl(args.out, rows)
    print(f'{len(rows)} branch requests from {len(files)} files -> {args.out} (sha256 {sha})')


# ------------------------------------------------------------------------------------------------- backends

class VLLMBackend:
    """vLLM offline engine built like Codex's gen.Engine; 'stream' adds requests to the engine and returns each one
    as soon as it finishes (what LLM.generate does internally), 'chunks' calls LLM.generate on `chunk` requests."""

    def __init__(self, model, revision, max_model_len, gpu_memory_utilization, max_num_seqs, fast_sampler=True,
                 mode='stream', chunk=64):
        if fast_sampler:  # Codex's exact top-k/top-p patch must run in the engine process
            os.environ.setdefault('VLLM_ENABLE_V1_MULTIPROCESSING', '0')
            C.patch_sampler()
        import vllm
        from vllm import LLM
        self.version = vllm.__version__
        self.llm = LLM(model=model, revision=revision, tokenizer_revision=revision, dtype='bfloat16',
                       max_model_len=max_model_len, gpu_memory_utilization=gpu_memory_utilization, seed=0,
                       enable_prefix_caching=True, max_num_seqs=max_num_seqs)
        self.tokenizer = self.llm.get_tokenizer()
        self.mode, self.chunk, self.queue, self.live = mode, chunk, [], 0

    @staticmethod
    def _params(params):
        from vllm import SamplingParams
        from vllm.sampling_params import RequestOutputKind
        sampling = SamplingParams(**params)
        sampling.output_kind = RequestOutputKind.FINAL_ONLY
        return sampling

    @staticmethod
    def _outputs(result):
        return [dict(text=o.text, finish_reason=o.finish_reason, n_tokens=len(o.token_ids)) for o in result.outputs]

    def add(self, request):
        if self.mode == 'stream':
            self.llm.llm_engine.add_request(request['key'], {'prompt_token_ids': request['prompt_ids']},
                                            self._params(request['params']))
            self.live += 1
        else:
            self.queue.append(request)

    def has_unfinished(self):
        return self.live > 0 if self.mode == 'stream' else bool(self.queue)

    def step(self):
        if self.mode == 'stream':
            done = [(o.request_id, self._outputs(o)) for o in self.llm.llm_engine.step() if o.finished]
            self.live -= len(done)
            return done
        batch, self.queue = self.queue[:self.chunk], self.queue[self.chunk:]
        results = self.llm.generate([{'prompt_token_ids': r['prompt_ids']} for r in batch],
                                    [self._params(r['params']) for r in batch], use_tqdm=False)
        return [(r['key'], self._outputs(o)) for r, o in zip(batch, results)]


def run_jobs(jobs, results, backend, ctx, writer, log_every=64, limit=None):
    """Drive every job to accepted/failed: add each job's ready requests, record finished ones, re-evaluate that job
    (so a merger starts as soon as its branches finish). Returns the number of requests run."""
    by_id = {job['id']: job for job in jobs}
    inflight, meta, count, start = set(), {}, 0, time.time()
    sampled = Counter()

    def refill(job_ids):
        added = 0
        for jid in job_ids:
            state = evaluate(by_id[jid], results, ctx)
            for req in state.get('pending', ()):
                if req['key'] in inflight or req['key'] in results:
                    continue
                if limit is not None and count + len(inflight) >= limit:
                    return added
                backend.add(req)
                inflight.add(req['key'])
                meta[req['key']] = req
                added += 1
        return added

    # longest first: branch requests (largest budgets) before the short merger calls
    order = sorted(by_id, key=lambda jid: (not by_id[jid]['truncated'], jid))
    refill(order)
    while backend.has_unfinished():
        for key, outputs in backend.step():
            req = meta.pop(key)
            inflight.discard(key)
            row = dict(key=key, job_id=key.rsplit('|', 1)[0], node=req['node'], thinking=req['thinking'],
                       params=req['params'], prompt_sha256=sha256_text(req['prompt']),
                       prompt_tokens=len(req['prompt_ids']), request=req['content'], outputs=outputs,
                       utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
            results[key] = row
            writer.write(row)
            count += 1
            sampled[req['node'].rstrip('0123456789')] += sum(o['n_tokens'] for o in outputs)
            if count % log_every == 0:
                print(json.dumps(dict(requests=count, inflight=len(inflight), minutes=round((time.time() - start) / 60,
                                      1), sampled_tokens=dict(sampled))), flush=True)
            refill([row['job_id']])
    return count, dict(sampled)


def require_math_verify(jobs):
    if any(job['source'] in ('math', 'gsm', 'exec') for job in jobs):
        import importlib
        try:
            importlib.import_module('math_verify')
        except ImportError:
            raise SystemExit("math_verify is required by Codex's scorer (gen.grade): pip install math-verify")


def load_work(work_dir):
    plan = json.loads((work_dir / 'plan.json').read_text())
    jobs = [row for _, row in raw_lines(work_dir / 'jobs.jsonl')]
    if sha256_file(work_dir / 'jobs.jsonl') != plan['jobs_file']['sha256']:
        raise SystemExit('jobs.jsonl changed since plan')
    return plan, jobs


def cmd_run(args, backend=None):
    plan, jobs = load_work(args.work_dir)
    require_math_verify(jobs)
    if args.limit_jobs:
        jobs = jobs[:args.limit_jobs]
    results = read_results(args.work_dir / 'results.jsonl')
    if backend is None:
        backend = VLLMBackend(args.model, args.revision, args.max_model_len, args.gpu_memory_utilization,
                              args.max_num_seqs, not args.no_fast_sampler, args.engine, args.checkpoint_every)
    ctx = Ctx(backend.tokenizer, plan['config'], args.max_model_len, not args.no_request_seeds)
    manifest = dict(revision=REVISION, model=args.model, revision_model=args.revision,
                    vllm=getattr(backend, 'version', None), engine=args.engine, max_model_len=args.max_model_len,
                    gpu_memory_utilization=args.gpu_memory_utilization, max_num_seqs=args.max_num_seqs,
                    fast_sampler=not args.no_fast_sampler, request_seeds=not args.no_request_seeds, engine_seed=0,
                    sampling=C.STUDENT_SAMPLING, checkpoint_every=args.checkpoint_every, jobs=len(jobs),
                    resumed_with=len(results), start=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    writer = ResultWriter(args.work_dir / 'results.jsonl', args.checkpoint_every)
    t0 = time.time()
    try:
        count, sampled = run_jobs(jobs, results, backend, ctx, writer, args.checkpoint_every, args.limit)
    finally:
        writer.close()
    states = Counter(evaluate(job, results, ctx)['status'] for job in jobs)
    manifest.update(requests_this_run=count, sampled_tokens=sampled, minutes=round((time.time() - t0) / 60, 2),
                    end=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), job_states=dict(states))
    runs = args.work_dir / 'run_manifest.jsonl'
    with runs.open('a') as handle:
        handle.write(json.dumps(manifest) + '\n')
    print(json.dumps(manifest, indent=1))
    return manifest


# -------------------------------------------------------------------------------------------------- assemble

def recheck_kept_branch(q, plan, index, body):
    """Codex's gen.check_branch on an unchanged accepted body (rebuilt as a finished output); the body it rebuilds
    must equal the stored body."""
    core, sep, line = body[1:].rpartition('\n\n')
    if not body.startswith(' ') or not sep:
        return dict(ok=False, reason='recheck_unparsable_body')
    ok, reason, rebuilt, _ = C.check_branch(q, plan, index, dict(finish_reason='stop',
                                                               text=core + '\n</think>\n\n' + line))
    if ok and rebuilt != body:
        return dict(ok=False, reason='recheck_body_mismatch')
    return dict(ok=ok, reason=reason)


def assemble_job(job, original, state, ctx, run_info):
    """(row or None, outcome dict). original: the raw row (its line sha256 must match the plan)."""
    kind = job['kind']
    if state['status'] == 'accepted':
        row = copy.deepcopy(original)
        row['segments'] = state['segments']
        prov = row['provenance']
        replaced = set(job['truncated'])
        checks = []
        for i, body in enumerate(state['bodies']):
            if i in replaced:
                checks.append(dict(ok=True, reason=state['nodes']['branches'][i]['reason']))
            else:
                checks.append(recheck_kept_branch(job['q'], job['plan'], i, body))
        raw_checks = job['original']['branch_checks']
        finished = all(i in replaced or raw_checks[i]['reason'] not in ('branch_truncated', 'branch_unfinished')
                       for i in range(len(checks)))  # the raw run's finish facts for kept branches
        correct, grade = C.final_grade(dict(q=job['q'], final=dict(
            text=state['summary'] + '\n</think>\n\n' + state['answer'].strip())))
        n_tokens = ctx.ntok(''.join(s['text'] for s in row['segments']))
        prov.update(model_finished=finished, correct=correct, grade=grade, branch_checks=checks,
                    n_tokens=n_tokens, over_budget=n_tokens > TOTAL, repair_failed=False)
        node = '+'.join([f'branch{i + 1}' for i in job['truncated']] + ['summary', 'answer'])
        prov['repair'] = dict(
            kind=kind, node=node, status='accepted', model=run_info.get('model'),
            revision=run_info.get('revision_model'), repair_revision=REVISION, attempts=state['nodes'],
            accepted_index=state['nodes']['summary']['accepted_index'],
            original_sha256=job['original']['line_sha256'],
            prompt_sha256={key: run_info['prompt_sha256'].get(key) for key in prompt_keys(job, state)},
            branch_request_sources={i: job['branch_requests'][str(i)]['source'] for i in job['truncated']},
            sampling=C.STUDENT_SAMPLING, seeds={key: run_info['seeds'].get(key) for key in prompt_keys(job, state)},
            lengths=dict(n_tokens_before=job['original']['n_tokens'], n_tokens_after=n_tokens,
                         summary_chars_before=job['original']['summary_chars'],
                         summary_chars_after=len(state['summary']),
                         answer_chars_before=job['original']['answer_chars'], answer_chars_after=len(state['answer']),
                         longest_branch_chars=state['longest_branch_chars'],
                         branch_chars_after={i + 1: len(state['bodies'][i]) for i in job['truncated']}),
            exec_input_products=(dict(summary=count_input_products(state['summary'], job['q']['task']['spec']),
                                      answer=count_input_products(state['answer'], job['q']['task']['spec']),
                                      summary_before=job['original']['exec_summary_input_products'],
                                      answer_before=job['original']['exec_answer_input_products'])
                                 if job['source'] == 'exec' else None))
        D.validate_row(row)
        ok = finished and correct and all(c['ok'] for c in checks) and n_tokens <= TOTAL
        return row, dict(id=job['id'], kind=kind, status='accepted' if ok else 'recheck_failed',
                         reason=None if ok else 'recheck', n_tokens=n_tokens)
    if state['status'] == 'failed' and kind in (EXEC, LONG):
        row = copy.deepcopy(original)
        row['provenance']['repair_failed'] = True
        row['provenance']['repair'] = dict(kind=kind, status='failed', reason=state['reason'],
                                           attempts=state.get('nodes'),
                                           original_sha256=job['original']['line_sha256'],
                                           model=run_info.get('model'), revision=run_info.get('revision_model'),
                                           repair_revision=REVISION)
        return row, dict(id=job['id'], kind=kind, status='repair_failed', reason=state['reason'])
    return None, dict(id=job['id'], kind=kind, status=state['status'], reason=state.get('reason', 'not_run'))


def prompt_keys(job, state):
    keys = [f'{job["id"]}|branch{i + 1}' for i in job['truncated']] + [f'{job["id"]}|summary']
    return keys + [f'{job["id"]}|answer{state["nodes"]["summary"]["accepted_index"] + 1}']


def assemble(work_dir, raw_path, tokenizer, max_model_len=18432):
    plan, jobs = load_work(work_dir)
    require_math_verify(jobs)
    results = read_results(work_dir / 'results.jsonl')
    if sha256_file(raw_path) != plan['raw']['sha256']:
        raise SystemExit('raw file differs from the planned one')
    originals = {row['id']: (line, row) for line, row in raw_lines(raw_path)}
    runs = [json.loads(x) for x in (work_dir / 'run_manifest.jsonl').read_text().splitlines()] \
        if (work_dir / 'run_manifest.jsonl').exists() else [{}]
    seeds_on = runs[-1].get('request_seeds', True)
    ctx = Ctx(tokenizer, plan['config'], max_model_len, seeds_on)
    run_info = dict(model=runs[-1].get('model'), revision_model=runs[-1].get('revision_model'),
                    prompt_sha256={k: r['prompt_sha256'] for k, r in results.items()},
                    seeds={k: r['params'].get('seed') for k, r in results.items()})
    rows, outcomes = [], []
    for job in jobs:
        line, original = originals[job['id']]
        if sha256_bytes(line) != job['original']['line_sha256'] or original['segments'] != job['segments']:
            raise SystemExit(f'{job["id"]}: raw row differs from the planned one')
        state = evaluate(job, results, ctx)
        if state['status'] == 'waiting':
            state = dict(status='not_run', reason='not_run')
        row, outcome = assemble_job(job, original, state, ctx, run_info)
        outcomes.append(outcome)
        if row is not None:
            rows.append(row)
    summary = defaultdict(Counter)
    for outcome in outcomes:
        summary[outcome['kind']][outcome['status'] + (':' + outcome['reason'] if outcome.get('reason') else '')] += 1
    accepted = [r for r in rows if not r['provenance'].get('repair_failed')]
    lengths = defaultdict(lambda: defaultdict(list))
    for row in accepted:
        rep = row['provenance']['repair']
        for key in ('summary_chars_before', 'summary_chars_after', 'answer_chars_before', 'answer_chars_after',
                    'n_tokens_before', 'n_tokens_after'):
            lengths[rep['kind']][key].append(rep['lengths'][key])
    stats = dict(revision=REVISION, jobs=len(jobs), results=len(results),
                 outcomes={k: dict(v) for k, v in summary.items()},
                 accepted=dict(Counter(r['provenance']['repair']['kind'] for r in accepted)),
                 repair_failed=dict(Counter(r['provenance']['repair']['kind'] for r in rows
                                            if r['provenance'].get('repair_failed'))),
                 mean_lengths={kind: {k: round(statistics.fmean(v), 1) for k, v in d.items()}
                               for kind, d in lengths.items()})
    stats['assembled_sha256'] = write_jsonl(work_dir / 'assembled.jsonl', rows)
    write_jsonl(work_dir / 'outcomes.jsonl', outcomes)
    write_json(work_dir / 'assemble_stats.json', stats)
    print(json.dumps(stats, indent=1))
    return rows, stats


def load_tokenizer(name, revision):
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(name, revision=revision)


def cmd_assemble(args, tokenizer=None):
    plan = json.loads((args.work_dir / 'plan.json').read_text())
    raw_path = args.raw or Path(plan['raw']['path'])
    tokenizer = tokenizer or load_tokenizer(args.tokenizer, args.revision)
    return assemble(args.work_dir, raw_path, tokenizer, args.max_model_len)


def cmd_export(args):
    rows = [row for _, row in raw_lines(args.work_dir / 'assembled.jsonl')]
    seen = set()
    for row in rows:
        D.validate_row(row)
        if row['id'] in seen:
            raise SystemExit(f'duplicate id {row["id"]}')
        seen.add(row['id'])
    sha = write_jsonl(args.out, rows)
    stats = dict(out=str(args.out), sha256=sha, rows=len(rows),
                 repaired=sum(not r['provenance'].get('repair_failed') for r in rows),
                 repair_failed=sum(bool(r['provenance'].get('repair_failed')) for r in rows),
                 by_kind=dict(Counter(f'{r["provenance"]["repair"]["kind"]}/'
                                      f'{"failed" if r["provenance"].get("repair_failed") else "repaired"}'
                                      for r in rows)))
    write_json(args.work_dir / 'export_stats.json', stats)
    print(json.dumps(stats, indent=1))
    return stats


# ------------------------------------------------------------------------------------------------------ cli

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('plan', help='CPU: triage, job list, stats')
    p.add_argument('--raw', type=Path, required=True)
    p.add_argument('--details', type=Path, required=True)
    p.add_argument('--work-dir', type=Path, default=None)
    p.add_argument('--stats', type=Path, default=None, help='also write the stats JSON here')
    p.add_argument('--branch-requests', type=Path, default=None, help='output of the requests subcommand')
    p.add_argument('--branch-request-fallback', choices=('none', 'arm_d'), default='none',
                   help="arm_d: Codex's in-context executor_prompt_d when the exact raw request is unavailable")
    p.add_argument('--summary-ratio', type=float, default=DEFAULTS['summary_ratio'])
    p.add_argument('--summary-max-tokens', type=int, default=DEFAULTS['summary_max_tokens'])
    p.add_argument('--answer-max-tokens', type=int, default=DEFAULTS['answer_max_tokens'])
    p.add_argument('--max-input-products', type=int, default=DEFAULTS['max_input_products'])
    p.add_argument('--long-summary-sources', default=','.join(DEFAULTS['long_summary_sources']))
    p.add_argument('--expect-sha256', default=RAW_SHA256, help="'' skips the raw sha256 check")
    r = sub.add_parser('requests', help='extract exact raw branch requests from the raw run directory')
    r.add_argument('--raw-run-root', type=Path, required=True)
    r.add_argument('--out', type=Path, required=True)
    g = sub.add_parser('run', help='GPU: generate (resumable)')
    g.add_argument('--work-dir', type=Path, required=True)
    g.add_argument('--model', default=BASE_MODEL)
    g.add_argument('--revision', default=BASE_REVISION)
    g.add_argument('--max-model-len', type=int, default=18432)
    g.add_argument('--gpu-memory-utilization', type=float, default=0.9)
    g.add_argument('--max-num-seqs', type=int, default=256)
    g.add_argument('--engine', choices=('stream', 'chunks'), default='stream')
    g.add_argument('--checkpoint-every', type=int, default=64)
    g.add_argument('--no-request-seeds', action='store_true')
    g.add_argument('--no-fast-sampler', action='store_true')
    g.add_argument('--limit', type=int, default=None, help='stop adding requests after this many (smoke test)')
    g.add_argument('--limit-jobs', type=int, default=None, help='only the first N jobs (smoke test)')
    a = sub.add_parser('assemble', help='CPU: build repaired rows')
    a.add_argument('--work-dir', type=Path, required=True)
    a.add_argument('--raw', type=Path, default=None)
    a.add_argument('--tokenizer', default=BASE_MODEL)
    a.add_argument('--revision', default=BASE_REVISION)
    a.add_argument('--max-model-len', type=int, default=18432)
    e = sub.add_parser('export', help='write repaired.jsonl')
    e.add_argument('--work-dir', type=Path, required=True)
    e.add_argument('--out', type=Path, required=True)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    return dict(plan=cmd_plan, requests=cmd_requests, run=cmd_run, assemble=cmd_assemble,
                export=cmd_export)[args.command](args)


if __name__ == '__main__':
    main()
