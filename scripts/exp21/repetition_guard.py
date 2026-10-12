"""Stop degenerate generations after four consecutive repeated spans."""


def repeated_suffix_period(tokens, min_period=12, max_period=128, repeats=4):
    """Return repeated span length in tokens, or None.

    Ignore very short spans: ordinary arithmetic and lists can repeat a few
    tokens without being generation loops.
    """
    for period in range(min_period, min(max_period, len(tokens) // repeats) + 1):
        span = tokens[-period:]
        if all(tokens[-period * (i + 1):-period * i] == span
               for i in range(1, repeats)):
            return period
    return None
