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
        return [200 + contract.TAGS.index(text)] if text in contract.TAGS else [ord(c) for c in text]


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

    def test_declared_count_must_match_the_plan(self):
        three = 'cases\n1: a\n2: b\n3: c\n'
        self.assertEqual(len(contract.parse_plan(three, 3).items), 3)
        for branches in (2, 4):
            self.assertIsNone(contract.parse_plan(three, branches))
            self.assertEqual(contract.plan_status(three, 'close', branches), contract.INVALID_PLAN)
        self.assertEqual(contract.plan_status(three, 'close', 3), contract.VALID)
        self.assertEqual(contract.COUNTS, ('2', '3', '4'))

    def test_format_block_is_the_v2_serialization(self):
        text = contract.format_block('cases', ['x > 0', 'x <= 0'], [' if x > 0 then 1', ' else 0'], ' 1 or 0')
        self.assertEqual(text, '<Parallel>branches=2<Plan>cases\n1: x > 0\n2: x <= 0\n</Plan>'
                               '<Path>1: if x > 0 then 1</Path><Path>2: else 0</Path></Parallel><Summary> 1 or 0</Summary>')
        self.assertEqual(contract.CONTRACT_VERSION, 2)
        with self.assertRaises(AssertionError):
            contract.format_block('cases', ['a\nb', 'c'], [' x', ' y'], '')

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

    def test_count_samples_only_the_digits(self):
        counts = contract.count_ids(Tokenizer())
        self.assertEqual(counts, (ord('2'), ord('3'), ord('4')))
        self.assertEqual(contract.branches_ids(Tokenizer()), [ord(c) for c in 'branches='])
        self.assertEqual(contract.sampling_constraint(contract.COUNT, self.ids, counts),
                         dict(allowed_token_ids=list(counts)))
        self.assertEqual(contract.sampling_constraint(contract.PATH, self.ids, counts),
                         dict(logit_bias=contract.logit_bias(contract.PATH, self.ids)))

        class Merged(Tokenizer):
            def encode(self, text, **kwargs):
                return [1, 2] if text == '3' else super().encode(text)
        with self.assertRaises(ValueError):
            contract.count_ids(Merged())

    def test_tag_ids_must_be_single_distinct_tokens(self):
        class Split(Tokenizer):
            def encode(self, text, **kwargs):
                return [1, 2] if text == '<Plan>' else super().encode(text)
        with self.assertRaises(ValueError):
            contract.tag_ids(Split())

    def test_actor_suppression_equals_sampling_bias(self):
        counts = contract.count_ids(Tokenizer())
        table = contract.suppression_table(self.ids, counts)
        logits = torch.randn(2, 7, 210)
        nodes = torch.tensor([[0, 1, 2, 3, 4, 5, -1], [5, 4, 3, 2, 1, 0, -1]])
        expected = logits.clone()
        for row in range(2):
            for column in range(7):
                node = nodes[row, column].item()
                if node == contract.COUNT:  # vLLM allowed_token_ids: every other token is (almost) impossible
                    others = torch.ones(210, dtype=torch.bool)
                    others[list(counts)] = False
                    expected[row, column, others] += contract.SUPPRESS_BIAS
                elif node >= 0:
                    for token, bias in contract.logit_bias(node, self.ids).items():
                        expected[row, column, token] += bias
        actual = contract.apply_suppression(logits.clone(), nodes, table)
        torch.testing.assert_close(actual, expected)
        count = actual[0, 5].log_softmax(-1)[list(counts)]
        torch.testing.assert_close(count, logits[0, 5, list(counts)].log_softmax(-1))  # exactly renormalized
        self.assertTrue(torch.equal(actual[0, 5, list(counts)], logits[0, 5, list(counts)]))


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
        calls = [dict(node=contract.MAIN_OPEN, block=None, sampled=9), dict(node=contract.COUNT, block=0, sampled=1),
                 dict(node=contract.PLAN, block=0, sampled=6),
                 dict(node=contract.PATH, block=0, sampled=20), dict(node=contract.PATH, block=0, sampled=35),
                 dict(node=contract.PATH, block=0, sampled=5), dict(node=contract.SUMMARY, block=0, sampled=8),
                 dict(node=contract.MAIN_CLOSED, block=None, sampled=12)]
        self.assertEqual(contract.depth_and_tokens(calls), (10 + 6 + 35 + 8 + 12, 10 + 6 + 60 + 8 + 12))
        failed = [dict(node=contract.MAIN_OPEN, block=None, sampled=4), dict(node=contract.PLAN, block=0, sampled=9)]
        self.assertEqual(contract.depth_and_tokens(failed), (13, 13))


if __name__ == '__main__':
    unittest.main()
