# work/experiments/rl-campaign-20261010

Ниже — сохранённые наблюдения и настройки конкретного каталога. Значения в plan/manifest могут быть плановыми; исполнение подтверждают метрики, число завершённых задач и terminal status соответствующей попытки. Неподтверждённые параметры нельзя переносить из соседнего запуска.

## Полная конфигурация и данные

- [work/experiments/rl-campaign-20261010/night-plan.json](../artifacts/work/experiments/rl-campaign-20261010/night-plan.json) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.

<details>

<summary>Числа и параметры</summary>

```json
{
  "hosts": {
    "Sirius8GPU": "DeepSeek teacher, reviewed50 pilot, regenerate3000, deep SFT and evaluation",
    "tmp2": "forward_only RL control",
    "tmp3": "strong_width RL"
  },
  "reward_sha256": "4c7ceb7f0fe50b2cdfb69308ae2a26459ea9bbd67dee351a14ead4c5f1db5eac",
  "common": {
    "initial_checkpoint": "work/experiments/base-format-20261010/runs/production/final",
    "steps": 64,
    "group_size": 4,
    "learning_rate": 1e-06,
    "advantage": "group mean centering; no std division or whitening",
    "loss_denominator": "4096 * group_size; DDP mean"
  },
  "reward": {
    "cost": "min(0.4, 0.02 * floor(actual_generation_forward_calls / 200))",
    "strong_bonus": "scale(step) * (0.3 * mean(min(width-1,3)/3) + 0.05 * min(completed_rounds,4))",
    "bonus_gate": "correct answer and canonical valid format",
    "accuracy_gate": "all incorrect answers score zero; correct score >= 0.6",
    "anneal": "scale1 through first32 updates; linear decay to0 by64",
    "depth_penalty": 0,
    "cost_scope": "instrumented generation model.forward calls, excluding replay/backward; charge shared batch once"
  },
  "selection": {
    "validation": "128 disjoint GSM questions at0/16/32/48/64; fixed sampling seeds",
    "priority": [
      "accuracy",
      "correct and valid parallel traces",
      "measured generation forwards and elapsed time"
    ],
    "final_evaluation": "Frozen mixed128 GSM/MATH protocol matches preRL Base; supplementary sealed512 GSM evaluated separately",
    "fixed_native_baseline": "98/128=76.5625%",
    "pre_rl_base": "84/128=65.625%"
  },
  "gates": [
    "actual Base decoder/replay parity PASS",
    "independent batched mask and physical cost audit",
    "actual two optimizer steps on8GPU with resident Adam, finite gradients and backbone updates",
    "sealed configuration, sources, initial model, disjoint data and proofs",
    "50 actual teacher pilot outcomes with independent math and dependency review before full SFT data generation"
  ],
  "monitoring": {
    "cadence_minutes": 30,
    "notify": "meaningful result, failure or intervention",
    "metrics": [
      "accuracy by dataset",
      "canonical format rate",
      "correct and parallel-valid rate",
      "forked task rate",
      "mean width and distribution",
      "rounds and distribution",
      "tokens",
      "critical-path token statistic",
      "physical generation forwards",
      "elapsed time",
      "peak GPU memory",
      "zero-advantage groups",
      "invalid and truncated trace reasons"
    ]
  },
  "followup_policy": "Use actual validation and trace failures to choose isolated followup experiments as soon as informative and useful. Do not claim positive quality from higher reward. Do not change frozen running inputs.",
  "report_milestone": "2026-10-11T15:00:00+03:00",
  "report_milestone_utc": "2026-10-11T12:00:00Z",
  "deadline_policy": "User extended duration;15:00MSK is interim report milestone, not stop. Continue useful authorized experiments and report first comparable results immediately.",
  "state": "paused_for_model_and_checkpoint_discussion",
  "latest_user_decision": {
    "at": "2026-10-11T00:35:20.634894+00:00",
    "model_family": "Qwen3-4B Instruct only",
    "base_experiments": "No further Base experiments",
    "quality_objective": "Maximum accuracy, at least intended unseen SFT, with minimum actual generation forwards",
    "unseen_sft_reference": "To resolve with user; old unseen-wide5145 is 0.6B and is not intended reference",
    "verified_70_percent_record": {
      "checkpoint": "work/experiments/instruct-token-warmup-20261010/variants/lr-1e-3/runs/production/final",
      "eval": "lr-1e-3-trained-structured-128",
      "correct": 90,
      "total": 128,
      "trainable_parameters": 15360,
      "only_six_rows_updated": true
    },
    "dispatch": "Held pending discussion; no Base production launched; runner stopping owned Base smoke211"
  }
}
```

</details>

## Исходники рецепта и награды

- [work/experiments/rl-campaign-20261010/reward.py](../artifacts/work/experiments/rl-campaign-20261010/reward.py) — local_saved, снимок 2026-10-12T17:38:52.274040+00:00.
