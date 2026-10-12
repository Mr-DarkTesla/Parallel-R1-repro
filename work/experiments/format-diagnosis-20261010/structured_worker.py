"""Exact Unseen attention using the existing vLLM Qwen3 weights (TP=PP=1).

Opt-in correctness backend: masked SDPA prefill and per-call KV decode. It
bypasses vLLM's causal attention scheduler and graphs, keeping weight transfer,
worker ownership and sleep lifecycle. No site-packages monkeypatches.
"""
import math
import torch
from torch import nn
from verl.utils.parallel_structure import attention,layout


def hf_weight_view(source, cached=None):
    """HF operations over live vLLM weights, with no second weight allocation.

    Fused vLLM QKV/GateUp matmuls and residual norms change BF16 rounding.
    Use the actor's operation order as well as its mask. Refresh aliases each
    call, including after vLLM sleep/wake or policy weight replacement.
    """
    from copy import deepcopy
    from transformers import AutoModelForCausalLM
    from transformers.models.qwen3.modeling_qwen3 import Qwen3RotaryEmbedding
    config=deepcopy(source.config);config._attn_implementation='sdpa'
    device=next(source.parameters()).device
    if cached is None:
        with torch.device('meta'):
            cached=AutoModelForCausalLM.from_config(config,torch_dtype=next(source.parameters()).dtype)
        cached.model.rotary_emb=Qwen3RotaryEmbedding(config,device=device)
        cached.eval()
    bindings={'model.embed_tokens.weight':source.model.embed_tokens.weight[:config.vocab_size],
              'model.norm.weight':source.model.norm.weight,'lm_head.weight':source.lm_head.weight[:config.vocab_size]}
    for i,layer in enumerate(source.model.layers):
        prefix=f'model.layers.{i}.';a=layer.self_attn
        q,k,v=a.qkv_proj.weight.split([a.q_size,a.kv_size,a.kv_size],dim=0)
        gate,up=layer.mlp.gate_up_proj.weight.chunk(2,dim=0)
        for name,weight in {'self_attn.q_proj.weight':q,'self_attn.k_proj.weight':k,'self_attn.v_proj.weight':v,
            'self_attn.o_proj.weight':a.o_proj.weight,'self_attn.q_norm.weight':a.q_norm.weight,'self_attn.k_norm.weight':a.k_norm.weight,
            'mlp.gate_proj.weight':gate,'mlp.up_proj.weight':up,'mlp.down_proj.weight':layer.mlp.down_proj.weight,
            'input_layernorm.weight':layer.input_layernorm.weight,'post_attention_layernorm.weight':layer.post_attention_layernorm.weight}.items():
            bindings[prefix+name]=weight
    names={name for name,_ in cached.named_parameters(remove_duplicate=False)}
    if names!=set(bindings):raise ValueError(f'Unsupported Qwen3 weight layout: {names ^ set(bindings)}')
    for name,weight in bindings.items():
        module,attribute=name.rsplit('.',1)
        setattr(cached.get_submodule(module),attribute,nn.Parameter(weight,requires_grad=False))
    return cached


def validate_sampling(params,evaluation_only=False):
    temperature=float(params.get('temperature',1.))
    if not math.isfinite(temperature) or temperature<0:raise ValueError('Invalid temperature')
    if params.get('min_tokens',0):raise ValueError('min_tokens changes the PPO action distribution')
    if params.get('allowed_token_ids') or params.get('bad_words') or params.get('guided_decoding'):
        raise ValueError('Constrained sampling is unsupported for exact PPO replay')
    if params.get('n',1)!=1:raise ValueError('Structured generation only supports n=1 per call')
    if not evaluation_only and (params.get('top_p',1.0)!=1.0 or params.get('top_k',-1) not in [-1,0]):
        raise ValueError('PPO likelihood alignment requires top_p=1 and top_k=-1')
    if params.get('repetition_penalty',1.0)!=1.0 or params.get('presence_penalty',0.0)!=0.0 or params.get('frequency_penalty',0.0)!=0.0:
        raise ValueError('Unsupported likelihood-changing sampling penalty')
    if params.get('stop') or params.get('logit_bias') or params.get('logits_processors'):
        raise ValueError('Use token ID stops; unsupported sampling transforms')
    if params.get('min_p',0.0)!=0.0:raise ValueError('min_p changes the PPO action distribution')


class StructuredWorkerExtension:
    @torch.inference_mode()
    def structured_generate(self,prompt_ids,sampling_params,structure_start,tags,pad_id):
        from vllm.distributed import get_tensor_model_parallel_world_size,get_pp_group
        if get_tensor_model_parallel_world_size()!=1 or get_pp_group().world_size!=1:
            raise ValueError('Exact Unseen backend requires TP=PP=1')
        params=dict(sampling_params);evaluation_only=bool(params.pop('_evaluation_only',False));validate_sampling(params,evaluation_only)
        budget=int(params['max_tokens']);temperature=float(params.get('temperature',1.0))
        if budget<=0:return []
        if not prompt_ids:raise ValueError('Empty prompt')
        model=self.model_runner.model
        if model.config.model_type != 'qwen3':raise ValueError('Structured worker supports Qwen3 only')
        self._structured_hf=hf_weight_view(model,getattr(self,'_structured_hf',None))
        hf=self._structured_hf;device=next(hf.parameters()).device
        tokens=torch.tensor(prompt_ids,dtype=torch.long)
        positions,_=layout(tokens,structure_start,tags,pad_id,allow_partial=True)
        allowed=attention(tokens,structure_start,tags,pad_id,allow_partial=True).to(device)
        mask=torch.zeros_like(allowed,dtype=next(hf.parameters()).dtype).masked_fill_(~allowed,-torch.inf)[None,None]
        generator=torch.Generator(device=device)
        seed = params.get('seed')
        generator.manual_seed(int(torch.seed() if seed is None else seed)%(2**63-1))
        stops=set(params.get('stop_token_ids',[]))
        output=[]
        result=hf(input_ids=tokens[None].to(device),position_ids=positions[None].to(device),attention_mask=mask,use_cache=True,logits_to_keep=1)
        last_position=int(positions[-1]);cache=result.past_key_values
        for i in range(budget):
            logits=result.logits[0,-1].float()
            if temperature==0:token=int(logits.argmax())
            else:
                scaled=logits[None]/temperature
                if evaluation_only:
                    from vllm.v1.sample.ops.topk_topp_sampler import apply_top_k_top_p
                    k=int(params.get('top_k',-1));p=float(params.get('top_p',1.))
                    scaled=apply_top_k_top_p(scaled,torch.tensor([k],device=device) if k>0 else None,torch.tensor([p],device=device) if p<1 else None)
                token=int(torch.multinomial(scaled.softmax(dim=-1)[0],1,generator=generator))
            output.append(token)
            if token in stops or i+1==budget:break
            last_position+=1
            allowed=torch.zeros((1,1,1,len(prompt_ids)+len(output)),dtype=mask.dtype,device=device)
            result=hf(input_ids=torch.tensor([[token]],device=device),position_ids=torch.tensor([[last_position]],device=device),attention_mask=allowed,past_key_values=cache,use_cache=True,logits_to_keep=1)
            cache=result.past_key_values
        return output

    @torch.inference_mode()
    def structured_logits(self,input_ids,structure_start,tags,pad_id):
        self._structured_hf=hf_weight_view(self.model_runner.model,getattr(self,'_structured_hf',None))
        hf=self._structured_hf;device=next(hf.parameters()).device
        ids=torch.tensor(input_ids,dtype=torch.long)
        positions,_=layout(ids,structure_start,tags,pad_id,allow_partial=True)
        allowed=attention(ids,structure_start,tags,pad_id,allow_partial=True).to(device)
        mask=torch.zeros_like(allowed,dtype=next(hf.parameters()).dtype).masked_fill_(~allowed,-torch.inf)[None,None]
        logits=hf(input_ids=ids[None].to(device),position_ids=positions[None].to(device),attention_mask=mask,use_cache=False,logits_to_keep=1).logits[0,-1].float()
        return logits.cpu().tolist()
