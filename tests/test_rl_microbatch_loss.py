"""Larger microbatches must retain the original microbatch-1 sequence weights."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
import torch

SOURCE = Path(__file__).resolve().parents[1] / 'verl/verl/trainer/ppo/core_algos.py'
nodes = [n for n in ast.parse(SOURCE.read_text()).body
         if isinstance(n, ast.FunctionDef) and n.name in ('agg_loss', 'compute_policy_loss')]
ns = dict(torch=torch, verl_F=SimpleNamespace(masked_mean=lambda x, mask: (x * mask).sum() / (mask.sum() + 1e-8)))
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), 'exec'), ns)


class MicrobatchLossTest(unittest.TestCase):
    def test_ppo_loss_and_gradient_match_microbatch_one(self):
        torch.manual_seed(5)
        old = torch.randn(4, 13)
        initial = old + torch.randn_like(old) * .4
        advantages = torch.randn_like(old)
        mask = torch.arange(13)[None, :] < torch.tensor([13, 7, 1, 0])[:, None]
        outcomes = []
        for size, mode in [(1, 'token-mean'), (2, 'seq-mean-token-mean'), (4, 'seq-mean-token-mean')]:
            logp = initial.clone().requires_grad_()
            total = 0
            for start in range(0, 4, size):
                sl = slice(start, start + size)
                loss = ns['compute_policy_loss'](old[sl], logp[sl], advantages[sl], mask[sl],
                                                cliprange=.2, clip_ratio_c=3., loss_agg_mode=mode)[0]
                total = total + loss * size / 4
            total.backward()
            outcomes.append((total.detach(), logp.grad))
        for outcome in outcomes[1:]:
            for expected, actual in zip(outcomes[0], outcome):
                torch.testing.assert_close(actual, expected, atol=1e-7, rtol=1e-6)


if __name__ == '__main__':
    unittest.main()
