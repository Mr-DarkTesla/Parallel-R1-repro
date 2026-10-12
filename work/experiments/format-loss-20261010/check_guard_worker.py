"""Exercise the actual guarded worker sampling loop on CPU with scripted logits.

Model/attention/CUDA ownership are mocked; real tokenizer and unmodified worker
function are used. This verifies integration, not model accuracy or GPU execution.
"""
import ast
import datetime
import hashlib
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

import torch
from transformers import AutoTokenizer

C = Path(__file__).resolve().parent
P = C.parents[2]
D = P / 'work/experiments/instruct-token-warmup-20261010'
E = C / 'evaluations'
sys.path.insert(0, str(E))
from native_eos import native_eos_ids

model_path = D / 'runs/production/final'
tok = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
ids = lambda text: tok.encode(text, add_special_tokens=False)
one = lambda text: ids(text)[0]
eos = native_eos_ids(model_path)
worker_file = E / 'runtime/verl/workers/rollout/vllm_rollout/structured_worker.py'
tree = ast.parse(worker_file.read_text())
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'structured_generate')


class ScriptedHF:
    def __init__(self, logits):
        self.sequence = logits
        self.index = 0
    def parameters(self):
        yield torch.zeros(1)
    def __call__(self, **kwargs):
        logits = torch.full((1, 1, len(tok)), -100.)
        for token, score in self.sequence[min(self.index, len(self.sequence) - 1)].items():
            logits[0, 0, token] = score
        self.index += 1
        return SimpleNamespace(logits=logits, past_key_values=None)


class Source:
    config = SimpleNamespace(model_type='qwen3')
    def parameters(self):
        yield torch.zeros(1)


dist = ModuleType('vllm.distributed')
dist.get_tensor_model_parallel_world_size = lambda: 1
dist.get_pp_group = lambda: SimpleNamespace(world_size=1)
reports = []


def run(phase, logits, expected, stops):
    hf = ScriptedHF(logits)
    env = {'torch': torch,
           'hf_weight_view': lambda source, cached=None: hf,
           'validate_sampling': lambda params, evaluation_only: None,
           'layout': lambda tokens, *args, **kwargs: (torch.arange(len(tokens)), None),
           'attention': lambda tokens, *args, **kwargs: torch.ones(len(tokens), len(tokens), dtype=torch.bool).tril()}
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(worker_file), 'exec'), env)
    instance = SimpleNamespace(model_runner=SimpleNamespace(model=Source()))
    params = dict(_evaluation_only=True, _format_phase=phase,
                  _format_eos_ids=eos, _format_model_path=str(model_path),
                  max_tokens=4, temperature=0, stop_token_ids=stops)
    with patch.dict(sys.modules, {'vllm': ModuleType('vllm'), 'vllm.distributed': dist}):
        output = env['structured_generate'](instance, ids('<think>\n'), params, 0,
                                           [one(t) for t in ['<Parallel>', '</Parallel>', '<Path>', '</Path>']], tok.pad_token_id)
    assert output == expected, (phase, output, expected)
    reports.append(dict(phase=phase, output=output, passed=True))


run('main', [{one('</think>'): 10., one('<Parallel>'): 9.},
             {one('<Parallel>'): 10., eos[0]: 9.}],
    [one('</think>'), eos[0]], eos)
run('width', [{one(' '): 10., one('3'): 9.},
              {one(' '): 10., one('\n'): 9.}],
    [one('3'), one('\n')], [one('\n')])
for phase, terminal in [('path', '</Path>'), ('summary', '</Summary>')]:
    run(phase, [{eos[0]: 12., one('</think>'): 11., one('<Parallel>'): 10., one(terminal): 9.}],
        [one(terminal)], [one(terminal), *eos])

proof = dict(passed=True, CPU_only=True, GPU_launched=False,
             at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             cases=reports, tokenizer=str(model_path), worker_sha256=hashlib.sha256(worker_file.read_bytes()).hexdigest(),
             limitation='Scripted CPU logits and mocked attention/ownership; no GPU/model correctness claim')
(C / 'guard-worker-cpu-proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof), flush=True)
