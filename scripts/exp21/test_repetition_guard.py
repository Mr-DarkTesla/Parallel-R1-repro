"""Focused checks for the generation loop guard."""

import unittest

from repetition_guard import repeated_suffix_period


class RepetitionGuardTest(unittest.TestCase):
    def test_four_consecutive_phrases_stop(self):
        prefix = list(range(256))
        phrase = list(range(500, 520))
        self.assertIsNone(repeated_suffix_period(prefix + phrase * 3))
        self.assertEqual(repeated_suffix_period(prefix + phrase * 4), 20)

    def test_different_phrases_do_not_stop(self):
        prefix = list(range(256))
        phrases = [list(range(i, i + 20)) for i in (500, 600, 700, 800)]
        self.assertIsNone(repeated_suffix_period(prefix + sum(phrases, [])))

    def test_short_repeat_does_not_stop_after_four(self):
        prefix = list(range(256))
        self.assertIsNone(repeated_suffix_period(prefix + [1, 2, 3] * 4))


if __name__ == "__main__":
    unittest.main()
