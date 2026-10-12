"""GPU probe: parallel-thinking records with TWO sequential <Parallel> blocks, to show what multi-block traces look like.

    block 1 (plan + branches) -> summary 1 -> one more paragraph -> block 2 (plan + branches) -> summary 2 -> rest
    -> </think> -> final answer

    python multiblock_probe.py run --pool POOL --out OUT [--ids a,b,...]    # driver: CPU + one subprocess per model stage
    python multiblock_probe.py assemble --out OUT                           # CPU only (re-run after the stages)

Stages (state files in OUT; a finished stage is skipped on re-run, delete its file to redo it). Each model stage runs
in its own process holding ONE model, as Codex's raw_acquisition launcher does, so it fits one H100 NVL 94 GB:
  select   (CPU)      the pool row of each id (all.raw.jsonl + details.jsonl): question, prompt, the record's prefix
                      (its first paragraph) and its block 1. The pool block 1 is a reuse candidate only if every
                      provenance.branch_checks[].ok, plan_status == 'fork' and every branch has a Result line.
  plan1    (planner)  reuse candidates: a coverage audit (temperature 0, JSON {"evidence","covers"}): the pool block 1
                      is reused only if the plan covers the problem (e.g. every interval of a case split). Ids in
                      --force-regenerate (default: math-intermediate_algebra-train-1130, whose pool plan misses the
                      interval (2, oo)) and every other id get a new block-1 plan the standard way: Codex's
                      gen.stage_plan request (gen.PLANNER_SYS + raw_acquisition's appended rules, question + prefix,
                      TEACHER_SAMPLING, 1024 tokens, one retry with the validation error), gold-in-plan rejected;
                      up to --plan1-attempts seeds until a FORK.
  student1 (student)  new block-1 branches (Codex's raw_work request: the planner's standalone mini-problem
                      gen.executor_prompt_e, else executor_prompt_d; Countdown suffix; thinking mode; n=--branch-samples;
                      gen.check_branch; passing samples, oracle/valid first, then shortest). Merger 1: non-thinking,
                      Results only (fast_repair.merger_context: the question + plan items + Result lines) with
                      BLOCK_SUMMARY_NOTE[1] (state each Result, combine explicitly step by step, intermediate step, no
                      Final Answer / \\boxed / markup), n=--merger-samples, <= 1024 tokens; accepted if finished,
                      plain text, no final-answer marker; within the 0.5x-longest-branch rule first, then shortest.
                      Continuation: the 4B in thinking mode continues the CAUSAL serialized text
                      '<think>\\n' + prefix + block 1 + '\\n\\n' (tags as plain text; graph positions are not used at
                      generation, recorded as provenance.context) for one paragraph: stop at '\\n\\n' or '</think>',
                      <= 400 tokens.
  plan2    (planner)  a possible SECOND block: the same planner request with SECOND_BLOCK_NOTE appended to the system
                      prompt (must not redo block-1 work), the user message = question + everything so far as plain
                      text (prefix, block-1 plan items with their Result lines, summary 1, the continuation paragraph;
                      never branch bodies, never gold). FORK (2-4 standalone mini-problems) or NO_FORK, same JSON schema
                      and validation as block 1. NO_FORK is final (not resampled); invalid / gold-in-plan get one more
                      seed, then count as no fork.
  student2 (student)  FORK: block-2 branches as in student1 (in-context fallback prompt gets the plain context), merger 2
                      as merger 1 (BLOCK_SUMMARY_NOTE[2]), then the 4B in thinking mode continues the causal text through
                      </Summary> of block 2: the rest of the reasoning + </think> + the answer (<= 4096 tokens).
                      NO_FORK (or a failed block 2): the 4B continues after the paragraph to the answer (single-block
                      record, kept for comparison; the reason is recorded). n=--final-samples, a finished, plain,
                      correct sample first (Codex's scorer; every sample's verdict is recorded).
  assemble (CPU)      contract segments (block ids 1 and 2; runtime-inserted 'branches=', '<Plan>', '<Path>', 'i:',
                      '</Parallel>', '<Summary>' loss=false, everything else loss=true, exactly as block 1 of the raw
                      records), sft_data.validate_row, Codex's final_grade, and OUT/records.jsonl, OUT/traces/<id>.md
                      (runtime-inserted pieces as [[...]]), OUT/traces.md (index), OUT/stats.json (per id: block-2
                      FORK/NO_FORK, correctness, lengths, critical path vs total tokens; gold-in-prompt audit of every
                      call in OUT/calls.jsonl).

Budget: the whole assistant text stays <= 16,384 generator tokens (Codex's shared budget). Block-1 branch cap =
(16,384 - overhead - --block1-reserve) / N; block-2 cap = (16,384 - text so far - block-2 overhead - --final-reserve)
/ N; the final call gets min(4096, what is left). Gold is used only by the checks and the scorer, never in a prompt.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import codex_rules as C  # noqa: E402
import fast_repair as F  # noqa: E402
import sft_data as D  # noqa: E402
from common import BASE_MODEL, BASE_REVISION, contract  # noqa: E402

REVISION = 'multiblock-probe-20261012-v1'
STUDENT = (BASE_MODEL, BASE_REVISION)
PLANNER = ('Qwen/Qwen3-30B-A3B-Instruct-2507', '0d7cf23991f47feeb3a57ecb4c9cee8ea4a17bfe')  # Codex's gen.TEACHER
TOTAL = C.MAX_TOTAL_TOKENS
STAGES = ('plan1', 'student1', 'plan2', 'student2')
MODEL_OF = dict(plan1='planner', student1='student', plan2='planner', student2='student')

# Pool ids where a second block is plausible: plan kind cases/candidates and a question that asks "how many" /
# "(sum of) all possible values" (Countdown: every pool branch reported "no expression", so a second search block is
# plausible). The note is metadata for the output only; it never reaches a prompt.
DEFAULT_IDS = {
    'math-intermediate_algebra-train-1130': 'cases; how many integers in [-11, 11] make (n-2)(n+4)(n+8) negative: '
                                            'signs on the 4 intervals, then integers per negative interval '
                                            '(pool plan misses (2, oo): block 1 regenerated)',
    'math-intermediate_algebra-train-1027': 'cases; how many positive integers make a cubic negative (1130 shape)',
    'math-intermediate_algebra-train-528': 'cases; how many real x solve |x-1| = |x-2| + |x-3|: per interval, then count',
    'math-intermediate_algebra-train-786': 'cases; sum of all possible values of |a-d|: sign cases, then the sum',
    'math-intermediate_algebra-train-459': 'cases; all possible values of a sign expression: sign cases, then collect',
    'math-precalculus-train-160': 'cases; sum of all possible values of BC (ambiguous SSA): triangles, then the sum',
    'math-intermediate_algebra-train-25': 'cases; how many 24th roots of unity have z^6 real: residues, then count',
    'math-geometry-train-721': 'cases; how many integer triangles of perimeter 7: cases, then count',
    'math-intermediate_algebra-train-723': 'cases; all possible r (area between 8 and 64): inequalities, then combine',
    'math-intermediate_algebra-train-1061': 'candidates; all possible values of f(100): substitutions, then values',
    'math-geometry-train-779': 'candidates; how many inches (smallest cut): candidate cuts, then more candidates',
    'countdown-8f39ef562102f8e2': 'countdown candidates; every pool branch found no expression: second search block',
}
FORCE_REGENERATE = ('math-intermediate_algebra-train-1130',)
DEFAULTS = dict(branch_samples=2, merger_samples=4, final_samples=2, continuation_samples=2, summary_max_tokens=1024,
                continuation_max_tokens=400, final_max_tokens=4096, block1_reserve=6144, final_reserve=2560,
                plan1_attempts=3, plan2_attempts=2, summary_ratio=0.5, min_branch_tokens=256)

# -------------------- verbatim from codex-code/gen.py (sha256 23c8e6ebb25f4929...): TEACHER_SAMPLING, PLANNER_SYS, parse_json_obj, plan_text, validate_plan

TEACHER_SAMPLING = dict(temperature=0.7, top_p=0.8, top_k=20)

PLANNER_SYS = """You plan one parallel step inside a student's step-by-step reasoning. You see a problem and the student's reasoning so far (an early prefix). Decide whether the REMAINING work should fork into 2-4 parallel branches. Each branch is executed independently by a small model that sees the problem, the reasoning so far and its own one-line assignment, but never the other branches. Afterwards a separate summary step (not you, not a branch) reads all branch results, combines them and finishes the problem.

Output ONLY one JSON object, no prose and no code fences:
{"analysis": "<2-4 sentences: which pieces of remaining work exist and whether each can be done from the problem text alone>", "decision": "FORK", "branches": N, "kind": "<kind>", "assignments": ["<task 1>", ..., "<task N>"], "subproblems": ["<mini-problem 1>", ..., "<mini-problem N>"]}
or
{"analysis": "<2-4 sentences>", "decision": "NO_FORK"}

Kinds:
- decompose: the remaining work splits into independent sub-computations (e.g. one branch per item, person, part or quantity). Each branch computes only its own part.
- cases: a case split; each branch analyzes exactly one case.
- candidates: each branch explores a different candidate direction. For puzzles that ask to find an expression or a configuration, give each branch a different search direction (e.g. which operation or which pair of numbers to try first), never a complete expression or a specific candidate answer.
- methods: each branch solves the whole problem with a genuinely different complete approach, so the summary can cross-check. Consecutive steps of one approach are NOT methods.
- verify: each branch checks a different condition or constraint.

Rules:
1. N is 2, 3 or 4, and "assignments" has exactly N entries.
2. INDEPENDENCE TEST: every assignment must be doable from the problem text and the reasoning so far alone. If an assignment needs a quantity that another assignment computes (e.g. "find the third plant's yield" when the third plant is defined through the second), the plan fails the test: choose NO_FORK.
3. NO COMBINE STEP: never an assignment like "compute the total", "add up", "combine", "compare the results" or "find the final answer". The summary does that.
4. Each assignment is ONE line: an imperative task such as "Compute Workshop 2's net profit." It names its inputs from the problem text. Never state computed values, candidate answers, intermediate results or the answer, and do not introduce numbers that are not in the problem or the reasoning so far.
5. Assignments are distinct and each is real work (not restating the problem, not a trivial lookup).
6. "subproblems" has one entry per assignment: a self-contained mini-problem that a solver can do WITHOUT seeing the original problem. Copy only the facts and numbers that assignment needs, word for word from the problem text, and end with the question that assignment answers. Never include computed values or the answer.
7. Fork only when there are at least two genuinely independent pieces of work or real alternative methods or cases. Choose NO_FORK when the problem is short or trivial, when the remaining work is a single chain where each step needs the previous one, or when there are no real independent parts or alternatives. Many short word problems are a single chain; NO_FORK is the right answer for them.
8. For Countdown candidates, make the first binary operation explicit in each assignment: "Try multiplying X and Y first", "Try adding X and Y first", or "Try subtracting X from Y first". Use two available input-number occurrences. Do not give a completed expression.

Example 1. Problem: "A shop sells 3 shirts at $12 each, 2 hats at $8 each and 5 pairs of socks at $3 each, and pays $10 rent. What is its profit?"
{"analysis": "The revenue of each product line uses only problem data and none needs another; adding them and subtracting rent is the summary's job.", "decision": "FORK", "branches": 3, "kind": "decompose", "assignments": ["Compute the revenue from the shirts.", "Compute the revenue from the hats.", "Compute the revenue from the socks."], "subproblems": ["A shop sells 3 shirts at $12 each. What is the revenue from the shirts?", "A shop sells 2 hats at $8 each. What is the revenue from the hats?", "A shop sells 5 pairs of socks at $3 each. What is the revenue from the socks?"]}

Example 2. Problem: "Tom has 5 apples. He buys twice as many as he has, then gives away 4. How many does he have now?"
{"analysis": "Each step needs the previous result, so there is no independent work.", "decision": "NO_FORK"}

Example 3. Problem: "A tank holds 120 liters. Each bucket carries 8 liters and Ann pours one bucket every 2 minutes. How many minutes does it take to fill the tank?"
{"analysis": "Number of buckets, then time per bucket times buckets: a 3-step chain where each step uses the previous result. Splitting it into 'count buckets' and 'compute time' would make the second branch depend on the first.", "decision": "NO_FORK"}

Example 4. Problem: "Using 3, 7, 8 and 25 each exactly once with +, - and *, make 208."
{"analysis": "The search can be split by which pair is multiplied first; each direction is independent.", "decision": "FORK", "branches": 3, "kind": "candidates", "assignments": ["Try multiplying 8 and 25 first, then combine with 3 and 7.", "Try multiplying 7 and 25 first, then combine with 3 and 8.", "Try multiplying 3 and 7 first, then combine with 8 and 25."], "subproblems": ["Using 3, 7, 8 and 25 each exactly once with +, - and *, make 208. You must start by multiplying 8 and 25. Report the expression, or say that no expression works this way.", "Using 3, 7, 8 and 25 each exactly once with +, - and *, make 208. You must start by multiplying 7 and 25. Report the expression, or say that no expression works this way.", "Using 3, 7, 8 and 25 each exactly once with +, - and *, make 208. You must start by multiplying 3 and 7. Report the expression, or say that no expression works this way."]}"""

def parse_json_obj(text):
    t = text.strip()
    t = re.sub(r'^```(?:json)?\s*', '', t)
    t = re.sub(r'\s*```$', '', t)
    start, end = t.find('{'), t.rfind('}')
    if start < 0 or end < start:
        raise ValueError('no JSON object found')
    return json.loads(t[start:end + 1])

def plan_text(kind, items):
    return kind + '\n' + ''.join(f'{i}: {item}\n' for i, item in enumerate(items, 1))

def validate_plan(raw):
    """('no_fork'|'fork', plan dict) or raises ValueError with a message fit for feedback."""
    try:
        obj = parse_json_obj(raw)
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError(f'not a valid JSON object ({e})')
    decision = obj.get('decision')
    if decision == 'NO_FORK':
        return 'no_fork', None
    if decision != 'FORK':
        raise ValueError('"decision" must be "FORK" or "NO_FORK"')
    n, kind, items = obj.get('branches'), obj.get('kind'), obj.get('assignments')
    if not isinstance(n, int) or not contract.MIN_PATHS <= n <= contract.MAX_PATHS:
        raise ValueError('"branches" must be the integer 2, 3 or 4')
    if kind not in contract.PLAN_KINDS:
        raise ValueError(f'"kind" must be one of {", ".join(contract.PLAN_KINDS)}')
    if not isinstance(items, list) or not all(isinstance(x, str) for x in items):
        raise ValueError('"assignments" must be a list of strings')
    if len(items) != n:
        raise ValueError(f'"assignments" has {len(items)} entries but "branches" is {n}')
    items = [x.strip() for x in items]
    if any('\n' in x or not x for x in items):
        raise ValueError('each assignment must be one non-empty line')
    text = plan_text(kind, items)
    parsed = contract.parse_plan(text, n)
    if parsed is None or list(parsed.items) != items:
        raise ValueError('assignments must be distinct one-line plain text without tags')
    subs = obj.get('subproblems')
    if not (isinstance(subs, list) and len(subs) == n and all(isinstance(x, str) and x.strip() for x in subs)):
        subs = None  # optional: without it the branch uses the in-context executor prompt only
    return 'fork', {'branches': n, 'kind': kind, 'items': items, 'plan_text': text,
                    'subproblems': [x.strip() for x in subs] if subs else None}


# -------------------- verbatim string from codex-code/raw_acquisition.py raw_plan (appended to gen.PLANNER_SYS there)

RAW_PLANNER_RULES = ('\nDo not split a trivial calculation into multiple workers. '
                     'A decompose branch must never compute the overall answer while another computes its part. '
                     'For Countdown, changing multiplication order alone is not a distinct strategy. '
                     'In every Countdown mini-problem say any subset of the allowed operations may be used; '
                     'it is NOT required to use every operation. Never introduce division or extra numbers.')

# -------------------- this probe's own prompts

PLANNER_SYSTEM_1 = PLANNER_SYS + RAW_PLANNER_RULES
SECOND_BLOCK_NOTE = (
    '\nThis call plans a possible SECOND parallel step. The reasoning so far already contains a first parallel step '
    '(its plan, the Result of each of its branches and its summary) and the paragraph the student wrote after it. '
    'Do not redo, repeat, re-check or extend the work of the first step: its Results are established. Plan only work '
    'that remains after the last paragraph. Choose FORK only if that remaining work has at least two genuinely '
    'independent pieces; otherwise choose NO_FORK. Facts the first step established are part of the reasoning so '
    'far: an assignment or mini-problem may state the ones it needs, copied as they are written there, but never a '
    'value that this step or the final answer still has to compute.')
PLANNER_SYSTEM_2 = PLANNER_SYSTEM_1 + SECOND_BLOCK_NOTE
COVERAGE_SYS = (
    "You review a parallel plan made inside a student's reasoning. You see a problem, the student's reasoning so far, "
    'the plan kind and its assignments; each assignment is done by an independent worker and a summary step combines '
    'their results. Decide whether the assignments together cover ALL the work this kind of split implies, so that '
    'combining the workers\' results needs no further case, interval, item or part: for cases, every case or interval '
    'the question needs has its own assignment (an interval or case left out means false); for decompose, every '
    'needed part is assigned; for candidates, methods or verify, the assignments are distinct and each is relevant '
    '(a candidate search need not be exhaustive). Do not solve the problem and do not judge formatting.\n'
    'Output ONLY one JSON object: {"evidence": "<1-3 sentences>", "covers": true or false}. Answer false when in '
    'doubt.')
_SUMMARY_RULES = (  # the rules of fast_repair's v2 Results-only summary prompt
    'Do not re-derive, recompute or re-check any Result from the original data, and do not restate how the tasks '
    'were solved. If a Result is missing or the Results conflict, say so instead of solving that task yourself. Write '
    'brief plain prose in the first person, as part of your own reasoning. Do not write a final response, a '
    '"Final Answer" line, \\boxed{}, or any markup.')
BLOCK_SUMMARY_NOTE = {
    1: ('\n\nThe Results above are verified and final. Write the summary step of the reasoning that follows these '
        'independent tasks. First state each Result you use, one short sentence each. Then combine them explicitly, '
        'one step at a time, writing every intermediate value, into what they establish together for the problem. '
        'This is an intermediate step: the reasoning continues after it, so do not finish the problem and do not do '
        'any work beyond combining these Results. ' + _SUMMARY_RULES),
    2: ('\n\nThe Results above are verified and final. Write the summary step of the reasoning that follows these '
        'independent tasks. First state each Result you use, one short sentence each. Then carry out the remaining '
        'combination explicitly, one operation per step, writing every intermediate value, as far as these Results '
        'allow. End with one sentence that states what the combination gives. ' + _SUMMARY_RULES),
}
FINAL_MARKER = re.compile(r'Final Answer|\\boxed|\\fbox|(?i:final\s+answer\s*:)')
SENTENCE_END = re.compile(r'[.!?](?=\s|$)')


# ------------------------------------------------------------------------------------------------ small helpers

def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def write_jsonl(path, rows):
    return F.write_jsonl(path, rows)


def write_json(path, obj):
    F.write_json(path, obj)


def chat(tok, messages, thinking):
    return tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=thinking)


def ntok(tok, text):
    return len(tok.encode(text, add_special_tokens=False))


def seed(*parts):
    return C.seed_of(REVISION, *parts)


def has_final_marker(text):
    return bool(FINAL_MARKER.search(text or ''))


class Recorder:
    """Appends every generation call (prompt, params, outputs) to OUT/calls.jsonl; `audit` scans them for gold."""

    def __init__(self, out, stage, backend):
        self.path, self.stage, self.backend = Path(out) / 'calls.jsonl', stage, backend

    def __call__(self, requests):
        if not requests:
            return []
        t0 = time.time()
        outputs = self.backend.generate(requests)
        seconds = round(time.time() - t0, 1)
        with self.path.open('a', encoding='utf-8') as handle:
            for req, outs in zip(requests, outputs):
                handle.write(json.dumps(dict(stage=self.stage, key=req['key'], model=self.backend.which,
                                             prompt=req['prompt'], prompt_sha256=sha256_text(req['prompt']),
                                             params=req['params'], outputs=outs, batch_seconds=seconds),
                                        ensure_ascii=False) + '\n')
        return outputs


class Engine:
    """vLLM 0.8.5 offline engine built like Codex's gen.Engine (bf16, engine seed 0, prefix caching, Codex's exact
    top-k/top-p sampler patch); one per stage process."""

    def __init__(self, which, max_model_len, gpu_memory_utilization, max_num_seqs, fast_sampler=True):
        if fast_sampler:
            os.environ.setdefault('VLLM_ENABLE_V1_MULTIPROCESSING', '0')
            C.patch_sampler()
        import vllm
        from vllm import LLM
        repo, rev = STUDENT if which == 'student' else PLANNER
        self.which, self.repo, self.rev, self.version = which, repo, rev, vllm.__version__
        self.llm = LLM(model=repo, revision=rev, tokenizer_revision=rev, dtype='bfloat16', max_model_len=max_model_len,
                       gpu_memory_utilization=gpu_memory_utilization, seed=0, enable_prefix_caching=True,
                       max_num_seqs=max_num_seqs)
        self.tok = self.llm.get_tokenizer()

    def generate(self, requests):
        from vllm import SamplingParams
        results = self.llm.generate([r['prompt'] for r in requests], [SamplingParams(**r['params']) for r in requests],
                                    use_tqdm=True)
        return [[dict(text=o.text, finish_reason=o.finish_reason, n_tokens=len(o.token_ids),
                      stop_reason=o.stop_reason if isinstance(o.stop_reason, (str, int)) else None)
                 for o in r.outputs] for r in results]


# ------------------------------------------------------------------------------------------------- state

def load_state(out):
    """{id: merged dict} from items.jsonl and every finished stage file, in stage order."""
    state = {row['id']: row for row in read_jsonl(Path(out) / 'items.jsonl')}
    for stage in STAGES:
        for row in read_jsonl(Path(out) / f'{stage}.jsonl'):
            state[row['id']].update(row)
    return state


def active(state):
    return [item for item in state.values() if item.get('status', 'ok') == 'ok']


def block_text(plan, bodies, summary):
    return contract.format_block(plan['kind'], plan['items'], bodies, summary)


def causal_text(item, upto):
    """The serialized assistant text the student continues (tags as plain text): through block 1 + '\\n\\n'
    ('continuation'), through the paragraph ('no_fork') or through block 2's </Summary> ('block2')."""
    b1 = item['block1']
    text = item['prefix'] + block_text(b1['plan'], b1['bodies'], item['summary1']['text'])
    if upto == 'continuation':
        return text + '\n\n'
    text += main_text(item)
    if upto == 'no_fork':
        return text
    b2 = item['block2']
    return text + block_text(b2['plan'], b2['bodies'], item['summary2']['text'])


def main_text(item):
    return '\n\n' + item['continuation']['text'] + '\n\n'


def generation_prompt(tok, item, upto):
    """Chat template (thinking) + '<think>\\n' + the causal text: what the student continues."""
    return chat(tok, [{'role': 'user', 'content': item['prompt']}], True) + '<think>\n' + causal_text(item, upto)


def plain_context(item):
    """Everything so far as plain text (planner 2 and the block-2 in-context branch prompt): prefix, block-1 plan items
    with their Result lines, summary 1, the continuation paragraph. No branch bodies, no tags."""
    b1 = item['block1']
    lines = [item['prefix'].strip(), '',
             f'First parallel step ({b1["plan"]["kind"]}), independent tasks and their Results:']
    for number, (task, result) in enumerate(zip(b1['plan']['items'], b1['results']), 1):
        lines += [f'{number}. {task}', f'   {result}']
    lines += ['', 'Summary of the first parallel step:', item['summary1']['text'].strip(), '',
              item['continuation']['text'].strip()]
    return '\n'.join(lines)


def planner_messages(item, block):
    if block == 1:
        reasoning, system = item['prefix'].strip(), PLANNER_SYSTEM_1
    else:
        reasoning, system = plain_context(item), PLANNER_SYSTEM_2
    return [{'role': 'system', 'content': system},
            {'role': 'user', 'content': f"Problem:\n{item['question']}\n\nReasoning so far:\n{reasoning}\n\n"
                                        f"Return the JSON object."}]


def plan_leak_status(q, plan, available_text):
    """gen.stage_plan's checks on a validated FORK plan (gold only checked, never shown): 'fork' or a reject reason;
    plus the mini-problem diagnostics stage_plan records."""
    items = '\n'.join(plan['items'])
    leak = C.contains_answer(items, q['task'], q['gold'])
    exempt = C.answer_in_question(q['task'], q['gold'])
    info = dict(novel_numbers=sorted(C.numbers_in(items) - C.numbers_in(available_text)))
    status = 'gold_in_plan' if leak and not exempt else 'fork'
    if plan.get('subproblems'):
        subs = '\n'.join(plan['subproblems'])
        sub_leak = C.contains_answer(subs, q['task'], q['gold']) and not exempt
        info.update(subproblem_novel_numbers=sorted(C.numbers_in(subs) - C.numbers_in(q['task']['question'])),
                    subproblems_plain=all(contract.plain_text(s) for s in plan['subproblems']))
        if sub_leak and status == 'fork':
            status = 'gold_in_subproblems'
    return status, info


# ------------------------------------------------------------------------------------------------- select (CPU)

def first_paragraph(text):
    head, sep, _ = text.partition('\n\n')
    return head.strip() + '\n\n' if sep and head.strip() else None


def select(pool, out, ids, force_regenerate, cfg):
    """OUT/items.jsonl + OUT/config.json from the pool (read only)."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    want = {f'{task_id}#raw': task_id for task_id in ids}
    rows, details = {}, {}
    for _, row in F.raw_lines(Path(pool) / 'all.raw.jsonl'):
        if row['id'] in want:
            rows[row['id']] = row
    for _, detail in F.raw_lines(Path(pool) / 'details.jsonl'):
        if detail['id'] in want:
            details[detail['id']] = detail
    missing = sorted(i for i in want if i not in rows or i not in details)
    if missing:
        raise SystemExit(f'not in the pool: {missing}')
    items = []
    for raw_id, task_id in want.items():
        row, detail = rows[raw_id], details[raw_id]
        q = F.build_q(row, detail)
        pool_block, reasons = None, []
        if row['mode'] == 'parallel':
            parsed = F.parse_parallel(row)
            prefix = parsed['prefix']
            checks = row['provenance'].get('branch_checks') or []
            results = [F.result_line_of(body) for body in parsed['bodies']]
            if not checks or not all(c.get('ok') for c in checks):
                reasons.append('pool_branch_checks_failed:' + ','.join(c['reason'] for c in checks if not c.get('ok')))
            if row['provenance'].get('plan_status') != 'fork':
                reasons.append(f'pool_plan_status:{row["provenance"].get("plan_status")}')
            if any(r is None for r in results):
                reasons.append('pool_branch_without_result_line')
            pool_block = dict(plan=parsed['plan'], bodies=parsed['bodies'], results=results,
                              branch_checks=checks)
        else:
            body = ''.join(s['text'] for s in row['segments'][1:] if s['text'] not in D.SPECIALS)
            prefix = first_paragraph(body)
            reasons.append('pool_sequential')
        if not prefix or not contract.plain_text(prefix):
            raise SystemExit(f'{task_id}: no usable prefix')
        forced = task_id in force_regenerate
        if forced:
            reasons.append('forced_regenerate')
        items.append(dict(id=task_id, raw_id=raw_id, source=row['source'], question=row['question'],
                          prompt=row['prompt'], q=q, prefix=prefix, pool_block=pool_block,
                          reuse_candidate=pool_block is not None and not reasons, pool_reject=reasons,
                          selection_note=DEFAULT_IDS.get(task_id, 'user-supplied id'),
                          pool_n_tokens=row['provenance'].get('n_tokens'), pool_correct=detail.get('correct'),
                          status='ok'))
    write_jsonl(out / 'items.jsonl', items)
    config = dict(revision=REVISION, pool=str(pool), ids=list(ids), force_regenerate=list(force_regenerate),
                  selection_notes={i: DEFAULT_IDS.get(i, 'user-supplied id') for i in ids}, cfg=cfg,
                  student=list(STUDENT), planner=list(PLANNER), total_tokens=TOTAL,
                  context='causal: the student continues the serialized text (prefix + plan + branches + summary, '
                          'tags as plain text); graph positions/masks are not used at generation')
    write_json(out / 'config.json', config)
    print(json.dumps(dict(selected=[i['id'] for i in items],
                          reuse_candidates=[i['id'] for i in items if i['reuse_candidate']]), indent=1))
    return items


# ------------------------------------------------------------------------------------------------- planner stages

def planner_rounds(gen, tok, items, block, attempts, q_of, available_of, stop_on_no_fork):
    """Codex's stage_plan per round (first call, one retry with the validation error); further rounds (new seeds) for
    ids without an accepted plan. Returns {id: dict(decision, plan, status, attempts)}."""
    done, log = {}, {item['id']: [] for item in items}
    pending = list(items)
    for attempt in range(attempts):
        if not pending:
            break
        first = {item['id']: planner_messages(item, block) for item in pending}
        reqs = [dict(key=f'plan{block}|{item["id"]}|a{attempt}', prompt=chat(tok, first[item['id']], False),
                     params=dict(n=1, max_tokens=1024, seed=seed('plan', block, item['id'], attempt, 0),
                                 **TEACHER_SAMPLING)) for item in pending]
        outs = gen(reqs)
        raws = {item['id']: o[0] for item, o in zip(pending, outs)}
        retry = []
        for item in pending:
            try:
                validate_plan(raws[item['id']]['text'])
            except ValueError as error:
                messages = first[item['id']] + [
                    {'role': 'assistant', 'content': raws[item['id']]['text']},
                    {'role': 'user', 'content': f'Your reply was invalid: {error}. Reply again with only the '
                                                f'corrected JSON object, following all rules.'}]
                retry.append((item, messages))
        retry_outs = gen([dict(key=f'plan{block}|{item["id"]}|a{attempt}r', prompt=chat(tok, m, False),
                               params=dict(n=1, max_tokens=1024, seed=seed('plan', block, item['id'], attempt, 1),
                                           **TEACHER_SAMPLING)) for item, m in retry])
        final = dict(raws)
        for (item, _), o in zip(retry, retry_outs):
            final[item['id']] = o[0]
        still = []
        for item in pending:
            raw = final[item['id']]
            entry = dict(attempt=attempt, retried=any(i['id'] == item['id'] for i, _ in retry), raw=raw['text'],
                         finish_reason=raw['finish_reason'])
            try:
                decision, plan = validate_plan(raw['text'])
            except ValueError as error:
                entry.update(status='invalid_plan', error=str(error))
                log[item['id']].append(entry)
                still.append(item)
                continue
            if decision == 'no_fork':
                entry['status'] = 'no_fork'
                log[item['id']].append(entry)
                if stop_on_no_fork:
                    done[item['id']] = dict(decision='NO_FORK', plan=None, status='no_fork')
                else:
                    still.append(item)
                continue
            status, info = plan_leak_status(q_of(item), plan, available_of(item))
            entry.update(status=status, **info)
            log[item['id']].append(entry)
            if status == 'fork':
                done[item['id']] = dict(decision='FORK', plan=plan, status='fork', **info)
            else:
                still.append(item)
        pending = still
    for item in pending:
        last = log[item['id']][-1]['status'] if log[item['id']] else 'not_run'
        done[item['id']] = dict(decision='NO_FORK', plan=None, status=f'no_plan:{last}')
    for task_id in done:
        done[task_id]['attempts'] = log[task_id]
    return done


def stage_plan1(out, backend, cfg):
    state = load_state(out)
    gen, tok = Recorder(out, 'plan1', backend), backend.tok
    items = active(state)
    candidates = [item for item in items if item['reuse_candidate']]
    audits = gen([dict(key=f'coverage|{item["id"]}', prompt=chat(tok, [
        {'role': 'system', 'content': COVERAGE_SYS},
        {'role': 'user', 'content': json.dumps(dict(problem=item['question'], reasoning_so_far=item['prefix'].strip(),
                                                    kind=item['pool_block']['plan']['kind'],
                                                    assignments=item['pool_block']['plan']['items']),
                                               ensure_ascii=False)}], False),
        params=dict(n=1, max_tokens=768, temperature=0.0)) for item in candidates])
    rows, regenerate = {}, []
    for item, outs in zip(candidates, audits):
        try:
            verdict = parse_json_obj(outs[0]['text'])
        except (ValueError, json.JSONDecodeError):
            verdict = None
        covers = isinstance(verdict, dict) and verdict.get('covers') is True
        rows[item['id']] = dict(id=item['id'], coverage=dict(verdict=verdict, raw=outs[0]['text'], covers=covers))
        if covers:
            rows[item['id']].update(block1_source='pool', plan1=item['pool_block']['plan'], plan1_status='pool_reused')
        else:
            regenerate.append(item)
    regenerate += [item for item in items if not item['reuse_candidate']]
    planned = planner_rounds(gen, tok, regenerate, 1, cfg['plan1_attempts'], lambda item: item['q'],
                             lambda item: item['question'] + '\n' + item['prefix'], stop_on_no_fork=False)
    for item in regenerate:
        result = planned[item['id']]
        row = rows.setdefault(item['id'], dict(id=item['id'], coverage=None))
        row.update(block1_source='regenerated', plan1=result['plan'], plan1_status=result['status'],
                   plan1_attempts=result['attempts'])
        if result['decision'] != 'FORK':
            row['status'] = 'no_block1_plan'
    write_jsonl(Path(out) / 'plan1.jsonl', [rows[item['id']] for item in items])
    return rows


def stage_plan2(out, backend, cfg):
    state = load_state(out)
    gen, tok = Recorder(out, 'plan2', backend), backend.tok
    items = active(state)
    planned = planner_rounds(gen, tok, items, 2, cfg['plan2_attempts'], lambda item: item['q'],
                             lambda item: item['question'] + '\n' + plain_context(item), stop_on_no_fork=True)
    rows = []
    for item in items:
        result = planned[item['id']]
        rows.append(dict(id=item['id'], plan2=dict(decision=result['decision'], plan=result['plan'],
                                                   status=result['status'], attempts=result['attempts']),
                         planner2_user=planner_messages(item, 2)[1]['content']))
    write_jsonl(Path(out) / 'plan2.jsonl', rows)
    return rows


# ------------------------------------------------------------------------------------------------- student stages

def branch_request_text(item, plan, i, context):
    q = item['q']
    text = C.executor_prompt_e(plan, i) if plan.get('subproblems') else C.executor_prompt_d(q, context, plan, i)
    if q['src'] == 'countdown' and 'ANY SUBSET' not in text:
        text += C.COUNTDOWN_BRANCH_SUFFIX
    return text


def run_branches(gen, tok, jobs, cfg):
    """jobs: [(item, block, plan, context, cap)] -> {id: dict(bodies, results, samples, status)} with Codex's
    check_branch and gen.stage_branch's choice (oracle/valid first, then shortest; Countdown expressions distinct)."""
    reqs, meta = [], []
    for item, block, plan, context, cap in jobs:
        for i in range(plan['branches']):
            text = branch_request_text(item, plan, i, context)
            reqs.append(dict(key=f'branch{block}|{item["id"]}|{i + 1}', prompt=chat(tok, [{'role': 'user',
                                                                                          'content': text}], True),
                             params=dict(n=cfg['branch_samples'], max_tokens=cap,
                                         seed=seed('branch', block, item['id'], i), **C.STUDENT_SAMPLING)))
            meta.append((item, plan, i, text, cap))
    outs = gen(reqs)
    found = {}
    for (item, plan, i, text, cap), samples in zip(meta, outs):
        entry = found.setdefault(item['id'], dict(bodies=[None] * plan['branches'], results=[None] * plan['branches'],
                                                  samples={}, requests={}, caps=cap, status='ok', used=set()))
        checked = []
        for k, o in enumerate(samples):
            ok, reason, body, line = C.check_branch(item['q'], plan, i, o)
            checked.append(dict(k=k, ok=ok, reason=reason, body=body, line=line, n_tokens=o['n_tokens'],
                                finish_reason=o['finish_reason']))
        entry['samples'][i + 1] = [{key: v for key, v in s.items() if key != 'body'} for s in checked]
        entry['requests'][i + 1] = text
        good = [s for s in checked if s['ok']]
        if item['q']['src'] == 'countdown':
            good = [s for s in good if s['reason'] == 'ok_countdown_none' or F.expression_key_of(s['line'])
                    not in entry['used']]
        good.sort(key=lambda s: (s['reason'] not in ('ok_oracle_verified', 'ok_countdown_valid'), s['n_tokens']))
        if not good:
            reasons = Counter(s['reason'] for s in checked).most_common(1)
            entry['status'] = f'branch{i + 1}_failed:' + (reasons[0][0] if reasons else 'no_sample')
            continue
        entry['bodies'][i], entry['results'][i] = good[0]['body'], good[0]['line']
        entry['samples'][i + 1].append(dict(chosen=good[0]['k']))
        if good[0]['reason'] == 'ok_countdown_valid':
            entry['used'].add(F.expression_key_of(good[0]['line']))
    for entry in found.values():
        entry.pop('used')
    return found


def run_mergers(gen, tok, jobs, cfg):
    """jobs: [(item, block, plan, results, longest_body_chars)] -> {id: dict(text, samples, status)}."""
    reqs = []
    for item, block, plan, results, _ in jobs:
        content = F.merger_context(dict(source=item['source'], q=item['q'], plan=plan), results) + \
            BLOCK_SUMMARY_NOTE[block]
        reqs.append(dict(key=f'summary{block}|{item["id"]}', prompt=chat(tok, [{'role': 'user', 'content': content}],
                                                                          False),
                         params=dict(n=cfg['merger_samples'], max_tokens=cfg['summary_max_tokens'],
                                     seed=seed('summary', block, item['id']), **C.STUDENT_SAMPLING)))
    found = {}
    for (item, block, plan, results, longest), samples in zip(jobs, gen(reqs)):
        checked = []
        for k, o in enumerate(samples):
            text = o['text'].strip()
            reason = ('summary_truncated' if o['finish_reason'] != 'stop' else 'summary_empty' if not text else
                      'summary_tags' if not contract.plain_text(text) else
                      'summary_final_marker' if has_final_marker(text) else 'ok')
            checked.append(dict(k=k, text=text, reason=reason, n_tokens=o['n_tokens'], chars=len(text),
                                within_ratio=len(text) <= cfg['summary_ratio'] * longest))
        good = sorted((s for s in checked if s['reason'] == 'ok'),
                      key=lambda s: (not s['within_ratio'], s['n_tokens'], s['k']))
        samples_log = [{key: v for key, v in s.items() if key != 'text'} for s in checked]
        if not good:
            found[item['id']] = dict(text=None, samples=samples_log, status='summary_failed:' + Counter(
                s['reason'] for s in checked).most_common(1)[0][0])
        else:
            found[item['id']] = dict(text=good[0]['text'], samples=samples_log, chosen=good[0]['k'], status='ok')
    return found


def cut_sentence(text):
    ends = list(SENTENCE_END.finditer(text))
    return text[:ends[-1].end()] if ends else ''


def stage_student1(out, backend, cfg):
    state = load_state(out)
    gen, tok = Recorder(out, 'student1', backend), backend.tok
    items = active(state)
    rows = {item['id']: dict(id=item['id']) for item in items}
    jobs = []
    for item in items:
        plan = item['plan1']
        if item['block1_source'] == 'pool':
            rows[item['id']]['block1'] = dict(plan=plan, bodies=item['pool_block']['bodies'],
                                              results=item['pool_block']['results'], source='pool',
                                              branch_checks=item['pool_block']['branch_checks'])
            continue
        overhead = C.overhead(backend, item['prefix'], plan)
        cap = (TOTAL - overhead - cfg['block1_reserve']) // plan['branches']
        if cap < cfg['min_branch_tokens']:
            rows[item['id']]['status'] = 'block1_budget'
            continue
        jobs.append((item, 1, plan, item['prefix'], cap))
    for task_id, found in run_branches(gen, tok, jobs, cfg).items():
        row = rows[task_id]
        row['block1'] = dict(plan=state[task_id]['plan1'], bodies=found['bodies'], results=found['results'],
                             source='regenerated', samples=found['samples'], requests=found['requests'],
                             cap=found['caps'], status=found['status'])
        if found['status'] != 'ok':
            row['status'] = 'block1_' + found['status']
    live = [dict(state[r['id']], **r) for r in rows.values() if r.get('status', 'ok') == 'ok']
    merged = run_mergers(gen, tok, [(item, 1, item['block1']['plan'], item['block1']['results'],
                                     max(map(len, item['block1']['bodies']))) for item in live], cfg)
    for task_id, found in merged.items():
        rows[task_id]['summary1'] = found
        if found['status'] != 'ok':
            rows[task_id]['status'] = 'summary1_failed'
    live = [dict(state[r['id']], **r) for r in rows.values() if r.get('status', 'ok') == 'ok']
    reqs = [dict(key=f'continuation|{item["id"]}', prompt=generation_prompt(tok, item, 'continuation'),
                 params=dict(n=cfg['continuation_samples'], max_tokens=cfg['continuation_max_tokens'],
                             stop=['\n\n', '</think>'], include_stop_str_in_output=True,
                             seed=seed('continuation', item['id']), **C.STUDENT_SAMPLING)) for item in live]
    for item, samples in zip(live, gen(reqs)):
        checked = []
        for k, o in enumerate(samples):
            text = o['text']
            if text.endswith('</think>'):
                stop, text = 'think_close', text[:-len('</think>')]
            elif text.endswith('\n\n') or o['finish_reason'] == 'stop':
                stop = 'paragraph'
            else:
                stop, text = 'length', cut_sentence(text)
            text = text.strip()
            reason = ('empty' if not text else 'tags' if not contract.plain_text(text) else
                      'final_marker' if has_final_marker(text) else 'ok')
            checked.append(dict(k=k, text=text, stop=stop, reason=reason, n_tokens=o['n_tokens']))
        good = sorted((s for s in checked if s['reason'] == 'ok'), key=lambda s: (s['stop'] != 'paragraph', s['k']))
        row = rows[item['id']]
        row['continuation'] = dict(text=good[0]['text'] if good else None, stop=good[0]['stop'] if good else None,
                                   chosen=good[0]['k'] if good else None,
                                   samples=[{key: v for key, v in s.items() if key != 'text'} for s in checked])
        if not good:
            row['status'] = 'continuation_failed:' + Counter(s['reason'] for s in checked).most_common(1)[0][0]
    write_jsonl(Path(out) / 'student1.jsonl', list(rows.values()))
    return rows


def stage_student2(out, backend, cfg):
    state = load_state(out)
    gen, tok = Recorder(out, 'student2', backend), backend.tok
    items = active(state)
    rows = {item['id']: dict(id=item['id'], block2_status='no_fork') for item in items}
    jobs = []
    for item in items:
        plan = item['plan2']['plan']
        if item['plan2']['decision'] != 'FORK':
            rows[item['id']]['block2_status'] = 'no_fork' if item['plan2']['status'] == 'no_fork' else \
                'no_fork:' + item['plan2']['status']
            continue
        skeleton = '<think>' + causal_text(item, 'no_fork') + block_text(plan, [''] * plan['branches'], '') + \
            '</think>\n\n<|im_end|>'
        cap = (TOTAL - ntok(tok, skeleton) - C.MARGIN - cfg['final_reserve']) // plan['branches']
        if cap < cfg['min_branch_tokens']:
            rows[item['id']]['block2_status'] = 'fork_failed:block2_budget'
            continue
        jobs.append((item, 2, plan, plain_context(item), cap))
    for task_id, found in run_branches(gen, tok, jobs, cfg).items():
        row = rows[task_id]
        row['block2'] = dict(plan=state[task_id]['plan2']['plan'], bodies=found['bodies'], results=found['results'],
                             source='generated', samples=found['samples'], requests=found['requests'],
                             cap=found['caps'], status=found['status'])
        row['block2_status'] = 'fork' if found['status'] == 'ok' else 'fork_failed:' + found['status']
    live = [dict(state[r['id']], **r) for r in rows.values() if r['block2_status'] == 'fork']
    merged = run_mergers(gen, tok, [(item, 2, item['block2']['plan'], item['block2']['results'],
                                     max(map(len, item['block2']['bodies']))) for item in live], cfg)
    for task_id, found in merged.items():
        rows[task_id]['summary2'] = found
        if found['status'] != 'ok':
            rows[task_id]['block2_status'] = 'fork_failed:' + found['status']
    reqs, live = [], []
    for row in rows.values():
        item = dict(state[row['id']], **row)
        upto = 'block2' if row['block2_status'] == 'fork' else 'no_fork'
        prompt = generation_prompt(tok, item, upto)
        used = ntok(tok, '<think>' + causal_text(item, upto) + '</think><|im_end|>')
        budget = min(cfg['final_max_tokens'], TOTAL - used - C.MARGIN)
        if budget < 256:
            row['status'] = 'final_budget'
            continue
        row['final_context'] = upto
        live.append((item, upto))
        reqs.append(dict(key=f'final|{row["id"]}', prompt=prompt,
                         params=dict(n=cfg['final_samples'], max_tokens=budget, seed=seed('final', row['id'], upto),
                                     **C.STUDENT_SAMPLING)))
    for (item, upto), samples in zip(live, gen(reqs)):
        checked = []
        for k, o in enumerate(samples):
            thinking, after = C.split_think(o['text'])
            answer = (after or '').strip()
            reason = ('unfinished' if after is None or o['finish_reason'] != 'stop' else 'empty_answer' if not answer
                      else 'tags' if not (contract.plain_text(thinking) and contract.plain_text(answer)) else 'ok')
            correct, grade = (C.final_grade(dict(q=item['q'], final=dict(text='</think>\n\n' + answer)))
                              if reason == 'ok' else (False, reason))
            checked.append(dict(k=k, rest=thinking, answer='\n\n' + answer, reason=reason, correct=correct,
                                grade=grade, n_tokens=o['n_tokens'], finish_reason=o['finish_reason']))
        good = sorted((s for s in checked if s['reason'] == 'ok'), key=lambda s: (not s['correct'], s['k']))
        row = rows[item['id']]
        log = [{key: v for key, v in s.items() if key not in ('rest', 'answer')} for s in checked]
        if not good:
            row.update(final=dict(samples=log), status='final_failed:' + Counter(
                s['reason'] for s in checked).most_common(1)[0][0])
            continue
        row['final'] = dict(rest=good[0]['rest'], answer=good[0]['answer'], chosen=good[0]['k'], samples=log,
                            correct=good[0]['correct'], grade=good[0]['grade'],
                            first_sample_correct=checked[0]['correct'],
                            any_sample_correct=any(s['correct'] for s in checked))
    write_jsonl(Path(out) / 'student2.jsonl', list(rows.values()))
    return rows


STAGE_FUNCS = dict(plan1=stage_plan1, student1=stage_student1, plan2=stage_plan2, student2=stage_student2)


# ------------------------------------------------------------------------------------------------- assemble (CPU)

def seg(text, loss, block=None, path=None):
    return dict(text=text, loss=loss, block=block, path=path)


def block_segments(number, plan, bodies, summary):
    """One block exactly as block 1 of the raw records (codex_rules.parallel_segments), with block id `number`."""
    s = [seg('<Parallel>', True, number), seg(contract.BRANCHES, False, number), seg(str(plan['branches']), True, number),
         seg('<Plan>', False, number), seg(plan['plan_text'], True, number), seg('</Plan>', True, number)]
    for i, body in enumerate(bodies, 1):
        s += [seg('<Path>', False, number, i), seg(contract.path_prefix(i), False, number, i),
              seg(body, True, number, i), seg('</Path>', True, number, i)]
    return s + [seg('</Parallel>', False, number), seg('<Summary>', False, number), seg(summary, True, number),
                seg('</Summary>', True, number)]


def build_segments(item):
    """Contract segments of a finished item: 2 blocks if block 2 forked, else 1 block (the paragraph and the rest are
    one main-text segment)."""
    b1, final = item['block1'], item['final']
    s = [seg('<think>', True), seg(item['prefix'], True)]
    s += block_segments(1, b1['plan'], b1['bodies'], item['summary1']['text'])
    main = main_text(item)
    if item.get('final_context') == 'block2':
        b2 = item['block2']
        s += [seg(main, True)] + block_segments(2, b2['plan'], b2['bodies'], item['summary2']['text'])
        if final['rest']:
            s.append(seg(final['rest'], True))
    else:
        s.append(seg(main + final['rest'], True))
    s += [seg('</think>', True), seg(final['answer'], True), seg('<|im_end|>', True)]
    text = ''.join(x['text'] for x in s)
    expected = '<think>' + causal_text(item, item['final_context']) + final['rest'] + '</think>' + final['answer'] + \
        '<|im_end|>'
    assert text == expected, 'segments differ from the generated causal text'
    return s


def critical_path(segments, tok):
    """Contract D/T over the loss segments (D = main + per block <Parallel>, count, plan, longest branch, summary;
    T = every loss token) and the user's definition prefix + longest branch per block + summaries + rest (rest = main
    text after block 1, </think>, the answer; block heads and runtime-inserted tokens reported separately)."""
    calls, paths = [], {}
    parts = dict(prefix=0, block_heads=0, branches={}, longest_branch={}, summaries=0, rest=0, inserted=0)
    for index, s in enumerate(segments):
        n = ntok(tok, s['text'])
        if not s['loss']:
            parts['inserted'] += n
        elif s['path']:  # one branch call: its body and </Path>
            paths[(s['block'], s['path'])] = paths.get((s['block'], s['path']), 0) + n
        else:
            calls.append(dict(node=contract.MAIN_OPEN, block=s['block'], sampled=n))
            if index == 1:
                parts['prefix'] += n
            elif s['block'] is not None and (segments[index - 1]['text'] == '<Summary>' or s['text'] == '</Summary>'):
                parts['summaries'] += n
            elif s['block'] is not None:  # <Parallel>, the count, the plan, </Plan>
                parts['block_heads'] += n
            else:
                parts['rest'] += n
    for (block, path), n in sorted(paths.items()):
        calls.append(dict(node=contract.PATH, block=block, sampled=n))
        parts['branches'].setdefault(str(block), []).append(n)
    for key, values in parts['branches'].items():
        parts['longest_branch'][key] = max(values)
    depth, total = contract.depth_and_tokens(calls)
    return dict(critical_path_tokens=depth, sampled_tokens=total, ratio=round(depth / total, 3) if total else None,
                user_critical_path=parts['prefix'] + sum(parts['longest_branch'].values()) + parts['summaries'] +
                parts['rest'], components=parts)


def gold_audit(out, state):
    """Scan every recorded prompt. oracle: the gold solution text appears verbatim (a leak by this code; expected
    none). answer_value: Codex's contains_answer finds the gold answer in a prompt although the question does not
    contain it; informational, since prompts carry model-written text (summary 1, the paragraph) that may already
    state the answer."""
    hits = dict(oracle=[], answer_value=[])
    for call in read_jsonl(Path(out) / 'calls.jsonl'):
        q = state[call['key'].split('|')[1]]['q']
        oracle = q['gold']['oracle']
        if isinstance(oracle, str) and len(oracle) > 3 and oracle in call['prompt']:
            hits['oracle'].append(call['key'])
        if not C.answer_in_question(q['task'], q['gold']) and C.contains_answer(call['prompt'], q['task'], q['gold']):
            hits['answer_value'].append(call['key'])
    return hits


def render_markdown(row, item, info):
    lines = [f'# {item["id"]}', '', f'- source: {item["source"]}; selection: {item["selection_note"]}',
             f'- block 1: {item["block1"]["source"]} ({item["block1"]["plan"]["kind"]}, '
             f'{item["block1"]["plan"]["branches"]} branches); block 2: {info["block2"]}',
             f'- correct: {info["correct"]} ({info["grade"]}); generator tokens: {info["n_tokens"]}; critical path '
             f'{info["critical_path_tokens"]} of {info["sampled_tokens"]} sampled tokens',
             '- context: causal serialized text (no graph positions at generation)', '',
             '## Question', '', item['question'], '',
             '## Trace', '', 'Runtime-inserted pieces (no loss) are shown as [[...]].', '', '`````text']
    lines.append(''.join(f'[[{s["text"]}]]' if not s['loss'] else s['text'] for s in row['segments']))
    lines += ['`````', '']
    return '\n'.join(lines)


def assemble(out, tok):
    out = Path(out)
    state = load_state(out)
    config = json.loads((out / 'config.json').read_text())
    records, per_id = [], {}
    (out / 'traces').mkdir(exist_ok=True)
    for task_id in config['ids']:
        item = state[task_id]
        decision = item.get('plan2', {}).get('decision')
        info = dict(status=item.get('status', 'ok'), block1_source=item.get('block1_source'),
                    block2_decision=decision, block2=item.get('block2_status'),
                    selection_note=item['selection_note'])
        if item.get('status', 'ok') != 'ok' or 'final' not in item or 'answer' not in item['final']:
            per_id[task_id] = info
            continue
        segments = build_segments(item)
        blocks = 2 if item['final_context'] == 'block2' else 1
        row = dict(id=f'{task_id}#multiblock', source=item['source'], mode='parallel', prompt=item['prompt'],
                   question=item['question'], segments=segments)
        summary = D.validate_row(row)
        assert len(summary['blocks']) == blocks
        correct, grade = C.final_grade(dict(q=item['q'], final=dict(text='</think>' + item['final']['answer'])))
        n_tokens = ntok(tok, ''.join(s['text'] for s in segments))
        path = critical_path(segments, tok)
        lengths = dict(prefix=ntok(tok, item['prefix']), plan1=ntok(tok, item['block1']['plan']['plan_text']),
                       branches1=[ntok(tok, b) for b in item['block1']['bodies']],
                       summary1=ntok(tok, item['summary1']['text']), continuation=ntok(tok, item['continuation']['text']),
                       plan2=ntok(tok, item['block2']['plan']['plan_text']) if blocks == 2 else None,
                       branches2=[ntok(tok, b) for b in item['block2']['bodies']] if blocks == 2 else None,
                       summary2=ntok(tok, item['summary2']['text']) if blocks == 2 else None,
                       rest=ntok(tok, item['final']['rest']), answer=ntok(tok, item['final']['answer']))
        info.update(blocks=blocks, correct=correct, grade=grade, first_final_sample_correct=item['final'][
            'first_sample_correct'], any_final_sample_correct=item['final']['any_sample_correct'], n_tokens=n_tokens,
                    over_budget=n_tokens > TOTAL, lengths=lengths, **path)
        row['provenance'] = dict(
            task_id=task_id, revision=REVISION, student=list(STUDENT), planner=list(PLANNER),
            contract_sha256=contract.SHA256, blocks=blocks, block1_source=item['block1_source'],
            coverage=item.get('coverage'), plan1_status=item.get('plan1_status'), plan2=item['plan2'],
            block2_status=item['block2_status'], branch_checks={
                '1': item['block1'].get('branch_checks') or item['block1'].get('samples'),
                '2': item['block2'].get('samples') if blocks == 2 else None},
            summary_samples={'1': item['summary1']['samples'], '2': item['summary2']['samples'] if blocks == 2
                             else None},
            continuation=item['continuation'], final_samples=item['final']['samples'], correct=correct, grade=grade,
            n_tokens=n_tokens, over_budget=n_tokens > TOTAL, model_finished=True, critical_path=path,
            context=config['context'], pool_n_tokens=item.get('pool_n_tokens'), selection_note=item['selection_note'])
        records.append(row)
        (out / 'traces' / f'{task_id}.md').write_text(render_markdown(row, item, info), encoding='utf-8')
        per_id[task_id] = info
    leaks = gold_audit(out, state)
    done = [v for v in per_id.values() if 'blocks' in v]
    stats = dict(revision=REVISION, ids=config['ids'], selection_notes=config['selection_notes'],
                 records=len(records), per_id=per_id, gold_in_prompts=leaks,
                 gold_oracle_in_any_prompt=bool(leaks['oracle']),
                 block2=dict(Counter(v.get('block2_decision') or v['status'] for v in per_id.values())),
                 two_block_records=sum(v['blocks'] == 2 for v in done),
                 correct=dict(two_block=sum(v['correct'] for v in done if v['blocks'] == 2),
                              single_block=sum(v['correct'] for v in done if v['blocks'] == 1)),
                 mean_critical_path_ratio=round(sum(v['ratio'] for v in done) / len(done), 3) if done else None,
                 calls=sum(1 for _ in read_jsonl(out / 'calls.jsonl')), context=config['context'])
    write_jsonl(out / 'records.jsonl', records)
    write_json(out / 'stats.json', stats)
    index = ['# Multi-block probe', '', '| id | block 1 | block 2 | blocks | correct | tokens | critical path |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    for task_id, v in per_id.items():
        link = f'[{task_id}](traces/{task_id}.md)' if 'blocks' in v else task_id
        index.append(f'| {link} | {v.get("block1_source")} | {v.get("block2")} | {v.get("blocks", "-")} | '
                     f'{v.get("correct", "-")} | {v.get("n_tokens", "-")} | {v.get("critical_path_tokens", "-")} |')
    (out / 'traces.md').write_text('\n'.join(index) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in stats.items() if k not in ('per_id', 'selection_notes')}, indent=1))
    return records, stats


# ------------------------------------------------------------------------------------------------------ cli

def cfg_of(args):
    return {key: getattr(args, key) for key in DEFAULTS}


def run_stage(args):
    config = json.loads((args.out / 'config.json').read_text())
    which = MODEL_OF[args.name]
    max_len = args.planner_max_model_len if which == 'planner' else args.student_max_model_len
    backend = Engine(which, max_len, args.gpu_memory_utilization, args.max_num_seqs, not args.no_fast_sampler)
    t0 = time.time()
    STAGE_FUNCS[args.name](args.out, backend, config['cfg'])
    with (args.out / 'stage_log.jsonl').open('a') as handle:
        handle.write(json.dumps(dict(stage=args.name, model=[backend.repo, backend.rev], vllm=backend.version,
                                     seconds=round(time.time() - t0, 1),
                                     utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))) + '\n')


def cmd_run(args):
    args.out.mkdir(parents=True, exist_ok=True)
    if not (args.out / 'items.jsonl').exists():
        ids = [x.strip() for x in args.ids.split(',') if x.strip()] if args.ids else list(DEFAULT_IDS)
        force = [x.strip() for x in args.force_regenerate.split(',') if x.strip()]
        select(args.pool, args.out, ids, force, cfg_of(args))
    import importlib
    importlib.import_module('math_verify')  # Codex's scorer needs it (VM venv)
    for name in STAGES:
        if (args.out / f'{name}.jsonl').exists():
            print(f'{name}: done, skipped', flush=True)
            continue
        command = [sys.executable, str(Path(__file__).resolve()), 'stage', name, '--out', str(args.out),
                   '--gpu-memory-utilization', str(args.gpu_memory_utilization),
                   '--max-num-seqs', str(args.max_num_seqs),
                   '--planner-max-model-len', str(args.planner_max_model_len),
                   '--student-max-model-len', str(args.student_max_model_len)] + \
            (['--no-fast-sampler'] if args.no_fast_sampler else [])
        print(f'{name}: {" ".join(command)}', flush=True)
        with (args.out / f'{name}.log').open('a') as log:
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True, cwd=str(HERE))
    return assemble(args.out, load_tokenizer())


def load_tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(STUDENT[0], revision=STUDENT[1])


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = parser.add_subparsers(dest='command', required=True)

    def engine_args(p):
        p.add_argument('--gpu-memory-utilization', type=float, default=0.88)
        p.add_argument('--max-num-seqs', type=int, default=128)
        p.add_argument('--planner-max-model-len', type=int, default=32768)
        p.add_argument('--student-max-model-len', type=int, default=20480)
        p.add_argument('--no-fast-sampler', action='store_true')

    r = sub.add_parser('run', help='select + the four model stages (one subprocess each) + assemble')
    r.add_argument('--pool', type=Path, required=True, help='folder with all.raw.jsonl and details.jsonl (read only)')
    r.add_argument('--out', type=Path, required=True)
    r.add_argument('--ids', default=None, help='comma-separated task ids (default: the 12 DEFAULT_IDS)')
    r.add_argument('--force-regenerate', default=','.join(FORCE_REGENERATE))
    for key, value in DEFAULTS.items():
        r.add_argument('--' + key.replace('_', '-'), type=type(value), default=value)
    engine_args(r)
    s = sub.add_parser('stage', help='internal: one model stage in this process')
    s.add_argument('name', choices=STAGES)
    s.add_argument('--out', type=Path, required=True)
    engine_args(s)
    a = sub.add_parser('assemble', help='CPU: records, traces, stats from the stage files')
    a.add_argument('--out', type=Path, required=True)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.command == 'run':
        return cmd_run(args)
    if args.command == 'stage':
        return run_stage(args)
    return assemble(args.out, load_tokenizer())


if __name__ == '__main__':
    main()
