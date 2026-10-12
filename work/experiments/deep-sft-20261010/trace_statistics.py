"""Post-hoc serialized student token statistics; does not mutate frozen traces."""
from pathlib import Path
import argparse, collections, hashlib, importlib.util, json, re
import numpy as np
from transformers import AutoTokenizer

P = Path.cwd()
B = P / 'work/experiments/deep-sft-20261010'
spec = importlib.util.spec_from_file_location('validator', P / 'exps/deepseek-gsm-wide3000-v2-20261009/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

def stats(xs):
    if not xs:
        return None
    return dict(count=len(xs), mean=float(np.mean(xs)), median=float(np.median(xs)),
                p5=float(np.percentile(xs, 5)), p95=float(np.percentile(xs, 95)),
                minimum=int(min(xs)), maximum=int(max(xs)))

def main(phase):
    out = B / phase
    rows = [json.loads(line) for line in (out / 'accepted.jsonl').open()]
    tok = AutoTokenizer.from_pretrained(P / 'work/experiments/base-format-20261010/runs/production/final', local_files_only=True)
    def tokens(t):
        return len(tok.encode(t, add_special_tokens=False))
    tasks = []
    for row in rows:
        text = row['response']
        cursor = 0
        serial = 0
        path_lengths = []
        whole_path_lengths = []
        round_maxima = []
        for block in validator.BLOCK.finditer(text):
            paths = list(re.finditer(r'<Path>[1-8]\n([\s\S]*?)</Path>', block[2]))
            assert paths
            prefix_end = block.start(2) + paths[0].start()
            suffix_start = block.start(2) + paths[-1].end()
            serial += tokens(text[cursor:prefix_end]) + tokens(text[suffix_start:block.end()])
            whole = [tokens(path[0]) for path in paths]
            path_lengths.extend(tokens(path[1]) for path in paths)
            whole_path_lengths.extend(whole)
            round_maxima.append(max(whole))
            cursor = block.end()
        serial += tokens(text[cursor:])
        tasks.append(dict(id=row['id'], rounds=row['fork_count'], widths=row['branch_schedule'],
                          path_tokens=path_lengths, whole_path_tokens=whole_path_lengths,
                          response_tokens=tokens(text), prompt_and_response_tokens=row['student_tokens'],
                          serial_tokens_split_proxy=serial,
                          critical_path_tokens_split_proxy=serial + sum(round_maxima)))
    report = dict(phase=phase, accepted=len(rows),
                  width=stats([n for t in tasks for n in t['widths']]),
                  rounds=stats([t['rounds'] for t in tasks]),
                  path_body_tokens=stats([n for t in tasks for n in t['path_tokens']]),
                  whole_path_tokens=stats([n for t in tasks for n in t['whole_path_tokens']]),
                  response_tokens=stats([t['response_tokens'] for t in tasks]),
                  student_context_tokens=stats([t['prompt_and_response_tokens'] for t in tasks]),
                  critical_path_tokens_split_proxy=stats([t['critical_path_tokens_split_proxy'] for t in tasks]),
                  serial_tokens_split_proxy=stats([t['serial_tokens_split_proxy'] for t in tasks]),
                  width_histogram=dict(collections.Counter(n for t in tasks for n in t['widths'])),
                  round_histogram=dict(collections.Counter(t['rounds'] for t in tasks)),
                  accepted_sha256=hashlib.sha256((out / 'accepted.jsonl').read_bytes()).hexdigest(),
                  limitations=['Student tokenizer and compacted training response; teacher hidden reasoning excluded.',
                               'Critical path includes entire Path opener/body/closer and all serial text.',
                               'Independent segment tokenization can differ at boundaries; split proxy is not runtime forwards or latency.',
                               'Prompt/context tokens count once; prompt is excluded from response critical path.'])
    (out / 'trace-statistics.json').write_text(json.dumps(report, indent=2) + '\n')
    (out / 'trace-statistics-per-task.jsonl').write_text(''.join(json.dumps(t) + '\n' for t in tasks))
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['pilot', 'pilot-rechecked', 'production'], required=True)
    main(parser.parse_args().phase)
