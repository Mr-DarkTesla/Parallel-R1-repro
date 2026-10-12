"""Separate actual4B FP32 inference protocol gate, max_paths2 versus8.

Does not launch workers, allocate resources, alter primary runtime or train.
An existing lane owner must invoke this after its protected queue predecessors.
"""
import argparse
import copy
import gc
import hashlib
import json
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
RUNNER=HERE.parent/'production-runner'
sys.path.insert(0,str(RUNNER))


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d): p.write_text(json.dumps(d,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',required=True)
    parser.add_argument('--device',default='cuda:0')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    config=json.loads(Path(args.config).read_text())
    output=Path(args.output); output.mkdir(parents=True,exist_ok=False)
    report=dict(passed=False,state='preparing',protocol='separate-width8-inference-FP32',
                config=config,config_sha256=sha(args.config),models=[],
                no_optimizer_resident=True,primary_runtime_changed=False,
                source_sha256={str(p.relative_to(ROOT)):sha(p) for p in
                    [Path(__file__),RUNNER/'train.py',RUNNER/'rollout.py',RUNNER/'structured_replay.py',
                     RUNNER/'decoder.py',RUNNER/'microbatch_decoder.py',RUNNER/'source/parallel_structure.py']})
    save(output/'result.json',report)
    try:
        import torch
        from transformers import AutoModelForCausalLM,AutoTokenizer
        import structured_replay as replay
        from rollout import execute,native_eos_ids
        from microbatch_decoder import MicrobatchedHFDecoder
        from train import instruct_prefix
        from source.parallel_structure import layout,attention
        if not args.device.startswith('cuda'):
            raise ValueError('Actual4B deployment proof requires the assigned CUDA lane')
        torch.backends.cuda.matmul.allow_tf32=False
        torch.backends.cudnn.allow_tf32=False
        torch.set_float32_matmul_precision('highest')
        device=torch.device(args.device); torch.cuda.set_device(device)
        questions=[json.loads(l) for l in Path(config['questions']).read_text().splitlines()]
        count=int(config.get('sample_count',2))
        assert 1<=count<=4 and len(config['models'])<=3
        questions=questions[:count]
        system=Path(config['system']).read_text()
        report['input_sha256']={config['questions']:sha(config['questions']),config['system']:sha(config['system'])}
        tolerance=float(config.get('max_logp_delta',.01))
        mean_limit=float(config.get('mean_logp_delta',.002)); p95_limit=float(config.get('p95_logp_delta',.005))
        response_budget=int(config.get('response_budget',4096))
        path_budget=int(config.get('path_budget',768)); max_context=int(config.get('max_context',16384))
        assert (response_budget,path_budget,max_context)==(4096,768,16384)
        for entry in config['models']:
            path=Path(entry['path']); assert path.is_relative_to(ROOT) and path.is_dir()
            tok=AutoTokenizer.from_pretrained(path,local_files_only=True)
            model=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,
                    torch_dtype=torch.float32,attn_implementation='sdpa').to(device).eval()
            model.gradient_checkpointing_disable()
            for parameter in model.parameters(): parameter.requires_grad_(False)
            assert sum(p.numel() for p in model.parameters())>=4_000_000_000
            assert all(p.dtype==torch.float32 for p in model.parameters())
            eos=native_eos_ids(path,tok)
            names=['<Parallel>','</Parallel>','<Path>','</Path>','<Summary>','</Summary>']
            encoded=[tok.encode(t,add_special_tokens=False) for t in names]
            assert all(len(v)==1 for v in encoded)
            tags=[v[0] for v in encoded]; tc=tok.encode('</think>',add_special_tokens=False)
            assert len(tc)==1 and tok.pad_token_id is not None
            original_forward=model.forward; observed=[0]; observed_shapes=[]
            def counted_forward(*a,**kw):
                observed[0]+=1
                observed_shapes.append(list(kw['input_ids'].shape))
                return original_forward(*a,**kw)
            model.forward=counted_forward
            decoders={n:MicrobatchedHFDecoder(model,replay,str(device),max_paths=n) for n in [2,8]}
            record=dict(name=entry['name'],path=str(path),dtype='FP32',tf32=False,
                        inference_no_optimizer=True,wide_fixtures=[],sampled_traces=[])
            model_peak=0
            def measured(function):
                nonlocal model_peak
                torch.cuda.synchronize(device); torch.cuda.reset_peak_memory_stats(device)
                observed[0]=0; observed_shapes.clear(); started=time.perf_counter()
                value=function()
                torch.cuda.synchronize(device)
                elapsed=time.perf_counter()-started; peak=torch.cuda.max_memory_allocated(device)
                model_peak=max(model_peak,peak)
                free,total=torch.cuda.mem_get_info(device)
                return value,dict(seconds=elapsed,observed_model_forward_calls=observed[0],
                                  observed_input_shapes=copy.deepcopy(observed_shapes),
                                  peak_allocated_bytes=peak,reserved_bytes=torch.cuda.memory_reserved(device),
                                  free_bytes=free,total_bytes=total)
            def drift(values):
                tensor=torch.tensor(values,dtype=torch.float32)
                summary=dict(maximum=float(tensor.max()),mean=float(tensor.mean()),p95=float(tensor.quantile(.95)))
                assert summary['maximum']<=tolerance and summary['mean']<=mean_limit and summary['p95']<=p95_limit,summary
                return summary
            fixture_prefix=instruct_prefix(tok,[dict(role='system',content=system),
                                               dict(role='user',content=questions[0]['problem'])])
            assert tok.decode(fixture_prefix,skip_special_tokens=False).endswith('<think>\n')
            body=tok.encode('1+1=2. ',add_special_tokens=False)
            assert body and not set(body)&set(tags+[tc[0]]+eos)
            for width in [2,4,8]:
                calls=[]; targets=[]
                for row in range(width):
                    suffix=tok.encode('Plan: Calculate independent parts.\n<Parallel>'+str(width)+'\n<Path>'+str(row+1)+'\n'+('Intermediate step. '*(row%3)),add_special_tokens=False)
                    call=dict(phase='path',prompt_ids=fixture_prefix+suffix,structure_start=len(fixture_prefix),
                              structure_tags=tags[:4],pad_id=tok.pad_token_id,blocked_token_ids=[tc[0]],
                              temperature=1.,seed=52161011+row)
                    target=(body*32)[:16+row*8]+[tags[3]]
                    assert len(call['prompt_ids'])+len(target)<max_context
                    calls.append(call); targets.append(target)
                results={}; times={}; stats={}
                for n in [2,8]:
                    results[n],times[n]=measured(lambda n=n:decoders[n].decode_many(calls,128,
                                                [*tags,*eos],target_sequences=targets))
                    stats[n]=copy.deepcopy(decoders[n].last_batch_stats)
                    assert times[n]['observed_model_forward_calls']==stats[n]['physical_forward_calls']
                    if n==8:
                        assert stats[n]['sequential_subgroup_count']==1
                        assert stats[n]['physical_forward_calls']==max(map(len,targets))
                        assert all(s[0]==width for s in times[n]['observed_input_shapes'])
                differences=[]; replay_differences=[]
                for call,a,b in zip(calls,results[2],results[8]):
                    assert a[0]==b[0] and a[2]==b[2]
                    differences.extend(abs(x-y) for x,y in zip(a[1],b[1]))
                    full,_=replay.score_call(model,dict(call,generated_ids=b[0]))
                    replay_differences.extend((full.detach().cpu()-torch.tensor(b[1])).abs().tolist())
                    del full
                # Masked left padding and another row's prompt cannot leak.
                changed=copy.deepcopy(calls); changed[0]['prompt_ids'][-1]=body[0]
                perturbed=decoders[8].decode_many(changed,128,[*tags,*eos],target_sequences=targets)
                sibling_differences=[abs(x-y) for a,b in zip(results[8][1:],perturbed[1:]) for x,y in zip(a[1],b[1])]
                changed=copy.deepcopy(calls)
                for call in changed: call['pad_id']=body[0]
                other_pad=decoders[8].decode_many(changed,128,[*tags,*eos],target_sequences=targets)
                padding_differences=[abs(x-y) for a,b in zip(results[8],other_pad) for x,y in zip(a[1],b[1])]
                model_peak=max(model_peak,torch.cuda.max_memory_allocated(device))
                record['wide_fixtures'].append(dict(width=width,generated_lengths=list(map(len,targets)),
                    old_logp_drift=drift(differences),replay_drift=drift(replay_differences),
                    sibling_perturbation_drift=drift(sibling_differences),padding_value_drift=drift(padding_differences),
                    timings={str(k):v for k,v in times.items()},
                    measured_forward_calls={str(k):stats[k]['physical_forward_calls'] for k in [2,8]},
                    prefix_lengths=[len(c['prompt_ids']) for c in calls]))
            for question in questions:
                seed=int(config.get('seed_base',42161011))+int(question['index'])*1000
                prefix=instruct_prefix(tok,[dict(role='system',content=system),dict(role='user',content=question['problem'])])
                traces={}; times={}
                for n in [2,8]:
                    traces[n],times[n]=measured(lambda n=n:execute(tok,prefix,decoders[n],eos,
                                                              response_budget,path_budget,max_context,seed))
                    assert times[n]['observed_model_forward_calls']==traces[n]['stats']['actual_model_forward_calls']
                    if n==8:
                        assert all(g['sequential_subgroup_count']==1 for g in traces[n]['fork_batch_ledger'])
                a,b=traces[2],traces[8]
                for key in ['prompt_ids','response_ids','response_mask','output','widths','path_lengths']:
                    assert a[key]==b[key],(entry['name'],question['id'],key,'sampled_trace_diverged')
                assert len(a['policy_calls'])==len(b['policy_calls'])
                differences=[]; replay_differences=[]; covered=[0]*len(b['response_mask'])
                for x,y in zip(a['policy_calls'],b['policy_calls']):
                    for key in ['phase','prompt_ids','generated_ids','response_start','seed','blocked_token_ids']:
                        assert x[key]==y[key],(question['id'],key)
                    differences.extend(abs(i-j) for i,j in zip(x['old_logprobs'],y['old_logprobs']))
                    full,_=replay.score_call(model,y)
                    replay_differences.extend((full.detach().cpu()-torch.tensor(y['old_logprobs'])).abs().tolist())
                    del full
                    for at in range(y['response_start'],y['response_start']+len(y['generated_ids'])):
                        assert not covered[at] and b['response_mask'][at]; covered[at]=1
                assert covered==b['response_mask']
                ids=torch.tensor(prefix+b['response_ids'])
                positions,spans=layout(ids,len(prefix),tags[:4],tok.pad_token_id,allow_partial=True)
                allowed=attention(ids,len(prefix),tags[:4],tok.pad_token_id,allow_partial=True)
                for ranges in spans:
                    assert len({int(positions[s]) for s,e in ranges})==1
                    for s,e in ranges[1:]: assert not allowed[s:e,ranges[0][0]:s].any()
                for n in [2,8]: save(output/(entry['name']+'-'+str(question['index'])+'-maxpaths'+str(n)+'.json'),traces[n])
                model_peak=max(model_peak,torch.cuda.max_memory_allocated(device))
                record['sampled_traces'].append(dict(id=question['id'],index=question['index'],seed=seed,
                    exact_actions_masks_prefixes=True,old_logp_drift=drift(differences),replay_drift=drift(replay_differences),
                    actual_forward_calls={str(n):traces[n]['stats']['actual_model_forward_calls'] for n in [2,8]},
                    sampled_tokens=b['stats']['sampled_tokens'],widths=b['widths'],timings={str(n):times[n] for n in [2,8]},
                    budget=response_budget,format_guard='same frozen execute think-close guard'))
            record['peak_allocated_bytes']=model_peak
            report['models'].append(record); report['state']='checking'; save(output/'result.json',report)
            # Drop every closure/decoder reference before loading another4B.
            model.forward=original_forward
            del decoders,original_forward,model,tok,measured
            gc.collect(); torch.cuda.empty_cache()
        report.update(passed=True,state='passed',quality_accuracy_not_measured=True,
                      separate_width8_protocol=True,optimizer_memory_not_proven=True,
                      sampling_parameters=dict(temperature=1.,top_p=None,top_k=None))
        save(output/'result.json',report)
        print(json.dumps(dict(passed=True,output=str(output),models=len(report['models']))))
    except BaseException as error:
        report.update(passed=False,state='failed',error=repr(error)); save(output/'result.json',report)
        raise


if __name__=='__main__': main()
