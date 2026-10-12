"""Full-weight exact-context PPO reference, one actor per retained Cloud GPU.

Group centered rewards, no std normalization, fixed response-budget denominator.
There is exactly one optimizer update per fresh rollout batch. The rollout and
replay share HF SDPA operations; no flattened causal trajectory replay exists.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import random
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


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
    good = '<think>' not in text and '</think>' not in text
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
    good = good and len(finals) == 1
    good = good and not any(m.start() <= f.start() < m.end() for m in blocks for f in finals)
    return bool(good), bool(good and blocks)


def identity_gate(config, receipt):
    """A root-reviewed receipt binds the exact runnable inputs and passed audit."""
    gate = json.loads(Path(receipt).read_text())
    if not gate.get('approved'):
        raise ValueError('Root receipt has not approved this run')
    for name, path in config['sealed_inputs'].items():
        if gate.get('sha256', {}).get(name) != sha(path):
            raise ValueError('Root receipt hash mismatch: '+name)
    audit = json.loads(Path(config['gpu_audit']).read_text())
    if not audit.get('passed'):
        raise ValueError('Actual GPU semantic audit did not pass')
    return gate


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
    if not args.smoke:
        if not args.receipt:
            raise ValueError('Production requires a root approval receipt')
        identity_gate(cfg, args.receipt)
    output = Path(cfg['output'])
    if not output.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Output must be inside project root')
    rank = int(os.environ.get('RANK', '0'))
    world = int(os.environ.get('WORLD_SIZE', '1'))
    local_rank = int(os.environ.get('LOCAL_RANK', '0'))
    torch.cuda.set_device(local_rank)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision('highest')
    device = torch.device('cuda', local_rank)
    if world > 1:
        dist.init_process_group('nccl')
    if rank == 0:
        output.mkdir(parents=True, exist_ok=False)
        atomic_json(output/'config.json', cfg)
        atomic_json(output/'status.json', dict(state='loading', started=time.time(), world_size=world))
    if world > 1:
        dist.barrier()
    train = [json.loads(x) for x in Path(cfg['train']).read_text().splitlines() if x.strip()]
    if not train:
        raise ValueError('Training set is empty')
    sys.path.insert(0, str(Path(cfg['replay']).parent))
    replay = load_module('exact_replay', cfg['replay'])
    reward = load_module('campaign_reward', cfg['reward'])
    scorer = load_module('frozen_answer_scorer', cfg['scorer'])
    validator = load_module('frozen_base_validator', cfg['format_validator'])
    tok = AutoTokenizer.from_pretrained(cfg['model'], local_files_only=True)
    instruction = Path(cfg['system']).read_text()
    torch.manual_seed(cfg.get('seed', 20261010))
    random.seed(cfg.get('seed', 20261010))
    model = AutoModelForCausalLM.from_pretrained(cfg['model'], torch_dtype=torch.float32,
            attn_implementation='sdpa', local_files_only=True, low_cpu_mem_usage=True).to(device)
    if any(float(getattr(model.config, name, 0) or 0) != 0 for name in ('attention_dropout', 'hidden_dropout', 'hidden_dropout_prob')):
        raise ValueError('Reference PPO requires zero dropout for exact replay')
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
    model.config.use_cache = True
    ddp = DDP(model, device_ids=[local_rank], broadcast_buffers=False,
              gradient_as_bucket_view=True, bucket_cap_mb=25) if world > 1 else model
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(cfg.get('lr', 1e-6)),
                                 betas=(.9, .999), eps=1e-8, weight_decay=0., foreach=False)
    params = sum(x.numel() for x in model.parameters() if x.requires_grad)
    if params < 4_000_000_000:
        raise ValueError('All-weight 4B arm required')
    decoder = HFDecoder(model, replay, device)
    eos = native_eos_ids(cfg['model'], tok)
    group = int(cfg.get('group', 4))
    steps = int(cfg.get('steps', 64))
    budget = int(cfg.get('response_budget', 4096))
    start_step = 0
    if cfg.get('resume'):
        checkpoint = Path(cfg['resume'])
        model.load_state_dict(torch.load(checkpoint/'model.pt', map_location=device, weights_only=True))
        optimizer.load_state_dict(torch.load(checkpoint/'optimizer.pt', map_location=device, weights_only=True))
        saved = torch.load(checkpoint/f'rng-{rank}.pt', weights_only=False)
        torch.set_rng_state(saved['cpu_rng'])
        torch.cuda.set_rng_state(saved['cuda_rng'], device)
        random.setstate(saved['python_rng'])
        start_step = int(json.loads((checkpoint/'complete.json').read_text())['step'])
    metric_file = (output/f'metrics-rank-{rank}.jsonl').open('w', buffering=1)
    traces = (output/f'traces-rank-{rank}.jsonl').open('w', buffering=1)
    probe = model.model.layers[0].self_attn.q_proj.weight.reshape(-1)

    def validate(step):
        """Selection validation uses an immutable sampler and never enters loss."""
        rows = [json.loads(x) for x in Path(cfg['val']).read_text().splitlines() if x.strip()]
        directory = output/f'validation-{step:04}'
        if rank==0:
            directory.mkdir(exist_ok=False)
        if world>1:
            dist.barrier()
        model.eval()
        records = []
        with (directory/f'rank-{rank}.jsonl').open('w',buffering=1) as f:
            for index in range(rank,len(rows),world):
                row = rows[index]
                prefix = tok.apply_chat_template([dict(role='system',content=instruction),dict(role='user',content=row['problem'])],
                                                 tokenize=True,add_generation_prompt=True)
                trace = execute(tok,prefix,decoder,eos,budget,cfg.get('path_budget',768),cfg.get('max_context',16384),
                                cfg.get('validation_seed',91261010)+index*100)
                grade = scorer.grade(trace['output'],str(row['answer']))
                if grade.get('error'):
                    raise ValueError('Validation scorer technical failure: '+str(grade['error']))
                flags = validator.canonical_format_flags(trace['output'])
                valid = bool(flags['format']) and not trace['stats']['invalid_width'] and not trace['stats']['truncated']
                trace.update(id=row['id'],answer=row['answer'],correct=bool(grade['correct']),format_valid=valid,
                             parallel_valid=valid and bool(trace['widths']),dataset='GSM_Infinite_selection_only',step=step,index=index)
                f.write(json.dumps(trace,ensure_ascii=False)+'\n')
                records.append(dict(id=row['id'],correct=trace['correct'],format_valid=valid,parallel_valid=trace['parallel_valid'],
                                    widths=trace['widths'],stats=trace['stats']))
        groups = [None]*world
        if world>1:
            dist.all_gather_object(groups,records)
        else:
            groups[0] = records
        if rank==0:
            all_rows = [r for group_rows in groups for r in group_rows]
            if len(all_rows)!=len(rows) or len({r['id'] for r in all_rows})!=len(rows):
                raise ValueError('Validation coverage is incomplete or duplicated')
            summary = dict(step=step,completed=len(rows),correct=sum(r['correct'] for r in all_rows),
                           format_valid=sum(r['format_valid'] for r in all_rows),parallel_valid=sum(r['parallel_valid'] for r in all_rows),
                           fork_tasks=sum(bool(r['widths']) for r in all_rows),widths=[w for r in all_rows for w in r['widths']],
                           actual_rounds=sum(len(r['widths']) for r in all_rows),
                           logical_depth=[r['stats']['critical_depth'] for r in all_rows],
                           sampled_tokens=[r['stats']['sampled_tokens'] for r in all_rows],
                           actual_forward_calls=[r['stats']['actual_model_forward_calls'] for r in all_rows],
                           sampler='Exact FP32 HF serial, temperature1 top_p1 nofilter; fixedselectionseed; not frozen128evaluation',
                           selection_allowed=True,benchmark=False)
            atomic_json(directory/'summary.json',summary)
        if world>1:
            dist.barrier()
    validate(start_step)
    for step in range(start_step+1, steps+1):
        began = time.time()
        torch.cuda.reset_peak_memory_stats(device)
        row = train[((step-1)*world+rank) % len(train)]
        messages = [dict(role='system', content=instruction), dict(role='user', content=row['problem'])]
        prefix = tok.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
        trajectories = []
        model.eval()
        for sample in range(group):
            trajectory = execute(tok, prefix, decoder, eos, budget, cfg.get('path_budget',768),
                                 cfg.get('max_context',16384),
                                 cfg.get('seed',20261010)+step*100000+rank*1000+sample*100)
            grade = scorer.grade(trajectory['output'], str(row['answer']))
            if grade.get('error'):
                raise ValueError('Scorer returned an unknown technical outcome: '+str(grade['error']))
            flags = validator.canonical_format_flags(trajectory['output'])
            valid = bool(flags['format']) and not trajectory['stats']['invalid_width'] and not trajectory['stats']['truncated']
            parallel = valid and bool(trajectory['widths'])
            components = reward.score(bool(grade['correct']), valid, trajectory['stats']['critical_depth'],
                                      trajectory['stats']['sampled_tokens'], trajectory['widths'], step-1,
                                      cfg['reward_mode'])
            trajectory.update(id=row['id'], answer=row['answer'], grade=grade, format_valid=valid,
                              parallel_protocol_valid=parallel, reward=components, step=step, rank=rank, sample=sample)
            trajectories.append(trajectory)
            traces.write(json.dumps(trajectory, ensure_ascii=False)+'\n')
        advantages = centered([float(t['reward']['score']) for t in trajectories])
        active = sum(abs(x)>1e-12 for x in advantages)
        model.train()
        optimizer.zero_grad(set_to_none=True)
        before = probe[:1024].detach().clone()
        total_loss = 0.
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
                logp, _ = replay.score_call(ddp, call)
                old = torch.tensor(call['old_logprobs'], device=device)
                if not torch.isfinite(logp).all() or not torch.isfinite(old).all():
                    raise FloatingPointError('Nonfinite rollout/replay likelihood')
                drift = (logp.detach()-old).abs()
                max_drift = max(max_drift, float(drift.max()))
                replay_deltas.append(drift.cpu())
                loss_tokens, ratio = ppo_token_loss(logp, old, advantages[i], cfg.get('clip', .2))
                loss = loss_tokens.sum()/(budget*group)
                total_loss += float(loss.detach())
                clip_hits += int(((ratio.detach()<.8)|(ratio.detach()>1.2)).sum())
                loss.backward()
        # All fresh-policy ratios must be close to one before any optimizer update.
        deltas = torch.cat(replay_deltas)
        mean_drift = float(deltas.mean())
        p95_drift = float(deltas.quantile(.95))
        if max_drift > float(cfg.get('max_replay_drift', .01)) or mean_drift > .002 or p95_drift > .005:
            raise ValueError('Decoder/replay probability divergence: '+str(max_drift))
        grad = torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg.get('max_grad_norm',1.)))
        if not math.isfinite(float(grad)):
            raise FloatingPointError('Nonfinite full-model gradient')
        active_tensor = torch.tensor(active, device=device)
        if world > 1:
            dist.all_reduce(active_tensor)
        updated = bool(active_tensor.item()>0)
        if updated:
            optimizer.step()
        update_l2 = float((probe[:1024]-before).double().norm())
        if updated and update_l2 <= 0:
            raise ValueError('Optimizer did not update sampled backbone weights')
        metric = dict(step=step, rank=rank, trainable=params, optimizer_step=updated,
                      loss=total_loss, grad_norm=float(grad), backbone_update_l2=update_l2,
                      correct=sum(t['grade']['correct'] for t in trajectories),
                      format_valid=sum(t['format_valid'] for t in trajectories),
                      parallel_valid=sum(t['parallel_protocol_valid'] for t in trajectories),
                      group=group, rewards=[t['reward'] for t in trajectories], advantages=advantages,
                      zero_advantage_group=active==0, actual_widths=[x for t in trajectories for x in t['widths']],
                      rounds=[t['stats']['forks'] for t in trajectories],
                      logical_depth=[t['stats']['critical_depth'] for t in trajectories],
                      sampled_tokens=[t['stats']['sampled_tokens'] for t in trajectories],
                      actual_forward_calls=[t['stats']['actual_model_forward_calls'] for t in trajectories],
                      ratio_clipped_fraction=clip_hits/max(action_count,1), max_replay_logp_drift=max_drift,
                      mean_replay_logp_drift=mean_drift, p95_replay_logp_drift=p95_drift,
                      seconds=time.time()-began, peak_gpu_bytes=torch.cuda.max_memory_allocated(device))
        metric_file.write(json.dumps(metric)+'\n')
        global_metrics = [None]*world
        if world > 1:
            dist.all_gather_object(global_metrics, metric)
        else:
            global_metrics[0] = metric
        if rank == 0:
            with (output/'metrics.jsonl').open('a') as f:
                f.write(json.dumps(dict(step=step, ranks=global_metrics))+'\n')
            atomic_json(output/'status.json', dict(state='training', step=step, steps=steps,
                        finite=True, optimizer_step=updated, backbone_update_l2=update_l2,
                        max_replay_logp_drift=max(x['max_replay_logp_drift'] for x in global_metrics)))
        if step % int(cfg.get('checkpoint_every',16)) == 0 or step == steps:
            validate(step)
            checkpoint = output/f'checkpoint-{step:04}'
            if rank==0:
                checkpoint.mkdir(exist_ok=False)
            if world>1:
                dist.barrier()
            torch.save(dict(cpu_rng=torch.get_rng_state(),cuda_rng=torch.cuda.get_rng_state(device),
                            python_rng=random.getstate()), checkpoint/f'rng-{rank}.pt')
            if rank==0:
                torch.save(model.state_dict(), checkpoint/'model.pt')
                torch.save(optimizer.state_dict(), checkpoint/'optimizer.pt')
                model.save_pretrained(checkpoint/'hf', safe_serialization=True, max_shard_size='4GB')
                tok.save_pretrained(checkpoint/'hf')
            if world>1:
                dist.barrier()
            if rank==0:
                atomic_json(checkpoint/'complete.json',dict(step=step,world_size=world,model=True,optimizer=True,rng=True))
    if rank==0:
        atomic_json(output/'result.json', dict(completed=True,steps=steps,world_size=world,trainable=params,
                    final=str(output/f'checkpoint-{steps:04}'/'hf')))
        atomic_json(output/'status.json',dict(state='completed',step=steps,steps=steps))
    if world>1:
        dist.destroy_process_group()


if __name__ == '__main__':
    main()
