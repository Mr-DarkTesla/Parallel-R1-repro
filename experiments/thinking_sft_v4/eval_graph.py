"""Evaluate an SFT'd parallel-thinking checkpoint with the exact graph sampler (graph_sampler.py).

  python eval_graph.py --model CKPT --tasks math500_test.jsonl --gold math500_test_gold.jsonl \
      --mode both --backend vllm --out runs/eval_v4

Task rows: id (id/index/uid/unique_id/idx/task_id) + question/problem/prompt; gold rows: id + answer/oracle/gold/
final (a MATH solution is reduced to its last \\boxed{...}). Without --gold the answer is read from the task rows.
With --gold, rows are paired by id; pairing by row order happens only when neither file has an id in any row.
Grading matches the RL reward (parallel_think_cost.compute_score): the answer region is the text after the last
</think> outside every block; its last \\boxed{...} (math_dapo.last_boxed_only_string + remove_boxed, else the last
'Final Answer:' line) is compared with the gold by DAPO normalization, then math_verify when installed; a
trajectory that ended on a plan failure (invalid_plan, plan_incomplete, plan_budget_exhausted) is never correct
(`answer_correct` keeps the ungated comparison). trajectory_budget stays gradable (RL status 'ok').

Outputs in --out: report.json (per mode), samples_<mode>.jsonl, samples.md (10 samples per mode).
"""
import argparse
import importlib.util
import json
import re
import statistics
import time
from collections import Counter
from pathlib import Path

import graph_sampler as gs
from common import REPO, contract

QUESTION_KEYS = ('question', 'problem', 'prompt', 'input', 'query')
ANSWER_KEYS = ('answer', 'oracle', 'gold', 'final', 'final_answer', 'ground_truth', 'solution', 'target')
ID_KEYS = ('id', 'index', 'uid', 'unique_id', 'idx', 'task_id')
# Statuses the RL loop reports as trajectory_status != 'ok': the reward forces c = 0.
ENDED = (contract.INVALID_PLAN, contract.PLAN_INCOMPLETE, contract.PLAN_BUDGET_EXHAUSTED)

# ------------------------------------------------------------------------------------------------ grading


def _load_math_dapo():
    path = REPO / 'verl/verl/utils/reward_score/math_dapo.py'
    try:
        spec = importlib.util.spec_from_file_location('math_dapo_eval', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception:  # pragma: no cover - only without the repo file
        return None


MATH_DAPO = _load_math_dapo()
try:
    from math_verify import parse as mv_parse, verify as mv_verify
except ImportError:  # CPU container: string fallback
    mv_parse = mv_verify = None

SPECIAL = re.compile(r'<\|[^|]*\|>')
BLOCK = re.compile(r'<Parallel>.*?(</Parallel>|$)', re.S)


def reward_boxed(text):
    """As the RL reward: content of the last '\\boxed{' with matched braces (math_dapo.last_boxed_only_string +
    remove_boxed), or None. No \\fbox, no bare '\\boxed x'."""
    if MATH_DAPO is not None:
        boxed = MATH_DAPO.last_boxed_only_string(text)
        return None if boxed is None else MATH_DAPO.remove_boxed(boxed)
    start = text.rfind('\\boxed{')  # same algorithm, only without the repo file
    if start < 0:
        return None
    depth = 0
    for index in range(start, len(text)):
        depth += {'{': 1, '}': -1}.get(text[index], 0)
        if text[index] == '}' and depth == 0:
            return text[start + len('\\boxed{'):index]
    return None


def last_boxed(text):
    """Content of the last \\boxed{...} / \\fbox{...} in text, or None (reduces gold MATH solutions only; model
    predictions go through reward_boxed)."""
    if text is None:
        return None
    start = max(text.rfind('\\boxed'), text.rfind('\\fbox'))
    if start < 0:
        return None
    brace = text.find('{', start)
    if brace < 0:
        rest = text[start:].split('$')[0]
        return rest[len('\\boxed '):].strip() if rest.startswith('\\boxed ') else None
    depth = 0
    for index in range(brace, len(text)):
        depth += {'{': 1, '}': -1}.get(text[index], 0)
        if depth == 0:
            return text[brace + 1:index].strip()
    return None


def answer_region(text):
    """As parallel_think_cost.answer_region: text after the last </think> outside blocks, or None."""
    end = text.rfind('</think>')
    if end < 0:
        return None
    before = text[:end]
    if before.count('<Parallel>') != before.count('</Parallel>'):
        return None
    return BLOCK.sub('', SPECIAL.sub('', text[end + len('</think>'):]))


def extract_answer(region):
    """As parallel_think_cost.extract_answer."""
    if region is None:
        return None
    boxed = reward_boxed(region)
    if boxed is not None:
        return boxed
    match = re.findall(r'(?i)Final Answer\s*:\s*([^\n]+)', region)
    return match[-1] if match else None


def graded(result, pred, gold):
    """(correct, answer_correct): correct is the RL reward's c (0 after a plan failure)."""
    answer_correct = equivalent(pred, gold)
    return answer_correct and result['status'] not in ENDED, answer_correct


def normalize(answer):
    if MATH_DAPO is not None:
        try:
            return MATH_DAPO.normalize_final_answer(answer)
        except Exception:
            pass
    answer = re.sub(r'\\text\{(.*?)\}', r'\1', answer)
    answer = answer.replace('\\left', '').replace('\\right', '').replace('\\!', '').replace('$', '')
    answer = answer.replace('dfrac', 'frac').replace('tfrac', 'frac')
    return re.sub(r'\s+', '', answer).rstrip('.')


def equivalent(pred, gold):
    if pred is None or gold is None:
        return False
    if normalize(pred) == normalize(gold):
        return True
    if mv_verify is None:
        return False
    try:
        return bool(mv_verify(mv_parse(f'${gold}$', parsing_timeout=5), mv_parse(f'${pred}$', parsing_timeout=5),
                              timeout_seconds=5))
    except Exception:
        return False


# ------------------------------------------------------------------------------------------------ data

def read_jsonl(path):
    with open(path) as handle:
        return [json.loads(line) for line in handle if line.strip()]


def pick(row, keys):
    for key in keys:
        if key in row and row[key] not in (None, ''):
            return row[key]
    return None


def question_of(row):
    value = pick(row, QUESTION_KEYS)
    if isinstance(value, list):  # chat messages
        value = next((m['content'] for m in value if m.get('role') == 'user'), None)
    if isinstance(value, dict):
        value = pick(value, QUESTION_KEYS)
    if value is None:
        raise KeyError(f'no question in task row keys {sorted(row)}')
    return str(value)


def gold_of(row):
    value = pick(row, ANSWER_KEYS)
    if value is None and isinstance(row.get('reward_model'), dict):
        value = row['reward_model'].get('ground_truth')
    if isinstance(value, dict):
        value = pick(value, ANSWER_KEYS)
    if isinstance(value, (list, tuple)):
        value = value[0] if value else None
    if value is None:
        return None
    value = str(value)
    boxed = last_boxed(value)
    return boxed if boxed is not None else value.strip()


def explicit_id(row):
    value = pick(row, ID_KEYS)
    if value is None and isinstance(row.get('extra_info'), dict):
        value = row['extra_info'].get('index')
    return None if value is None else str(value)


def id_of(row, index):
    value = explicit_id(row)
    return value if value is not None else str(index)


def load_items(tasks_path, gold_path=None, limit=None):
    tasks = read_jsonl(tasks_path)
    golds = {}
    if gold_path:
        gold_rows = read_jsonl(gold_path)
        with_id = [sum(explicit_id(r) is not None for r in rows) for rows in (tasks, gold_rows)]
        if with_id == [0, 0]:
            print(f'eval_graph: neither {tasks_path} nor {gold_path} has an id key {ID_KEYS}: pairing golds by row '
                  f'order', flush=True)
            if len(tasks) != len(gold_rows):
                raise ValueError(f'{len(tasks)} task rows but {len(gold_rows)} gold rows (paired by order)')
        elif with_id != [len(tasks), len(gold_rows)]:
            raise ValueError(f'id keys {ID_KEYS} in {with_id[0]}/{len(tasks)} task rows and {with_id[1]}/'
                             f'{len(gold_rows)} gold rows: refusing to pair golds by row order')
        for index, row in enumerate(gold_rows):
            gold_id = id_of(row, index)
            if gold_id in golds:
                raise ValueError(f'duplicate gold id {gold_id} in {gold_path}')
            golds[gold_id] = gold_of(row)
    items = []
    for index, row in enumerate(tasks):
        task_id = id_of(row, index)
        gold = golds.get(task_id) if gold_path else gold_of(row)
        if gold_path and task_id not in golds:
            raise KeyError(f'task {task_id} has no gold row')
        items.append(dict(id=task_id, question=question_of(row), gold=gold))
    return items[:limit] if limit else items


# ------------------------------------------------------------------------------------------------ backends

class LazyHF:
    """HFBackend built on first use (sequential mode with vLLM never needs it)."""
    graph = True

    def __init__(self, factory):
        self.factory, self.backend = factory, None

    def generate(self, requests, sampling):
        if self.backend is None:
            self.backend = self.factory()
        return self.backend.generate(requests, sampling)


def hf_backend(args):
    import torch
    from transformers import AutoModelForCausalLM
    dtype = getattr(torch, args.dtype)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=dtype, attn_implementation='sdpa')
    model.to('cuda' if torch.cuda.is_available() else 'cpu')
    return gs.HFBackend(model, batch_tokens=args.hf_batch_tokens, max_batch=args.hf_max_batch)


def build_sampler(args, tokenizer):
    graph = LazyHF(lambda: hf_backend(args))
    if args.backend == 'vllm':
        causal = gs.VLLMBackend(args.model, gpu_memory_utilization=args.gpu_memory_utilization,
                                max_model_len=args.max_model_len, dtype=args.dtype, seed=args.seed)
    else:
        causal = graph
    sampling = gs.Sampling(args.temperature, args.top_p, args.top_k)
    return gs.GraphSampler(tokenizer, causal, graph, sampling=sampling, max_blocks=args.max_blocks,
                           budget=args.budget, branch_cap=args.branch_cap, plan_cap=args.plan_cap)


# ------------------------------------------------------------------------------------------------ metrics

def stats(values):
    if not values:
        return dict(n=0)
    ordered = sorted(values)
    return dict(n=len(values), mean=statistics.fmean(values), median=statistics.median(values),
                p90=ordered[min(len(ordered) - 1, int(0.9 * len(ordered)))], max=ordered[-1], min=ordered[0])


def summarize(rows):
    n = len(rows)
    if not n:
        return dict(n=0)
    blocks = [b for r in rows for b in r['blocks']]
    forked = [r for r in rows if r['forked']]
    branches = [p for b in blocks for p in b['branches']]
    T = [r['T'] for r in rows]
    D = [r['D'] for r in rows]
    report = dict(
        n=n,
        accuracy=sum(r['correct'] for r in rows) / n,
        answer_accuracy_ungated=sum(r.get('answer_correct', r['correct']) for r in rows) / n,
        fork_rate=len(forked) / n,
        blocks_per_sample=len(blocks) / n,
        valid_plan_rate=(sum(b['plan_status'] == contract.VALID for b in blocks) / len(blocks)) if blocks else None,
        plan_status=dict(Counter(b['plan_status'] for b in blocks)),
        N_histogram=dict(sorted(Counter(b['N'] for b in blocks if b['N'] is not None).items())),
        kind_histogram=dict(Counter(b['kind'] for b in blocks if b['kind'] is not None)),
        mean_T=statistics.fmean(T), mean_D=statistics.fmean(D),
        D_over_T=statistics.fmean(D) / max(statistics.fmean(T), 1e-9),
        mean_sample_D_over_T=statistics.fmean(d / t for d, t in zip(D, T) if t) if any(T) else None,
        branch_length=stats([p['sampled'] for p in branches]),
        branch_stop=dict(Counter(p['stop'] for p in branches)),
        summary_length=stats([b['summary_tokens'] for b in blocks if b['summary_tokens'] is not None]),
        summary_stop=dict(Counter(b['summary_stop'] for b in blocks if b['summary_stop'] is not None)),
        status=dict(Counter(r['status'] for r in rows)),
        truncation_rate=sum(r['truncated'] for r in rows) / n,
        no_answer_rate=sum(r['pred'] is None for r in rows) / n,
        accuracy_forked=(sum(r['correct'] for r in forked) / len(forked)) if forked else None,
        accuracy_not_forked=(sum(r['correct'] for r in rows if not r['forked']) / (n - len(forked)))
        if n > len(forked) else None,
        mean_T_correct=statistics.fmean([r['T'] for r in rows if r['correct']]) if any(r['correct'] for r in rows)
        else None,
    )
    return report


def markdown(mode, rows, count=10, width=6000):
    lines = [f'## {mode}: {count} samples\n']
    chosen = [r for r in rows if r['forked']][:count // 2] if mode == 'graph' else []
    chosen += [r for r in rows if r not in chosen][:count - len(chosen)]
    for row in chosen:
        text = row['text'] if len(row['text']) <= width else row['text'][:width // 2] + '\n[...]\n' + row['text'][
            -width // 2:]
        lines.append(f"### {row['id']} (status {row['status']}, correct {row['correct']}, T {row['T']}, D {row['D']}, "
                     f"blocks {[(b['N'], b['kind'], b['plan_status']) for b in row['blocks']]})\n")
        lines.append(f"**Q:** {row['question']}\n\n**gold:** `{row['gold']}`  **pred:** `{row['pred']}`\n")
        lines.append('```text\n' + text.replace('```', "'''") + '\n```\n')
    return '\n'.join(lines)


# ------------------------------------------------------------------------------------------------ main

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--model', required=True)
    parser.add_argument('--tasks', required=True)
    parser.add_argument('--gold')
    parser.add_argument('--prompt-template', default=gs.DEFAULT_TEMPLATE,
                        help='Python format string with {problem}')
    parser.add_argument('--mode', choices=('graph', 'sequential', 'both'), default='both')
    parser.add_argument('--backend', choices=('vllm', 'hf'), default='vllm')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--samples', type=int, default=1, help='samples per task')
    parser.add_argument('--out', required=True)
    parser.add_argument('--budget', type=int, default=16384, help='response tokens per trajectory, inserted ones included (= RL response_length)')
    parser.add_argument('--branch-cap', type=int, default=4096)
    parser.add_argument('--plan-cap', type=int, default=256)
    parser.add_argument('--max-blocks', type=int, default=1, choices=(0, 1, 2))
    parser.add_argument('--temperature', type=float, default=0.6)
    parser.add_argument('--top-p', type=float, default=0.95)
    parser.add_argument('--top-k', type=int, default=20)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--chunk', type=int, default=512, help='trajectories per sampler call')
    parser.add_argument('--dtype', default='bfloat16')
    parser.add_argument('--gpu-memory-utilization', type=float, default=0.45)
    parser.add_argument('--max-model-len', type=int, default=32768)
    parser.add_argument('--hf-batch-tokens', type=int, default=200_000,
                        help='HF graph stage: rows x (context + new tokens) per batch (KV memory bound)')
    parser.add_argument('--hf-max-batch', type=int, default=64)
    args = parser.parse_args(argv)

    from transformers import AutoTokenizer
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    items = load_items(args.tasks, args.gold, args.limit)
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    sampler = build_sampler(args, tokenizer)
    modes = ('graph', 'sequential') if args.mode == 'both' else (args.mode,)
    config = {k: v for k, v in vars(args).items()}
    config.update(contract_sha256=contract.SHA256, contract_revision=contract.CONTRACT_REVISION,
                  math_verify=mv_verify is not None)
    reports, docs = dict(config=config), []
    jobs = [(item, j) for item in items for j in range(args.samples)]
    for mode in modes:
        started = time.time()
        rows = []
        path = out / f'samples_{mode}.jsonl'
        with open(path, 'w') as handle:
            for begin in range(0, len(jobs), args.chunk):
                chunk = jobs[begin:begin + args.chunk]
                prompts = [args.prompt_template.format(problem=item['question']) for item, _ in chunk]
                seeds = [args.seed * 1_000_003 + (begin + k) for k in range(len(chunk))]
                results = sampler.generate(prompts, seeds=seeds, allow_parallel=mode == 'graph')
                for (item, j), result in zip(chunk, results):
                    pred = extract_answer(answer_region(result['text']))
                    correct, answer_correct = graded(result, pred, item['gold'])
                    row = dict(id=item['id'], sample=j, question=item['question'], gold=item['gold'], pred=pred,
                               correct=correct, answer_correct=answer_correct, **result)
                    row.pop('prompt_ids', None)
                    rows.append(row)
                    handle.write(json.dumps(row, ensure_ascii=False) + '\n')
                handle.flush()
                done = summarize(rows)
                print(f"[{mode}] {len(rows)}/{len(jobs)} acc {done['accuracy']:.3f} fork {done['fork_rate']:.3f} "
                      f"mean T {done['mean_T']:.0f} ({time.time() - started:.0f}s)", flush=True)
        reports[mode] = summarize(rows)
        reports[mode]['seconds'] = time.time() - started
        docs.append(markdown(mode, rows))
    (out / 'report.json').write_text(json.dumps(reports, indent=2, ensure_ascii=False))
    (out / 'samples.md').write_text(f'# eval_graph {args.model}\n\n' + '\n'.join(docs))
    print(json.dumps({m: reports[m] for m in modes}, indent=2, ensure_ascii=False))
    return reports


if __name__ == '__main__':
    main()
