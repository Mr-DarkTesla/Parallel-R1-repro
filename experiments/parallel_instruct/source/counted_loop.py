"""Counted flat forks with exact Unseen rollout contexts and sampled-action masks."""
import asyncio,copy,logging,os,random,re
from typing import Any
from uuid import uuid4
import torch
from verl.parallel_thinking_generation_v3.agent_loop import AgentLoopBase,AgentLoopOutput,register
from verl.parallel_thinking_generation_v3.repro_trace import Trace,TOKENS
from verl.utils.parallel_structure import layout
from verl.utils.rollout_trace import rollout_trace_op

@register('parallel_thinking_agent_v3')
class ParallelThinkingAgentLoopV3(AgentLoopBase):
    @classmethod
    def init_class(cls,config,tokenizer,**kwargs):
        if cls._class_initialized:return
        agent=config.actor_rollout_ref.rollout.agent
        if not config.actor_rollout_ref.rollout.get('structured_unseen',False):
            raise ValueError('Counted Unseen loop requires structured_unseen=true; causal fallback is prohibited')
        encoded=[tokenizer.encode(t,add_special_tokens=False) for t in TOKENS]
        if any(len(x)!=1 for x in encoded) or len({x[0] for x in encoded})!=6:
            raise ValueError('Six distinct single-token control tags required')
        cls.tokenizer=tokenizer
        (cls.start_parallel_token,cls.end_parallel_token,cls.start_path_token,cls.end_path_token,cls.start_summary_token,cls.end_summary_token)=[x[0] for x in encoded]
        cls.structure_tags=[x[0] for x in encoded[:4]]
        cls.eos_token_id=tokenizer.eos_token_id
        from native_eos import native_eos_ids
        cls.eos_token_ids=native_eos_ids(tokenizer.name_or_path, tokenizer.eos_token_id)
        cls.new_line_token=tokenizer.encode('\n',add_special_tokens=False)
        if len(cls.new_line_token)!=1:raise ValueError('Counted width decoding requires single-token newline')
        think=tokenizer.encode('<think>',add_special_tokens=False)
        if len(think)!=1 or tokenizer.decode(think,skip_special_tokens=False)!='<think>' or think[0] in [*cls.structure_tags,*cls.eos_token_ids,tokenizer.pad_token_id]:
            raise ValueError('A distinct single-token <think> is required; tokenizer/embeddings must be prepared first')
        cls.think_prefix=think+cls.new_line_token
        cls.force_think_prefix=bool(agent.get('force_think_prefix',True))
        cls.max_iterations_for_parallel_thinking=agent.max_iterations_for_parallel_thinking
        cls.max_path_response_length=agent.max_path_response_length
        cls.min_paths=int(agent.get('min_paths',2));cls.max_paths=int(agent.get('max_paths',8))
        if not 2<=cls.min_paths<=cls.max_paths<=8:raise ValueError('Supported width range is 2..8')
        cls.prompt_length=config.actor_rollout_ref.rollout.prompt_length
        cls.response_length=config.actor_rollout_ref.rollout.response_length
        cls._class_initialized=True

    @rollout_trace_op
    async def run(self,messages:list[dict[str,Any]],sampling_params:dict[str,Any])->AgentLoopOutput:
        prefix=await self.loop.run_in_executor(None,lambda:self.tokenizer.apply_chat_template(messages,add_generation_prompt=True,tokenize=True))
        initial=list(prefix);start=len(initial)
        if start>self.prompt_length:raise ValueError('Prompt exceeds configured limit')
        ids=list(initial);mask=[];calls=[];forks=0;path_groups=[];critical_depth=0;invalid=False
        self.trace=Trace(getattr(self,'trajectory',{}),start)
        self.trace.record.update(messages=messages,prompt_ids=initial)
        def left():return self.response_length-len(mask)
        def inject(tokens):ids.extend(tokens);mask.extend([0]*len(tokens))
        def sampled(tokens,call):
            assert len(tokens)==len(call['generated_ids'])
            call['response_start']=len(mask);ids.extend(tokens);mask.extend([1]*len(tokens));calls.append(call)
        async def generate(phase,prompt,budget,stops):
            sp={**copy.deepcopy(sampling_params),'n':1,'max_tokens':int(budget),'stop_token_ids':stops,'_structure_start':start,'seed':random.randrange(2**31)}
            result=await self.trace.generate(self.server_manager,phase,request_id=uuid4().hex,prompt_ids=list(prompt),sampling_params=sp)
            if len(result)>budget:raise ValueError('Generation server exceeded token budget')
            return list(result),dict(prompt_ids=list(prompt),generated_ids=list(result),phase=phase,temperature=sp.get('temperature',1.),
                structure_start=start,structure_tags=self.structure_tags,pad_id=self.tokenizer.pad_token_id,structured_unseen=True)
        already_thinking=initial[-1:]==self.think_prefix[:1] or initial[-len(self.think_prefix):]==self.think_prefix
        forced_think=self.think_prefix[:max(0,left())] if self.force_think_prefix and not already_thinking else []
        inject(forced_think)
        self.trace.record.update(forced_think_prefix_tokens=len(forced_think),think_prefix_already_in_prompt=already_thinking)
        while left()>0:
            raw,call=await generate('main',ids,left(),[self.start_parallel_token,*self.eos_token_ids])
            sampled(raw,call);critical_depth+=len(raw)
            if not raw or raw[-1]!=self.start_parallel_token or left()<=0:break
            if self.max_iterations_for_parallel_thinking and forks>=self.max_iterations_for_parallel_thinking:break
            header,hcall=await generate('width',ids,min(4,left()),[self.new_line_token[0],*self.eos_token_ids,self.start_path_token,self.end_path_token,self.start_parallel_token,self.end_parallel_token,self.start_summary_token,self.end_summary_token])
            sampled(header,hcall);critical_depth+=len(header)
            text=self.tokenizer.decode(header,skip_special_tokens=False)
            if re.fullmatch(r'[2-8]\n',text) is None or not self.min_paths<=int(text)<=self.max_paths or not header or header[-1]!=self.new_line_token[0]:
                invalid=True;break
            width=int(text)
            path_prefixes=[[self.start_path_token]+self.tokenizer.encode(str(i)+'\n',add_special_tokens=False) for i in range(1,width+1)]
            suffix=[self.end_parallel_token]+self.new_line_token+[self.start_summary_token]
            overhead=sum(len(p)+1 for p in path_prefixes)+len(suffix)+1
            budget=min(int(self.max_path_response_length or left()),(left()-overhead)//width)
            if budget<=0:break
            fork_prefix=list(ids);self.trace.fork(len(mask)-len(header)-1)
            results=await asyncio.gather(*[generate('path',fork_prefix+p,budget,[self.end_path_token,*self.eos_token_ids,self.start_path_token,self.start_parallel_token,self.end_parallel_token,self.start_summary_token,self.end_summary_token]) for p in path_prefixes])
            spans=[];lengths=[]
            for p,(raw,call) in zip(path_prefixes,results):
                opening=len(ids);inject(p)
                assembled=list(raw)
                if assembled and assembled[-1] in [*self.eos_token_ids,self.start_path_token,self.start_parallel_token,self.end_parallel_token,self.start_summary_token,self.end_summary_token]:assembled[-1]=self.end_path_token
                sampled(assembled,call)
                if not assembled or assembled[-1]!=self.end_path_token:inject([self.end_path_token])
                spans.append((opening,len(ids)));lengths.append(len(raw))
            path_groups.append(spans);forks+=1;critical_depth+=max(lengths,default=0)
            inject(suffix)
            if left()>1:
                raw,call=await generate('summary',ids,left()-1,[self.end_summary_token,*self.eos_token_ids,self.start_parallel_token,self.end_parallel_token,self.start_path_token,self.end_path_token,self.start_summary_token])
                assembled=list(raw)
                if assembled and assembled[-1] in [*self.eos_token_ids,self.start_parallel_token,self.end_parallel_token,self.start_path_token,self.end_path_token,self.start_summary_token]:assembled[-1]=self.end_summary_token
                sampled(assembled,call);critical_depth+=len(raw)
                if not assembled or assembled[-1]!=self.end_summary_token:inject([self.end_summary_token])
            else:inject([self.end_summary_token])
        assert len(mask)<=self.response_length
        response=ids[start:]
        # An invalid header may terminate on a misnested control tag. Its last
        # label is still sampled/scored, but has no outgoing prediction context.
        parsed_ids=ids[:-1]+[1] if invalid and ids[-1] in self.structure_tags else ids
        positions,_=layout(torch.tensor(parsed_ids),start,self.structure_tags,self.tokenizer.pad_token_id,allow_partial=True)
        leftpad=self.prompt_length-start
        positions=torch.cat([torch.zeros(leftpad,dtype=torch.long),positions,torch.zeros(self.response_length-len(response),dtype=torch.long)])
        masks=[]
        for spans in path_groups:
            for i,(s,e) in enumerate(spans):
                for t,u in spans[:i]:masks.append((leftpad,s+leftpad,e+leftpad,t+leftpad,u+leftpad))
        self.trace.record.update(policy_calls=calls,critical_depth=critical_depth,invalid_width=invalid)
        self.trace.finish(self.tokenizer,response,mask,positions,masks,len(response),truncated=len(response)>=self.response_length)
        return AgentLoopOutput(prompt_ids=initial,response_ids=response,response_mask=mask,rollout_calls=calls,position_required_mask=masks,
            multiverse_pos_ids=positions,num_turns=forks+1,metrics={},repro_stats=dict(forks=forks,critical_depth=critical_depth,
                positions=self.trace.record['parallel_relative_positions'],generation_calls=len(self.trace.record['calls']),
                generated_tokens=self.trace.record['generated_tokens_total'],sampled_tokens=sum(mask),forced_tokens=len(mask)-sum(mask),truncated=len(response)>=self.response_length,invalid_width=invalid))
