from pathlib import Path
import json,os,socket,tempfile
import torch,torch.distributed as dist,torch.multiprocessing as mp
from replay_guard import synchronized_guard
B=Path(__file__).resolve().parent

def worker(rank,port):
    torch.set_num_threads(1)
    dist.init_process_group('gloo',init_method='tcp://127.0.0.1:'+str(port),rank=rank,world_size=2)
    p=torch.nn.Parameter(torch.tensor([1.]));opt=torch.optim.Adam([p],lr=.01)
    original=p.detach().clone();cases=[]
    for i in range(2):
        opt.zero_grad();(p.square().sum()).backward()
        passed,local_bad=synchronized_guard(.01761 if i==0 and rank==1 else .0001,.00001,.0001,'cpu',2)
        if passed:opt.step()
        cases.append(dict(iteration=i+1,local_bad=local_bad,passed=passed,weight=float(p.detach())))
        assert passed==(i==1)
        assert torch.equal(p.detach(),original) if i==0 else not torch.equal(p.detach(),original)
    (B/('guard-rank-'+str(rank)+'.json')).write_text(json.dumps(cases))
    dist.destroy_process_group()

if __name__=='__main__':
    s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
    mp.spawn(worker,args=(port,),nprocs=2,join=True)
    (B/'guard-collective-proof.json').write_text(json.dumps(dict(passed=True,ranks=2,one_rank_bad_all_skip=True,next_good_batch_all_update=True,no_threshold_relaxation=True),indent=2))
    print('Actual two-rank guard/Adam proof PASS')
