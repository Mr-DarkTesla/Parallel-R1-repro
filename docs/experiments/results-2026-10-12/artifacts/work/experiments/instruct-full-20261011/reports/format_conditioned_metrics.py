"""CPU-only audit of saved traces; shape statistics conditioned on valid format."""
from pathlib import Path
import hashlib,json,statistics
R=Path.cwd();E=R/'work/experiments/rl-instruct-20261011'

def read_rows(paths):
    rows=[json.loads(l) for p in paths for l in p.read_text().splitlines() if l.strip()]
    assert len({r['id'] for r in rows})==len(rows)
    return rows

def groups_from_calls(calls):
    groups=[];current=None
    for c in calls:
        if c['phase']=='width':
            current=dict(paths=0,summary=False)
            groups.append(current)
        elif c['phase']=='path':
            assert current is not None
            current['paths']+=1
        elif c['phase']=='summary':
            assert current is not None
            current['summary']=True
    return [g['paths'] for g in groups if g['paths']>=2 and g['summary']]

runs=[
 ('Original Instruct',R/'work/experiments/instruct-token-warmup-20261010/evaluations/original-native-128','native'),
 ('Instruct +6token rows',R/'work/experiments/instruct-full-20261011/evaluations/warmup-lr1e3-guard-structured-128','warmup'),
 ('Full SFT42',E/'math500-fullwidth8/runs/001-fullSFT-baseline','instrumented'),
 ('RL R1 step64',E/'math500-priority-RL64/runs/R1-checkpoint-0064','instrumented'),
 ('RL R2 step64',E/'math500-priority-RL64/runs/R2-checkpoint-0064','instrumented')]
output=[]
for label,directory,kind in runs:
    paths=[directory/'scores.jsonl'] if kind in ['native','warmup'] else sorted(directory.glob('rank-*.jsonl'))
    rows=read_rows(paths)
    if kind!='instrumented':rows=[r for r in rows if r['dataset']=='math']
    assert len(rows)==(500 if kind=='instrumented' else 64)
    valid=[r for r in rows if r['format_valid']]
    assert valid
    widths=[];rounds=[];forwards=[];sampled=[];pairs=[]
    for r in valid:
        if kind=='native':
            w=[];f=r['stats']['sampled_tokens']
            assert r['stats']['forks']==0 and r['stats']['generation_calls']==1
        elif kind=='warmup':
            calls=r['trace']['policy_calls']
            w=groups_from_calls(calls)
            f=sum(len(c['generated_ids']) for c in calls)
            assert f==r['stats']['sampled_tokens']==r['trace']['generated_tokens_total']
        else:
            w=r['widths'];f=r['instrumented_forward_calls']
            assert f==r['stats']['actual_model_forward_calls']
        assert len(w)==r['stats']['forks'],(label,r['id'],w,r['stats'])
        assert all(2<=v<=8 for v in w)
        widths.extend(w);rounds.append(len(w));forwards.append(f);sampled.append(r['stats']['sampled_tokens'])
        pairs.append(dict(id=r['id'],correct=bool(r['grade']['correct']),forwards=f,widths=w,rounds=len(w)))
    record=dict(model=label,suite='MATH500' if kind=='instrumented' else 'MATH64 from mixed128',
        total=len(rows),correct=sum(bool(r['grade']['correct']) for r in rows),
        accuracy_all_pct=100*sum(bool(r['grade']['correct']) for r in rows)/len(rows),
        valid_format_count=len(valid),valid_format_pct=100*len(valid)/len(rows),
        accuracy_given_valid_format_pct=100*sum(bool(r['grade']['correct']) for r in valid)/len(valid),
        mean_F_given_valid_format=statistics.mean(forwards),median_F_given_valid_format=statistics.median(forwards),
        mean_width_given_valid_format=sum(widths)/len(widths) if widths else None,
        width_denominator_rounds=len(widths),mean_rounds_given_valid_format=statistics.mean(rounds),
        total_rounds_given_valid_format=sum(rounds),max_rounds_given_valid_format=max(rounds),
        forked_tasks_given_valid_format=sum(v>0 for v in rounds),
        forked_task_fraction_given_valid_format=sum(v>0 for v in rounds)/len(valid),
        mean_sampled_tokens_given_valid_format=statistics.mean(sampled),
        forward_kind='instrumented physical generation forwards' if kind=='instrumented' else 'reconstructed serial AR forwards; not instrumented',
        source=str(directory),source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        task_rows=pairs)
    output.append(record)
    print(json.dumps({k:v for k,v in record.items() if k not in ['source_sha256','task_rows']},ensure_ascii=False))
report=dict(passed=True,definition='Accuracy_all uses every task; all cost/width/depth statistics condition on format_valid. Serial valid tasks count as depth0; mean width averages executed completed rounds only, not textual tags.',models=output,
    historical_format_schema_caveat='MATH64 native/warmup use their saved basic schema_v2; MATH500 uses canonical counted Instruct schema. Different suites/backends must not be interpreted as matched improvements.')
path=R/'work/experiments/instruct-full-20261011/reports/format-conditioned-metrics-20261012.json'
path.write_text(json.dumps(report,indent=2)+'\n')
print('REPORT',str(path))
