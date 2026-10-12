import unittest
from format_loss import attach_format_mask, target_weights, weighted_ce


class CharacterTokenizer:
    def __call__(self, text, **kwargs):
        return {'input_ids': [ord(c) for c in text],
                'offset_mapping': [(i, i + 1) for i in range(len(text))]}


class FormatLossTests(unittest.TestCase):
    def test_coordinates_syntax_content_and_forced_exclusion(self):
        content = ('<think>\nPlan:\n1: Add 2 and 3.\n2: Verify the sum.\n'
                   '<Parallel>2\n<Path>1\n1: 2+3=5\n</Path>\n<Path>2\n3+2=5\n</Path>\n'
                   '</Parallel>\n<Summary>Both give 5.</Summary>\n</think>\nFinal Answer: \\boxed{5}')
        response = content[len('<think>\n'):]
        start = 3
        targets = [0] * start + [1] * (len(response) + 1)
        for forced in ['<Path>1\n', '<Path>2\n', '</Parallel>\n<Summary>']:
            a = response.index(forced)
            targets[start+a:start+a+len(forced)] = [0] * len(forced)
        sample = {'input_ids': [1, 2, 3] + [ord(c) for c in response] + [999],
                  'prompt_length': start, 'target_mask': targets, 'position_ids': [], 'spans': []}
        result = attach_format_mask(sample, {'assistant_content': content}, CharacterTokenizer())
        mask = result['format_mask']
        self.assertEqual(mask[:start], [0] * start)
        self.assertFalse(any(f and not t for t, f in zip(targets, mask)))
        for text in ['<Parallel>2\n', '</Path>', '</Summary>', '</think>', 'Final Answer: ', '\\boxed{']:
            a = response.index(text)
            self.assertTrue(all(mask[start+a:start+a+len(text)]), text)
        for text in ['Add 2 and 3.', '1: 2+3=5', 'Both give 5.']:
            a = response.index(text)
            self.assertFalse(any(mask[start+a:start+a+len(text)]), text)
        self.assertEqual(mask[-2:], [1, 1])  # boxed closing brace and EOS
        self.assertEqual(result['input_ids'], sample['input_ids'])
        self.assertIs(result['position_ids'], sample['position_ids'])

    def test_plain_response_is_finite_without_inventing_parallel(self):
        content = '<think>\n2+3=5.\n</think>\nFinal Answer: \\boxed{5}'
        response = content[len('<think>\n'):]
        sample = {'input_ids': [42]+[ord(c) for c in response]+[999],
                  'prompt_length': 1, 'target_mask': [0]+[1]*(len(response)+1)}
        result = attach_format_mask(sample, {'assistant_content': content}, CharacterTokenizer())
        self.assertGreater(sum(target_weights(result['target_mask'], result['format_mask'], 1)), 0)
        self.assertFalse(any(result['format_mask'][1:6]))

    def test_schedule_and_zero_masks(self):
        targets, syntax = [0, 1, 1, 0, 1], [0, 1, 0, 0, 1]
        self.assertEqual(target_weights(targets, syntax, 1), [0, 1, 0, 0, 1])
        self.assertEqual(target_weights(targets, syntax, 2), [0, 5, 1, 0, 5])
        with self.assertRaises(ValueError):
            target_weights([0, 1], [1, 0], 1)
        with self.assertRaises(ValueError):
            target_weights([0, 1], [0, 0], 1)

    def test_shift_normalization_and_gradient(self):
        import torch
        # Slot0 is prompt. CE0 predicts slot1; slot2 is forced and must be zero.
        sample = {'target_mask': [0, 1, 0, 1, 1], 'format_mask': [0, 1, 0, 0, 1]}
        ce = torch.tensor([2., 100., 3., 4.], requires_grad=True)
        first = weighted_ce(ce, sample, 1)
        self.assertAlmostEqual(first.item(), 3.)
        first.backward()
        self.assertTrue(torch.equal(ce.grad, torch.tensor([.5, 0., 0., .5])))
        ce.grad = None
        later = weighted_ce(ce, sample, 2)
        self.assertAlmostEqual(later.item(), 33/11, places=6)
        later.backward()
        self.assertTrue(torch.allclose(ce.grad, torch.tensor([5/11, 0., 1/11, 5/11])))


if __name__ == '__main__':
    unittest.main()
