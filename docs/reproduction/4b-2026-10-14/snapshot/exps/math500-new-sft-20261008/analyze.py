"""Match scored outputs to actual runtime calls; exclude padded duplicate samples."""
import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import re
import statistics
from score import grade, wilson

ROOT=Path(__file__).resolve().parent

def clean(text):
    return re.sub(r'(?:\s*<\|endoftext\|>)+\s*$','',text).strip()

def stats(values):
    if not values:return None
    s=sorted(values)
    return dict(mean=statistics.mean(s),median=statistics.median(s),p90=s[min(len(s)-1,int(.9*len(s)))],max=max(s))

def shape(text):
    tags=re.findall(r'</?(?:Parallel|Path|Summary)>',text)
    stack=[]; valid=True; grammar=True
    for t in tags:
        if t.startswith('</'):
            if not stack or stack.pop()!=t[2:-1]:valid=False;break
        else:
            name=t[1:-1]
            if name=='Path':grammar=grammar and stack==['Parallel']
            else:grammar=grammar and not stack
            stack.append(name)
    valid=valid and not stack
    blocks=re.findall(r'<Parallel>(.*?)</Parallel>',text,re.S)
    widths=[]; lengths=[]; duplicates=0
    for block in blocks:
        paths=re.findall(r'<Path>(.*?)</Path>',block,re.S)
        widths.append(len(paths)); lengths.extend(len(p) for p in paths)
        normalized=[' '.join(p.split()) for p in paths]
        duplicates+=len(normalized)-len(set(normalized))
    joins=re.findall(r'</Parallel>\s*<Summary>(.*?)</Summary>',text,re.S)
    strict=valid and grammar and all(w>=2 for w in widths) and len(joins)==len(blocks) and '<Parallel>' in text
    return dict(has_parallel='<Parallel>' in text,balanced_tags=valid,strict_parallel_format=strict,
                completed_blocks=len(blocks),widths=widths,exact_duplicate_paths=duplicates,
                path_characters=lengths,summary_characters=[len(x) for x in joins])

def analyze(name):
    folder=ROOT/'runs'/name
    results=[json.loads(x) for x in (folder/'results/eval'/name/'0.jsonl').read_text().splitlines()]
    questions={r['index']:r for r in map(json.loads,(ROOT/'questions.jsonl').read_text().splitlines())}
    assert len(results)==500 and len({r['sample_index'] for r in results})==500
    traces=defaultdict(list)
    for p in (folder/'traces').glob('traces-*.jsonl'):
        for line in p.open():
            r=json.loads(line);traces[int(r['trajectory']['sample_index'])].append(r)
    rows=[];texts={}
    for output in results:
        index=int(output['sample_index']);q=questions[index]
        matches=[t for t in traces[index] if clean(t['text'])==clean(output['output'])]
        assert matches,(name,index,'Missing runtime trace for scored output')
        t=matches[0];g=grade(t['text'],q['answer']);assert float(g['correct'])==output['acc']
        texts[index]=t['text']
        assert not g['error'],(index,g)
        calls=t['calls'];paths=[c for c in calls if c['phase']=='path']
        assert len(paths)==2*t['executed_fork_count'],(name,index,'Unexpected executed path count')
        raw_ids=[v for c in calls for v in c['generated_ids']]
        # Counts raw sampled control tags, independently of assembled repairs.
        token_ids={151669:'path_open',151670:'path_close',151671:'parallel_open',151672:'parallel_close',151673:'summary_open',151674:'summary_close'}
        raw_tags=Counter(token_ids[v] for v in raw_ids if v in token_ids)
        record=dict(index=index,id=q['id'],subject=q['subject'],level=q['level'],**g,**shape(t['text']),
            forks=t['executed_fork_count'],response_tokens=t['response_tokens'],generated_tokens=t['generated_tokens_total'],
            executed_widths=[2]*t['executed_fork_count'],
            first_fork_relative_position=t['parallel_relative_positions'][0] if t['parallel_relative_positions'] else None,
            path_token_share=sum(c['generated_tokens'] for c in paths)/max(t['generated_tokens_total'],1),
            phase_tokens={phase:sum(c['generated_tokens'] for c in calls if c['phase']==phase) for phase in ('main','path','summary')},
            critical_decode_depth=t['critical_depth'],critical_depth_ratio=t['generated_tokens_total']/max(t['critical_depth'],1),
            generation_calls=len(calls),path_generated_tokens=[c['generated_tokens'] for c in paths],
            raw_sampled_tags=dict(raw_tags),path_calls_without_sampled_close=sum(not c['generated_ids'] or c['generated_ids'][-1]!=151670 for c in paths),
            summary_calls_without_sampled_close=sum(not c['generated_ids'] or c['generated_ids'][-1]!=151674 for c in calls if c['phase']=='summary'),
            path_calls_at_token_cap=sum(c['generated_tokens']>=c['sampling_params']['max_tokens'] for c in paths),
            response_at_budget=t['response_tokens']>=30720,truncated=t['truncated'],
            duration_seconds=t['finished_at']-t['started_at'])
        rows.append(record)
    rows.sort(key=lambda r:r['index'])
    (folder/'trace-statistics.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    def group(items):
        return dict(n=len(items),correct=sum(r['correct'] for r in items),accuracy=sum(r['correct'] for r in items)/len(items) if items else None)
    k=sum(r['correct'] for r in rows)
    summary=dict(complete=True,model=name,questions=500,correct=k,accuracy=k/500,ci95=wilson(k,500),
        parallel_ratio=sum(r['forks']>0 for r in rows)/500,multi_round_ratio=sum(r['forks']>=2 for r in rows)/500,
        fork_histogram=dict(Counter(r['forks'] for r in rows)),
        executed_width_histogram=dict(Counter(w for r in rows for w in r['executed_widths'])),
        rendered_width_histogram=dict(Counter(w for r in rows for w in r['widths'])),
        first_fork_relative_position=stats([r['first_fork_relative_position'] for r in rows if r['first_fork_relative_position'] is not None]),
        path_token_share=stats([r['path_token_share'] for r in rows]),
        phase_tokens={phase:sum(r['phase_tokens'][phase] for r in rows) for phase in ('main','path','summary')},
        response_tokens=stats([r['response_tokens'] for r in rows]),generated_tokens=stats([r['generated_tokens'] for r in rows]),
        path_generated_tokens=stats([v for r in rows for v in r['path_generated_tokens']]),
        critical_decode_depth=stats([r['critical_decode_depth'] for r in rows]),
        theoretical_decode_work_over_depth=stats([r['critical_depth_ratio'] for r in rows]),
        generation_calls=stats([r['generation_calls'] for r in rows]),
        unbalanced_tags=sum(not r['balanced_tags'] for r in rows),
        strict_format_among_parallel=sum(r['strict_parallel_format'] for r in rows)/max(sum(r['has_parallel'] for r in rows),1),
        exact_duplicate_paths=sum(r['exact_duplicate_paths'] for r in rows),
        samples_with_duplicate_paths=sum(r['exact_duplicate_paths']>0 for r in rows),
        path_calls_without_sampled_close=sum(r['path_calls_without_sampled_close'] for r in rows),
        summary_calls_without_sampled_close=sum(r['summary_calls_without_sampled_close'] for r in rows),
        path_calls_at_token_cap=sum(r['path_calls_at_token_cap'] for r in rows),
        response_budget_exhausted=sum(r['response_at_budget'] for r in rows),truncated=sum(r['truncated'] for r in rows),
        invalid_final_answers=sum(not r['valid'] for r in rows),scorer_errors=0,
        accuracy_by_parallel={str(p):group([r for r in rows if (r['forks']>0)==p]) for p in (False,True)},
        accuracy_by_subject={s:group([r for r in rows if r['subject']==s]) for s in sorted({r['subject'] for r in rows})},
        accuracy_by_level={str(s):group([r for r in rows if r['level']==s]) for s in sorted({r['level'] for r in rows})},
        raw_trace_count=sum(len(v) for v in traces.values()),scored_unique_traces=500,
        limitations=['Two paths are imposed by runtime.','Decode work/depth is not measured wall-clock speedup.',
                     'Text equality only detects literal duplicate paths, not semantic duplication or valid reasoning.',
                     'Unseen custom mask/positions are not applied to vLLM continuation.'])
    (folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    selected={}
    for label,predicate in [('correct_parallel',lambda r:r['correct'] and r['forks']>0),
                            ('incorrect_parallel',lambda r:not r['correct'] and r['forks']>0),
                            ('multi_round',lambda r:r['forks']>=2),
                            ('duplicate_paths',lambda r:r['exact_duplicate_paths']>0),
                            ('budget_exhausted',lambda r:r['response_at_budget'])]:
        selected[label]=[dict(statistics=r,problem=questions[r['index']]['problem'],output=texts[r['index']])
                         for r in rows if predicate(r)][:3]
    (folder/'review-examples.json').write_text(json.dumps(selected,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('name');args=parser.parse_args();analyze(args.name)
