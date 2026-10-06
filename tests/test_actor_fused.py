"""CUDA numerical check for fused PPO with trimmed custom parallel attention."""
from types import MethodType, SimpleNamespace
import unittest
from unittest.mock import patch
import torch
from transformers import Qwen3Config, Qwen3ForCausalLM
from test_actor_padding import Config, ns


@unittest.skipUnless(torch.cuda.is_available(), 'CUDA required for Triton PPO kernel')
class FusedActorTest(unittest.TestCase):
    def test_parallel_logprobs_and_gradients(self):
        for vocab_size in (1024, 1031, 151675):
            with self.subTest(vocab_size=vocab_size):
                self.check_vocab(vocab_size)

    def check_vocab(self, vocab_size):
        from verl.models.transformers.dense_common import forward_with_triton_backend
        from verl.utils import torch_functional as functional
        torch.manual_seed(9)
        config = Qwen3Config(vocab_size=vocab_size, hidden_size=128, intermediate_size=256,
                            num_hidden_layers=2, num_attention_heads=4, num_key_value_heads=2, head_dim=32)
        config._attn_implementation = 'sdpa'
        model = Qwen3ForCausalLM(config).to(device='cuda', dtype=torch.bfloat16).eval()
        original = model.forward
        actor = SimpleNamespace(config=Config(), actor_module=model, device_name='cuda', use_remove_padding=False)
        ids = torch.randint(1, vocab_size, (2, 16), device='cuda')
        ids[0, 12] = vocab_size - 1
        mask = torch.zeros_like(ids);mask[0, 3:14] = 1;mask[1, 1:12] = 1
        positions = (mask.cumsum(-1)-1).clamp_min(0);positions[:, 10:12] = positions[:, 8:10]
        batch = dict(input_ids=ids, responses=ids[:, 8:], attention_mask=mask, position_ids=positions,
                     left_pad_lens=[3, 1], position_required_masks=[[[3, 8, 10, 10, 12]], [[1, 8, 10, 10, 12]]])
        valid = mask[:, 8:].bool();coeff = torch.randn(2, 8, device='cuda')
        results = []
        with patch.dict(ns, verl_F=functional, logprobs_from_logits=lambda logits, labels: functional.logprobs_from_logits(logits, labels, inplace_backward=False)):
            for fused, trim in [(False, False), (False, True), (True, True)]:
                actor.use_fused_kernels = fused;actor.config['trim_parallel_padding'] = trim
                model.forward = MethodType(forward_with_triton_backend, model) if fused else original
                model.zero_grad(set_to_none=True)
                entropy, logp = ns['_forward_micro_batch'](actor, batch, 1.0, True)
                ((logp * coeff + .01 * entropy) * valid).sum().backward()
                results.append((logp.detach()[valid].float(), entropy.detach()[valid].float(),
                                torch.cat([p.grad.flatten().float() for p in model.parameters() if p.grad is not None])))
        for actual in results[1:]:
            torch.testing.assert_close(actual[0], results[0][0], atol=.01, rtol=.002)
            torch.testing.assert_close(actual[1], results[0][1], atol=.01, rtol=.002)
            relative = (actual[2]-results[0][2]).norm()/results[0][2].norm()
            print('gradient_relative_l2', relative.item())
            self.assertLess(relative.item(), .015)


if __name__ == '__main__':
    unittest.main()
