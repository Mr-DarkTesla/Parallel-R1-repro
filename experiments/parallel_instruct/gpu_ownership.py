"""Identify the GPUs owned by this run without treating other devices as ours."""

def assigned_uuids(gpu_rows, visible, processes_per_node):
    devices=[(int(row.split(',',1)[0]),row.split(',',1)[1].strip()) for row in gpu_rows.splitlines() if row.strip()]
    if processes_per_node < 1:
        raise ValueError('Positive processes_per_node required')
    if visible is None:
        selected=[uuid for _,uuid in sorted(devices)][:processes_per_node]
    else:
        selected=[]
        for value in visible.split(',')[:processes_per_node]:
            value=value.strip()
            matches=[uuid for index,uuid in devices if str(index)==value or uuid==value or (value.startswith('GPU-') and uuid.startswith(value))]
            if len(matches)!=1:
                raise ValueError('Visible GPU cannot be resolved uniquely')
            selected.append(matches[0])
    if len(selected)!=processes_per_node or len(set(selected))!=processes_per_node:
        raise ValueError('Insufficient or duplicated assigned GPUs')
    return set(selected)


def owned_processes(compute_rows, assigned):
    result=[]
    for row in compute_rows.splitlines():
        if not row.strip():continue
        uuid,pid=row.split(',',1)
        if uuid.strip() in assigned:result.append(int(pid.strip()))
    return result
