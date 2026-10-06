"""CPU integration checks for interruption, duplicate runners, failures and concurrent enqueue.
Run on Linux (flock): python3 -m unittest discover -s tests -p test_gpu_queue.py -v
"""
import os
from pathlib import Path
import shlex
import signal
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]


class QueueTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.directory = Path(self.tmp.name)
        activate = self.directory / 'activate'
        activate.touch()
        self.env = dict(os.environ, QUEUE_DIR=self.tmp.name, VENV_ACTIVATE=str(activate))
        self.queue = self.directory / 'gpu0.txt'
        self.processes = []

    def tearDown(self):
        for process in self.processes:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=5)
        self.tmp.cleanup()

    def wait_for(self, condition):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if condition():
                return
            time.sleep(0.02)
        self.fail('queue condition timed out')

    def runner(self):
        process = subprocess.Popen(['bash', str(ROOT / 'scripts/queue_runner.sh'), '0'], env=self.env,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        self.processes.append(process)
        return process

    def enqueue(self, command):
        subprocess.run(['bash', str(ROOT / 'scripts/enqueue.sh'), '0', command], env=self.env, check=True)

    def blocked_command(self):
        started = shlex.quote(str(self.directory / 'started'))
        release = shlex.quote(str(self.directory / 'release'))
        return f'touch {started}; while [ ! -e {release} ]; do sleep 0.02; done'

    def test_interruption_replays_pending_command(self):
        attempts = self.directory / 'attempts'
        command = f'echo attempt >> {shlex.quote(str(attempts))}; ' + self.blocked_command()
        self.enqueue(command)
        process = self.runner()
        self.wait_for(lambda: attempts.exists())
        self.assertEqual(self.queue.read_text(), command + '\n')
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)
        self.runner()
        self.wait_for(lambda: len(attempts.read_text().splitlines()) == 2)
        (self.directory / 'release').touch()
        self.wait_for(lambda: self.queue.read_text() == '')

    def test_duplicate_runner_is_rejected(self):
        command = self.blocked_command()
        self.enqueue(command)
        self.runner()
        self.wait_for(lambda: (self.directory / 'started').exists())
        duplicate = self.runner()
        self.assertEqual(duplicate.wait(timeout=5), 1)
        self.assertEqual(self.queue.read_text(), command + '\n')

    def test_failed_command_is_saved_and_queue_advances(self):
        self.enqueue('exit 7')
        command = self.blocked_command()
        self.enqueue(command)
        self.runner()
        self.wait_for(lambda: (self.directory / 'started').exists())
        self.assertEqual((self.directory / 'gpu0.txt.failed').read_text(), 'exit 7\n')
        self.assertEqual(self.queue.read_text(), command + '\n')
        self.assertIn('END exit=7 exit 7', (self.directory / 'gpu0.log').read_text())

    def test_enqueue_while_busy_is_preserved(self):
        command = self.blocked_command()
        self.enqueue(command)
        self.runner()
        self.wait_for(lambda: (self.directory / 'started').exists())
        completed = self.directory / 'completed'
        self.enqueue(f'touch {shlex.quote(str(completed))}')
        (self.directory / 'release').touch()
        self.wait_for(lambda: completed.exists() and self.queue.read_text() == '')
        self.assertEqual((self.directory / 'gpu0.log').read_text().count('END exit=0'), 2)

    def test_supervisor_exits_when_runner_cannot_start(self):
        self.enqueue(self.blocked_command())
        self.runner()
        self.wait_for(lambda: (self.directory / 'started').exists())
        supervisor = subprocess.Popen(['bash', str(ROOT / 'scripts/run_gpu_queues.sh'), '2'], env=self.env,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        self.processes.append(supervisor)
        self.assertEqual(supervisor.wait(timeout=5), 1)

    def test_blank_line_does_not_block_queue(self):
        self.queue.write_text('\n')
        completed = self.directory / 'completed'
        self.enqueue(f'touch {shlex.quote(str(completed))}')
        self.runner()
        self.wait_for(lambda: completed.exists() and self.queue.read_text() == '')

    def test_repeated_crashes_reach_retry_limit(self):
        command = self.blocked_command()
        self.enqueue(command)
        for attempt in range(1, 4):
            process = self.runner()
            self.wait_for(lambda: (self.directory / 'gpu0.txt.attempts').exists()
                          and (self.directory / 'gpu0.txt.attempts').read_text().startswith(str(attempt) + '\n'))
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
        self.runner()
        self.wait_for(lambda: self.queue.read_text() == '')
        self.assertEqual((self.directory / 'gpu0.txt.failed').read_text(), command + '\n')
        self.assertIn('END exit=125', (self.directory / 'gpu0.log').read_text())


if __name__ == '__main__':
    unittest.main()
