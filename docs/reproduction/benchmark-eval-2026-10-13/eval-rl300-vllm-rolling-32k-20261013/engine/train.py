"""Full-weight exact-context PPO reference, configurable response allocation across distributed GPUs.

Group centered rewards, no std normalization, fixed response-budget denominator.
There is exactly one optimizer update per fresh rollout batch. The rollout and
replay share HF SDPA operations; no flattened causal trajectory replay exists.
"""
import argparse
import contextlib
import gc
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import random
import sys
import time
import lane_profile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/"verl").is_dir() and (p/"README.md").is_file())


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2)+'\n')
    os.replace(tmp, path)


def centered(rewards):
    if len(rewards) < 2 or not all(math.isfinite(x) for x in rewards):
        raise ValueError('Finite group of >=2 rewards required')
    mean = sum(rewards)/len(rewards)
    return [x-mean for x in rewards]


def ppo_token_loss(new_logp, old_logp, advantage, clip=.2):
    import torch
    ratio = (new_logp-old_logp).exp()
    return -torch.minimum(ratio*advantage, ratio.clamp(1-clip, 1+clip)*advantage), ratio


def format_flags(text, stats):
    """No-think counted schema with Plan assignment before every executed fork."""
    good = '<think>' not in text and text.count('</think>') == 1
    thinking, final = text.split('</think>',1) if '</think>' in text else (text,'')
    good = good and not any(tag in final for tag in ['<Parallel>','</Parallel>','<Path>','</Path>','<Summary>','</Summary>'])
    good = good and not stats['invalid_width'] and not stats['truncated']
    for a, b in [('Parallel', 'Parallel'), ('Path', 'Path'), ('Summary', 'Summary')]:
        good = good and text.count('<'+a+'>') == text.count('</'+b+'>')
    blocks = list(__import__('re').finditer(r'<Parallel>([2-8])\n(.*?)</Parallel>\s*<Summary>(.*?)</Summary>', text, __import__('re').S))
    good = good and len(blocks) == stats['forks'] == text.count('<Parallel>')
    previous = 0
    for m in blocks:
        width = int(m[1])
        paths = __import__('re').findall(r'<Path>\s*([1-8])\n(.*?)</Path>', m[2], __import__('re').S)
        good = good and len(paths) == width and [int(x[0]) for x in paths] == list(range(1, width+1))
        plan = text[previous:m.start()].rsplit('Plan:', 1)
        assigned = [int(x) for x in __import__('re').findall(r'^\s*([1-8]):', plan[-1], __import__('re').M)]
        good = good and len(plan) == 2 and assigned == list(range(1, width+1))
        previous = m.end()
    finals = list(__import__('re').finditer(r'(?im)^Final Answer:\s*', text))
    good = good and len(finals) == 1 and finals[0].start() > text.find('</think>')
    good = good and not any(m.start() <= f.start() < m.end() for m in blocks for f in finals)
    return bool(good), bool(good and blocks)


def identity_gate(config, receipt, config_path):
    """A root-reviewed receipt binds the exact runnable inputs and passed audit."""
    gate = json.loads(Path(receipt).read_text())
    if not gate.get('approved'):
        raise ValueError('Root receipt has not approved this run')
    if gate.get('config_sha256') != sha(config_path):
        raise ValueError('Root receipt must bind the exact configuration')
    for name, path in config['sealed_inputs'].items():
        if gate.get('sha256', {}).get(name) != sha(path):
            raise ValueError('Root receipt hash mismatch: '+name)
    audit = json.loads(Path(config['gpu_audit']).read_text())
    if not audit.get('passed'):
        raise ValueError('Actual GPU semantic audit did not pass')
    optimizer_proof = gate['distributed_smoke']
    if sha(optimizer_proof['path']) != optimizer_proof['sha256']:
        raise ValueError('Distributed optimizer proof hash mismatch')
    if not json.loads(Path(optimizer_proof['path']).read_text()).get('passed'):
        raise ValueError('Distributed optimizer proof failed')
    return gate


def instruct_prefix(tok, messages):
    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)
    if text.endswith('<think>'):
        text += '\n'
    elif not text.endswith('<think>\n'):
        text += '<think>\n'
    return tok.encode(text, add_special_tokens=False)


def main():
    import torch
    import torch.distributed as dist
    from torch.nn.parallel import DistributedDataParallel as DDP
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from rollout import execute, HFDecoder, native_eos_ids
    p = argparse.ArgumentParser()
    p.add_argument('--config', required=True)
    p.add_argument('--receipt')
    p.add_argument('--smoke', action='store_true')
    args = p.parse_args()
    cfg = json.loads(Path(args.config).read_text())
    assert cfg['ppo_epochs']==1 and cfg['updates_per_fresh_batch']==1 and cfg['async_rollout'] is False
    assert cfg['precision_mode']=='full_bf16_compute_fp32_master' and cfg['actor_dtype']=='vllm_bf16'
    assert cfg['master_dtype']=='fp32' and cfg['learner_compute_dtype']=='bf16' and cfg['gradient_reduce_dtype']=='fp32'
    assert cfg['rollout_correction']==dict(mode='token_tis',upper=2.,lower=0.,batch_normalize=False,bypass=False)
    assert cfg['global_batch']==dict(prompts_per_step=8,rollouts_per_prompt=4,responses_per_step=32)
    assert cfg['std_normalization'] is False and cfg['bonus_schedule']=='constant_no_annealing'
    assert (cfg['response_budget'],cfg['path_budget'],cfg['max_context'])==(4096,768,16384)
    if not args.smoke:
        if not args.receipt:
            raise ValueError('Production requires a root approval receipt')
        identity_gate(cfg, args.receipt, args.config)
    output = Path(cfg['output'])
    if not output.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Output must be inside project root')
    rank = int(os.environ.get('RANK', '0'))
    world = int(os.environ.get('WORLD_SIZE', '1'))
    if world != int(cfg['expected_world_size']):
        raise ValueError('World size must match the configured GPU count')
    if cfg.get('resume'):
        raise ValueError('This run exports weights only and uses fresh Adam; configure weights-only initial_step for continuation')
    local_rank = int(os.environ.get('LOCAL_RANK', '0'))
    torch.cuda.set_device(local_rank)
    torch.backends.cuda.matmul.allow_tf32 = cfg.get("precision_mode", "fp32") == "tf32"
    torch.backends.cudnn.allow_tf32 = cfg.get("precision_mode", "fp32") == "tf32"
    torch.set_float32_matmul_precision('high' if cfg.get('precision_mode') == 'tf32' else 'highest')
    device = torch.device('cuda', local_rank)
    if world > 1:
        dist.init_process_group('nccl')
        metadata_group=dist.new_group(backend='gloo')
    if rank == 0:
        output.mkdir(parents=True, exist_ok=False)
        atomic_json(output/'config.json', cfg)
        atomic_json(output/'status.json', dict(state='loading', started=time.time(), world_size=world))
    if world > 1:
        dist.barrier()
    # DDP barriers do not invalidate per-node NFS negative directory caches.
    # mkdir from each client refreshes the parent before creating rank-local files.
    output.mkdir(parents=True, exist_ok=True)
    profiler = lane_profile.Profile(output/'profile', rank, cfg.get('precision_mode', 'fp32'))
    train = [json.loads(x) for x in Path(cfg['train']).read_text().splitlines() if x.strip()]
    if len(train)!=1024:
        raise ValueError('Pinned1024 training rows required')
    sys.path.insert(0, str(Path(cfg['replay']).parent))
    replay = load_module('exact_replay', cfg['replay'])
    reward = load_module('campaign_reward', cfg['reward'])
    scorer = load_module('frozen_answer_scorer', cfg['scorer'])
    validator = load_module('frozen_base_validator', cfg['format_validator'])
    tok = AutoTokenizer.from_pretrained(cfg['model'], local_files_only=True)
    instruction = Path(cfg['system']).read_text()
    torch.manual_seed(cfg.get('seed', 20261010))
    random.seed(cfg.get('seed', 20261010))
    initial_model = str(Path(cfg['resume'])/'hf') if cfg.get('resume') else cfg['model']
    model = AutoModelForCausalLM.from_pretrained(initial_model, torch_dtype=torch.float32,
            attn_implementation='sdpa', local_files_only=True, low_cpu_mem_usage=True).to(device)
    if any(float(getattr(model.config, name, 0) or 0) != 0 for name in ('attention_dropout', 'hidden_dropout', 'hidden_dropout_prob')):
        raise ValueError('Reference PPO requires zero dropout for exact replay')
    physical_forward_counter = [0]
    operation_dtypes={}
    original_forward = model.forward
    def counted_forward(*args, **kwargs):
        physical_forward_counter[0] += 1
        out=lane_profile.model_forward(original_forward, *args, **kwargs)
        if torch.is_autocast_enabled('cuda'):
            role='teacher' if model.training else 'actor_or_fixture'
            operation_dtypes[role]=dict(logits=str(out.logits.dtype),master_lm_head=str(model.lm_head.weight.dtype),autocast=str(torch.get_autocast_dtype('cuda')),softmax_logprobs='torch.float32')
        return out
    model.forward = counted_forward
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    model.config.use_cache = True
    ddp = DDP(model, device_ids=[local_rank], broadcast_buffers=False,
              gradient_as_bucket_view=True, bucket_cap_mb=25) if world > 1 else model
    optimizer_options = dict(lr=float(cfg.get('lr', 1e-6)), betas=(.9,.999), eps=1e-8, weight_decay=0., foreach=False)
    if cfg.get('zero1_optimizer', True) and world > 1:
        from torch.distributed.optim import ZeroRedundancyOptimizer
        optimizer = ZeroRedundancyOptimizer(model.parameters(), optimizer_class=torch.optim.AdamW, **optimizer_options)
    else:
        optimizer = torch.optim.AdamW(model.parameters(), **optimizer_options)
    sharded_optimizer = cfg.get('zero1_optimizer', True) and world > 1
    params = sum(x.numel() for x in model.parameters() if x.requires_grad)
    assert all(p.dtype==torch.float32 for p in model.parameters())
    if params < 4_000_000_000:
        raise ValueError('All-weight 4B arm required')
    from actor_buddy import ActorBuddy
    decoder=ActorBuddy(model,cfg,rank,local_rank)
    eos = native_eos_ids(cfg['model'], tok)
    from batching import assignments, prompt_advantages, ddp_loss_scale, rollout_seed
    batch = cfg['global_batch']
    prompts = int(batch['prompts_per_step'])
    reward_group = int(batch['rollouts_per_prompt'])
    assert batch['responses_per_step'] == prompts * reward_group
    local_assignments = assignments(rank, world, prompts, reward_group)
    group = len(local_assignments)
    loss_scale = ddp_loss_scale(world, prompts, reward_group)
    steps = int(cfg.get('steps', 64))
    budget = int(cfg.get('response_budget', 4096))
    start_step = int(cfg.get('initial_step', 0))
    if not 0 <= start_step < steps:
        raise ValueError('initial_step must be below the global target steps')
    resume_proof = None
    if start_step:
        checkpoint = Path(cfg['initial_checkpoint'])
        complete = json.loads((checkpoint/'complete.json').read_text())
        assert complete['step'] == start_step and complete['unsharded'] and complete['model']
        assert Path(cfg['model']).resolve() == (checkpoint/'hf').resolve()
        resume_proof = dict(checkpoint=str(checkpoint), initial_step=start_step,
                            weights_only_continuation=True, optimizer_reset=True, exact_optimizer_resume=False)
    def memory_snapshot(stage):
        free,total=torch.cuda.mem_get_info(device)
        return dict(stage=stage,allocated=torch.cuda.memory_allocated(device),reserved=torch.cuda.memory_reserved(device),free=free,total=total,peak_allocated=torch.cuda.max_memory_allocated(device))

    metric_file = (output/f'metrics-rank-{rank}.jsonl').open('w', buffering=1)
    traces = (output/f'traces-rank-{rank}.jsonl').open('w', buffering=1)
    proximal_records=(output/f'proximal-rank-{rank}.jsonl').open('w',buffering=1)
    probe = model.model.layers[0].self_attn.q_proj.weight.reshape(-1)

    optimizer_update_id=start_step

    def validate(step):
        """Buddy actor snapshot over all clean val32; no reward/gradient/selection."""
        rows=[json.loads(line) for line in Path(cfg['val']).read_text().splitlines() if line.strip()]
        assert len(rows)==32 and len({row['id'] for row in rows})==32
        directory=output/f'validation-{step:04}'
        if rank==0:directory.mkdir(exist_ok=False);atomic_json(output/'status.json',dict(state='validating',step=step,planned=32,optimizer_update_id=optimizer_update_id))
        if world>1:dist.barrier()
        directory.mkdir(parents=True,exist_ok=True);requests=[]
        for index in range(rank,32,world):
            row=rows[index];prefix=instruct_prefix(tok,[dict(role='system',content=instruction),dict(role='user',content=row['problem'])])
            requests.append(dict(prefix=prefix,seed=cfg.get('validation_seed',91261011)+index*100,id=row['id'],answer=row['answer'],prompt_index=index,sample=0,index=index))
        model.eval();received=decoder.collect(requests,eos,step,purpose='validation');records=[]
        from replay_guard import synchronized_guard
        guard=decoder.last_rollout['guard'];parity,local_bad=synchronized_guard(guard['max'],guard['mean'],guard['p95'],device,world,max_allowed=.01)
        with (directory/f'rank-{rank}.jsonl').open('w',buffering=1) as f:
            for trace,request in zip(received,requests):
                assert trace['behavior_version']==optimizer_update_id
                coverage=[0]*len(trace['response_mask'])
                for call in trace['policy_calls']:
                    assert len(call['generated_ids'])==len(call['old_logprobs']) and all(math.isfinite(v) for v in call['old_logprobs'])
                    for at in range(call['response_start'],call['response_start']+len(call['generated_ids'])):assert not coverage[at] and trace['response_mask'][at]==1;coverage[at]=1
                assert coverage==trace['response_mask'];assert all(x['microbatch_max_paths']==8 and x['sequential_subgroup_count']==1 for x in trace['fork_batch_ledger'])
                grade=scorer.grade('<think>\n'+trace['output'],str(request['answer']));unknown=bool(grade.get('error')) or not parity
                flags=format_flags(trace['output'],trace['stats']);valid=bool(flags[0]) and not trace['stats']['invalid_width'] and not trace['stats']['truncated']
                trace.update(grade=grade,technical_unknown=unknown,correct=None if unknown else bool(grade['correct']),format_valid=valid,parallel_valid=valid and bool(trace['widths']),dataset=rows[request['index']].get('source','clean_val32'),step=step,index=request['index'],optimizer_update_id=optimizer_update_id,selection_allowed=False,benchmark=False,q_cached_guard=guard)
                f.write(json.dumps(trace,ensure_ascii=False)+'\n');records.append(dict(id=trace['id'],correct=trace['correct'],technical_unknown=unknown,format_valid=valid,parallel_valid=trace['parallel_valid'],widths=trace['widths'],stats=trace['stats']))
        groups=[None]*world
        if world>1:dist.all_gather_object(groups,records,group=metadata_group)
        else:groups[0]=records
        if rank==0:
            all_rows=[r for group in groups for r in group];assert len(all_rows)==32 and len({r['id'] for r in all_rows})==32
            atomic_json(directory/'summary.json',dict(step=step,optimizer_update_id=optimizer_update_id,completed=32,known=sum(not r['technical_unknown'] for r in all_rows),technical_unknown=sum(r['technical_unknown'] for r in all_rows),correct=sum(r['correct'] is True for r in all_rows),format_valid=sum(r['format_valid'] for r in all_rows),parallel_valid=sum(r['parallel_valid'] for r in all_rows),rows=all_rows,sampler='vLLM wholeBF16 same immutable actor; cleanval32 seed; fullwidth8/caps4096/768/16384',selection_allowed=False,benchmark=False,q_guard_passed=parity))
        if world>1:dist.barrier()
    if not cfg.get('skip_validation', False) and not cfg.get('skip_initial_validation',False):
        validate(start_step)
    parity_skips = 0
    parity_skip_streak = 0
    for step in range(start_step+1, steps+1):
        began = time.time()
        profiler.start(step)
        with profiler.phase('actor_weight_refresh',cuda=True):decoder.refresh_actor(optimizer_update_id)
        torch.cuda.reset_peak_memory_stats(device)
        memory_stages=[memory_snapshot('before_rollout')]
        trajectories = []
        model.eval()
        requests=[]
        for prompt_index,sample_index in local_assignments:
            position=int(cfg.get('prompt_exposure_offset',0))+(step-start_step-1)*prompts+prompt_index
            epoch,offset=divmod(position,len(train));order=list(range(len(train)));random.Random(cfg.get('data_seed',20261012)+epoch).shuffle(order);row=train[order[offset]]
            prefix=instruct_prefix(tok,[dict(role='system',content=instruction),dict(role='user',content=row['problem'])])
            requests.append(dict(prefix=prefix,seed=rollout_seed(cfg.get('seed',20261012),step,prompt_index,sample_index),id=row['id'],answer=row['answer'],prompt_index=prompt_index,sample=sample_index))
        with profiler.phase('rollout_execute_and_scoring',cuda=True):
            received=decoder.collect(requests,eos,step)
            for trajectory,request in zip(received,requests):
                assert trajectory['behavior_version']==optimizer_update_id
                row=dict(id=request['id'],answer=request['answer']);prompt_index=request['prompt_index'];sample_index=request['sample']
                assert all(x['microbatch_max_paths']==8 and x['sequential_subgroup_count']==1 for x in trajectory['fork_batch_ledger'])
                grade = scorer.grade('<think>\n'+trajectory['output'], str(row['answer']))
                if grade.get('error'):
                    raise ValueError('Scorer returned an unknown technical outcome: '+str(grade['error']))
                flags = dict(zip(['format','parallel'],format_flags(trajectory['output'],trajectory['stats'])))
                valid = bool(flags['format']) and not trajectory['stats']['invalid_width'] and not trajectory['stats']['truncated']
                parallel = valid and bool(trajectory['widths'])
                components = reward.score(bool(grade['correct']), valid, trajectory['stats']['critical_depth'],
                                          trajectory['stats']['sampled_tokens'], trajectory['widths'], step-1,
                                          cfg['reward_mode'],forward_calls=trajectory['stats']['actual_model_forward_calls'])
                trajectory.update(id=row['id'], answer=row['answer'], grade=grade, format_valid=valid,
                                  parallel_protocol_valid=parallel, reward=components, step=step, rank=rank, sample=sample_index, prompt_index=prompt_index)
                coverage = [0]*len(trajectory['response_mask'])
                for call in trajectory['policy_calls']:
                    for at in range(call['response_start'],call['response_start']+len(call['generated_ids'])):
                        assert not coverage[at] and trajectory['response_mask'][at] == 1
                        coverage[at] = 1
                assert coverage == trajectory['response_mask']
                trajectories.append(trajectory)
                traces.write(json.dumps(trajectory, ensure_ascii=False)+'\n')
        memory_stages.append(memory_snapshot('after_rollout'))
        local_rewards = [dict(prompt_index=t['prompt_index'], sample_index=t['sample'],
                              id=t['id'], reward=float(t['reward']['score'])) for t in trajectories]
        with profiler.phase('reward_gather_and_advantages', cuda=True):
            gathered_rewards = [None]*world
            if world > 1:
                dist.all_gather_object(gathered_rewards, local_rewards,group=metadata_group)
            else:
                gathered_rewards[0] = local_rewards
            by_response = prompt_advantages(gathered_rewards, prompts, reward_group)
            advantages = [by_response[t['prompt_index'], t['sample']] for t in trajectories]
        active = sum(abs(x)>1e-12 for x in advantages)
        model.train()
        optimizer.zero_grad(set_to_none=False)
        before = probe[:1024].detach().clone()
        total_loss = 0.
        rho_deltas=[];rho_weights=[]
        # q reexecution compares identical vLLM weights/query/KV/mask/shape;
        # learner BF16 teacher is a separate policy and never enters this guard.
        q_fixture=decoder.last_rollout['guard']
        from learner_layout_oracle import fp32_layout_oracle
        with profiler.phase('fp32_layout_oracle',cuda=True):p0_fixture=fp32_layout_oracle(model,replay,trajectories)
        native_q_fixture=dict(q_fixture,mode='same_vLLM_cached_operator_geometry')
        atomic_json(output/f'vllm-q-reference-step-{step}-rank-{rank}.json',native_q_fixture)
        max_drift = 0.
        replay_deltas = []
        clip_hits = 0
        action_count = sum(sum(t['response_mask']) for t in trajectories)
        all_calls = [(i,c) for i,t in enumerate(trajectories) for c in t['policy_calls'] if c['generated_ids']]
        if not all_calls:
            raise ValueError('Rollout returned no policy actions')
        for j, (i, call) in enumerate(all_calls):
            sync = j == len(all_calls)-1
            context = contextlib.nullcontext() if world==1 or sync else ddp.no_sync()
            with context:
                with profiler.phase("replay_forward"),torch.autocast('cuda',dtype=torch.bfloat16):
                    logp, _ = replay.score_call(ddp, call)
                old = torch.tensor(call['old_logprobs'], device=device)
                if not torch.isfinite(logp).all() or not torch.isfinite(old).all():
                    raise FloatingPointError('Nonfinite rollout/replay likelihood')
                # Exactly one fresh PPO update: p0 is theta BEFORE the optimizer step.
                # q remains immutable and is explicitly corrected through detached token TIS.
                p0=logp.detach() # SAME BF16 full-context teacher at frozen pre-update theta
                drift=(logp.detach()-p0).abs()
                p0_cpu=p0.cpu()
                rho_deltas.append(p0_cpu-torch.tensor(call['old_logprobs']))
                proximal_records.write(json.dumps(dict(step=step,rank=rank,trajectory=i,call=j,phase=call['phase'],behavior_version=trajectories[i]['behavior_version'],proximal_update_id=optimizer_update_id,q_logprobs=call['old_logprobs'],p0_logprobs=p0_cpu.tolist(),p0_is_frozen_pre_update=True,q_preserved=True))+'\n')
                del p0_cpu
                max_drift = max(max_drift, float(drift.max()))
                replay_deltas.append(drift.cpu())
                from tis_loss import three_policy_token_loss
                loss_tokens,ratio,rho=three_policy_token_loss(logp,p0,old,advantages[i],cfg.get('clip',.2),cfg['rollout_correction']['upper'])
                rho_weights.append(rho.cpu())
                loss = loss_tokens.sum()*loss_scale/budget
                total_loss += float(loss.detach())
                clip_hits += int(((ratio.detach()<.8)|(ratio.detach()>1.2)).sum())
                with profiler.phase("backward"):
                    loss.backward()
                # Release final-call autograd references before validation and collectives.
                del logp, old, p0, rho, drift, loss_tokens, ratio, loss
        # All fresh-policy ratios must be close to one before any optimizer update.
        deltas = torch.cat(replay_deltas)
        max_drift=max(max_drift,q_fixture['max'],p0_fixture['max'])
        mean_drift=max(float(deltas.mean()),q_fixture['mean'],p0_fixture['mean'])
        p95_drift=max(float(deltas.quantile(.95)),q_fixture['p95'],p0_fixture['p95'])
        with profiler.phase('collective_parity_guard', cuda=True):
            from replay_guard import synchronized_guard
            parity_passed, local_parity_bad = synchronized_guard(max_drift, mean_drift, p95_drift,
                    device, world, max_allowed=float(cfg.get('max_replay_drift', .01)))
            if not parity_passed:
                parity_skips += 1
                parity_skip_streak += 1
                rejected = output/'rejected-batches'
                rejected.mkdir(parents=True, exist_ok=True)
                atomic_json(rejected/(f'step-{step:04}-rank-{rank}.json'),dict(step=step,rank=rank,
                            technical_unknown=True,optimizer_update_forbidden=True,local_parity_bad=local_parity_bad,
                            max_replay_drift=max_drift,mean_replay_drift=mean_drift,p95_replay_drift=p95_drift,
                            thresholds=dict(max=.01,mean=.002,p95=.005),
                            trace_reference=str(output/f'traces-rank-{rank}.jsonl')))
            else:
                parity_skip_streak = 0
            # All ranks see the same rejection before any Adam state is advanced.
            if parity_skip_streak >= 3 or ((step-start_step) >= 20 and parity_skips/(step-start_step) > .10):
                raise ValueError('Collective stop: persistent replay parity failures')
        memory_stages.append(memory_snapshot('after_backward'))
        with profiler.phase('clip_active_collective_optimizer', cuda=True):
            grad = torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg.get('max_grad_norm',1.)))
            if not math.isfinite(float(grad)):
                raise FloatingPointError('Nonfinite full-model gradient')
            active_tensor = torch.tensor(active, device=device)
            if world > 1:
                dist.all_reduce(active_tensor)
            updated = bool(active_tensor.item()>0) and parity_passed
            if updated:
                optimizer.step()
                optimizer_update_id+=1
                decoder.refresh_actor(optimizer_update_id)
        memory_stages.append(memory_snapshot('after_optimizer'))
        update_l2 = float((probe[:1024]-before).double().norm())
        if updated and update_l2 <= 0:
            raise ValueError('Optimizer did not update sampled backbone weights')
        metric = dict(step=step, rank=rank, trainable=params, optimizer_step=updated, optimizer_update_id=optimizer_update_id,
                      loss=total_loss, grad_norm=float(grad), backbone_update_l2=update_l2,
                      correct=sum(t['grade']['correct'] for t in trajectories),
                      format_valid=sum(t['format_valid'] for t in trajectories),
                      parallel_valid=sum(t['parallel_protocol_valid'] for t in trajectories),
                      group=group, reward_group=reward_group, phase_iteration=step-start_step,
                      global_responses_per_step=prompts*reward_group, ddp_loss_scale=loss_scale, rewards=[t['reward'] for t in trajectories], advantages=advantages,
                      estimator='token_TIS_upper2_PPO_center_p0_single_fresh_update',sampler_precision='vLLM_whole_model_BF16',learner_precision='full_bf16_autocast_fp32_master_gradient_reduce_adam',q_cached_fixture=q_fixture,native_same_master_q_fixture=native_q_fixture,fp32_layout_oracle_cached_full_fixture=p0_fixture,p0_identity_single_update_max=0.,
                      q_to_p0_max_abs_logratio=float(torch.cat(rho_deltas).abs().max()),q_to_p0_mean_abs_logratio=float(torch.cat(rho_deltas).abs().mean()),tis_cap_fraction=float((torch.cat(rho_deltas).exp()>2).float().mean()),tis_mean_weight=float(torch.cat(rho_weights).mean()),
                      replay_guard_passed=parity_passed, local_replay_guard_bad=local_parity_bad,
                      technical_skip_reason=None if parity_passed else 'replay_probability_parity',
                      cumulative_replay_parity_skips=parity_skips,
                      zero_advantage_group=active==0, actual_widths=[x for t in trajectories for x in t['widths']],
                      rounds=[t['stats']['forks'] for t in trajectories],
                      logical_depth=[t['stats']['critical_depth'] for t in trajectories],
                      sampled_tokens=[t['stats']['sampled_tokens'] for t in trajectories],
                      actual_forward_calls=[t['stats']['actual_model_forward_calls'] for t in trajectories],
                      ratio_clipped_fraction=clip_hits/max(action_count,1), max_replay_logp_drift=max_drift,
                      mean_replay_logp_drift=mean_drift, p95_replay_logp_drift=p95_drift,
                      seconds=time.time()-began, peak_gpu_bytes=torch.cuda.max_memory_allocated(device))
        metric['operation_dtype_receipts']=dict(operation_dtypes)
        metric['master_parameter_dtypes']=sorted(set(str(p.dtype) for p in model.parameters()))
        metric['gradient_storage_dtypes']=sorted(set(str(p.grad.dtype) for p in model.parameters() if p.grad is not None))
        metric['local_adam_state_dtypes']=sorted(set(str(v.dtype) for state in (optimizer.optim if sharded_optimizer else optimizer).state.values() for v in state.values() if torch.is_tensor(v)))
        metric['actor_rollout']=dict((k,v) for k,v in decoder.last_rollout.items() if k not in ['traces','backend_batches'])
        metric['actor_refresh']=dict(decoder.last_refresh)
        metric['memory_stages']=memory_stages
        metric['optimizer_state_sharded']=sharded_optimizer
        metric['resume_proof']=resume_proof
        with profiler.phase('serialization', cuda=False):
            metric_file.write(json.dumps(metric)+'\n')
        # Preserve DDP bucket views while clearing gradients before next inference.
        optimizer.zero_grad(set_to_none=False)
        del before, grad, active_tensor, deltas, replay_deltas, rho_deltas, rho_weights, all_calls, trajectories
        with profiler.phase('cleanup', cuda=False):
            gc.collect()
            torch.cuda.empty_cache()
        memory_stages.append(memory_snapshot('after_cleanup'))
        with profiler.phase('metric_gather_write', cuda=True):
            global_metrics = [None]*world
            if world > 1:
                dist.all_gather_object(global_metrics, metric,group=metadata_group)
            else:
                global_metrics[0] = metric
            if rank == 0:
                with (output/'metrics.jsonl').open('a') as f:
                    f.write(json.dumps(dict(step=step, ranks=global_metrics))+'\n')
                atomic_json(output/'status.json', dict(state='training', step=step, steps=steps,
                            finite=True, optimizer_step=updated, backbone_update_l2=update_l2,
                            replay_guard_passed=parity_passed, replay_parity_skips=parity_skips,
                            max_replay_logp_drift=max(x['max_replay_logp_drift'] for x in global_metrics)))
        profiler.finish(updated, metric)
        from weights_export import due,export_weights_only
        if not cfg.get('skip_exports',False) and due(step):
            if not cfg.get('skip_validation',False):validate(step)
            if rank==0:
                atomic_json(output/'status.json',dict(state='saving',step=step,optimizer_update_id=optimizer_update_id))
                export_weights_only(model,tok,output,step,optimizer_update_id,world)
            if world>1:dist.barrier()
    if cfg.get("validation_after_final",False) and (cfg.get("skip_exports",False) or steps%50):validate(steps)
    if rank==0:
        atomic_json(output/'result.json', dict(completed=True,steps=steps,world_size=world,trainable=params,
                    final=str(output/f'checkpoint-{steps:04}'/'hf') if (output/f'checkpoint-{steps:04}'/'hf').exists() else None, initial_step=start_step,optimizer_update_id=optimizer_update_id,
                    positive_updates=sum(json.loads(line)['optimizer_step'] for line in (output/'metrics-rank-0.jsonl').read_text().splitlines()),
                    optimizer_reset=bool(start_step)))
        atomic_json(output/'status.json',dict(state='completed',step=steps,steps=steps))
    # Free model/Adam/bucket storage before NCCL allocates shutdown workspaces.
    metric_file.close()
    traces.close()
    proximal_records.close()
    decoder.close()
    del decoder, optimizer, ddp, probe, model, original_forward, counted_forward
    gc.collect()
    torch.cuda.empty_cache()
    if world>1:
        dist.destroy_process_group()


if __name__ == '__main__':
    main()
