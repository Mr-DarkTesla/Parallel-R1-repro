"""Reference-blind final-answer extraction and isolated symbolic verification."""
import argparse
import hashlib
import json
import re
import sys
from math import sqrt
from pathlib import Path

WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(WORK / 'scorer-deps'))
from math_verify import parse, verify
from math_verify.parser import LatexExtractionConfig


def extract(text):
    if '</think>' in text:
        text = text.rsplit('</think>', 1)[1]
    elif '<think>' in text:
        return None, 'unfinished_thinking'
    headers = list(re.finditer(r'(?i)(?:\*\*)?Final\s+Answer(?:\*\*)?\s*:', text))
    # A later explicit final answer supersedes an earlier branch's boxed value.
    if headers:
        text = text[headers[-1].end():]
    boxes = list(re.finditer(r'\\(?:boxed|fbox)\s*\{', text))
    if boxes:
        start = boxes[-1].end()
        depth = 1
        for i in range(start, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            if depth == 0:
                return text[start:i], 'boxed'
        return None, 'unclosed_box'
    if headers:
        for line in text.splitlines():
            line = line.strip().strip('*').strip()
            line = re.sub(r'<\|[^>]*\|>|</?(?:Parallel|Path|Summary)>', '', line).strip()
            if line and line not in ('$$', '$', r'\[', r'\]'):
                return line.strip('$'), 'final_answer_line'
    return None, 'missing_final_answer'


def compute_score(data_source, solution_str, solution_str_with_special_tokens, ground_truth, extra_info=None):
    value = grade(solution_str_with_special_tokens, str(ground_truth))
    return dict(score=float(value['correct']), acc=float(value['correct']),
                valid_answer=float(value['valid']), scorer_error=float(value['error'] is not None),
                sample_index=int((extra_info or {}).get('index', -1)))


def parsed(answer):
    return parse('\\boxed{' + answer + '}', extraction_config=[LatexExtractionConfig()], parsing_timeout=5)


def grade(output, gold):
    answer, method = extract(output)
    if answer is None:
        return dict(correct=False, answer=None, extraction=method, valid=False, error=None)
    try:
        gold_parsed, prediction = parsed(gold), parsed(answer)
        if not gold_parsed:
            raise ValueError('unparseable reference')
        return dict(correct=bool(prediction and verify(gold_parsed, prediction, timeout_seconds=5)), answer=answer, extraction=method, valid=bool(prediction), error=None)
    except Exception as error:
        return dict(correct=False, answer=answer, extraction=method, valid=False, error=f'{type(error).__name__}: {error}')


def wilson(k, n):
    z = 1.959963984540054
    p = k / n
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    radius = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return [max(0, center-radius), min(1, center+radius)]


def check():
    cases = [
        ('Final Answer:\n$$\n\\boxed{70}\n$$', '70', True),
        (r'\boxed{0.5}', r'\frac{1}{2}', True),
        (r'\boxed{\frac{2}{4}}', r'\frac{1}{2}', True),
        (r'\boxed{2\sqrt{2}}', r'\sqrt{8}', True),
        (r'\boxed{71}', '70', False),
        (r'<think>\boxed{70}', '70', False),
        (r'<think>\boxed{70}</think>\boxed{71}', '70', False),
        (r'\boxed{70} later \boxed{71}', '70', False),
        (r'\boxed{70} later \boxed{', '70', False),
        ('No final answer', '70', False),
        ('A branch found \\boxed{70}. Final Answer: 71', '70', False),
        ('A branch found \\boxed{70}. Final Answer: 71', '71', True),
        ('Final Answer:\n\\frac{1}{2}<|im_end|>', '0.5', True),
    ]
    for output, gold, expected in cases:
        result = grade(output, gold)
        assert result['correct'] == expected and result['error'] is None, (output, result)
    return len(cases)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--mode', choices=['instant', 'reasoning'])
    args = parser.parse_args()
    if args.worker:
        for line in sys.stdin:
            request=json.loads(line)
            result=grade(request['output'],request['gold'])
            print(json.dumps(result),flush=True)
        sys.exit(0)
    tests = check()
    data = [json.loads(line) for line in (WORK / 'questions.jsonl').read_text().splitlines()]
    assert len(data) == 500 and len({r['id'] for r in data}) == 500
    reference_errors = [r['id'] for r in data if not parsed(r['answer'])]
    assert not reference_errors, reference_errors
    if args.check:
        print(json.dumps(dict(tests=tests, reference_coverage=len(data), status='passed')))
        sys.exit(0)
    targets = {r['id']: r['answer'] for r in data}
    trace = WORK / args.mode / 'traces.jsonl'
    records = [json.loads(line) for line in trace.read_text().splitlines()]
    assert len(records) == 500 and {r['id'] for r in records} == set(targets)
    assert len({r['id'] for r in records}) == 500
    scores = [dict(id=r['id'], **grade(r['output'], targets[r['id']])) for r in records]
    score_path = WORK / args.mode / 'scores.jsonl'
    score_path.write_text(''.join(json.dumps(r) + '\n' for r in scores))
    errors = [r for r in scores if r['error']]
    correct = sum(r['correct'] for r in scores)
    summary = dict(complete=not errors, mode=args.mode, questions=500, answers=500,
                   samples_per_question=1, accuracy=correct/500, correct=correct,
                   ci95=wilson(correct, 500), ci_method='Wilson two-sided 95%',
                   invalid_answers=sum(not r['valid'] for r in scores), scorer_errors=errors,
                   finish_reasons={k: sum(r['finish_reason'] == k for r in records) for k in ('stop', 'length', 'abort')},
                   output_tokens=sum(r['output_tokens'] for r in records),
                   scoring='Final-answer extraction independent of gold, Math-Verify 0.8.0 symbolic equivalence',
                   traces_sha256=hashlib.sha256(trace.read_bytes()).hexdigest(), extraction_tests=tests)
    (WORK / args.mode / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))
    assert not errors, 'Scorer errors require review; results are incomplete'
