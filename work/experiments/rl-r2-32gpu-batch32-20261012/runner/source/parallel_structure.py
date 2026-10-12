"""Flat counted parallel blocks: shared header, isolated siblings, merged suffix."""
import torch


def parallel_blocks(ids, start, parallel_open, parallel_close, path_open, path_close, allow_partial=False):
    ids=ids.tolist() if hasattr(ids,'tolist') else list(ids)
    blocks=[];block=None;path=None
    for i in range(start,len(ids)):
        token=ids[i]
        if token==parallel_open:
            if block is not None:raise ValueError('Nested Parallel blocks are unsupported')
            block=[i,None,[]]
        elif token==path_open and block is not None:
            if path is not None:raise ValueError('Nested Path')
            path=i
        elif token==path_close and block is not None:
            if path is None:raise ValueError('Unmatched Path close')
            block[2].append((path,i+1));path=None
        elif token==parallel_close and block is not None:
            if path is not None:raise ValueError('Unclosed Path')
            block[1]=i
            if not block[2]:raise ValueError('Parallel block contains no paths')
            blocks.append(block);block=None
    if block is not None:
        if not allow_partial:raise ValueError('Unclosed parallel block')
        if path is not None:block[2].append((path,len(ids)))
        if block[2]:
            block[1]=len(ids);blocks.append(block)
    return blocks


def layout(ids,start,tags,pad_id,allow_partial=False):
    ids=ids.flatten();tokens=ids.tolist();n=len(tokens)
    blocks=parallel_blocks(tokens,start,*tags,allow_partial=allow_partial)
    positions=torch.zeros(n,dtype=torch.long);spans=[];cursor=0;pos=0
    for opening,closing,paths in blocks:
        # Count and newline after <Parallel> are shared and keep real positions.
        first=paths[0][0]
        positions[cursor:first]=torch.arange(pos,pos+first-cursor);pos+=first-cursor
        ranges=[]
        for k,(s,e) in enumerate(paths):
            # Attach inter-path whitespace to its preceding path, preventing
            # an indirect sibling leak through that whitespace in deeper layers.
            end=paths[k+1][0] if k+1<len(paths) else closing
            positions[s:end]=torch.arange(pos,pos+end-s);ranges.append((s,end))
        pos+=max(e-s for s,e in ranges);spans.append(ranges);cursor=closing
    valid_end=n
    while valid_end>cursor and tokens[valid_end-1]==pad_id:valid_end-=1
    positions[cursor:valid_end]=torch.arange(pos,pos+valid_end-cursor)
    return positions,spans


def attention(ids,start,tags,pad_id,allow_partial=False):
    _,blocks=layout(ids,start,tags,pad_id,allow_partial=allow_partial)
    n=ids.numel();mask=torch.ones(n,n,dtype=torch.bool).tril_()
    for spans in blocks:
        first=spans[0][0]
        for s,e in spans[1:]:mask[s:e,first:s]=False
    return mask
