"""Optional small-model replication must not silently change mesh semantics."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from torch.distributed.fsdp import ShardingStrategy

path = Path(__file__).resolve().parents[1] / 'verl/verl/workers/fsdp_workers.py'
node = next(n for n in ast.parse(path.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'get_sharding_strategy')
ns = {}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), ns)
choose = ns['get_sharding_strategy']

class StrategyTest(unittest.TestCase):
    def test_defaults_and_explicit_modes(self):
        self.assertEqual(choose(SimpleNamespace(ndim=1)), ShardingStrategy.FULL_SHARD)
        self.assertEqual(choose(SimpleNamespace(ndim=2)), ShardingStrategy.HYBRID_SHARD)
        for name in ('FULL_SHARD', 'SHARD_GRAD_OP', 'NO_SHARD'):
            self.assertEqual(choose(SimpleNamespace(ndim=1), name), ShardingStrategy[name])

    def test_reshard_cleanup_skips_replicated_or_empty_root(self):
        from unittest.mock import Mock
        tree = ast.parse(path.read_text())
        guards = [n for n in ast.walk(tree) if isinstance(n, ast.If)
                  and 'self.world_size > 1' in ast.unparse(n.test)
                  and 'fsdp_version' in ast.unparse(n.test)]
        self.assertEqual(len(guards), 3)
        for guard in guards:
            for sharded in (True, False, None):
                handle = None if sharded is None else SimpleNamespace(uses_sharded_strategy=sharded, reshard=Mock())
                module = SimpleNamespace(_handle=handle)
                worker = SimpleNamespace(world_size=8, actor=SimpleNamespace(actor_module=module),
                                         ref_policy=SimpleNamespace(actor_module=module), reward_module=module)
                exec(compile(ast.Module(body=[guard], type_ignores=[]), str(path), 'exec'),
                     dict(self=worker, fsdp_version=lambda _: 1))
                if handle is not None:
                    self.assertEqual(handle.reshard.call_count, int(sharded))

    def test_rejects_unsupported_mesh_or_name(self):
        for ndim, name in [(2, 'NO_SHARD'), (1, 'FULL_SHRAD')]:
            with self.assertRaises(ValueError):
                choose(SimpleNamespace(ndim=ndim), name)

if __name__ == '__main__':
    unittest.main()
