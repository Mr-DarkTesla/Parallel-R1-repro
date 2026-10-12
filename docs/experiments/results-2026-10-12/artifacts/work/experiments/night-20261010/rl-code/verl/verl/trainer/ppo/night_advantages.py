"""Night experiments: prompt-group centering, no std scaling or whitening."""
import torch

NIGHT_ESTIMATORS = ("night_accuracy", "night_scalar_success", "night_split_success")


def components(y, critical_depth, index, mode, eta=.05, budget=0., scale=4096., bonus=None):
    if mode not in NIGHT_ESTIMATORS:
        raise ValueError(mode)
    if not y.is_floating_point():y=y.float()
    critical_depth=critical_depth.to(device=y.device,dtype=y.dtype)
    if not 0 <= eta or not scale > 0 or budget < 0:
        raise ValueError("eta>=0, budget>=0 and scale>0 required")
    if y.ndim != 1 or critical_depth.shape != y.shape or len(index) != len(y):
        raise ValueError("One correctness, runtime critical depth and prompt ID per sample required")
    if not torch.isfinite(critical_depth).all() or (critical_depth < 0).any():
        raise ValueError("Invalid runtime sampled critical depth")
    if not ((y == 0) | (y == 1)).all():
        raise ValueError("Correctness must be binary; KL/format shaping cannot enter accuracy")
    cost = ((critical_depth-budget).clamp_min(0)/scale).clamp(0,1)
    acc = torch.zeros_like(y); efficiency = torch.zeros_like(y); structure = torch.zeros_like(y)
    bonus = torch.zeros_like(y) if bonus is None else bonus.to(device=y.device,dtype=y.dtype)
    if (bonus < 0).any() or (bonus > .1).any():
        raise ValueError("Structure bonus must be bounded in [0,.1]")
    groups = {}
    for i, uid in enumerate(index):
        groups.setdefault(str(uid), []).append(i)
    counts = []
    for members in groups.values():
        ix = torch.tensor(members, device=y.device)
        gy, gc = y[ix], cost[ix]
        if eta >= 1/len(members):
            raise ValueError("eta must be strictly below 1/group size")
        acc[ix] = gy-gy.mean()
        n = int(gy.sum().item()); counts.append(n)
        if mode == "night_scalar_success":
            v = -eta*gy*gc; efficiency[ix] = v-v.mean()
        elif mode == "night_split_success" and n >= 2:
            efficiency[ix] = eta*gy*((gc*gy).sum()/gy.sum()-gc)
        sb = gy*bonus[ix]; structure[ix] = sb-sb.mean()
    total = acc+efficiency+structure
    metrics = {"night/group_allwrong_fraction": sum(n == 0 for n in counts)/max(len(counts),1),
               "night/group_allcorrect_fraction": sum(n == len(m) for n,m in zip(counts,groups.values()))/max(len(counts),1),
               "night/group_success_count_mean": sum(counts)/max(len(counts),1),
               "night/group_count": len(counts), "night/cost_mean": cost.mean().item()}
    for n in range(max(map(len,groups.values()),default=0)+1):
        metrics[f"night/group_success_count_{n}_fraction"] = counts.count(n)/max(len(counts),1)
    for label, value in (("accuracy",acc),("efficiency",efficiency),("structure",structure),("total",total)):
        metrics[f"night/adv_{label}_mean"] = value.mean().item()
        metrics[f"night/adv_{label}_abs_mean"] = value.abs().mean().item()
        metrics[f"night/adv_{label}_min"] = value.min().item()
        metrics[f"night/adv_{label}_max"] = value.max().item()
    return total, metrics


def estimate(token_level_rewards, response_mask, index, config=None, critical_depth=None, correctness=None,
             structure_bonus=None, mode="night_accuracy", **kwargs):
    cfg = config or {}
    if cfg.get("use_kl_in_reward",False):
        raise ValueError("Night outcome advantages require use_kl_in_reward=false; use actor KL loss")
    if critical_depth is None or correctness is None:
        raise ValueError("Night estimators require actual runtime critical_depth and separate acc")
    adv, _ = components(correctness, critical_depth, index, mode, float(cfg.get("night_eta",.05)),
                        float(cfg.get("night_budget",0)),float(cfg.get("night_scale",4096)),structure_bonus)
    masked = adv.unsqueeze(-1)*response_mask
    return masked, masked.clone()


def register_all(register):
    for mode in NIGHT_ESTIMATORS:
        def fn(*args, _mode=mode, **kwargs):
            return estimate(*args, mode=_mode, **kwargs)
        register(mode)(fn)


def telemetry(stats, y, response_mask):
    """Driver aggregation: each trajectory contributes once, never rank means."""
    out = {}
    fields = {"F_idealized_sampled_depth":"critical_depth", "T_sampled":"sampled_tokens",
              "T_assembled":"assembled_tokens", "forced_token_fraction":"forced_token_fraction",
              "fork_count":"forks", "width":"max_width", "rounds":"rounds",
              "TT_over_F":"TT_over_F", "sampled_eos":"sampled_eos", "invalid":"invalid_width", "invalid_main_control":"invalid_main_control",
              "truncated":"truncated", "actual_calls":"generation_calls",
              "sampled_work_tokens":"generated_tokens", "actual_wall_seconds":"wall_seconds",
              "guided_first_width":"guided_first_width", "guided_forced_tokens":"guided_forced_tokens",
              "guided_skipped_budget":"guided_skipped_budget", "merge_reserve_tokens":"merge_reserve_tokens"}
    for label,key in fields.items():
        vals = torch.tensor([float(s.get(key,0)) for s in stats],dtype=torch.float64)
        for suffix, select in (("all",torch.ones_like(y,dtype=torch.bool).cpu()),("correct",y.bool().cpu())):
            subset=vals[select]
            if len(subset):
                out[f"night/{label}_{suffix}_mean"] = subset.mean().item()
                out[f"night/{label}_{suffix}_p95"] = torch.quantile(subset,.95).item()
    out["night/sampled_loss_tokens"] = response_mask.sum().item()
    out["night/zero_sampled_token_fraction"] = (response_mask.sum(-1)==0).float().mean().item()
    return out
