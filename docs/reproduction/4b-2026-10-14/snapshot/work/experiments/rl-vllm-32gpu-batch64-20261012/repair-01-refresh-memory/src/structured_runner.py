"""Real vLLM GPU ModelRunner subclass with explicit DAG execution entry point."""
import torch

def structured_runner_class():
 from vllm.worker.model_runner import ModelRunner
 from vllm.forward_context import set_forward_context
 class StructuredModelRunner(ModelRunner):
  @torch.inference_mode()
  def execute_structured(self,input_tokens,semantic_positions,dag_metadata,selected_logit_indices):
   if self.vllm_config.parallel_config.data_parallel_size!=1:raise ValueError('Prototype uses one TP1 actor per GPU, separate learner communicator')
   # Stock execute_model accepts only its causal prefill/decode metadata. This
   # isolated entry executes actual vLLM model kernels with our explicit DAG
   # metadata, and prunes lm_head rows before computing FP32 actor logprobs.
   with set_forward_context(dag_metadata,self.vllm_config,virtual_engine=0):
    hidden=self.model(input_ids=input_tokens,positions=semantic_positions)
   return self.model.compute_logits(hidden.index_select(0,selected_logit_indices),None).float()
 return StructuredModelRunner

def patch_model_runner(runner):
 """Worker0.8.5's model_runner_cls hook receives an initialized runner object.
 Keep its state and weakrefs intact; add the isolated subclass execution method.
 """
 from vllm.worker.model_runner import ModelRunner
 if not isinstance(runner,ModelRunner):raise TypeError('Expected installed vLLM V0 ModelRunner instance')
 runner.__class__=structured_runner_class()
 return runner
