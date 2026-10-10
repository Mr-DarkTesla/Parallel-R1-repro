import unittest

from math_verify import parse, verify

from bench.answer_normalization import lone_number, normalize_superscripts


class AnswerNormalizationTest(unittest.TestCase):
    def test_prose_numeric_answer(self):
        self.assertEqual(lone_number("Each of them will get 9 apples."), "9")
        self.assertTrue(verify(parse("$9$"), parse("$9$")))
        self.assertIsNone(lone_number("9 apples for 2 people"))
        self.assertIsNone(lone_number("2x"))

    def test_unicode_superscript(self):
        candidate = normalize_superscripts("2x(15x² - 4x + 10)")
        self.assertTrue(verify(parse("$2x(15x^2-4x+10)$"), parse(f"${candidate}$")))
        self.assertEqual(normalize_superscripts("x⁻² + y³"), "x^-2 + y^3")


if __name__ == "__main__":
    unittest.main()
