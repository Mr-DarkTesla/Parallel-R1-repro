"""Scheduling may reorder compute, but must preserve output order and token-mean PPO updates."""
import ast
from contextlib import contextmanager, nullcontext
from pathlib import Path
from types import SimpleNamespace
import unittest
import torch
from test_rl_microbatch_loss import ns as loss_ns


class Config(dict):
    __getattr__ = dict.__getitem__


class RecordingFSDP(torch.nn.Linear):
    deferred = False
    cpu_offload = SimpleNamespace(offload_params=False)

    @contextmanager
    def no_sync(self):
        self.deferred = True
        try:
            yield
        finally:
            self.deferred = False


class Data:
    def __init__(self, batch, metadata=None):
        self.batch = batch
        self.non_tensor_batch = {}
        self.meta_info = metadata or {}

    def select(self, batch_keys, non_tensor_keys=None, non_tensor_select_keys=None, **kwargs):
        return Data({k: self.batch[k] for k in batch_keys}, self.meta_info)

    def split(self, size):
        count = next(iter(self.batch.values())).shape[0]
        return [Data({k: v[i:i+size] for k, v in self.batch.items()}, self.meta_info)
                for i in range(0, count, size)]

    def reorder(self, order):
        self.batch = {k: v[order] for k, v in self.batch.items()}


def append(metrics, values):
    for key, value in values.items():
        metrics.setdefault(key, []).append(value)


source = Path(__file__).resolve().parents[1] / 'verl/verl/workers/actor/dp_actor.py'
cls = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.ClassDef) and n.name == 'DataParallelPPOActor')
nodes = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in ('compute_log_prob', 'update_policy')]
for node in nodes:
    node.decorator_list = []
ns = dict(torch=torch, FSDP=RecordingFSDP, nullcontext=nullcontext, DataProto=Data, append_to_dict=append, **{k: loss_ns[k] for k in ('agg_loss', 'compute_policy_loss')})
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), ns)


class OrderTest(unittest.TestCase):
    def data(self):
        torch.manual_seed(19)
        lengths = torch.tensor([8, 1, 2, 6, 0, 5, 4, 8, 1, 3, 7, 2])
        mask = torch.arange(8)[None] < lengths[:, None]
        inputs = torch.randn(12, 8)
        return Data(dict(input_ids=inputs, responses=inputs.clone(), attention_mask=mask,
                         position_ids=torch.zeros_like(inputs), response_mask=mask,
                         old_log_probs=inputs * .1, advantages=torch.randn(12, 8)),
                    dict(micro_batch_size=4, temperature=1., use_dynamic_bsz=False))

    def actor(self, ordered, deferred=False):
        model = RecordingFSDP(1, 1)
        with torch.no_grad():
            model.weight.fill_(.1); model.bias.zero_()
        config = Config(ppo_mini_batch_size=6, ppo_micro_batch_size_per_gpu=2,
                        ppo_epochs=1, use_dynamic_bsz=False, use_kl_loss=False,
                        clip_ratio=.2, clip_ratio_low=.2, clip_ratio_high=.2, clip_ratio_c=3.,
                        entropy_coeff=0., loss_agg_mode='token-mean', policy_loss=Config(loss_mode='vanilla'),
                        sort_microbatch_groups_by_length=ordered, sort_logprob_rows_by_length=ordered,
                        defer_gradient_sync=deferred)
        actor = SimpleNamespace(actor_module=model, config=config, ulysses_sequence_parallel_size=1)
        actor.actor_optimizer = torch.optim.SGD(model.parameters(), lr=.03)
        actor.groups = []; actor.gradients = []; actor.deferred = []
        def forward(inputs, temperature, calculate_entropy=False):
            actor.deferred.append(model.deferred)
            actor.groups.append(inputs['input_ids'].clone())
            scores = model(inputs['input_ids'][..., None]).squeeze(-1)
            return scores.square() if calculate_entropy else None, scores
        def step():
            grad = torch.cat([p.grad.flatten() for p in model.parameters()])
            actor.gradients.append(grad.clone()); actor.actor_optimizer.step(); return grad.norm()
        actor._forward_micro_batch = forward; actor._optimizer_step = step
        return actor

    def test_last_microbatch_synchronizes_each_optimizer_update(self):
        reference, actual = self.actor(True), self.actor(True, deferred=True)
        for actor in (reference, actual):
            ns['update_policy'](actor, self.data())
        self.assertEqual(actual.deferred, [True, True, False] * 2)
        self.assertFalse(actual.actor_module.deferred)
        for expected, observed in zip(reference.gradients, actual.gradients):
            torch.testing.assert_close(observed, expected)

    def test_logprob_restores_original_rows(self):
        data = self.data(); original = data.batch['input_ids'].clone()
        reference = ns['compute_log_prob'](self.actor(False), data, calculate_entropy=True)
        actor = self.actor(True)
        actual = ns['compute_log_prob'](actor, data, calculate_entropy=True)
        for expected, observed in zip(reference, actual):
            torch.testing.assert_close(observed, expected)
        torch.testing.assert_close(data.batch['input_ids'], original)
        self.assertFalse(torch.equal(torch.cat(actor.groups), original))

    def test_token_mean_minibatch_updates_are_preserved(self):
        actors = [self.actor(False), self.actor(True)]
        for actor in actors:
            ns['update_policy'](actor, self.data())
        self.assertEqual(len(actors[0].gradients), 2)
        for expected, actual in zip(actors[0].gradients, actors[1].gradients):
            torch.testing.assert_close(actual, expected, atol=1e-7, rtol=1e-6)
        for expected, actual in zip(actors[0].actor_module.parameters(), actors[1].actor_module.parameters()):
            torch.testing.assert_close(actual, expected, atol=1e-7, rtol=1e-6)
        # Original pairs remain intact, within each original optimizer minibatch.
        for start in (0, 3):
            old = actors[0].groups[start:start+3]; new = actors[1].groups[start:start+3]
            self.assertTrue(all(any(torch.equal(a, b) for b in new) for a in old))


if __name__ == '__main__':
    unittest.main()
