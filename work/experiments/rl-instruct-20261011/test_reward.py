import unittest
from reward import score, centered_advantages


class RewardTests(unittest.TestCase):
    def s(self, mode='strong_width', step=0, correct=True, valid=True, forwards=1000,
          depth=500, total=3000, widths=(4,4,4,4)):
        return score(correct, valid, depth, total, widths, step, mode, forward_calls=forwards)

    def test_constant_bonus_at_all_steps(self):
        expected = self.s()['score']
        for step in (0, 16, 32, 48, 64, 128, 10000):
            self.assertEqual(self.s(step=step)['score'], expected)
            self.assertAlmostEqual(self.s(step=step)['score'] - self.s('forward_only', step)['score'], .5)

    def test_correctness_and_format_gates(self):
        for mode in ('forward_only', 'strong_width'):
            self.assertEqual(self.s(mode, correct=False)['score'], 0.)
            self.assertGreaterEqual(self.s(mode, forwards=100000, total=100000)['score'], .6)
        self.assertEqual(self.s(valid=False)['fork_bonus'], 0.)

    def test_discrete_actual_cost_not_depth_or_tokens(self):
        self.assertEqual(self.s(forwards=200)['score'], self.s(forwards=399)['score'])
        self.assertAlmostEqual(self.s(forwards=399)['score'] - self.s(forwards=400)['score'], .02)
        self.assertEqual(self.s(depth=2500,total=4000)['score'], self.s()['score'])

    def test_width_and_round_saturation(self):
        self.assertLess(self.s(widths=(2,))['score'], self.s(widths=(4,))['score'])
        self.assertEqual(self.s(widths=(4,))['score'], self.s(widths=(8,))['score'])
        self.assertEqual(self.s(widths=(4,)*4)['score'], self.s(widths=(4,)*20)['score'])
        self.assertEqual(self.s(widths=())['fork_bonus'], 0.)

    def test_no_std_preserves_scale(self):
        a = centered_advantages([0., .8, 1., 1.3])
        b = centered_advantages([0., .08, .1, .13])
        for x,y in zip(a,b):self.assertAlmostEqual(x*.1,y)
        self.assertEqual(centered_advantages([0.]*4), [0.]*4)

    def test_missing_bad_counts_fail_not_zero_reward(self):
        for forwards in (None, 0, -1, True, 3001, float('nan')):
            with self.assertRaises(ValueError):self.s(forwards=forwards)
        with self.assertRaises(ValueError):self.s(widths=(1,))


if __name__ == '__main__':unittest.main()
