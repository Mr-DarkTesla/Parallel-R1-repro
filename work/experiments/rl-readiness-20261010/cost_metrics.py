"""Costs from actual generation calls; no textual headers or prompt tokens."""


def costs(calls):
    depth = total = 0
    group = []
    widths, round_lengths = [], []
    serial = dict(main=0, width=0, summary=0)
    def flush():
        nonlocal depth, group
        if group:
            widths.append(len(group))
            round_lengths.append(max(group))
            depth += max(group)
            group = []
    for call in calls:
        n = len(call['generated_ids'])
        total += n
        phase = call['phase']
        if phase == 'path':
            group.append(n)
        else:
            flush()
            if phase not in serial:
                raise ValueError(f'Unknown policy phase: {phase}')
            serial[phase] += n
            depth += n
    flush()
    return dict(F=depth, T=total, executed_rounds=len(widths), widths=widths,
                mean_width=sum(widths)/len(widths) if widths else None,
                path_critical_lengths=round_lengths, serial_tokens=serial,
                logical_T_over_F=total/depth if depth else None,
                cost_measurement='logical sampled-token critical path; not measured batched GPU forwards')
