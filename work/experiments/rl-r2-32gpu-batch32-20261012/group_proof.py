from pathlib import Path
import json,os,tempfile
os.environ['OMP_NUM_THREADS']='1'
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
import sys
sys.path.insert(0,str(Path(__file__).parent/'runner'))
from rollout_partition import partition, grouped_advantages

REWARDS=[1.,.6,0.,0.,0.,0.,0.,0.]
def worker(rank, init, output):
    torch.set_num_threads(1)
    dist.init_process_group('gloo',init_method=init,rank=rank,world_size=8)
    group,sample=partition(rank,8)
    records=[None]*8
    dist.all_gather_object(records,dict(rank=rank,prompt_index=group,sample_index=sample,id=str(group),reward=REWARDS[rank]))
    advantages=grouped_advantages(records)
    torch.manual_seed(3)
    model=DDP(torch.nn.Linear(2,1,bias=False).double())
    initial=model.module.weight.detach().clone()
    optimizer=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=0.)
    x=torch.tensor([[rank+1.,(rank%3)-1.]],dtype=torch.float64)
    # Each rank contributes one response /4096, DDP averages over8.
    loss=(model(x)*advantages[rank]).sum()/4096
    loss.backward()
    actual_grad=model.module.weight.grad.clone()
    ref=torch.nn.Linear(2,1,bias=False).double(); ref.weight.data.copy_(initial)
    old=torch.optim.AdamW(ref.parameters(),lr=1e-3,weight_decay=0.)
    # Previous layout: two actors, four local responses each, DDP mean2.
    reference=0.
    for prompt in range(2):
        local=0.
        for sample in range(4):
            index=prompt*4+sample
            vector=torch.tensor([[index+1.,(index%3)-1.]],dtype=torch.float64)
            local=local+(ref(vector)*advantages[index]).sum()/(4096*4)
        reference=reference+local/2
    reference.backward()
    assert torch.allclose(actual_grad,ref.weight.grad,atol=1e-15,rtol=1e-12)
    optimizer.step();old.step()
    assert torch.allclose(model.module.weight,ref.weight,atol=1e-15,rtol=1e-12)
    assert advantages[:4]==[.6,.19999999999999996,-.4,-.4] and advantages[4:]==[0.]*4
    Path(output,f'rank-{rank}.json').write_text(json.dumps(dict(passed=True,rank=rank,group=group,sample=sample,advantages=advantages,gradient_max_error=float((actual_grad-ref.weight.grad).abs().max()),adam_max_error=float((model.module.weight-ref.weight).abs().max()))))
    dist.destroy_process_group()

if __name__=='__main__':
    base=Path(__file__).parent
    directory=base/'cpu-proof-ranks';directory.mkdir(exist_ok=True)
    rendezvous=base/'cpu-rendezvous';rendezvous.unlink(missing_ok=True)
    mp.spawn(worker,args=('file://'+str(rendezvous.resolve()),str(directory)),nprocs=8,join=True)
    records=[dict(rank=r,prompt_index=r//4,sample_index=r%4,id=str(r//4),reward=REWARDS[r]) for r in range(8)]
    for corrupt in ['mixed_prompt','duplicate_sample','nonfinite']:
        bad=[dict(x) for x in records]
        if corrupt=='mixed_prompt':bad[1]['id']='bad'
        if corrupt=='duplicate_sample':bad[1]['sample_index']=0
        if corrupt=='nonfinite':bad[1]['reward']=float('nan')
        try:grouped_advantages(bad)
        except ValueError:pass
        else:raise AssertionError(corrupt)
    rows=[json.loads((directory/f'rank-{r}.json').read_text()) for r in range(8)]
    (base/'cpu-reward-group-proof.json').write_text(json.dumps(dict(passed=True,actual_gloo_ranks=8,prompt_groups=2,group_size=4,old_vs_new_gradient_and_adam_parity=True,no_std=True,invalid_assignment_checks=3,ranks=rows),indent=2))
    print(json.dumps(dict(passed=True,gradient_max_error=max(r['gradient_max_error'] for r in rows))))
