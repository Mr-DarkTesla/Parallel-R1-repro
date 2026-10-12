"""Exercise the actual frozen Base counted-loop body without Ray/vLLM."""
import ast
import asyncio
import copy
import hashlib
import json
import random
import re
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import uuid4
import torch
from transformers import AutoTokenizer
from source.parallel_structure import layout, attention

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = ROOT/'work/experiments/base-format-20261010'
sys.path.insert(0,str(BASE/'evaluations'))
TOKENS = ('<Parallel>','</Parallel>','<Path>','</Path>','<Summary>','</Summary>')


class Config(dict):
    __getattr__ = dict.__getitem__


class Trace:
    def __init__(self, trajectory, start):
        self.record = dict(calls=[], forks=[])
    async def generate(self, manager, phase, **kwargs):
        out = await manager.generate(phase=phase, **kwargs)
        self.record['calls'].append(dict(phase=phase, generated_ids=out, generated_tokens=len(out)))
        return out
    def fork(self, index):
        self.record['forks'].append(index)
    def finish(self, tokenizer, ids, mask, positions, masks, length, **kwargs):
        self.record.update(parallel_relative_positions=[], calls=self.record['calls'],
                          generated_tokens_total=sum(c['generated_tokens'] for c in self.record['calls']))


class Server:
    def __init__(self, tokenizer, width, mode):
        self.tok, self.width, self.mode = tokenizer, width, mode
        self.rounds = 0
    async def generate(self, phase, prompt_ids, sampling_params, **kwargs):
        enc = lambda s:self.tok.encode(s,add_special_tokens=False)
        if phase=='main':
            self.rounds += 1
            return enc('Plan: independent calculations.\n<Parallel>') if self.rounds<=4 else enc('Final Answer: 5.')+[self.tok.eos_token_id]
        if phase=='width':
            return enc(str(self.width)+'\n')
        if phase=='path':
            tail = {'normal':'</Path>', 'eos':self.tok.eos_token, 'wrong-control':'<Parallel>'}[self.mode]
            return enc('Result = 5. '+tail)
        if phase=='summary':
            tail = '</Summary>' if self.mode=='normal' else self.tok.eos_token
            return enc('Combine results = 5. '+tail)
        raise AssertionError(phase)


def load_loop():
    path = HERE/'source/counted_loop.py'
    tree = ast.parse(path.read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    cls.decorator_list=[]
    for n in cls.body:
        if isinstance(n,ast.AsyncFunctionDef):n.decorator_list=[]
    env = dict(torch=torch, asyncio=asyncio, copy=copy, random=random, re=re,
               Any=Any, uuid4=uuid4, AgentLoopBase=object, layout=layout,
               Trace=Trace, TOKENS=TOKENS, AgentLoopOutput=lambda **kw:SimpleNamespace(**kw))
    exec(compile(ast.Module(body=[cls],type_ignores=[]),str(path),'exec'),env)
    return env[cls.name]


async def check(width, mode, tok):
    cls = load_loop(); cls._class_initialized=False
    agent = Config(force_think_prefix=False,min_paths=2,max_paths=8,
                    max_iterations_for_parallel_thinking=4,max_path_response_length=64)
    config = Config(actor_rollout_ref=Config(rollout=Config(prompt_length=1024,response_length=4096,
                   structured_unseen=True,agent=agent)))
    cls.init_class(config,tok)
    loop = cls(); loop.loop=asyncio.get_running_loop();loop.server_manager=Server(tok,width,mode)
    out = await loop.run([dict(role='system',content='Solve carefully.'),dict(role='user',content='2+3?')],
                         dict(temperature=1.,top_p=1.,top_k=-1))
    assert out.repro_stats['forks']==4
    assert len(out.position_required_mask)==4*width*(width-1)//2
    assert sum(out.response_mask)==sum(len(c['generated_ids']) for c in out.rollout_calls)
    assert sum(out.response_mask)<len(out.response_mask)
    assert out.repro_stats['critical_depth']<out.repro_stats['sampled_tokens']
    coverage=[0]*len(out.response_mask)
    replacements=0
    for c in out.rollout_calls:
        s=c['response_start'];e=s+len(c['generated_ids'])
        coverage[s:e]=[1]*(e-s)
        replacements+=sum(a!=b for a,b in zip(c['generated_ids'],out.response_ids[s:e]))
    assert coverage==out.response_mask
    assert replacements==(0 if mode=='normal' else 4*(width+1))
    initial=out.prompt_ids;ids=torch.tensor(initial+out.response_ids)
    positions,groups=layout(ids,len(initial),cls.structure_tags,tok.pad_token_id)
    assert len(groups)==4 and all(len(g)==width for g in groups)
    offset=1024-len(initial)
    assert torch.equal(out.multiverse_pos_ids[offset:offset+len(ids)],positions)
    mask=attention(ids,len(initial),cls.structure_tags,tok.pad_token_id)
    for paths in groups:
        for i,(s,e) in enumerate(paths):
            for j,(t,u) in enumerate(paths):
                if i!=j:assert not mask[s:e,t:u].any()
    return dict(width=width,mode=mode,forks=4,replaced_raw_actions=replacements,
                sampled_tokens=sum(out.response_mask),forced_tokens=len(out.response_mask)-sum(out.response_mask))


def main():
    tok=AutoTokenizer.from_pretrained(BASE/'runs/production/final',local_files_only=True)
    rows=[asyncio.run(check(w,m,tok)) for w in [2,3,4,6,8] for m in ['normal','eos','wrong-control']]
    report=dict(passed=True,cases=rows,actual_frozen_loop_tested=True,
                token_policy='Raw sampled controls are scored; assembled stop replacements are never relabeled as sampled actions',
                hashes={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [HERE/'source/counted_loop.py',HERE/'source/parallel_structure.py',Path(__file__)]})
    (HERE/'loop-proof.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases=len(rows))))


if __name__=='__main__':main()
