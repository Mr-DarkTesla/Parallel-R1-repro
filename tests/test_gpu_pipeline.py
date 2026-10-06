"""CPU-only pipeline checks with stub SFT/eval commands. No models or GPU work."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name)
        self.repo = self.work / 'parallel-r1'
        (self.repo / 'scripts').mkdir(parents=True)
        (self.repo / 'verl').mkdir()
        (self.repo / 'verl/.keep').touch()
        self.env = dict(os.environ, PR1_WORK_ROOT=str(self.work))
        self.run = self.work / 'runs/test-run'

    def tearDown(self):
        self.tmp.cleanup()

    def script(self, name, text):
        (self.repo / 'scripts' / name).write_text(text)

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True).strip()

    def test_old_branch_uses_safe_wrapper_and_pinned_commit(self):
        self.script('run_experiment.sh', 'exit 99\n')
        self.script('sft_qwen3_0.6b.sh', 'echo old-version; mkdir -p "$2/global_step_1"; exit 7\n')
        self.git('init', '-q')
        self.git('config', 'user.name', 'Queue Test')
        self.git('config', 'user.email', 'queue-test@example.invalid')
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')
        initial = self.git('rev-parse', 'HEAD')
        (self.run / 'ckpt').mkdir(parents=True)
        (self.run / 'ckpt/preserved').write_text('old checkpoint')
        (self.run / 'train.log').write_text('old log')
        def launch():
            return subprocess.run(['bash', str(ROOT / 'scripts/start_experiment.sh'), 'HEAD', 'test-run'],
                                  env=self.env, capture_output=True, text=True)
        self.assertEqual(launch().returncode, 7)
        archives = list((self.run / 'interrupted').iterdir())
        self.assertEqual(len(archives), 1)
        self.assertEqual((archives[0] / 'ckpt/preserved').read_text(), 'old checkpoint')
        self.assertEqual((archives[0] / 'train.log').read_text(), 'old log')
        self.assertFalse((self.run / 'results/sft_metrics.txt').exists())
        self.script('sft_qwen3_0.6b.sh', 'echo new-version; exit 8\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'advance branch')
        self.assertEqual(launch().returncode, 7)
        self.assertEqual((self.run / 'source_commit').read_text().strip(), initial)
        self.assertIn('old-version', (self.run / 'train.log').read_text())

    def test_partial_summary_does_not_mark_evaluation_complete(self):
        self.script('sft_qwen3_0.6b.sh', 'mkdir -p "$2/global_step_1"; echo "step:1 - train/loss:1.0"\n')
        self.script('eval_qwen3_0.6b.sh', 'mkdir -p "$2/generations"; touch "$2/generations/0.jsonl"\n')
        self.script('summarize_eval.py', 'print("partial summary"); raise SystemExit(7)\n')
        env = dict(self.env, EXPERIMENT_REPO=str(self.repo))
        result = subprocess.run(['bash', str(ROOT / 'scripts/run_experiment.sh'), 'test-run'],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 7)
        self.assertTrue((self.run / 'results/sft_metrics.txt').exists())
        self.assertFalse((self.run / 'results/eval_apo.txt').exists())
        self.assertIn('partial summary', (self.run / 'eval_apo.tmp').read_text())


if __name__ == '__main__':
    unittest.main()
