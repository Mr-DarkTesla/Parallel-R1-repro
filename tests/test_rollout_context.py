"""Call-batched PPO log-probabilities/gradients must match independent causal replay."""
from unittest import TestCase, main
from unittest.mock import patch

import torch
from transformers import Qwen3Config, Qwen3ForCausalLM
from verl.workers.actor.rollout_context import forward_rollout_calls


def logp(logits, labels, **kwargs):
    return logits.log_softmax(-1).gather(-1, labels[..., None]).squeeze(-1)


class ContextTest(TestCase):
    def test_replay_values_and_gradients(self):
        torch.set_num_threads(1); torch.manual_seed(31)
        config = Qwen3Config(vocab_size=40, hidden_size=32, intermediate_size=64,
                            num_hidden_layers=2, num_attention_heads=4, num_key_value_heads=2, head_dim=8)
        config._attn_implementation = 'sdpa'
        model = Qwen3ForCausalLM(config).eval()
        # Two independent paths; summary recomputes both paths in ordinary causal context.
        calls = [[dict(prompt_ids=[1, 2], generated_ids=[3], response_start=0),
                  dict(prompt_ids=[1, 2, 3, 4], generated_ids=[5, 6], response_start=2),
                  dict(prompt_ids=[1, 2, 3, 4], generated_ids=[7, 0], response_start=5, temperature=1.0),
                  dict(prompt_ids=[1, 2, 3, 4, 5, 6, 4, 7, 8, 9], generated_ids=[10, 11], response_start=8)],
                 [], [dict(prompt_ids=[1], generated_ids=[12, 13, 14], response_start=0)]]
        responses = torch.zeros((3, 12), dtype=torch.long)  # Labels must come from calls, not these slots.
        weights = torch.randn(3, 12)
        results = []
        for batched in (False, True):
            model.zero_grad(set_to_none=True)
            if batched:
                with patch('verl.workers.actor.rollout_context.logprobs_from_logits', logp):
                    entropy, scores = forward_rollout_calls(model, calls, responses, .8, True)
                loss = ((scores + .01 * entropy) * weights).sum()
                values = scores.detach()
            else:
                loss = 0; values = torch.zeros_like(weights)
                for owner, row in enumerate(calls):
                    for call in row:
                        p, g, start = call['prompt_ids'], call['generated_ids'], call['response_start']
                        ids = torch.tensor([p + g]); logits = model(ids, use_cache=False).logits[0, len(p)-1:-1] / call.get('temperature', .8)
                        scores = logp(logits, torch.tensor(g))
                        entropy = -(logits.softmax(-1) * logits.log_softmax(-1)).sum(-1)
                        values[owner, start:start+len(g)] = scores.detach()
                        loss = loss + ((scores + .01 * entropy) * weights[owner, start:start+len(g)]).sum()
            loss.backward()
            results.append((values, torch.cat([p.grad.flatten() for p in model.parameters()])))
        for reference, actual in zip(*results):
            torch.testing.assert_close(actual, reference, atol=3e-6, rtol=3e-5)
        model.zero_grad(set_to_none=True)
        _, empty = forward_rollout_calls(model, [[], [], []], responses, 1)
        empty.sum().backward()
        self.assertEqual(empty.abs().sum().item(), 0)
        self.assertTrue(all(p.grad is not None and p.grad.abs().sum() == 0 for p in model.parameters()))


if __name__ == '__main__':
    main()
