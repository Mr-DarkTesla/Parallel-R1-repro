"""Create a separate train.py; do not edit frozen baseline or launch GPU work."""
from pathlib import Path
import ast
import hashlib

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'baseline_train.py').read_text()
expected = 'bdeabce08d10423708fb0b21a2319b755616df34e5c8070145815b9d6ba0b28d'
if hashlib.sha256(source.encode()).hexdigest() != expected:
    raise RuntimeError('Frozen baseline source differs')
replacements = [
    ('from data import build_sample',
     'from data import build_sample\nfrom format_loss import attach_format_mask, weighted_ce'),
    ("D=Path(__file__).resolve().parent;P=D.parents[2];N=P/'work/experiments/night-20261010'",
     "D=Path(__file__).resolve().parent;P=D.parents[2];A=P/'work/experiments/instruct-token-warmup-20261010';N=P/'work/experiments/night-20261010'\nLOSS_EPOCH=1"),
    ('self.samples=[build_sample(r,tok,system,max_length=8192) for r in rows]',
     'self.samples=[attach_format_mask(build_sample(r,tok,system,max_length=8192),r,tok) for r in rows]'),
    ('loss=(ce*targets).sum()/targets.sum().clamp_min(1)',
     'loss=weighted_ce(ce,sample,LOSS_EPOCH) if model.training else (ce*targets).sum()/targets.sum().clamp_min(1)'),
    ("AutoTokenizer.from_pretrained(D/'tokenizer',local_files_only=True);proof=json.loads((D/'tokenizer-proof.json').read_text());system=(D/'system.txt').read_text()",
     "AutoTokenizer.from_pretrained(A/'tokenizer',local_files_only=True);proof=json.loads((A/'tokenizer-proof.json').read_text());system=(A/'system.txt').read_text()"),
    ("D/'initial-rows.safetensors'", "A/'initial-rows.safetensors'"),
    ('def main():\n', 'def main():\n    global LOSS_EPOCH\n'),
    ('for epoch in range(epochs):\n        sampler.set_epoch(epoch)',
     'for epoch in range(epochs):\n        LOSS_EPOCH=epoch+1\n        sampler.set_epoch(epoch)'),
    ('optimizer.zero_grad(set_to_none=True);loss_sum=0.;tokens=0;targets=0',
     "LOSS_EPOCH=(1 if step==0 else 2) if a.stage=='smoke' else epoch+1\n            optimizer.zero_grad(set_to_none=True);loss_sum=0.;tokens=0;targets=0"),
    ("'frozen_parameter_versions_unchanged':True}",
     "'frozen_parameter_versions_unchanged':True,'loss_phase':'format_only' if LOSS_EPOCH==1 else 'format_x5','format_weight':1 if LOSS_EPOCH==1 else 5}"),
]
for before, after in replacements:
    if source.count(before) != 1:
        raise RuntimeError(f'Unexpected baseline match count: {before}')
    source = source.replace(before, after)
ast.parse(source)
destination = ROOT / 'train.py'
if destination.exists() and destination.read_text() != source:
    raise FileExistsError('Refuse overwriting a different candidate')
destination.write_text(source)
print(hashlib.sha256(source.encode()).hexdigest())
