"""Small deterministic inference set; no training or sample selection by outcome."""
import json
import os
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

root = Path(os.getenv('PARALLEL_R1_ROOT', str(Path.home() / 'parallel-r1')))
rows = []
train = pq.read_table(root / 'data/s1_train.parquet').to_pylist()
val = pq.read_table(root / 'data/s1_val.parquet').to_pylist()
sft = pq.read_table(root / 'data/sft_reference.parquet').to_pylist()
for category, selected in [('GSM8K_SFT_reference', sft[:2]), ('DAPO_train', train[:2])]:
    for i, row in enumerate(selected):
        rows.append(dict(data_source='math_dapo', prompt=row['prompt'], ability='MATH',
                         reward_model=row['reward_model'], index=f'{category}-{i}',
                         extra_info=dict(reward_method='accuracy_reward', preview_source=category)))
for category in sorted({r['data_source'] for r in val}):
    for i, row in enumerate([r for r in val if r['data_source'] == category][:1]):
        row = dict(row)
        row['index'] = f'{category}-{i}'
        row['extra_info'] = dict(reward_method='accuracy_reward', preview_source=category)
        rows.append(row)
pq.write_table(pa.Table.from_pylist(rows), root / 'data/preview.parquet')
(root / 'data/preview_questions.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
print('Preview questions:', len(rows))
