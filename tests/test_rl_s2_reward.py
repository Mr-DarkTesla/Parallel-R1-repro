"""The S2 schedule must reward correctness and only valid parallel answers on steps 9/10."""
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / 'verl/verl/utils/reward_score/math_dapo_acc_parallel_interved.py'
spec = importlib.util.spec_from_file_location('author_s2_reward', path)
reward = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reward)

class S2RewardTest(unittest.TestCase):
    def test_schedule_and_format(self):
        valid = '<Parallel><Path>A</Path><Path>B</Path></Parallel><Summary>C</Summary>'
        cases = [(True, '', 1.), (True, valid, 1.2), (True, '<Parallel>', -1.), (False, valid, -1.)]
        for step in range(1, 31):
            for correct, tags, parallel_reward in cases:
                with self.subTest(step=step, correct=correct, tags=tags):
                    text = 'Final Answer: ' + ('42' if correct else '0')
                    actual = reward.compute_score(text, tags + text, '42', step)
                    expected = (1. if correct else -1.) if (step - 1) % 10 < 8 else parallel_reward
                    self.assertEqual(actual['score'], expected)
                    self.assertEqual(actual['acc'], correct)

if __name__ == '__main__':
    unittest.main()
