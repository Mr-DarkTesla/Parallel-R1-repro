"""CPU regressions for reward scale, wrong-answer signal and the trainer bridge."""

import ast
from collections import defaultdict
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import torch

ROOT = Path(__file__).resolve().parents[1] / 'verl/verl'


def load(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


math_reward = load('math_accuracy', 'utils/reward_score/math_dapo.py')
with patch.dict(sys.modules, {'verl.utils.reward_score.math_dapo': math_reward}):
    reward = load('efficiency_reward', 'utils/reward_score/parallel_efficiency.py')
split = load('split_grpo', 'trainer/ppo/split_grpo.py')
trace = load('depth_trace', 'parallel_thinking_generation_v3/repro_trace.py')


def load_definition(path, name, namespace):
    """Exercise real definitions without importing GPU/Ray infrastructure."""
    tree = ast.parse((ROOT / path).read_text())
    node = next(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name)
    node.decorator_list = []
    module = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0), node], type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), str(ROOT / path), 'exec'), namespace)
    return namespace[name]


PARALLEL = '<Parallel><Path>A</Path><Path>B</Path></Parallel><Summary>C</Summary>\nFinal Answer: 2'


def score(mode, text=PARALLEL, depth=500, total=800, forks=1, **kwargs):
    validate = kwargs.pop('validate', False)
    return reward.compute_score('gsm', text, text, '2', {
        'validate': validate,
        'parallel_stats': dict(critical_depth=depth, generated_tokens=total, forks=forks),
    }, mode=mode, **kwargs)


class EfficiencyRewardTest(unittest.TestCase):
    def test_formulas_and_validation(self):
        self.assertAlmostEqual(score('gated_depth')['score'], .95)
        self.assertAlmostEqual(score('parallel_gain')['score'], 1.075)
        self.assertAlmostEqual(score('parallel_gain', depth=250, total=400)['score'], 1.075)
        self.assertAlmostEqual(score('gated_depth', depth_lambda=.00001)['aux_reward'], -.005)
        self.assertAlmostEqual(score('parallel_gain', bonus_alpha=.02)['aux_reward'], .0075)
        for mode in ('gated_depth', 'parallel_gain'):
            self.assertEqual(score(mode, validate=True)['score'], 1)
            for depth in (5, 500, 3000):
                self.assertEqual(score(mode, text='Final Answer: 3', depth=depth, total=depth)['score'], 0)
        self.assertEqual(score('parallel_gain', text='Final Answer: 2', forks=0)['aux_reward'], 0)

    def test_complete_format_required_for_bonus(self):
        self.assertTrue(reward.valid_structure(PARALLEL * 2))
        self.assertTrue(reward.valid_structure('Final Answer: 2'))
        for text in (PARALLEL.replace('</Summary>', ''), PARALLEL.replace('</Path>', '', 1),
                     PARALLEL.replace('<Path>B</Path>', ''), '<Summary>x</Summary>',
                     '<Parallel>' + PARALLEL + '</Parallel>'):
            self.assertFalse(reward.valid_structure(text))
            self.assertEqual(score('parallel_gain', text=text)['aux_reward'], 0)

    def test_invalid_statistics_and_coefficients_fail(self):
        for kwargs in ({'depth': -1}, {'depth': 801}, {'total': float('nan')},
                       {'depth_lambda': -.1}, {'bonus_alpha': float('inf')}, {'forks': -1}):
            with self.assertRaises(ValueError):
                score('gated_depth', **kwargs)
        with self.assertRaises(ValueError):
            score('unknown')

    def test_depth_counts_multiple_forks_and_unfinished_paths(self):
        def calls(*pairs):
            return [dict(phase=phase, generated_tokens=count) for phase, count in pairs]
        self.assertEqual(trace.critical_depth([]), 0)
        self.assertEqual(trace.critical_depth(calls(('main', 10), ('path', 50), ('path', 30),
                                                  ('summary', 5), ('main', 2), ('path', 7), ('path', 9))), 76)
        self.assertEqual(trace.critical_depth(calls(('main', 10), ('summary', 4))), 14)
        with self.assertRaises(ValueError):
            trace.critical_depth(calls(('path', -1)))


class SplitAdvantageTest(unittest.TestCase):
    def setUp(self):
        self.correct = [0, 0, 1, 1, 1, 0, 1]
        self.aux = [0, 0, -.01, -.03, -.02, 0, -.01]
        self.uid = ['wrong', 'wrong', 'right', 'right', 'mixed', 'mixed', 'singleton']
        self.mask = torch.tensor([[1., 1., 0.]] * 7)

    def test_masks_singletons_wrong_groups_and_coefficient_scale(self):
        adv, _, metrics = split.compute_split_advantage(self.correct, self.aux, self.uid, self.mask)
        base, _, _ = split.compute_split_advantage(self.correct, [0] * 7, self.uid, self.mask)
        scaled, _, _ = split.compute_split_advantage(self.correct, [a / 10 for a in self.aux], self.uid, self.mask)
        self.assertTrue((adv[:2] == 0).all())
        self.assertTrue((adv[-1] == 0).all())
        self.assertTrue((adv[:, -1] == 0).all())
        self.assertAlmostEqual(adv[2, 0].item(), .01)
        torch.testing.assert_close(scaled - base, (adv - base) / 10, atol=1e-7, rtol=1e-5)
        self.assertEqual(metrics['grpo/mixed_accuracy_group_fraction'], .25)

    def test_invalid_components_fail(self):
        for c, a in (([0], [.1]), ([.5], [0]), ([1], [float('nan')]), ([1], [])):
            with self.assertRaises(ValueError):
                split.compute_split_advantage(c, a, ['a'], torch.ones(1, 2))

    def test_trainer_bridge_and_legacy_accuracy_parity(self):
        legacy = load_definition('trainer/ppo/core_algos.py', 'compute_grpo_outcome_advantage',
                                 dict(torch=torch, defaultdict=defaultdict))
        estimator = SimpleNamespace(GAE='gae', GRPO='grpo')
        trainer = load_definition('trainer/ppo/ray_trainer.py', 'compute_advantage',
                                  dict(AdvantageEstimator=estimator, core_algos=SimpleNamespace(
                                      compute_grpo_outcome_advantage=legacy)))
        rewards = torch.zeros(7, 3)
        rewards[:, 0] = torch.tensor(self.correct)
        data = SimpleNamespace(batch={'response_mask': self.mask, 'token_level_rewards': rewards},
                               non_tensor_batch=dict(uid=self.uid, accuracy_reward=self.correct, aux_reward=self.aux),
                               meta_info={})
        trainer(data, 'grpo', config=None)
        baseline, _, _ = split.compute_split_advantage(self.correct, [0] * 7, self.uid, self.mask)
        # Ordinary GRPO's singleton behavior differs; groups with >=2 agree.
        torch.testing.assert_close(data.batch['advantages'][:-1], baseline[:-1])
        with patch.dict(sys.modules, {'verl.trainer.ppo.split_grpo': split}):
            trainer(data, 'grpo', config={'split_accuracy_aux': True})
        expected, _, _ = split.compute_split_advantage(self.correct, self.aux, self.uid, self.mask)
        torch.testing.assert_close(data.batch['advantages'], expected)
        self.assertIn('split_reward_metrics', data.meta_info)
        for config, mode in (({'split_accuracy_aux': True, 'use_kl_in_reward': True}, 'grpo'),
                             ({'split_accuracy_aux': True}, 'gae')):
            with self.assertRaises(ValueError):
                trainer(data, mode, config=config)

    def test_reward_manager_copies_metadata_and_passes_validation(self):
        manager = load_definition('workers/reward_manager/naive.py', 'NaiveRewardManager',
                                  dict(torch=torch, defaultdict=defaultdict))
        metadata = {'index': 'original'}
        item = SimpleNamespace(batch=dict(prompts=torch.tensor([1]), responses=torch.tensor([2, 3]),
                                         attention_mask=torch.ones(3, dtype=torch.long)),
                               non_tensor_batch=dict(extra_info=metadata, data_source='gsm',
                                                     reward_model={'ground_truth': '2'},
                                                     parallel_stats=dict(critical_depth=500, generated_tokens=800, forks=1)))

        class Batch:
            batch = {'responses': torch.tensor([[2, 3]])}
            meta_info = {'global_steps': 1, 'validate': True}

            def __len__(self):
                return 1

            def __getitem__(self, index):
                return item

        tokenizer = SimpleNamespace(decode=lambda *args, **kwargs: PARALLEL)
        result = manager(tokenizer, 0, compute_score=reward.compute_score)(Batch(), return_dict=True)
        self.assertEqual(result['reward_tensor'].sum().item(), 1.)
        self.assertEqual(result['reward_extra_info']['aux_reward'], [0.])
        self.assertEqual(metadata, {'index': 'original'})


if __name__ == '__main__':
    unittest.main()
