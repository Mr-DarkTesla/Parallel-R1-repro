#!/usr/bin/env python3
"""One launcher for Qwen3-0.6B SFT, evaluation and S1/S2 RL.

Use the active Python environment. Pass Hydra overrides after --.
--dry-run prints commands and paths without creating files or importing ML libraries.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

REPO = Path(__file__).resolve().parents[1]
VERL = REPO / 'verl'
HELPERS = REPO / 'experiments/qwen06'


def absolute(value):
    return Path(value).expanduser().resolve()


def quoted(value):
    # Quote the value for Hydra's override parser, not a shell.
    return json.dumps(str(value))


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for command in ('sft', 'eval', 'rl'):
        s = sub.add_parser(command)
        if command == 'sft':
            s.add_argument('variant', choices=('seen', 'unseen'), nargs='?', default='seen')
            s.add_argument('--final-dir', type=absolute)
        elif command == 'rl':
            s.add_argument('variant', choices=('s1', 's2'))
            s.add_argument('--data-dir', type=absolute)
            s.add_argument('--resume', action='store_true')
            s.add_argument('--smoke', action='store_true', help='One update with disposable data/reward')
        s.add_argument('--model', type=absolute, required=command != 'sft')
        s.add_argument('--name')
        s.add_argument('--gpus', type=int, default=int(os.getenv('NPROC_PER_NODE', '1')))
        s.add_argument('--run-dir', type=absolute)
        s.add_argument('--trace', action='store_true', help='Write rollout telemetry (eval/RL)')
        s.add_argument('--dry-run', action='store_true')
    return p


def build_plan(args, overrides):
    if args.gpus < 1:
        raise ValueError('--gpus must be positive')
    stage = args.command
    output = absolute(os.getenv('PARALLEL_R1_OUTPUT_ROOT', VERL / 'checkpoints'))
    scratch = absolute(os.getenv('PARALLEL_R1_SCRATCH_ROOT', output))
    model = args.model or absolute(os.getenv('PARALLEL_R1_MODEL_PATH', scratch / 'Qwen3-0.6B-Base-special-v2'))
    name = args.name or (f'Parallel-SFT-{args.variant.title()}-Qwen3-0.6B' if stage == 'sft'
                         else f'qwen06-{args.variant}-seed1' if stage == 'rl'
                         else f'{model.parent.name}-{model.name}')
    if Path(name).name != name or name in ('.', '..'):
        raise ValueError('--name must be a single directory name')
    run = args.run_dir or output / stage / name
    env = dict(PYTHONPATH=str(VERL) + (os.pathsep + os.environ['PYTHONPATH'] if os.getenv('PYTHONPATH') else ''),
               PARALLEL_R1_MODEL_PATH=str(model), PARALLEL_R1_EVAL_MODEL=str(model),
               PARALLEL_R1_EVAL_NAME=name, PARALLEL_R1_SCRATCH_ROOT=str(scratch),
               PARALLEL_R1_OUTPUT_ROOT=str(output), HF_HOME=os.getenv('HF_HOME', str(scratch / 'huggingface')),
               VLLM_USE_V1='1', PYTHONUNBUFFERED='1')
    prepare = []
    shared = [f'trainer.experiment_name={quoted(name)}', f'trainer.n_gpus_per_node={args.gpus}',
              f'trainer.default_local_dir={quoted(run / "checkpoints")}', f'hydra.run.dir={quoted(run / "hydra")}']
    if stage == 'sft':
        if not (model / 'config.json').exists():
            if args.model:
                raise ValueError(f'No config.json in supplied model: {model}')
            prepare.append([sys.executable, str(VERL / 'training_scripts/prepare_qwen3_parallel.py'), str(model)])
        config = 'sft_qwen3_06b_seen' if args.variant == 'seen' else 'sft_qwen3_06b'
        cmd = [sys.executable, '-m', 'torch.distributed.run', '--standalone', '--nnodes=1',
               f'--nproc_per_node={args.gpus}', '-m', 'verl.trainer.fsdp_parallel_sft_trainer']
        shared += [f'trainer.final_dir={quoted(args.final_dir or run / "final")}']
    else:
        config = 'eval_qwen3_06b' if stage == 'eval' else 'rl_qwen3_06b'
        cmd = [sys.executable, '-m', 'verl.trainer.main_ppo']
        shared += [f'trainer.validation_data_dir={quoted(run / "validation")}']
        if args.trace or stage == 'rl':
            env['PARALLEL_R1_TRACE_DIR'] = str(run / 'telemetry')
            shared += ['actor_rollout_ref.rollout.enforce_eager=true']
    if stage == 'rl':
        data = args.data_dir or absolute(os.getenv('PARALLEL_R1_DATA_DIR', scratch / 'rl-data'))
        env.update(PARALLEL_R1_DATA_DIR=str(data), PARALLEL_R1_RL_STAGE=args.variant,
                   WANDB_MODE=os.getenv('WANDB_MODE', 'offline'), WANDB_DIR=str(run),
                   OMP_NUM_THREADS=os.getenv('OMP_NUM_THREADS', '4'))
        needed = [data / f'{args.variant}_{split}.parquet' for split in ('train', 'val')]
        if args.smoke:
            needed += [data / f'{args.variant}_smoke_{split}.parquet' for split in ('train', 'val')]
        if not all(p.exists() for p in needed):
            prepare.append([sys.executable, str(HELPERS / 'prepare.py'), '--output-dir', str(data)])
        shared += [f'trainer.rollout_data_dir={quoted(run / "rollouts")}',
                   f'trainer.resume_mode={"auto" if args.resume else "disable"}']
        if args.resume:
            shared += ['trainer.val_before_train=true']
        if args.smoke:
            shared += [f'data.{split}_files={quoted(data / (args.variant + "_smoke_" + split + ".parquet"))}' for split in ('train', 'val')]
            shared += ['data.train_batch_size=2', 'actor_rollout_ref.actor.ppo_mini_batch_size=2',
                       'actor_rollout_ref.rollout.n=2', 'trainer.total_training_steps=1',
                       'data.max_response_length=128', 'data.max_prompt_length=1024',
                       'actor_rollout_ref.rollout.agent.num_workers=1',
                       f'custom_reward_function.path={quoted(HELPERS / "smoke_reward.py")}']
    # These paths also drive preflight and provenance; do not let them silently diverge.
    protected = {'model.partial_pretrain', 'actor_rollout_ref.model.path', 'trainer.default_local_dir',
                 'trainer.experiment_name', 'trainer.n_gpus_per_node', 'trainer.validation_data_dir',
                 'trainer.rollout_data_dir', 'trainer.resume_mode', 'trainer.final_dir'}
    for item in overrides:
        if '=' not in item or item.lstrip('+~').split('=', 1)[0] in protected:
            raise ValueError(f'Use launcher options for model/name/GPU/output/resume settings: {item}')
    cmd += [f'--config-name={config}', *shared, *overrides]
    return dict(command=cmd, prepare=prepare, cwd=str(VERL), env=env, run_dir=str(run), model=str(model))


def execute(args, plan):
    run = Path(plan['run_dir'])
    model = Path(plan['model'])
    resume = getattr(args, 'resume', False)
    if run.exists() and any(run.iterdir()) and not resume:
        raise ValueError(f'Run directory is not empty: {run}; choose a new --name/--run-dir or RL --resume')
    identity = run / 'launch.json'
    if resume and identity.exists():
        original = json.loads(identity.read_text())
        if original['model'] != str(model):
            raise ValueError('Resume must use the original SFT model path')
        if original['env'].get('PARALLEL_R1_RL_STAGE') != args.variant:
            raise ValueError('Resume cannot switch between S1 and S2')
    if args.command != 'sft' and not (model / 'config.json').is_file():
        raise ValueError(f'Expected a local HF checkpoint: {model}')
    if args.command == 'rl' and (model / 'SMOKE_ONLY').exists() and not args.smoke:
        raise ValueError('Disposable SMOKE_ONLY model requires --smoke')
    env = {**os.environ, **plan['env']}
    for command in plan['prepare']:
        subprocess.run(command, cwd=VERL, env=env, check=True)
    validation = None
    if args.command != 'sft':
        validation = subprocess.check_output([sys.executable, str(HELPERS / 'check_checkpoint.py'), str(model), '--read-only'], cwd=VERL, env=env, text=True)
    run.mkdir(parents=True, exist_ok=True)
    launch = run / 'launches' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    launch.mkdir(parents=True)
    (launch / 'launch.json').write_text(json.dumps(plan, indent=2) + '\n')
    if not identity.exists():
        identity.write_text(json.dumps(plan, indent=2) + '\n')
    if validation:
        (launch / 'checkpoint.json').write_text(validation)
        if not (run / 'checkpoint.json').exists():
            (run / 'checkpoint.json').write_text(validation)
    for command, filename in [(['git', 'rev-parse', 'HEAD'], 'source_commit.txt'),
                              (['git', 'diff', 'HEAD'], 'source.patch')]:
        (launch / filename).write_bytes(subprocess.check_output(command, cwd=REPO))
    with (run / 'run.log').open('a') as log:
        process = subprocess.Popen(plan['command'], cwd=VERL, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            for line in process.stdout:
                print(line, end='', flush=True)
                log.write(line)
                log.flush()
            code = process.wait()
        except KeyboardInterrupt:
            process.wait()
            raise
        finally:
            process.stdout.close()
    (launch / 'exit_code').write_text(str(code) + '\n')
    return code


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    split = argv.index('--') if '--' in argv else len(argv)
    args = parser().parse_args(argv[:split])
    try:
        plan = build_plan(args, argv[split + 1:])
        if args.dry_run:
            print(json.dumps(plan, indent=2))
            return 0
        return execute(args, plan)
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
