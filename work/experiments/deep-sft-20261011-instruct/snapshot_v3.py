"""Read durable live records; never writes controller inputs."""
from pathlib import Path
import collections,json,time
b=Path('work/experiments/deep-sft-20261011-instruct/production-v3')
status=json.loads((b/'status.json').read_text())
rows=[json.loads(s) for s in (b/'journal.jsonl').read_text().splitlines()] if (b/'journal.jsonl').exists() else []
accepted=[r['row'] for r in rows if r['decision']=='accepted']
raw=[json.loads(s) for s in (b/'teacher-responses.jsonl').read_text().splitlines()] if (b/'teacher-responses.jsonl').exists() else []
elapsed=time.time()-status['started_at']
tokens=sum((r['response'].get('usage') or {}).get('completion_tokens',0) for r in raw)
result=dict(status=status,elapsed_s=elapsed,completed=len(rows),accepted=len(accepted),raw_responses=len(raw),
            new_accepted=max(0,len(accepted)-554),new_completed=max(0,len(rows)-571),accepted_per_minute=max(0,len(accepted)-554)*60/elapsed,teacher_completion_tokens=tokens,teacher_tokens_per_second=tokens/elapsed,
            acceptance_rate=len(accepted)/len(rows) if rows else None,
            rounds=dict(collections.Counter(r['fork_count'] for r in accepted)),
            widths=dict(collections.Counter(w for r in accepted for w in r['branch_schedule'])),
            errors=dict(collections.Counter(r.get('error') for r in rows if r['decision']!='accepted')))
(b/'live-snapshot.json').write_text(json.dumps(result,indent=2)+'\n')
(b/'accepted-so-far.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in accepted))
print(json.dumps(result,indent=2))
