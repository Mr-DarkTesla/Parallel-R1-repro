"""Evaluation-only sampled-logit guards. These are not an RL policy/replay path.

Partial syntax constraints; do not repair text or claim learned format validity.
Plan semantics, ID/width agreement, useful paths, and final-answer syntax still
need the unchanged independent scorer.
"""
XML = ['<Parallel>', '</Parallel>', '<Path>', '</Path>', '<Summary>', '</Summary>']


class FormatGuard:
    def __init__(self, tokenizer, phase, prompt_ids, structure_start, eos_ids):
        self.phase = phase
        self.tokenizer = tokenizer
        self.tags = {tag: self.single(tag) for tag in XML}
        self.think_open = self.single('<think>')
        self.think_close = self.single('</think>')
        self.newline = self.single('\n')
        self.widths = {self.single(str(i)) for i in range(2, 9)}
        self.eos_ids = set(eos_ids)
        response = tokenizer.decode(prompt_ids[structure_start:], skip_special_tokens=False)
        self.closed = '</think>' in response
        if phase not in ['main', 'width', 'path', 'summary']:
            raise ValueError('Unknown guarded generation phase')
        if phase != 'main' and self.closed:
            raise ValueError('Cannot fork, decode width, or summarize outside think')

    def single(self, text):
        ids = self.tokenizer.encode(text, add_special_tokens=False)
        if len(ids) != 1 or self.tokenizer.decode(ids, skip_special_tokens=False) != text:
            raise ValueError(f'Exact single-token syntax required: {text}')
        return ids[0]

    def restriction(self, output):
        """Return (allowed or None, forbidden), recomputed before EACH sample."""
        if self.phase == 'width':
            if not output:
                return self.widths, set()
            if len(output) == 1 and output[0] in self.widths:
                return {self.newline}, set()
            raise ValueError('Guarded width must stop after digit+newline')
        closed = self.closed or self.think_close in output
        if self.phase == 'main':
            allowed_tag = None if closed else self.tags['<Parallel>']
            forbidden = set(self.tags.values()) - ({allowed_tag} if allowed_tag is not None else set())
            forbidden.add(self.think_open)
            if closed:
                forbidden.add(self.think_close)
            else:
                forbidden.update(self.eos_ids)  # finish think before native EOS
            return None, forbidden
        terminator = self.tags['</Path>' if self.phase == 'path' else '</Summary>']
        return None, (set(self.tags.values()) - {terminator}) | self.eos_ids | {self.think_open, self.think_close}
