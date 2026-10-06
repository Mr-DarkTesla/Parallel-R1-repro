"""Create Figure-3 data, forward counts, segmented lengths and a trace viewer."""
import argparse
import csv
import html
import json
import statistics
from collections import defaultdict
from pathlib import Path


def records(folder, prefix):
    for file in sorted(folder.glob(prefix + '-*.jsonl')):
        with file.open() as stream:
            for line in stream:
                yield json.loads(line)


def segments(ids, token_ids):
    names = {int(v[0]): k for k, v in token_ids.items()}
    result, stack, start = [], [], 0
    phase = 'main_before'
    for i, token in enumerate(ids):
        tag = names.get(token)
        if tag in ('<Parallel>', '<Path>', '<Summary>'):
            if i > start:
                result.append(dict(phase=phase, start=start, end=i, tokens=i-start))
            stack.append(phase)
            phase = {'<Parallel>': 'parallel_control', '<Path>': 'path', '<Summary>': 'summary'}[tag]
            start = i
        elif tag in ('</Path>', '</Parallel>', '</Summary>'):
            result.append(dict(phase=phase, start=start, end=i+1, tokens=i+1-start))
            phase = stack.pop() if stack else 'main_after'
            if tag in ('</Parallel>', '</Summary>'):
                phase = 'main_after'
            start = i+1
    if start < len(ids):
        result.append(dict(phase=phase, start=start, end=len(ids), tokens=len(ids)-start))
    return result


def runtime_segments(trace, token_ids):
    """Use executed branch windows, not hallucinated tag strings inside paths."""
    ids = trace['response_ids']
    limit = len(ids)
    spans = set()
    for left_pad, start1, end1, start2, end2 in trace['path_masks']:
        offset = left_pad + trace['prompt_tokens']
        spans.update(((start1-offset, end1-offset), (start2-offset, end2-offset)))
    forks = [item['response_token_index'] for item in trace['forks']]
    result, cursor = [], 0
    def add(phase, start, end):
        start, end = max(0, start), min(limit, end)
        if end > start:
            result.append(dict(phase=phase, start=start, end=end, tokens=end-start))
    summary_open = int(token_ids['<Summary>'][0])
    summary_close = int(token_ids['</Summary>'][0])
    for index, fork in enumerate(forks):
        next_fork = forks[index+1] if index+1 < len(forks) else limit
        add('main_before' if index == 0 else 'main_between', cursor, fork)
        cursor = fork
        paths = sorted((start, end) for start, end in spans if fork <= start < next_fork)
        for start, end in paths:
            add('parallel_control', cursor, start)
            add('path', start, end)
            cursor = end
        summary_starts = [i for i in range(min(cursor, limit), min(next_fork, limit)) if ids[i] == summary_open]
        if summary_starts:
            start = summary_starts[0]
            add('parallel_control', cursor, start)
            ends = [i+1 for i in range(start+1, min(next_fork, limit)) if ids[i] == summary_close]
            end = ends[0] if ends else min(next_fork, limit)
            add('summary', start, end)
            cursor = end
    add('main_after' if forks else 'main_before', cursor, limit)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('runs', nargs='+', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'enriched_traces.jsonl').write_text('')
    grouped = defaultdict(list)
    sample_rows, view = [], []
    for run in args.runs:
        checkpoint = json.loads((run / 'checkpoint.json').read_text())
        token_ids = checkpoint['special_tokens']
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(checkpoint['model_path'], local_files_only=True)
        validation = defaultdict(list)
        for file in (run / 'validation').glob('*.jsonl'):
            for validation_index, line in enumerate(file.read_text().splitlines()):
                item = json.loads(line)
                item['_validation_row_index'] = validation_index
                output_text = item['output']
                while tokenizer.pad_token and output_text.endswith(tokenizer.pad_token):
                    output_text = output_text[:-len(tokenizer.pad_token)]
                validation[output_text].append(item)
        forward = {}
        for row in records(run / 'telemetry', 'forwards'):
            previous = forward.setdefault(row['request_id'], dict(forward_passes=0, scheduler_steps=0, scheduled_tokens=0))
            for key in previous:
                previous[key] += row[key]
        for trace in records(run / 'telemetry', 'traces'):
            info = trace['trajectory']
            split = 'val' if info.get('validate') else 'train'
            step = int(info.get('step', -1))
            grouped[(run.name, split, step)].append(trace)
            breakdown = runtime_segments(trace, token_ids)
            trace['segments'] = breakdown
            for part in breakdown:
                part['text'] = tokenizer.decode(trace['response_ids'][part['start']:part['end']], skip_special_tokens=False)
            normalized_text = tokenizer.decode(trace['response_ids'], skip_special_tokens=False)
            while tokenizer.pad_token and normalized_text.endswith(tokenizer.pad_token):
                normalized_text = normalized_text[:-len(tokenizer.pad_token)]
            matching = validation.get(normalized_text, [])
            prompt = matching[0]['input'] if matching else json.dumps(trace.get('messages', []), ensure_ascii=False)
            trace['validation_match_count'] = len(matching)
            trace['validation_row_index'] = matching[0]['_validation_row_index'] if len(matching) == 1 else None
            trace['prompt_text'] = prompt
            trace['reward'] = matching[0]['score'] if matching else None
            trace['forward_counts_complete'] = True
            total_forward = 0
            for call in trace['calls']:
                keys = [key for key in forward if key == call['request_id'] or key.startswith(call['request_id'] + '-')]
                call['forward_passes'] = sum(forward[key]['forward_passes'] for key in keys) if keys else None
                if not keys:
                    trace['forward_counts_complete'] = False
                else:
                    total_forward += call['forward_passes']
            trace['request_forward_participations'] = total_forward if trace['forward_counts_complete'] else None
            sample_index = trace['validation_row_index'] if split == 'val' and trace['validation_row_index'] is not None else info.get('sample_index')
            row = dict(run=run.name, split=split, step=step, sample_index=sample_index,
                       worker_sample_index=info.get('sample_index'),
                       rollout_n=info.get('rollout_n'), response_tokens=trace['response_tokens'],
                       fork_count=trace['executed_fork_count'], generated_tokens=trace['generated_tokens_total'],
                       generation_calls=trace['generation_calls'], request_forward_participations=trace['request_forward_participations'],
                       truncated=trace['truncated'],
                       main_before_tokens=sum(x['tokens'] for x in breakdown if x['phase'] == 'main_before'),
                       path_tokens=sum(x['tokens'] for x in breakdown if x['phase'] == 'path'),
                       summary_tokens=sum(x['tokens'] for x in breakdown if x['phase'] == 'summary'),
                       main_between_tokens=sum(x['tokens'] for x in breakdown if x['phase'] == 'main_between'),
                       main_after_tokens=sum(x['tokens'] for x in breakdown if x['phase'] == 'main_after'))
            sample_rows.append(row)
            heading = f"{run.name} / {split} / step {step} / sample {sample_index} / rollout {info.get('rollout_n')}"
            blocks = ''.join('<section class="' + part['phase'] + '"><h3>' + html.escape(part['phase']) +
                             ' · ' + str(part['tokens']) + ' tokens</h3><pre>' + html.escape(part['text']) + '</pre></section>' for part in breakdown)
            view.append('<details><summary>' + html.escape(heading) + ' · ' + str(row['fork_count']) + ' forks · ' + str(row['response_tokens']) + ' tokens</summary><h3>Вопрос</h3><pre>' + html.escape(prompt) + '</pre><h3>Метрики</h3><pre>' +
                        html.escape(json.dumps(row, indent=2)) + '</pre>' + blocks +
                        '<details><summary>Все вызовы генерации</summary><pre>' + html.escape(json.dumps(trace['calls'], indent=2)) + '</pre></details></details>')
            with (args.out / 'enriched_traces.jsonl').open('a') as stream:
                stream.write(json.dumps(trace, ensure_ascii=False) + '\n')
        engine = list(records(run / 'telemetry', 'engine'))
        (args.out / f'{run.name}_engine.json').write_text(json.dumps(dict(
            actual_batched_forward_passes=sum(x['actual_forward_passes'] for x in engine),
            scheduled_request_participations=sum(x['scheduled_requests'] for x in engine),
            note='Batch forwards and request participation totals are different; warmup excluded.'), indent=2))
    curve = []
    for (run, split, step), traces in sorted(grouped.items()):
        positions = [p for trace in traces for p in trace['parallel_relative_positions']]
        curve.append(dict(run=run, split=split, step=step, samples=len(traces), blocks=len(positions),
                          parallel_ratio=sum(bool(t['parallel_relative_positions']) for t in traces)/len(traces),
                          relative_position_mean=statistics.mean(positions) if positions else None,
                          relative_position_sem=statistics.stdev(positions)/(len(positions)**0.5) if len(positions)>1 else None,
                          truncated_ratio=sum(t['truncated'] for t in traces)/len(traces)))
    for name, rows in (('samples.csv', sample_rows), ('figure3.csv', curve)):
        if rows:
            with (args.out / name).open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    (args.out / 'traces.html').write_text('<!doctype html><meta charset="utf-8"><title>Parallel-R1 traces</title><style>body{font:16px system-ui;max-width:1100px;margin:30px auto;padding:0 20px;color:#173042}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f7fa;padding:16px;border-radius:8px}details{margin:20px 0}summary{cursor:pointer;font-weight:650;padding:10px;border:1px solid #ccd7e0;border-radius:8px}section{border-left:5px solid #94a3b8;padding-left:18px;margin:18px 0}.path{border-color:#6d5dfc}.summary{border-color:#059669}.main_before,.main_after{border-color:#0284c7}h3{font-size:14px;text-transform:uppercase;letter-spacing:.04em}</style><h1>Parallel-R1 · SFT-трейсы</h1><p>Вопрос → основной текст → ветви → summary → продолжение. Теги и текст сохранены как выдала система rollout; часть управляющих тегов вставляет код. Счётчики forwards показывают участие запроса в фактических вызовах модели.</p>' + ''.join(view), encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    for run, split in sorted({(r['run'], r['split']) for r in curve}):
        rows = [r for r in curve if r['run']==run and r['split']==split]
        valid = [r for r in rows if r['relative_position_mean'] is not None]
        if valid:
            axes[0].plot([r['step'] for r in valid], [r['relative_position_mean'] for r in valid], marker='.', label=f'{run} {split}')
        axes[1].plot([r['step'] for r in rows], [r['parallel_ratio'] for r in rows], label=f'{run} {split}')
    axes[0].set(ylabel='Parallel start / response length', ylim=(0, 1))
    axes[1].set(xlabel='RL optimizer step', ylabel='Parallel ratio', ylim=(0, 1))
    for ax in axes:
        ax.grid(alpha=.25)
        if ax.get_legend_handles_labels()[0]: ax.legend()
    fig.tight_layout(); fig.savefig(args.out / 'figure3.png', dpi=180); fig.savefig(args.out / 'figure3.pdf')
    print('Reports:', args.out)


if __name__ == '__main__':
    main()
