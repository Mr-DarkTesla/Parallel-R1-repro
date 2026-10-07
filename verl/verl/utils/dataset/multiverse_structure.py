"""Attention mask and position ids for the Multiverse format with nesting (variant C).

Format inside the response: <Parallel> <Goal> <Outline>..</Outline>.. </Goal> <Path>..</Path>.. <Conclusion>..</Conclusion> </Parallel>;
a <Path> may contain inner <Parallel> blocks. Rules, as in Multiverse (arXiv 2506.09991):
- sibling paths of one block are mutually invisible; each sees everything before the block, the Goal, and its own text;
- every sibling path starts at the same position id (right after the Goal); after the paths, positions continue from the longest path;
- tokens after the last path (Conclusion, </Parallel>, later text) see all paths.
Text between two sibling paths (the "\\n" of "</Path>\\n<Path>") belongs to the following path, so it cannot carry the earlier
path's content into the next one (the plain verl masks leave it shared). Pure Python on token id lists; `dense_mask` needs torch.
"""


class StructureError(ValueError):
    pass


def multiverse_structure(ids, tags):
    """ids: list of int (response tokens, no padding). tags: dict with ids of "Parallel", "/Parallel", "Path", "/Path".

    Returns (positions, groups): positions are ints from 0 at the response start; groups has one entry per block (any depth),
    a list of half-open (start, end) token spans of its sibling paths (end is after </Path>).
    """
    P, EP, A, EA = tags["Parallel"], tags["/Parallel"], tags["Path"], tags["/Path"]
    n = len(ids)
    pos = [0] * n
    groups = []

    def plain_until(i, cur, stop):
        """Sequential tokens from i up to a token in `stop` (not consumed); nested blocks are handled; -> (i, cur)."""
        while i < n and ids[i] not in stop:
            if ids[i] == P:
                i, cur = block(i, cur)
                continue
            if ids[i] in (A, EA, EP):
                raise StructureError(f"unexpected structural token {ids[i]} at {i}")
            pos[i] = cur
            i, cur = i + 1, cur + 1
        return i, cur

    def block(i, cur):
        pos[i] = cur  # <Parallel>
        i, cur = i + 1, cur + 1
        while i < n and ids[i] != A:  # Goal section, shared by all paths
            if ids[i] in (P, EP, EA):
                raise StructureError(f"structural token {ids[i]} before the first <Path> at {i}")
            pos[i] = cur
            i, cur = i + 1, cur + 1
        if i >= n:
            raise StructureError("<Parallel> without <Path>")
        base, spans, ends, start = cur, [], [], i
        while True:
            c, k = base, start
            while ids[k] != A:  # gap before this sibling's <Path>
                pos[k] = c
                k, c = k + 1, c + 1
            pos[k] = c
            k, c = plain_until(k + 1, c + 1, {EA})
            if k >= n:
                raise StructureError("unclosed <Path>")
            pos[k] = c  # </Path>
            k, c = k + 1, c + 1
            spans.append((start, k))
            ends.append(c)
            m = k
            while m < n and ids[m] not in (A, P, EP, EA):
                m += 1
            if m < n and ids[m] == A:
                start = k
                continue
            break
        if len(spans) < 2:
            raise StructureError(f"block at {spans[0][0]} has {len(spans)} path")
        groups.append(spans)
        k, c = plain_until(k, max(ends), {EP})  # Conclusion
        if k >= n:
            raise StructureError("unclosed <Parallel>")
        pos[k] = c
        return k + 1, c + 1

    plain_until(0, 0, set())
    return pos, groups


def dense_mask(n, groups, device="cpu"):
    """Boolean (n, n) mask, True = may attend: causal, minus sibling paths of every block."""
    import torch

    mask = torch.ones(n, n, dtype=torch.bool, device=device).tril_()
    for spans in groups:
        for a, (s1, e1) in enumerate(spans):
            for s2, e2 in spans[a + 1:]:
                mask[s2:e2, s1:e1] = False  # later sibling cannot see an earlier one (the reverse is already causal)
    return mask
