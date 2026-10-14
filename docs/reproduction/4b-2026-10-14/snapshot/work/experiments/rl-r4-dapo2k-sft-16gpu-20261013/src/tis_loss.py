"""Explicit token TIS + clipped PPO: q sampler, p0 proximal, ptheta learner."""
import torch

def three_policy_token_loss(new_logp, proximal_logp, sampler_logp, advantage, clip=.2, upper=2.):
    if upper!=2.:
        raise ValueError('This proof pins upstream tokenTIS upper2; no invented estimator setting')
    p0=proximal_logp.detach();q=sampler_logp.detach()
    rho=(p0-q).exp().clamp(min=0.,max=upper).detach()
    ratio=(new_logp-p0).exp()
    loss=-rho*torch.minimum(ratio*advantage,ratio.clamp(1-clip,1+clip)*advantage)
    return loss,ratio,rho
