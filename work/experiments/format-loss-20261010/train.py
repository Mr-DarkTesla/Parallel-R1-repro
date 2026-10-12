"""Isolated tied-six-row warmup. No original model file is modified."""
import argparse, contextlib, datetime as dt, hashlib, json, math, os, random, time
from pathlib import Path
import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch import nn
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import Dataset, DataLoader, DistributedSampler
from transformers import AutoModelForCausalLM, AutoTokenizer
from safetensors.torch import save_file, load_file
from data import build_sample
from format_loss import attach_format_mask, weighted_ce
D=Path(__file__).resolve().parent;P=D.parents[2];A=P/'work/experiments/instruct-token-warmup-20261010';N=P/'work/experiments/night-20261010'
LOSS_EPOCH=1

def save(path,data):
    path=Path(path);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');tmp.replace(path)
def now():return dt.datetime.now(dt.timezone.utc).isoformat()

class RowEmbedding(nn.Module):
    def __init__(self,base,rows,first):
        super().__init__();self.base=base;self.rows=rows;self.first=first
    @property
    def weight(self):return self.base.weight
    def forward(self,ids):
        old=self.base(ids);local=ids-self.first;hits=(local>=0)&(local<self.rows.shape[0])
        selected=F.embedding(local.clamp(0,self.rows.shape[0]-1),self.rows.to(old.dtype))
        return torch.where(hits.unsqueeze(-1),selected,old)

class RowHead(nn.Module):
    def __init__(self,base,rows,newids):
        super().__init__();self.base=base;self.rows=rows;self.register_buffer('newids',newids)
    @property
    def weight(self):return self.base.weight
    def forward(self,hidden):
        old=self.base(hidden);new=F.linear(hidden,self.rows.to(hidden.dtype))
        return old.index_copy(-1,self.newids,new)

class Samples(Dataset):
    def __init__(self,split,tok,system,smoke=False):
        source=P/'exps/deepseek-gsm-wide3000-v2-20261009/production/sft-think'/f'{split}.jsonl'
        rows=[json.loads(l) for l in source.read_text().splitlines()]
        if smoke:
            rows=sorted(rows,key=lambda r:len(r['assistant_content']),reverse=True)[:16]
        self.samples=[attach_format_mask(build_sample(r,tok,system,max_length=8192),r,tok) for r in rows]
    def __len__(self):return len(self.samples)
    def __getitem__(self,i):return self.samples[i]

def batch_tensors(sample,device):
    ids=torch.tensor(sample['input_ids'],device=device).unsqueeze(0);length=ids.shape[1]
    allowed=torch.ones(length,length,device=device,dtype=torch.bool).tril()
    for group in sample['spans']:
        first=group[0][0]
        for s,e in group[1:]:allowed[s:e,first:s]=False
    mask=torch.zeros(length,length,device=device,dtype=torch.float32).masked_fill_(~allowed,-torch.inf)
    return ids,mask[None,None],torch.tensor(sample['position_ids'],device=device).unsqueeze(0),torch.tensor(sample['target_mask'],device=device,dtype=torch.float32)[1:]

def compute(model,sample,device):
    ids,mask,pos,targets=batch_tensors(sample,device)
    with torch.autocast('cuda',dtype=torch.bfloat16):
        logits=model(input_ids=ids,attention_mask=mask,position_ids=pos,use_cache=False).logits
    ce=F.cross_entropy(logits[0,:-1].float(),ids[0,1:],reduction='none')
    loss=weighted_ce(ce,sample,LOSS_EPOCH) if model.training else (ce*targets).sum()/targets.sum().clamp_min(1)
    return loss,ids.numel(),int(targets.sum())

@torch.no_grad()
def isolation_check(model,tok,system,device):
    # Same-length perturbation confined to sibling1. Sibling3's logits must not change.
    content='<think>\nPlan:\n1: Compute a sum.\n2: Compute a product.\n3: Compute a difference.\n<Parallel>3\n<Path>1\n2 + 3 = 5.\n</Path>\n<Path>2\n2 * 3 = 6.\n</Path>\n<Path>3\n3 - 2 = 1.\n</Path>\n</Parallel>\n<Summary>\nThe three results are 5, 6, and 1.\n</Summary>\n</think>\nFinal Answer: \\boxed{1}'
    sample=build_sample({'problem':'Compute a sum, product and difference of 2 and 3.','assistant_content':content},tok,system,max_length=8192)
    ids,mask,pos,_=batch_tensors(sample,device);first,last=sample['spans'][0][0],sample['spans'][0][-1]
    special=set(tok.all_special_ids);candidates=[i for i in range(first[0]+1,first[1]-1) if int(ids[0,i]) not in special]
    assert candidates
    altered=ids.clone();altered[0,candidates[-1]]=tok.encode('7',add_special_tokens=False)[0]
    assert not torch.equal(altered,ids)
    model.eval()
    with torch.autocast('cuda',dtype=torch.bfloat16):
        one=model(input_ids=ids,attention_mask=mask,position_ids=pos,use_cache=False).logits[0,last[0]:last[1]].float()
        two=model(input_ids=altered,attention_mask=mask,position_ids=pos,use_cache=False).logits[0,last[0]:last[1]].float()
    error=float((one-two).abs().max());assert error<=1e-5,('Sibling leakage',error)
    return {'width':3,'third_sibling_max_logit_difference':error,'passed':True}

def main():
    global LOSS_EPOCH
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['smoke','production'],required=True);a=ap.parse_args()
    rank=int(os.environ['RANK']);world=int(os.environ['WORLD_SIZE']);local=int(os.environ['LOCAL_RANK']);assert world==8
    torch.cuda.set_device(local);dist.init_process_group('nccl',timeout=dt.timedelta(minutes=20));device=torch.device('cuda',local)
    torch.set_num_threads(1);torch.manual_seed(20261010);random.seed(20261010)
    out=D/'runs'/a.stage
    if rank==0:out.mkdir(exist_ok=False)
    dist.barrier();start=time.monotonic()
    native=N/'qwen3-4b-tag-probe-20261010/model';tok=AutoTokenizer.from_pretrained(A/'tokenizer',local_files_only=True);proof=json.loads((A/'tokenizer-proof.json').read_text());system=(A/'system.txt').read_text()
    model=AutoModelForCausalLM.from_pretrained(native,local_files_only=True,torch_dtype=torch.bfloat16,attn_implementation='sdpa').to(device)
    model.requires_grad_(False);embedding=model.get_input_embeddings();head=model.get_output_embeddings()
    assert embedding.weight.data_ptr()==head.weight.data_ptr(),'Expected genuinely tied4B input/output'
    tagids=list(proof['tags'].values());assert tagids==list(range(tagids[0],tagids[0]+6))
    recomputed=torch.stack([embedding.weight[proof['native_pieces'][tag]].float().mean(0) for tag in proof['tags']]).detach()
    initial=load_file(str(A/'initial-rows.safetensors'),device='cpu')['initial_rows'].to(device)
    assert torch.allclose(initial,recomputed,atol=1e-6,rtol=1e-5),'Native mean-piece initialization mismatch'
    rows=nn.Parameter(initial.clone());newids=torch.tensor(tagids,device=device)
    frozen=[(name,param,param._version) for name,param in model.named_parameters()]
    model.set_input_embeddings(RowEmbedding(embedding,rows,tagids[0]));model.set_output_embeddings(RowHead(head,rows,newids))
    trainable=[(name,p) for name,p in model.named_parameters() if p.requires_grad]
    assert len(trainable)==1 and trainable[0][1] is rows and rows.numel()==15360
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False});model.config.use_cache=False
    if rank==0:
        save(out/'initialization-proof.json',{'at':now(),'only_trainable':trainable[0][0],'trainable_parameters':rows.numel(),'tag_ids':tagids,'mean_original_piece_init':True,'initial_rows_sha256':hashlib.sha256(initial.cpu().numpy().tobytes()).hexdigest(),'native_embeddings_and_lm_head_tied':True,'all_base_parameters_frozen':True,'no_weight_resize':True,'rank0_gpu_isolation':isolation_check(model,tok,system,device)})
    def frozen_bytehash():
        digest=hashlib.sha256()
        for name,param,_ in frozen:
            digest.update(name.encode());digest.update(param.detach().cpu().contiguous().view(torch.uint8).numpy().tobytes())
        return digest.hexdigest()
    # DDP constructor broadcasts even frozen parameters and advances their versions.
    # Prove that synchronization preserves bytes, then establish the training baseline.
    before_sync=frozen_bytehash() if rank==0 else None
    dist.barrier();ddp=DDP(model,device_ids=[local],broadcast_buffers=False)
    if rank==0:
        after_sync=frozen_bytehash();assert before_sync==after_sync,'DDP changed frozen parameter bytes'
        initproof=json.loads((out/'initialization-proof.json').read_text())
        initproof.update(ddp_frozen_bytes_equal=True,frozen_bytehash_before_DDP=before_sync,frozen_bytehash_after_DDP=after_sync)
        save(out/'initialization-proof.json',initproof)
    dist.barrier()
    frozen=[(name,param,param._version) for name,param,_ in frozen]
    optimizer=torch.optim.AdamW([rows],lr=5e-4,weight_decay=0)
    train=Samples('train',tok,system,smoke=a.stage=='smoke');val=Samples('val',tok,system)
    sampler=DistributedSampler(train,num_replicas=world,rank=rank,shuffle=True,seed=20261010,drop_last=False)
    loader=DataLoader(train,batch_size=None,sampler=sampler,num_workers=0)
    epochs=1 if a.stage=='smoke' else 3;accum=1 if a.stage=='smoke' else 8;total_steps=2 if a.stage=='smoke' else math.ceil(len(loader)/accum)*epochs
    step=0;model.train()
    for epoch in range(epochs):
        LOSS_EPOCH=epoch+1
        sampler.set_epoch(epoch);batch=[]
        for index,sample in enumerate(loader):
            batch.append(sample)
            if len(batch)<accum and index+1<len(loader):continue
            LOSS_EPOCH=(1 if step==0 else 2) if a.stage=='smoke' else epoch+1
            optimizer.zero_grad(set_to_none=True);loss_sum=0.;tokens=0;targets=0
            for j,s in enumerate(batch):
                with ddp.no_sync() if j+1<len(batch) else contextlib.nullcontext():
                    loss,nt,ns=compute(ddp,s,device);assert torch.isfinite(loss)
                    (loss/len(batch)).backward();loss_sum+=float(loss.detach())/len(batch);tokens+=nt;targets+=ns
            assert rows.grad is not None and torch.isfinite(rows.grad).all();gn=float(nn.utils.clip_grad_norm_([rows],1.))
            lr=5e-4 if a.stage=='smoke' else 5e-4*min(1.,(step+1)/5)*(.1+.9*(1+math.cos(math.pi*step/max(total_steps-1,1)))/2)
            optimizer.param_groups[0]['lr']=lr;optimizer.step();step+=1
            assert all(p._version==version and not p.requires_grad for _,p,version in frozen),'Frozen base changed'
            metrics=torch.tensor([loss_sum,gn,tokens,targets],device=device,dtype=torch.float64);dist.all_reduce(metrics);metrics/=world
            if rank==0:
                elapsed=time.monotonic()-start;r={'at':now(),'step':step,'target_steps':total_steps,'epoch':epoch+1,'loss':float(metrics[0]),'row_grad_norm':float(metrics[1]),'lr':lr,'mean_input_tokens':float(metrics[2]),'mean_supervised_tokens':float(metrics[3]),'row_update_l2':float((rows-initial).norm()),'elapsed_seconds':elapsed,'estimated_remaining_seconds':elapsed/step*(total_steps-step),'trainable_parameters':15360,'frozen_parameter_versions_unchanged':True,'loss_phase':'format_only' if LOSS_EPOCH==1 else 'format_x5','format_weight':1 if LOSS_EPOCH==1 else 5}
                with (out/'metrics.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
                save(out/'status.json',{'state':'running',**r});print(json.dumps(r),flush=True)
            batch=[]
            if step>=total_steps:break
        model.eval();valsum=torch.zeros(3,device=device,dtype=torch.float64)
        with torch.no_grad():
            for i in range(rank,len(val),world):
                loss,_,_=compute(model,val[i],device);assert torch.isfinite(loss);valsum[0]+=loss;valsum[1]+=1
                if a.stage=='smoke' and i>=rank+world:break
        dist.all_reduce(valsum);assert valsum[1]>0
        if rank==0:
            save_file({'rows':rows.detach().float().cpu()},str(out/f'rows-epoch{epoch+1}.safetensors'))
            save(out/f'epoch{epoch+1}.json',{'step':step,'val_teacher_forced_loss':float(valsum[0]/valsum[1]),'validation_samples':int(valsum[1]),'frozen_parameters_unchanged':True})
        model.train()
        if step>=total_steps:break
    dist.barrier()
    if rank==0:
        assert all(p._version==v for _,p,v in frozen)
        save_file({'rows':rows.detach().float().cpu(),'initial_rows':initial.cpu()},str(out/'rows-final.safetensors'))
        if a.stage=='production':
            # Export standard tied HF weights; mutate only six previously-unused native rows IN MEMORY.
            model.set_input_embeddings(embedding);model.set_output_embeddings(head)
            with torch.no_grad():embedding.weight.index_copy_(0,newids,rows.detach().to(embedding.weight.dtype))
            assert embedding.weight.data_ptr()==head.weight.data_ptr()
            model.config.use_cache=True;model.save_pretrained(out/'final',max_shard_size='2GB');tok.save_pretrained(out/'final')
            for name in ['generation_config.json','chat_template.jinja']:
                src=native/name
                if src.exists():(out/'final'/name).write_bytes(src.read_bytes())
        save(out/'result.json',{'state':'complete','at':now(),'steps':step,'epochs':epochs,'trainable_parameters':15360,'only_six_rows_updated':True,'all_other_parameters_frozen_version_checks_passed':True,'elapsed_seconds':time.monotonic()-start,'final':str(out/'final') if a.stage=='production' else None})
        save(out/'status.json',json.loads((out/'result.json').read_text()))
    dist.barrier();dist.destroy_process_group()
if __name__=='__main__':main()
