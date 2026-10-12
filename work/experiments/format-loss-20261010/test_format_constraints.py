import unittest
from format_constraints import FormatGuard, XML


class Tokenizer:
    texts = XML + ['<think>', '</think>', '\n'] + list('2345678') + ['words']
    def encode(self, text, **kwargs):
        return [self.texts.index(text)]
    def decode(self, ids, **kwargs):
        return ''.join(self.texts[i] for i in ids)


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tok = Tokenizer()
        self.id = lambda text: self.tok.encode(text)[0]

    def guard(self, phase, closed=False):
        prefix = [self.id('<think>')] + ([self.id('</think>')] if closed else [])
        return FormatGuard(self.tok, phase, prefix, 0, [100, 101])

    def test_parallel_banned_after_think_even_within_one_call(self):
        g = self.guard('main')
        self.assertNotIn(self.id('<Parallel>'), g.restriction([])[1])
        banned = g.restriction([self.id('</think>')])[1]
        self.assertTrue(set(g.tags.values()).issubset(banned))
        self.assertNotIn(100, banned)
        self.assertNotIn(self.id('words'), banned)
        self.assertTrue(set(g.tags.values()).issubset(self.guard('main', True).restriction([])[1]))

    def test_exact_width_two_sampled_tokens(self):
        g = self.guard('width')
        self.assertEqual(g.restriction([])[0], {self.id(str(i)) for i in range(2, 9)})
        self.assertEqual(g.restriction([self.id('3')])[0], {self.id('\n')})
        with self.assertRaises(ValueError):
            g.restriction([self.id('words')])

    def test_path_summary_cannot_close_think_or_end_message(self):
        for phase, end in [('path', '</Path>'), ('summary', '</Summary>')]:
            g = self.guard(phase)
            forbidden = g.restriction([])[1]
            self.assertNotIn(self.id(end), forbidden)
            self.assertIn(self.id('</think>'), forbidden)
            self.assertIn(100, forbidden)
            self.assertIn(self.id('<Parallel>'), forbidden)
            with self.assertRaises(ValueError):
                self.guard(phase, True)


if __name__ == '__main__':
    unittest.main()
