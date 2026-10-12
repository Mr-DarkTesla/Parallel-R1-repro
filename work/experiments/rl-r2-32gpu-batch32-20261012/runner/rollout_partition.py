"""One response/rank, four ranks/prompt; exact prompt-local mean centering."""
import math

def partition(rank, world, group=4):
    if world % group or not 0 <= rank < world:
        raise ValueError('Invalid response partition')
    return rank//group, rank%group

def grouped_advantages(records, group=4):
    if len(records)%group: raise ValueError('Incomplete prompt groups')
    result=[]
    for start in range(0,len(records),group):
        chunk=records[start:start+group]
        if any(r['rank']!=start+i or r['prompt_index']!=start//group or r['sample_index']!=i for i,r in enumerate(chunk)):
            raise ValueError('Duplicate or misordered response assignments')
        if len({r['id'] for r in chunk})!=1: raise ValueError('Mixed prompts in reward group')
        rewards=[r['reward'] for r in chunk]
        if not all(math.isfinite(x) for x in rewards): raise ValueError('Nonfinite rewards')
        mean=sum(rewards)/group
        result.extend(x-mean for x in rewards)
    return result
