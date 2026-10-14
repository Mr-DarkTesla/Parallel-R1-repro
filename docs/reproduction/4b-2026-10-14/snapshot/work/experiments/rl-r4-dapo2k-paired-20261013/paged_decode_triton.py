"""One-query fully-visible paged GQA. RoPE/visibility are supplied by the DAG.

No KV gathers/repeated heads; FP32 online softmax, BF16 tensor-core attention.
Masked or multiquery prefills remain on the established SDPA path.
"""
import torch
import triton
import triton.language as tl

@triton.jit
def _decode(Q,K,V,Slots,Cu,O,
            H:tl.constexpr,HK:tl.constexpr,D:tl.constexpr,
            GROUP:tl.constexpr,SCALE:tl.constexpr,
            BQ:tl.constexpr,BN:tl.constexpr):
 row=tl.program_id(0);kh=tl.program_id(1)
 qr=tl.arange(0,BQ);ds=tl.arange(0,D);ns=tl.arange(0,BN)
 start=tl.load(Cu+row);end=tl.load(Cu+row+1);length=end-start
 heads=kh*GROUP+qr
 q=tl.load(Q+row*H*D+heads[:,None]*D+ds[None,:],mask=qr[:,None]<GROUP,other=0)
 m=tl.full((BQ,),float('-inf'),tl.float32)
 den=tl.zeros((BQ,),tl.float32);acc=tl.zeros((BQ,D),tl.float32)
 for block in range(tl.cdiv(length,BN)):
  ix=block*BN+ns;slot=tl.load(Slots+start+ix,mask=ix<length,other=0)
  k=tl.load(K+slot[None,:]*HK*D+kh*D+ds[:,None],mask=ix[None,:]<length,other=0)
  score=tl.dot(q,k)*SCALE
  score=tl.where(ix[None,:]<length,score,float('-inf'))
  nxt=tl.maximum(m,tl.max(score,1));alpha=tl.exp(m-nxt)
  prob=tl.exp(score-nxt[:,None])
  v=tl.load(V+slot[:,None]*HK*D+kh*D+ds[None,:],mask=ix[:,None]<length,other=0)
  acc=acc*alpha[:,None]+tl.dot(prob.to(v.dtype),v)
  den=den*alpha+tl.sum(prob,1);m=nxt
 result=acc/den[:,None]
 tl.store(O+row*H*D+heads[:,None]*D+ds[None,:],result,mask=qr[:,None]<GROUP)

def paged_gqa_decode(query,store,slots,cu,scale):
 assert query.is_cuda and query.dtype in (torch.bfloat16,torch.float16)
 assert query.is_contiguous() and store.is_contiguous()
 assert store.shape[0]==2 and query.shape[-1]==store.shape[-1]==128
 heads=query.shape[1];kvheads=store.shape[2];assert heads%kvheads==0
 group=heads//kvheads;assert group<=16
 result=torch.empty_like(query)
 _decode[(query.shape[0],kvheads)](query,store[0],store[1],slots,cu,result,
     H=heads,HK=kvheads,D=128,GROUP=group,SCALE=float(scale),
     BQ=16,BN=64,num_warps=4,num_stages=2)
 return result
