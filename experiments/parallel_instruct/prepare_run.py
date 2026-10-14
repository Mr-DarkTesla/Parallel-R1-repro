"""Prepare a fresh run directory; no allocation, process launch, or stop."""
import argparse
import hashlib
import json
from pathlib import Path
from batching import assignments

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'verl').is_dir() and (p/'README.md').is_file())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--run-root', required=True)
    args = parser.parse_args()
    cfg = json.loads(Path(args.config).read_text())
    output = Path(args.run_root).resolve()
    if not output.is_relative_to(ROOT):
        raise ValueError('Run directory must be inside the repository')
    world = cfg['expected_world_size']
    batch = cfg['global_batch']
    assignments(0, world, batch['prompts_per_step'], batch['rollouts_per_prompt'])
    if batch['responses_per_step'] != batch['prompts_per_step']*batch['rollouts_per_prompt']:
        raise ValueError('Response batch mismatch')
    if world % cfg.get('processes_per_node', 8):
        raise ValueError('World size must be divisible by processes_per_node')
    initial = int(cfg.get('initial_step', 0))
    if not 0 <= initial < cfg['steps']:
        raise ValueError('initial_step must be below target steps')
    if initial and 'prompt_exposure_offset' not in cfg:
        raise ValueError('Weights-only continuation must specify the previous prompt cursor')
    for name in ['model','train','val','scorer','system']:
        path = Path(cfg[name]).resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        cfg[name] = str(path)
    cfg.update(output=str(output/'production'),resume=None,max_batched_paths=8,
               batch_decoder=str(HERE/'microbatch_decoder.py'),replay=str(HERE/'structured_replay.py'),
               reward=str(HERE/'reward.py'),format_validator=cfg['scorer'],
               gpu_audit=str(output/'distributed-smoke-proof.json'),std_normalization=False,
               bonus_schedule='constant_no_annealing')
    cfg.setdefault('response_budget',4096)
    cfg.setdefault('path_budget',768)
    cfg.setdefault('max_context',16384)
    cfg.setdefault('max_replay_drift',.01)
    cfg.setdefault('reward_mode','strong_width')
    cfg.setdefault('lr',1e-6)
    cfg.setdefault('zero1_optimizer',True)
    cfg.setdefault('checkpoint_steps',list(range(50,cfg['steps']+1,50)))
    if cfg['reward_mode'] not in ('strong_width','forward_only'):
        raise ValueError('Unknown reward mode')
    if not all(0<s<=cfg['steps'] for s in cfg['checkpoint_steps']):
        raise ValueError('Checkpoint outside configured training budget')
    sealed = {str(p.relative_to(ROOT)):str(p) for p in HERE.rglob('*.py')}
    for name in ['train','val','scorer','system']:
        sealed[name] = cfg[name]
    cfg['sealed_inputs'] = sealed
    smoke = dict(cfg,steps=initial+2,output=str(output/'smoke'),
                 skip_validation=True,skip_exports=True,resident_fixture_step=initial+2)
    output.mkdir(parents=True,exist_ok=False)
    paths=[]
    for stage,config in [('production',cfg),('smoke',smoke)]:
        path=output/(stage+'-config-v2.json')
        path.write_text(json.dumps(config,indent=2)+'\n');paths.append(str(path))
    digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    manifest=dict(passed=True,world_size=world,global_batch=batch,
                  sha256={p:digest(p) for p in [*sealed.values(),*paths]},actual_gpu_smoke_pending=True)
    (output/'runtime-build-v2.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(run_root=str(output),gpu_count=world,global_batch=batch,launch=False)))

if __name__=='__main__':
    main()
