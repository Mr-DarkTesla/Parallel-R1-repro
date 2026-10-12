import unittest
from reward import score as actual_score, centered_advantages


def score(correct, valid, depth, total, widths, step=0, mode='strong_width'):
    return actual_score(correct, valid, depth, total, widths, step, mode,
                        forward_calls=total)


class RewardTests(unittest.TestCase):
    def test_accuracy_dominates_failure_at_all_costs(self):
        for mode in ['token_only', 'forward_only', 'strong_width', 'bucketed_width']:
            for width in [2, 3, 4, 6, 8]:
                for step in [0, 32, 48, 64, 200]:
                    good = score(True, True, 100000, 200000, [width] * 20, step, mode)
                    bad = score(False, True, 100000, 200000, [width] * 20, step, mode)
                    self.assertGreaterEqual(good['score'], .6)
                    self.assertEqual(bad['score'], 0)
                    self.assertEqual(bad['aux_reward'], 0)

    def test_annealing_recovers_exact_control(self):
        for step in [64, 80]:
            control = score(True, True, 700, 2200, [4] * 4, step, 'forward_only')
            strong = score(True, True, 700, 2200, [4] * 4, step, 'strong_width')
            self.assertEqual(control['score'], strong['score'])
        self.assertAlmostEqual(score(True, True, 700, 2200, [4] * 4, 48)['fork_bonus'], .25)

    def test_depth_is_statistic_not_penalty(self):
        for mode in ['token_only', 'strong_width', 'bucketed_width']:
            shallow = score(True, True, 100, 2200, [4] * 4, mode=mode)
            deep = score(True, True, 2000, 2200, [4] * 4, mode=mode)
            self.assertEqual(shallow['score'], deep['score'])
            self.assertEqual(deep['depth_penalty'], 0)
            self.assertLess(score(True, True, 100, 2400, [4] * 4, mode=mode)['score'], shallow['score'])

    def test_physical_forward_cost_is_discrete(self):
        def s(forwards):
            return actual_score(True, True, 100, 3000, [4] * 4,
                                mode='forward_only', forward_calls=forwards)['score']
        self.assertEqual(s(200), s(399))
        self.assertAlmostEqual(s(399)-s(400), .02)
        self.assertGreater(s(1000), s(2000))
        with self.assertRaises(ValueError):
            actual_score(True, True, 100, 3000, [4])
        for forwards in [0, 3001, -1, float('nan'), True]:
            with self.assertRaises(ValueError):
                actual_score(True, True, 100, 3000, [4], forward_calls=forwards)

    def test_bounded_width_and_round_incentives(self):
        def s(widths):return score(True, True, 700, 2200, widths)
        self.assertLess(s([2])['score'], s([4])['score'])
        self.assertEqual(s([4])['fork_bonus'], s([8])['fork_bonus'])
        self.assertEqual(s([4] * 4)['fork_bonus'], s([4] * 40)['fork_bonus'])
        self.assertEqual(score(True, False, 700, 2200, [4] * 4)['fork_bonus'], 0)

    def test_no_std_keeps_coefficient_scale(self):
        values = [1., .95, .8, 0.]
        a = centered_advantages(values)
        b = centered_advantages([.1 * value for value in values])
        for x, y in zip(a, b):self.assertAlmostEqual(y, .1 * x)
        self.assertEqual(centered_advantages([0., 0., 0., 0.]), [0.] * 4)
        self.assertEqual(centered_advantages([1.]), [0.])

    def test_bad_statistics_are_unknown_not_failure_reward(self):
        for depth, total, widths in [(0, 0, []), (30, 20, []), (2, 3, [1]),
                                      (2, 3, [9]), (2, 3, [2.5]), (float('nan'), 3, []),
                                      (2, 3, [True])]:
            with self.assertRaises(ValueError):score(True, True, depth, total, widths)


if __name__ == '__main__':unittest.main()
