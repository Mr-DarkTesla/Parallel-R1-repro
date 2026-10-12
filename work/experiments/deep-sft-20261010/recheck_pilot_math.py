"""Rescore identical first responses without any teacher or GPU calls."""
from pathlib import Path
import hashlib, importlib.util, json, re, sys
from transformers import AutoTokenizer
from arithmetic_check_v2 import check as arithmetic_check
from oracle_check_v2 import check as oracle_check
P = Path.cwd(); B = P / 'work/experiments/deep-sft-20261010'; OUT = B / 'pilot-rechecked'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result); return result
validator = module('validator', P / 'exps/deepseek-gsm-wide3000-v2-20261009/validate.py')
scorer = module('scorer', P / 'exps/math500-new-sft-20261008/score.py')

def main():
    OUT.mkdir(exist_ok=True)
    tasks = {r['id']: r for r in map(json.loads, (B / 'pilot-tasks.jsonl').read_text().splitlines())}
    old = {r['id']: r for r in map(json.loads, (B / 'pilot/journal.jsonl').read_text().splitlines())}
    raws = [r for r in map(json.loads, (B / 'pilot/teacher-responses.jsonl').read_text().splitlines()) if r['attempt'] == 1]
    assert len(raws) == 50 and {r['id'] for r in raws} == tasks.keys() == old.keys()
    independent_path = B / 'reviews/independent/first50-math-review.json'
    # Actual independent review explicitly resolves this one verification-LHS
    # parsing issue. Its old/new machine findings remain in the journal.
    independent = json.loads(independent_path.read_text())
    independent_raw = {r['id']: r for r in map(json.loads, (B / 'reviews/independent/first-attempt-raw-responses.jsonl').read_text().splitlines())}
    oracle = {r['id']: r for r in map(json.loads, (B / 'oracle-source.jsonl').read_text().splitlines())}
    tok = AutoTokenizer.from_pretrained(P / 'work/experiments/base-format-20261010/runs/production/final', local_files_only=True)
    system = (P / 'work/experiments/base-format-20261010/system.txt').read_text()
    accepted = []; outcomes = []
    for raw in sorted(raws, key=lambda r: r['id']):
        item = tasks[raw['id']]; response = raw['response']['choices'][0]; text = response['message']['content']
        shape = validator.validate(text); blocks = shape.pop('blocks'); matches = list(validator.BLOCK.finditer(text))
        arithmetic = arithmetic_check(text); replay = oracle_check(text, oracle[item['id']],
            [dict(block, start=m.start(), end=m.end()) for block, m in zip(blocks, matches)])
        grade = scorer.grade(text, item['reference'])
        xml_counts = {tag: [len(re.findall('<'+tag+'>', text)), len(re.findall('</'+tag+'>', text))] for tag in ['Parallel','Path','Summary']}
        exact_xml = (xml_counts['Parallel'] == [shape['rounds']]*2 and
                     xml_counts['Summary'] == [shape['rounds']]*2 and
                     xml_counts['Path'] == [sum(shape['widths'])]*2)
        expected_alias_failures = [dict(type='reference_unavailable_to_sibling',round=s,path_id=4,label=name)
            for s,name in [(1,'Fir_1'),(2,'Elm_2'),(3,'Cedar_3'),(4,'Fir_4')]]
        manually_resolved = (item['id'] == 'synthetic-layered-dag-v1/2026101061' and
            replay['failures'] == expected_alias_failures and raw == independent_raw[item['id']])
        canonical = shape['valid'] and exact_xml and response['finish_reason'] == 'stop' and '<think>' not in text and '</think>' not in text
        accepted_math = canonical and grade['correct'] and not grade['error'] and not arithmetic['mismatches'] and (not replay['failures'] or manually_resolved)
        old_first = old[item['id']]['attempts'][0]
        outcome = dict(id=item['id'], first_attempt_only=True, output=text, shape=shape, exact_xml=exact_xml,
            xml_counts=xml_counts, grade=grade, arithmetic_check_v2=arithmetic, oracle_check_v2=replay,
            manual_oracle_exception=dict(resolved=bool(manually_resolved), independent_report=str(independent_path),
                independent_report_sha256=sha(independent_path), reason='Independently recomputed check-LHS alias; RHS uses only pre-fork source inputs.') if manually_resolved else None,
            original_first_attempt=old_first, original_final_decision=old[item['id']]['decision'],
            decision='accepted_math_and_canonical' if accepted_math else 'rejected',
            semantic_judge=old_first.get('judge'), semantic_judge_pending=not bool(old_first.get('judge')))
        if accepted_math:
            def compact(m):
                body=m.group(1); ix=body.index('<Path>'); ps=re.findall(r'<Path>.*?</Path>',body,re.S)
                assert not re.sub(r'<Path>.*?</Path>','',body[ix:],flags=re.S).strip()
                return '<Parallel>'+body[:ix]+''.join(ps)+'</Parallel>'
            compacted = re.sub(r'<Parallel>(.*?)</Parallel>',compact,text,flags=re.S)
            messages = [dict(role='system',content=system),dict(role='user',content=item['question'])]
            prefix = tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
            assert prefix.endswith('Solution:\n')
            context = len(tok.encode(prefix,add_special_tokens=False))+len(tok.encode(compacted+tok.eos_token,add_special_tokens=False))
            assert context <= 8192
            row = dict(id=item['id'],source=item['source'],problem=item['question'],answer=item['reference'],response=compacted,
                prompt_messages=json.dumps(messages,ensure_ascii=False),split_group=item['split_group'],fork_count=shape['rounds'],
                branch_schedule=shape['widths'],student_tokens=context,raw_response_sha256=hashlib.sha256(text.encode()).hexdigest(),
                verification=dict(final_answer=grade,explicit_arithmetic=arithmetic,oracle_replay=replay,independent_report_sha256=sha(independent_path)),
                release_status='HOLD: math-canonical engineering snapshot, semantic judge and Instruct template adaptation pending')
            accepted.append(row);outcome['row']=row
        outcomes.append(outcome)
    for name, rows in [('journal.jsonl',outcomes),('accepted.jsonl',accepted),('first-attempt-raw-responses.jsonl',sorted(raws,key=lambda r:r['id']))]:
        (OUT/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    report = dict(planned=50,completed=50,first_attempt_only=True,first_math_correct=sum(r['grade']['correct'] and not r['grade']['error'] for r in outcomes),
        canonical=sum(r['shape']['valid'] and r['exact_xml'] for r in outcomes),accepted_math_canonical=len(accepted),
        rejected=[r['id'] for r in outcomes if r['decision']=='rejected'],
        semantic_judge_missing=[r['id'] for r in outcomes if r['semantic_judge_pending']],
        original_outcomes_preserved=True,new_teacher_calls=0,production_released=False,
        status='HOLD: math/canonical snapshot complete; semantic review and Instruct template pending',
        independent_report_sha256=sha(independent_path),
        checker_sha256={f:sha(B/f) for f in ['arithmetic_check.py','oracle_check.py','arithmetic_check_v2.py','oracle_check_v2.py','test_checker_repair.py']},
        artifact_sha256={f:sha(OUT/f) for f in ['journal.jsonl','accepted.jsonl','first-attempt-raw-responses.jsonl']},
        provenance_sha256={f:sha(B/f) for f in ['teacher-prompt.txt','judge-prompt.txt','pilot-tasks.jsonl','oracle-source.jsonl','candidate-pool.jsonl']},
        limitations=['Failed internal HTTP transport retries were not individually journaled by original generation.',
                    'Independent reviewer proves source relations; numeric checker does not prove prose meanings.',
                    'Raw 1022 drafting preamble is rejected, not sanitized or replaced with a retry.'])
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
if __name__ == '__main__':main()
