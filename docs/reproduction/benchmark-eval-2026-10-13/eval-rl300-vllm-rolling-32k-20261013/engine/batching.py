"""Fixed 8 prompts x 4 responses; DDP rank sums average to global batch32."""
import hashlib
import math
from pathlib import Path

SUPPORTED_WORLDS = (1, 2, 4, 8, 16, 24, 32)
PROMPTS, RESPONSES, GLOBAL_BATCH, LOSS_DENOMINATOR = 8, 4, 32, 4096

def _dimensions(world, prompts, responses):
    if any(type(x) is not int for x in (world,prompts,responses)):
        raise ValueError('Batch dimensions must be integers')
    if world not in SUPPORTED_WORLDS:
        raise ValueError('Supported GPU worlds are 1,2,4,8,16,24,32; no empty ranks')
    if (prompts,responses)!=(PROMPTS,RESPONSES):
        raise ValueError('This production contract requires exactly 8 prompts x 4 = 32 responses')

def assignments(rank, world, prompts=PROMPTS, responses_per_prompt=RESPONSES):
    """Balanced ownership, keeping each prompt on one or contiguous ranks."""
    _dimensions(world,prompts,responses_per_prompt)
    if type(rank) is not int or not 0<=rank<world:
        raise ValueError('Rank must be an integer inside this GPU world')
    if world<=prompts:
        return [(p,s) for p in range(rank,prompts,world) for s in range(responses_per_prompt)]
    base,extra=divmod(world,prompts);start=0
    for prompt in range(prompts):
        count=base+int(prompt<extra)
        if start<=rank<start+count:
            return [(prompt,s) for s in range(rank-start,responses_per_prompt,count)]
        start+=count
    raise AssertionError('Rank ownership incomplete')

def prompt_advantages(rank_records, prompts=PROMPTS, responses_per_prompt=RESPONSES):
    """Reward minus its own four-response prompt mean; never std-normalize."""
    world=len(rank_records);_dimensions(world,prompts,responses_per_prompt)
    groups=[[] for _ in range(prompts)]
    for rank,records in enumerate(rank_records):
        if records is None: raise ValueError('Missing rank reward records')
        for r in records:
            if type(r['prompt_index']) is not int or type(r['sample_index']) is not int:
                raise ValueError('Response indices must be integers')
        if [(r['prompt_index'],r['sample_index']) for r in records]!=assignments(rank,world,prompts,responses_per_prompt):
            raise ValueError('Response ownership/order/coverage mismatch')
        for r in records:
            if r.get('technical_unknown',False) or type(r['reward']) not in (int,float) or not math.isfinite(r['reward']):
                raise ValueError('Unknown or nonfinite reward cannot enter a group mean')
            if r['id'] is None or r['id']=='': raise ValueError('Missing prompt identity')
            groups[r['prompt_index']].append(r)
    result={}
    for prompt,records in enumerate(groups):
        if len(records)!=responses_per_prompt or len({r['id'] for r in records})!=1:
            raise ValueError('Incomplete or mixed prompt reward group')
        records.sort(key=lambda r:r['sample_index'])
        mean=sum(r['reward'] for r in records)/responses_per_prompt
        for r in records: result[prompt,r['sample_index']]=r['reward']-mean
    return result

def ddp_loss_scale(world, prompts=PROMPTS, responses_per_prompt=RESPONSES):
    """Multiply LOCAL SUM by world/32, then /4096; DDP averages ranks once.

    Never divide by this rank's response count: world24 owns 1 or 2 responses.
    Variable policy-call counts accumulate with no_sync; each rank joins one
    final synchronized backward, including one zero backward on zero-adv ranks.
    """
    _dimensions(world,prompts,responses_per_prompt)
    return world/GLOBAL_BATCH

def sync_flags(policy_calls):
    if type(policy_calls) is not int or policy_calls<1:
        raise ValueError('Every active rank requires a final DDP backward; no empty calls')
    return [False]*(policy_calls-1)+[True]

def rollout_seed(seed,step,prompt,sample):
    if any(type(x) is not int for x in (seed,step,prompt,sample)) or seed<0 or step<0 or not 0<=prompt<PROMPTS or not 0<=sample<RESPONSES:
        raise ValueError('Invalid rank-independent sampling seed coordinates')
    key=f'{seed}:{step}:{prompt}:{sample}'.encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8],'little')%(2**63)

def weights_only_checkpoint_steps(initial_step,target_step):
    if any(type(x) is not int for x in (initial_step,target_step)) or not 0<=initial_step<target_step:
        raise ValueError('Checkpoint schedule requires valid logical step bounds')
    return list(range((initial_step//50+1)*50,target_step+1,50))

def validate_weights_only_export(directory):
    """Check a completed single-file HF export, never a resume-state export."""
    root=Path(directory);hf=root/'hf'
    if not (hf/'model.safetensors').is_file() or not (hf/'config.json').is_file():
        raise ValueError('Missing unified HF weights or config')
    if list(hf.glob('*.safetensors.index.json')) or any(p.name.startswith(('optimizer','rng')) for p in root.rglob('*')):
        raise ValueError('Only unified weights/tokenizer export is admitted; no Adam/RNG')
    return dict(model=True,optimizer=False,rng=False,unsharded=True)
