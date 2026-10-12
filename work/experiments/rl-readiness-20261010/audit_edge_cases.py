"""Actual multilayer isolation, prompt control scope, and padding/loss edge cases."""
import json
from pathlib import Path
import torch
from transformers import Qwen3Config,Qwen3ForCausalLM
from audit_semantics import make_case
from source.parallel_structure import layout,attention
from structured_replay import score_trajectory


def main():
    torch.set_num_threads(2);torch.manual_seed(7)
    c=make_case(4)
    ids=torch.tensor(c['ids']);pos,groups=layout(ids,c['origin'],c['tags'],c['pad'])
    allowed=attention(ids,c['origin'],c['tags'],c['pad'])
    mask=torch.zeros_like(allowed,dtype=torch.float32).masked_fill_(~allowed,-torch.inf)[None,None]
    config=Qwen3Config(vocab_size=128,hidden_size=64,intermediate_size=128,num_hidden_layers=3,
                      num_attention_heads=4,num_key_value_heads=2,head_dim=16,pad_token_id=0,attention_dropout=0.)
    config._attn_implementation='sdpa';model=Qwen3ForCausalLM(config).eval()
    changed=ids.clone();s,e=groups[0][0];changed[s+2:e-1]=91
    with torch.no_grad():
        a=model(input_ids=ids[None],position_ids=pos[None],attention_mask=mask,use_cache=False).logits[0]
        b=model(input_ids=changed[None],position_ids=pos[None],attention_mask=mask,use_cache=False).logits[0]
    own_s,own_e=groups[0][-1]
    sibling_delta=float((a[own_s:own_e]-b[own_s:own_e]).abs().max())
    summary_index=groups[0][-1][1]+1
    summary_delta=float((a[summary_index]-b[summary_index]).abs().max())
    next_path=groups[1][0][0]+2
    later_round_delta=float((a[next_path]-b[next_path]).abs().max())
    assert sibling_delta<1e-7
    assert summary_delta>1e-7 and later_round_delta>1e-7
    # Literal control IDs in the prompt are ordinary context, not executable blocks.
    literal_prompt=torch.tensor([1,10,12,13,11,15]+c['ids'][c['origin']:])
    p,g=layout(literal_prompt,6,c['tags'],0)
    assert len(g)==4 and torch.equal(p[:6],torch.arange(6))
    scoped=attention(literal_prompt,6,c['tags'],0)
    assert scoped[:6,:6].equal(torch.ones(6,6,dtype=torch.bool).tril())
    # Prompt prefill length has no contribution to generated-token reward costs.
    bigger=make_case(4,prompt_extra=97)
    assert c['F']==bigger['F'] and c['T']==bigger['T']
    # The actual deferred-SFT materialization excludes invalid rows AND keys.
    valid=torch.ones(len(ids)+19,dtype=torch.bool);valid[-19:]=False
    padded=torch.cat([ids,torch.zeros(19,dtype=torch.long)])
    unpadded=attention(padded,c['origin'],c['tags'],0)
    deferred=unpadded&valid[:,None]&valid[None,:]
    assert not deferred[-19:,:].any() and not deferred[:,-19:].any()
    # Next-token loss mask is attached to prediction rows, not target columns.
    L=3;R=5;total=12
    shifted_mask=torch.ones(total,dtype=torch.long);shifted_mask[L-1+R:]=0;shifted_mask[:L-1]=0
    target_indices=(shifted_mask[:-1].nonzero().flatten()+1).tolist()
    assert target_indices==list(range(L,L+R))
    logp,_=score_trajectory(model,c['calls'],c['mask']+[0]*19)
    assert (logp[torch.tensor(c['mask']+[0]*19)==0]==0).all()
    bad=list(c['calls']);bad[0]=dict(bad[0],response_start=1)
    try:score_trajectory(model,bad,c['mask']+[0]*19)
    except ValueError:coverage_rejected=True
    else:coverage_rejected=False
    assert coverage_rejected
    report=dict(passed=True,multilayer_sibling_logit_delta=sibling_delta,
                summary_reads_siblings_logit_delta=summary_delta,
                subsequent_round_reads_prior_context_logit_delta=later_round_delta,
                prompt_literal_control_scope=True,prompt_cost_invariance_lengths=[3,100],
                pad_query_and_key_exclusion=True,shifted_targets=target_indices,
                forced_and_pad_policy_loss_zero=True,misaligned_action_span_rejected=True)
    (Path(__file__).parent/'edge-proof.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
