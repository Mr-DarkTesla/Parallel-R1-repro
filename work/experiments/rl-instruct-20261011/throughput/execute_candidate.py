"""Opt-in adapter for a separate candidate; never imported by frozen runners."""
from cohort_decoder import CohortDecoder


def execute_cohort(execute, tokenizer, decoder_core, prompts, seeds, eos_ids,
                   response_budget=4096, path_budget=768, max_context=16384,
                   max_rows=4, max_paths=2):
    """Run independent episodes; caller retains grading, centering and update.

    prompts/seeds follow the baseline episode order. No model train/optimizer
    activity may run concurrently; model eval state is caller-owned. The server
    ledger must not replace per-episode reward forward counts.
    """
    if len(prompts) != len(seeds) or not prompts:
        raise ValueError('Require equally sized nonempty prompts and seeds')
    server = CohortDecoder(decoder_core,max_rows=max_rows,max_paths=max_paths)
    jobs = [lambda client,p=p,s=s: execute(tokenizer,p,client,eos_ids,response_budget,
                                         path_budget,max_context,s)
            for p,s in zip(prompts,seeds)]
    trajectories = server.run(jobs)
    telemetry = dict(
        cross_episode_server_forward_calls=sum(b['physical_forward_calls'] for b in server.server_batches),
        cross_episode_server_prefill_calls=sum(b['prefill_forward_calls'] for b in server.server_batches),
        cross_episode_server_decode_calls=sum(b['decode_forward_calls'] for b in server.server_batches),
        episode_reward_forward_calls=[t['stats']['actual_model_forward_calls'] for t in trajectories],
        reward_forward_accounting='Standalone max_paths subgroup cost retained per episode',
        server_batches=server.server_batches)
    return trajectories,telemetry
