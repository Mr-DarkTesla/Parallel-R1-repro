"""Opt-in GPU check: PARALLEL_R1_TEST_MODEL=/path/to/qwen3 python this_file.py."""
import os
import unittest


@unittest.skipUnless(os.getenv('PARALLEL_R1_TEST_MODEL'), 'set PARALLEL_R1_TEST_MODEL for the GPU check')
class DecodeGraphTest(unittest.TestCase):
    def test_variable_batch_and_sleep(self):
        os.environ.update(VLLM_USE_V1='1', VLLM_ATTENTION_BACKEND='FLASH_ATTN',
                          VLLM_ENABLE_V1_MULTIPROCESSING='0')
        from vllm import LLM, SamplingParams
        from verl.workers.rollout.vllm_rollout.decode_graph import enable_decode_graph

        model = LLM(model=os.environ['PARALLEL_R1_TEST_MODEL'], max_model_len=4096,
                    max_num_seqs=32, max_num_batched_tokens=4096,
                    gpu_memory_utilization=.45, enable_sleep_mode=True,
                    enable_prefix_caching=False, enforce_eager=False,
                    compilation_config={'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32]})
        prompts = ['Calculate the sum from 1 to ' + str(i + 100) + '.' for i in range(32)]
        parameters = [SamplingParams(temperature=0, max_tokens=4 + 4*i, ignore_eos=True) for i in range(32)]

        def generate():
            return [output.outputs[0].token_ids for output in model.generate(prompts, parameters, use_tqdm=False)]

        expected = generate()

        def install(worker):
            enable_decode_graph(worker.model_runner, check_replays=True)
            return True

        model.collective_rpc(install)
        self.assertEqual(generate(), expected)
        self.assertEqual(generate(), expected)
        model.sleep(level=1)
        model.wake_up()
        self.assertEqual(generate(), expected)
        stats = model.collective_rpc(lambda worker: worker.model_runner._decode_graph_stats)
        self.assertGreater(stats[0]['captures'], 1)
        self.assertGreater(stats[0]['replays'], stats[0]['captures'])
        model.collective_rpc(lambda worker: delattr(worker.model_runner.model, 'forward'))
        del model
        import gc
        gc.collect()


if __name__ == '__main__':
    unittest.main()
