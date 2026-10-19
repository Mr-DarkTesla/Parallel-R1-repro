"""Reject an uncertain PPO batch collectively; never relax likelihood checks."""
import math
import torch
import torch.distributed as dist


def synchronized_guard(max_drift, mean_drift, p95_drift, device, world,
                       max_allowed=.01, mean_allowed=.002, p95_allowed=.005):
    values=[max_drift,mean_drift,p95_drift]
    local_bad=not all(math.isfinite(x) for x in values) or max_drift>max_allowed or mean_drift>mean_allowed or p95_drift>p95_allowed
    flag=torch.tensor(int(local_bad),device=device,dtype=torch.int32)
    if world>1:dist.all_reduce(flag,op=dist.ReduceOp.MAX)
    return not bool(flag.item()),local_bad
