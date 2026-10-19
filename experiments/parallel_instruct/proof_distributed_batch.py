"""CPU Gloo/Adam parity for local and cross-rank prompt groups."""
from pathlib import Path
import argparse,json,os
os.environ.setdefault('OMP_NUM_THREADS','1')
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
from batching import assignments,prompt_advantages,ddp_loss_scale

def worker(rank,world,init,output):
    torch.set_num_threads(1)
    dist.init_process_group('gloo',init_method=init,rank=rank,world_size=world)
    reports=[]
    for prompts in [2,8]:
        group=4; owned=assignments(rank,world,prompts,group)
        def reward(p,s):return [1.,.6,0.,0.][s] if p%2==0 else 0.
        local=[dict(prompt_index=p,sample_index=s,id=str(p),reward=reward(p,s)) for p,s in owned]
        gathered=[None]*world;dist.all_gather_object(gathered,local)
        advantages=prompt_advantages(gathered,prompts,group)
        torch.manual_seed(3)
        core=torch.nn.Linear(2,1,bias=False).double()
        model=DDP(core) if world>1 else core
        initial=core.weight.detach().clone()
        if world>1:
            from torch.distributed.optim import ZeroRedundancyOptimizer
            optimizer=ZeroRedundancyOptimizer(model.parameters(),optimizer_class=torch.optim.AdamW,lr=1e-3,weight_decay=0.,foreach=False)
        else:
            optimizer=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=0.,foreach=False)
        vectors=torch.tensor([[p*group+s+1.,((p*group+s)%3)-1.] for p,s in owned],dtype=torch.float64)
        adv=torch.tensor([advantages[p,s] for p,s in owned],dtype=torch.float64)
        (model(vectors).reshape(-1)*adv*ddp_loss_scale(world,prompts,group)/4096).sum().backward()
        observed=core.weight.grad.clone()
        reference=torch.nn.Linear(2,1,bias=False).double();reference.weight.data.copy_(initial)
        reference_optimizer=torch.optim.AdamW(reference.parameters(),lr=1e-3,weight_decay=0.)
        # Independent legacy layout: one actor/prompt, four local responses;
        # no distributed batching helper in this reference calculation.
        loss=0.
        for p in range(prompts):
            values=[reward(p,s) for s in range(group)];mean=sum(values)/group
            for s in range(group):
                x=torch.tensor([[p*group+s+1.,((p*group+s)%3)-1.]],dtype=torch.float64)
                loss=loss+(reference(x)*(values[s]-mean)).sum()/(4096*prompts*group)
        loss.backward()
        assert torch.allclose(observed,reference.weight.grad,atol=1e-15,rtol=1e-12)
        optimizer.step();reference_optimizer.step()
        assert torch.allclose(core.weight,reference.weight,atol=1e-15,rtol=1e-12)
        reports.append(dict(prompts=prompts,group=group,local_responses=len(owned),gradient_error=float((observed-reference.weight.grad).abs().max()),adam_error=float((core.weight-reference.weight).abs().max())))
        del model,optimizer,reference,reference_optimizer
    Path(output,f'rank-{rank}.json').write_text(json.dumps(dict(rank=rank,passed=True,optimizer="Zero1AdamW" if world>1 else "AdamW",cases=reports)))
    dist.destroy_process_group()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--world',type=int,default=8)
    args=parser.parse_args();output=Path(args.output).resolve();output.mkdir(parents=True,exist_ok=False)
    rendezvous=output/'rendezvous'
    mp.spawn(worker,args=(args.world,'file://'+str(rendezvous),str(output)),nprocs=args.world,join=True)
    ranks=[json.loads((output/f'rank-{r}.json').read_text()) for r in range(args.world)]
    (output/'proof.json').write_text(json.dumps(dict(passed=True,actual_gloo_ranks=args.world,cross_rank_and_local_prompt_groups=True,reference='Legacy four responses per prompt, globally averaged over prompts',ranks=ranks),indent=2))
    print(json.dumps(dict(passed=True,ranks=args.world,max_gradient_error=max(c['gradient_error'] for r in ranks for c in r['cases']))))
