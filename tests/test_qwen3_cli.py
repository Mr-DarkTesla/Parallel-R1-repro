"""Launcher contracts; these tests never start a GPU process."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('qwen3_cli', ROOT / 'scripts/qwen3.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class LauncherTests(unittest.TestCase):
    def plan(self, *argv, overrides=()):
        return cli.build_plan(cli.parser().parse_args(argv), list(overrides))

    def test_dry_run_does_not_create_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / 'run with spaces'
            p = subprocess.run([sys.executable, str(ROOT / 'scripts/qwen3.py'), 'rl', 's2',
                                '--model', str(Path(tmp) / 'hf model'), '--run-dir', str(run),
                                '--dry-run', '--', 'trainer.total_training_steps=2'], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            plan = json.loads(p.stdout)
            self.assertEqual(plan['run_dir'], str(run.resolve()))
            self.assertIn('trainer.total_training_steps=2', plan['command'])
            self.assertFalse(run.exists())

    def test_options_preserve_path_and_gpu_contract(self):
        for mode in ('s1', 's2'):
            p = self.plan('rl', mode, '--model', '/tmp/model with spaces', '--name', 'test', '--gpus', '2')
            self.assertEqual(p['env']['PARALLEL_R1_RL_STAGE'], mode)
            self.assertIn('trainer.n_gpus_per_node=2', p['command'])
            self.assertEqual(p['env']['PARALLEL_R1_MODEL_PATH'], '/private/tmp/model with spaces' if sys.platform == 'darwin' else '/tmp/model with spaces')
        p = self.plan('sft', 'unseen', '--gpus', '4')
        self.assertIn('--nproc_per_node=4', p['command'])
        self.assertIn('--config-name=sft_qwen3_06b', p['command'])

    def test_rejects_model_and_output_override_bypasses(self):
        for override in ('actor_rollout_ref.model.path=/other', '+trainer.default_local_dir=/other', 'trainer.resume_mode=auto'):
            with self.assertRaises(ValueError):
                self.plan('rl', 's1', '--model', '/tmp/hf', overrides=[override])
        with self.assertRaises(ValueError):
            self.plan('sft', '--gpus', '0')

    def test_existing_run_and_smoke_model_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / 'model'; model.mkdir(); (model / 'config.json').write_text('{}')
            run = root / 'run'; run.mkdir(); (run / 'run.log').write_text('old')
            args = cli.parser().parse_args(['rl', 's1', '--model', str(model), '--run-dir', str(run)])
            with patch.object(cli.subprocess, 'run') as launch:
                with self.assertRaisesRegex(ValueError, 'not empty'):
                    cli.execute(args, cli.build_plan(args, []))
                launch.assert_not_called()
            (run / 'run.log').unlink(); (model / 'SMOKE_ONLY').touch()
            with self.assertRaisesRegex(ValueError, 'SMOKE_ONLY'):
                cli.execute(args, cli.build_plan(args, []))

    def test_resume_checks_model_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            (run / 'launch.json').write_text(json.dumps({'model': '/another/model'}))
            args = cli.parser().parse_args(['rl', 's1', '--model', '/tmp/hf', '--run-dir', str(run), '--resume'])
            with self.assertRaisesRegex(ValueError, 'original SFT'):
                cli.execute(args, cli.build_plan(args, []))

    def test_execution_records_failure_without_modifying_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            model = root / 'model'; model.mkdir(); (model / 'config.json').write_text('{}')
            run = root / 'run'
            args = cli.parser().parse_args(['eval', '--model', str(model), '--run-dir', str(run)])
            plan = cli.build_plan(args, [])
            plan['command'] = [sys.executable, '-c', 'print("fake trainer"); raise SystemExit(7)']
            def output(command, **kw):
                if 'check_checkpoint.py' in str(command):
                    self.assertIn('--read-only', command)
                    return '{"model_path": "test"}'
                return b'test source\n'
            with patch.object(cli.subprocess, 'check_output', side_effect=output):
                self.assertEqual(cli.execute(args, plan), 7)
            self.assertEqual((run / 'run.log').read_text(), 'fake trainer\n')
            self.assertEqual(next((run / 'launches').glob('*/exit_code')).read_text(), '7\n')
            self.assertEqual([p.name for p in model.iterdir()], ['config.json'])

    def test_legacy_launchers_delegate(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            capture = tmp / 'capture'; result = tmp / 'args.json'
            capture.write_text(f'#!{sys.executable}\nimport json,sys,os\nopen(os.environ["CAPTURE"],"w").write(json.dumps(sys.argv[1:]))\n')
            capture.chmod(0o755)
            env = {**os.environ, 'PARALLEL_R1_PYTHON': str(capture), 'CAPTURE': str(result),
                   'PARALLEL_R1_ROOT': str(tmp), 'RUN_NAME': 'legacy', 'BATCH': '16', 'NPROC_PER_NODE': '2'}
            p = subprocess.run(['bash', str(ROOT / 'experiments/qwen06/run_rl.sh'), 's2', '/tmp/hf',
                                'trainer.resume_mode=auto', 'trainer.total_training_steps=20'], env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            args = json.loads(result.read_text())
            self.assertIn('--resume', args); self.assertIn('data.train_batch_size=16', args)
            self.assertIn('trainer.total_training_steps=20', args)
            self.assertEqual(args[1:3], ['rl', 's2'])
            for script, inputs, command in [('sft_qwen3_06b.sh', ['seen'], 'sft'),
                                            ('eval_qwen3_06b.sh', [str(tmp)], 'eval')]:
                p = subprocess.run(['bash', str(ROOT / 'verl/training_scripts' / script), *inputs], env=env, capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stderr)
                self.assertEqual(json.loads(result.read_text())[1], command)


class ConfigTests(unittest.TestCase):
    def test_composed_profiles_and_override_precedence(self):
        from hydra import compose, initialize_config_dir
        from omegaconf import OmegaConf
        for command in (['sft','seen'], ['sft','unseen'], ['eval','--model','/tmp/hf'],
                        ['rl','s1','--model','/tmp/hf'], ['rl','s2','--model','/tmp/hf'],
                        ['rl','s2','--model','/tmp/hf','--smoke']):
            args = cli.parser().parse_args(command)
            plan = cli.build_plan(args, ['trainer.total_training_steps=2'])
            idx = next(i for i, x in enumerate(plan['command']) if x.startswith('--config-name='))
            with patch.dict(os.environ, plan['env']), initialize_config_dir(config_dir=str(ROOT / 'verl/verl/trainer/config'), version_base=None):
                cfg = compose(config_name=plan['command'][idx].split('=',1)[1], overrides=plan['command'][idx+1:])
                self.assertEqual(cfg.trainer.total_training_steps, 2)
                self.assertEqual(cfg.trainer.n_gpus_per_node, args.gpus)
                self.assertEqual(cfg.trainer.default_local_dir, plan['run_dir'] + '/checkpoints')
                if args.command == 'rl':
                    self.assertEqual(cfg.actor_rollout_ref.actor.optim.lr, 1e-6)
                    self.assertEqual(cfg.actor_rollout_ref.actor.clip_ratio_high, 0.28)
                    self.assertEqual(cfg.actor_rollout_ref.model.override_config._attn_implementation, 'sdpa')
                    self.assertEqual(cfg.trainer.resume_mode, 'disable')
                    self.assertIn(args.variant + ('_smoke' if args.smoke else '') + '_train.parquet', cfg.data.train_files)
                    self.assertEqual(cfg.data.train_batch_size, 2 if args.smoke else 32)
                    self.assertEqual(cfg.actor_rollout_ref.rollout.n, 2 if args.smoke else 8)
                    self.assertEqual(cfg.actor_rollout_ref.rollout.agent.max_path_response_length, cfg.data.max_response_length)
                OmegaConf.to_container(cfg, resolve=True)


if __name__ == '__main__':
    unittest.main()
