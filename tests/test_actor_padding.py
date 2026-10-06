"""Compare trimmed and padded custom attention on a tiny real Qwen3 (CPU)."""
import ast
import contextlib
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch
from transformers import Qwen3Config, Qwen3ForCausalLM

SOURCE = Path(__file__).resolve().parents[1] / 'verl/verl/workers/actor/dp_actor.py'
tree = ast.parse(SOURCE.read_text())
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'DataParallelPPOActor')
method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '_forward_micro_batch')
ns = dict(torch=torch, logprobs_from_logits=lambda logits, labels: logits.log_softmax(-1).gather(-1, labels[..., None]).squeeze(-1),
          verl_F=SimpleNamespace(entropy_from_logits=lambda logits: -(logits.softmax(-1) * logits.log_softmax(-1)).sum(-1)))
exec(compile(ast.Module(body=[method], type_ignores=[]), str(SOURCE), 'exec'), ns)


class Config(dict):
    entropy_checkpointing = False


class PaddingTest(unittest.TestCase):
    def test_logprobs_entropy_and_gradients(self):
        torch.set_num_threads(1)
        torch.manual_seed(7)
        config = Qwen3Config(vocab_size=40, hidden_size=32, intermediate_size=64,
                            num_hidden_layers=2, num_attention_heads=4, num_key_value_heads=2, head_dim=8)
        config._attn_implementation = 'sdpa'
        model = Qwen3ForCausalLM(config).eval()
        model.register_forward_pre_hook(
            lambda module, args, kwargs: (args, {**kwargs, 'attention_mask': kwargs['attention_mask'].float()}),
            with_kwargs=True)
        actor = SimpleNamespace(config=Config(), actor_module=model, device_name='cpu',
                                use_remove_padding=False, use_fused_kernels=False)
        for lefts, lengths, paths in [([3, 1], [6, 4], True), ([0, 2], [8, 8], True),
                                      ([4, 4], [1, 1], False), ([3, 2], [0, 0], False)]:
            with self.subTest(lefts=lefts, lengths=lengths, paths=paths):
                ids = torch.randint(1, 40, (2, 16))
                mask = torch.zeros_like(ids)
                for i, (left, length) in enumerate(zip(lefts, lengths)):
                    mask[i, left:8 + length] = 1
                positions = (mask.cumsum(-1) - 1).clamp_min(0)
                if paths:
                    positions[:, 10:12] = positions[:, 8:10]
                batch = dict(input_ids=ids, responses=ids[:, 8:], attention_mask=mask,
                             position_ids=positions, left_pad_lens=lefts,
                             position_required_masks=[[[left, 8, 10, 10, 12]] if paths else [] for left in lefts])
                valid = mask[:, 8:].bool()
                outputs = []
                for trim, trim_logits in ((False, False), (False, True), (True, True)):
                    actor.config['trim_parallel_padding'] = trim
                    actor.config['trim_prompt_logits'] = trim_logits
                    model.zero_grad(set_to_none=True)
                    # Float32 isolates indexing/mask equivalence from bf16 rounding.
                    with patch.object(torch, 'autocast', lambda **kw: contextlib.nullcontext()):
                        entropy, logp = ns['_forward_micro_batch'](actor, batch, 1.0, True)
                        (logp[valid].sum() + .01 * entropy[valid].sum()).backward()
                    outputs.append((logp.detach()[valid], entropy.detach()[valid],
                                    torch.cat([p.grad.flatten() for p in model.parameters() if p.grad is not None])))
                for candidate in outputs[1:]:
                    for reference, actual in zip(outputs[0], candidate):
                        torch.testing.assert_close(reference, actual, atol=2e-6, rtol=2e-5)


if __name__ == '__main__':
    unittest.main()
