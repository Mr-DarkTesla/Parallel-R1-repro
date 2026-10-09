"""Shared parallel-thinking contract: plan grammar, tag suppression, graph positions and mask, D/T.

python -m unittest tests.test_contract
"""
import importlib.util
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('contract', ROOT / 'verl/verl/parallel_thinking_generation_v3/contract.py')
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)
Span = contract.Span


class Tokenizer:
    def encode(self, text, **kwargs):
        return [100 + contract.TAGS.index(text)] if text in contract.TAGS else [ord(c) for c in text]


class PlanTest(unittest.TestCase):
    def test_valid_plans(self):
        self.assertEqual(contract.parse_plan('cases\n1: x > 0\n2: x <= 0\n'),
                         contract.Plan('cases', ('x > 0', 'x <= 0')))
        self.assertEqual(contract.parse_plan('verify\r\n1:  a \r\n2:b\r\n3: c'),
                         contract.Plan('verify', ('a', 'b', 'c')))
        four = 'decompose\n' + ''.join(f'{i}: part {i}\n' for i in range(1, 5))
        self.assertEqual(len(contract.parse_plan(four).items), 4)

    def test_invalid_plans(self):
        for text in ['guess\n1: a\n2: b', 'cases\n1: a', 'cases\n' + ''.join(f'{i}: a\n' for i in range(1, 6)),
                     'cases\n1: a\n3: b', 'cases\n2: a\n1: b', 'cases\n1: a\n2: ', 'cases\n1: a\n\n2: b',
                     'cases\n1: a\n2: b\n\n', 'cases\n1: a\nso 2: b', '\ncases\n1: a\n2: b', '']:
            self.assertIsNone(contract.parse_plan(text), repr(text))

    def test_status(self):
        good = 'methods\n1: algebra\n2: geometry\n'
        self.assertEqual(contract.plan_status(good, 'close'), contract.VALID)
        self.assertEqual(contract.plan_status('methods\n1: a', 'close'), contract.INVALID_PLAN)
        self.assertEqual(contract.plan_status(good, 'eos'), contract.PLAN_INCOMPLETE)
        self.assertEqual(contract.plan_status(good, 'budget'), contract.PLAN_BUDGET_EXHAUSTED)

    def test_path_prefix_has_no_trailing_space(self):
        self.assertEqual(contract.path_prefix(3), '3:')
        self.assertEqual(contract.path_prefix_ids(Tokenizer(), 2), [ord('2'), ord(':')])


class SuppressionTest(unittest.TestCase):
    def setUp(self):
        self.ids = contract.tag_ids(Tokenizer())

    def test_each_node_samples_only_its_tag(self):
        self.assertEqual(contract.main_node(0), contract.MAIN_OPEN)
        self.assertEqual(contract.main_node(2), contract.MAIN_CLOSED)
        self.assertEqual(contract.main_node(0, allow_parallel=False), contract.MAIN_CLOSED)
        for node, tag in contract.SAMPLED_TAG.items():
            allowed = set(contract.TAGS) - set(contract.suppressed_tags(node))
            self.assertEqual(allowed, set() if tag is None else {tag})
        self.assertEqual(contract.logit_bias(contract.PLAN, self.ids),
                         {self.ids[t]: -100.0 for t in contract.TAGS if t != '</Plan>'})

    def test_tag_ids_must_be_single_distinct_tokens(self):
        class Split(Tokenizer):
            def encode(self, text, **kwargs):
                return [1, 2] if text == '<Plan>' else super().encode(text)
        with self.assertRaises(ValueError):
            contract.tag_ids(Split())

    def test_actor_suppression_equals_sampling_bias(self):
        table = contract.suppression_table(self.ids)
        logits = torch.randn(2, 6, 110)
        nodes = torch.tensor([[0, 1, 2, 3, 4, -1], [4, 3, 2, 1, 0, -1]])
        expected = logits.clone()
        for row in range(2):
            for column in range(6):
                node = nodes[row, column].item()
                if node >= 0:
                    for token, bias in contract.logit_bias(node, self.ids).items():
                        expected[row, column, token] += bias
        actual = contract.apply_suppression(logits.clone(), nodes, table)
        torch.testing.assert_close(actual, expected)


class GraphTest(unittest.TestCase):
    # prompt-relative layout: 0-2 main, 3-5 path 1, 6-10 path 2, 11-12 summary, 13-14 main,
    # 15-16 path 1 of block 2, 17-17 path 2 of block 2, 18 after.
    spans = [Span(3, 6, 0, 1), Span(6, 11, 0, 2), Span(15, 17, 1, 1), Span(17, 18, 1, 2)]

    def test_positions(self):
        positions = contract.graph_positions(19, self.spans, first=10)
        self.assertEqual(positions[:3], [10, 11, 12])
        self.assertEqual(positions[3:6], [13, 14, 15])
        self.assertEqual(positions[6:11], [13, 14, 15, 16, 17])
        self.assertEqual(positions[11:15], [18, 19, 20, 21])  # </Parallel> = longest branch end + 1
        self.assertEqual(positions[15:18], [22, 23, 22])
        self.assertEqual(positions[18], 24)

    def test_positions_of_a_truncated_block(self):
        self.assertEqual(contract.graph_positions(8, self.spans), [0, 1, 2, 3, 4, 5, 3, 4])
        self.assertEqual(contract.graph_positions(16, self.spans), contract.graph_positions(19, self.spans)[:16])

    def test_branches_must_be_adjacent(self):
        with self.assertRaises(AssertionError):
            contract.graph_positions(12, [Span(3, 6, 0, 1), Span(7, 11, 0, 2)])

    def test_mask_isolates_only_sibling_branches(self):
        mask = contract.graph_attention_mask(21, self.spans, offset=2)
        causal = torch.ones(21, 21, dtype=torch.bool).tril()
        self.assertFalse(mask[2 + 6, 2 + 3:2 + 6].any())  # path 2 never sees path 1
        self.assertTrue(mask[2 + 11, 2 + 3:2 + 11].all())  # the summary sees both
        self.assertTrue(mask[2 + 15, 2 + 3:2 + 11].all())  # block 2 sees block 1's branches
        self.assertFalse(mask[2 + 17, 2 + 15:2 + 17].any())
        changed = (mask != causal).nonzero().tolist()
        self.assertEqual(len(changed), 3 * 5 + 2 * 1)
        self.assertEqual(sorted(contract.isolation_pairs(self.spans)),
                         sorted([(self.spans[0], self.spans[1]), (self.spans[1], self.spans[0]),
                                 (self.spans[2], self.spans[3]), (self.spans[3], self.spans[2])]))


class DepthTest(unittest.TestCase):
    def test_depth_and_tokens(self):
        calls = [dict(node=contract.MAIN_OPEN, block=None, sampled=10), dict(node=contract.PLAN, block=0, sampled=6),
                 dict(node=contract.PATH, block=0, sampled=20), dict(node=contract.PATH, block=0, sampled=35),
                 dict(node=contract.PATH, block=0, sampled=5), dict(node=contract.SUMMARY, block=0, sampled=8),
                 dict(node=contract.MAIN_CLOSED, block=None, sampled=12)]
        self.assertEqual(contract.depth_and_tokens(calls), (10 + 6 + 35 + 8 + 12, 10 + 6 + 60 + 8 + 12))
        failed = [dict(node=contract.MAIN_OPEN, block=None, sampled=4), dict(node=contract.PLAN, block=0, sampled=9)]
        self.assertEqual(contract.depth_and_tokens(failed), (13, 13))


if __name__ == '__main__':
    unittest.main()
