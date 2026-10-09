#!/usr/bin/env bash
set -euo pipefail
ROOT=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
MODE=${1:?Usage: run_rl.sh s1|s2|think /absolute/model/path [Hydra overrides]}
MODEL=${2:?Supply the validated SFT HF model directory}
shift 2
[[ "$MODE" == s1 || "$MODE" == s2 || "$MODE" == think ]] || exit 2
PY="$ROOT/.venv/bin/python"
SMOKE=${SMOKE:-0}
MODE_ARGS=()
if [[ "$MODE" == think ]]; then
  # Qwen3-0.6B thinking SFT: RLOO over the group without std, reward V0/V1/V2 (README).
  REWARD=${REWARD:-v0}
  case "$REWARD" in v0|v1_low|v1_high|v2) ;; *) echo 'REWARD must be v0, v1_low, v1_high or v2'; exit 2;; esac
  ADV=rloo; DEFAULT_RESPONSE=16384; DEFAULT_BLOCKS=2; TAG=think-$REWARD; CHECK_ARGS=(--plan)
  [[ "${ALLOW_PARALLEL:-true}" == false ]] && TAG=think-sequential-$REWARD
  # Blocks follow the shared contract with the thinking SFT (contract.py): the model writes a plan
  # after <Parallel> that sets 2-4 branches; an invalid plan ends the trajectory with c = 0.
  MODE_ARGS=(actor_rollout_ref.rollout.agent.enable_thinking=true
             "actor_rollout_ref.rollout.agent.allow_parallel=${ALLOW_PARALLEL:-true}"
             actor_rollout_ref.rollout.agent.protocol=plan_v1
             "actor_rollout_ref.rollout.agent.max_plan_tokens=${MAX_PLAN_TOKENS:-256}"
             "+reward_model.reward_kwargs.reward_method=think_$REWARD")
  if [[ "$REWARD" == v2 ]]; then
    [[ -f "${COST_SCALES:-}" ]] || { echo 'REWARD=v2 needs COST_SCALES=<output of calibrate_cost_scales.py>'; exit 2; }
    MODE_ARGS+=("+reward_model.reward_kwargs.cost_scales=$COST_SCALES")
  fi
else
  ADV=grpo; DEFAULT_RESPONSE=3000; DEFAULT_BLOCKS=4; TAG=$MODE; CHECK_ARGS=()
fi
RUN_NAME=${RUN_NAME:-qwen06-$TAG-seed1}
RUN="$ROOT/runs/$RUN_NAME"
mkdir -p "$RUN"
export PARALLEL_R1_TRACE_DIR="$RUN/telemetry"
export VLLM_USE_V1=1
export TOKENIZERS_PARALLELISM=false
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=4
export HYDRA_FULL_ERROR=1
export WANDB_MODE=offline
export WANDB_DIR="$RUN"
"$PY" "$ROOT/repo/experiments/qwen06/check_checkpoint.py" "$MODEL" "${CHECK_ARGS[@]}" > "$RUN/checkpoint.json"
if [[ -f "$MODEL/SMOKE_ONLY" && "$SMOKE" != 1 ]]; then echo 'Refusing production RL from disposable smoke weights'; exit 2; fi
TRAIN="$ROOT/data/${MODE}_train.parquet"
VAL="$ROOT/data/${MODE}_val.parquet"
BATCH=${BATCH:-32}
MINI=${MINI:-32}
ROLLOUT_N=${ROLLOUT_N:-8}
STEPS=${STEPS:-300}
RESPONSE=${RESPONSE:-$DEFAULT_RESPONSE}
MAX_BLOCKS=${MAX_BLOCKS:-$DEFAULT_BLOCKS}
NUM_PATHS=${NUM_PATHS:-2}
PROMPT=${PROMPT:-2000}
WORKERS=${WORKERS:-4}
REWARD_ARGS=()
if [[ "$SMOKE" == 1 ]]; then
  TRAIN="$ROOT/data/${MODE}_smoke_train.parquet"
  VAL="$ROOT/data/${MODE}_smoke_val.parquet"
  BATCH=2; MINI=2; ROLLOUT_N=2; STEPS=1; RESPONSE=128; PROMPT=1024; WORKERS=1
  REWARD_ARGS=("custom_reward_function.path=$ROOT/repo/experiments/qwen06/smoke_reward.py")
fi
cd "$ROOT/repo/verl"
git rev-parse HEAD > "$RUN/source_commit.txt"
git diff > "$RUN/source.patch"
cp "$ROOT/environment.freeze.txt" "$RUN/" || true
exec "$PY" -m verl.trainer.main_ppo \
  algorithm.adv_estimator="$ADV" algorithm.use_kl_in_reward=False \
  data.train_files="['$TRAIN']" data.val_files="['$VAL']" \
  data.train_batch_size="$BATCH" data.return_raw_chat=True \
  data.max_prompt_length="$PROMPT" data.max_response_length="$RESPONSE" \
  data.filter_overlong_prompts=True data.truncation=error data.dataloader_num_workers=2 \
  actor_rollout_ref.model.path="$MODEL" actor_rollout_ref.model.use_remove_padding=False \
  actor_rollout_ref.model.enable_gradient_checkpointing=True \
  +actor_rollout_ref.model.override_config._attn_implementation=sdpa \
  actor_rollout_ref.actor.optim.lr=1e-6 actor_rollout_ref.actor.clip_ratio_high=0.28 \
  actor_rollout_ref.actor.ppo_mini_batch_size="$MINI" actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=1 \
  actor_rollout_ref.actor.use_dynamic_bsz=False actor_rollout_ref.actor.use_kl_loss=False \
  actor_rollout_ref.actor.use_torch_compile=False \
  actor_rollout_ref.actor.fsdp_config.param_offload=False actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \
  actor_rollout_ref.rollout.n="$ROLLOUT_N" actor_rollout_ref.rollout.name=vllm actor_rollout_ref.rollout.mode=async \
  actor_rollout_ref.rollout.tensor_model_parallel_size=1 actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=1 \
  actor_rollout_ref.rollout.gpu_memory_utilization=0.45 actor_rollout_ref.rollout.enforce_eager=True \
  actor_rollout_ref.rollout.max_num_seqs=64 actor_rollout_ref.rollout.temperature=1.0 \
  actor_rollout_ref.rollout.agent.num_workers="$WORKERS" \
  actor_rollout_ref.rollout.agent.max_path_response_length="$RESPONSE" \
  actor_rollout_ref.rollout.agent.max_iterations_for_parallel_thinking="$MAX_BLOCKS" \
  actor_rollout_ref.rollout.agent.num_paths="$NUM_PATHS" \
  actor_rollout_ref.rollout.agent.logprob_context="${LOGPROB_CONTEXT:-flat_packed}" \
  actor_rollout_ref.rollout.agent.rollout_logprobs="${ROLLOUT_LOGPROBS:-true}" \
  actor_rollout_ref.rollout.val_kwargs.temperature=1.0 actor_rollout_ref.rollout.val_kwargs.do_sample=True \
  actor_rollout_ref.rollout.val_kwargs.n=1 \
  trainer.logger="['console','wandb']" trainer.project_name=Parallel-R1-qwen06 trainer.experiment_name="$RUN_NAME" \
  trainer.n_gpus_per_node=1 trainer.nnodes=1 trainer.save_freq=10 trainer.test_freq=10 \
  trainer.total_epochs=100 trainer.total_training_steps="$STEPS" trainer.val_before_train=False \
  trainer.default_local_dir="$RUN/checkpoints" trainer.max_actor_ckpt_to_keep=3 \
  trainer.rollout_data_dir="$RUN/rollouts" trainer.validation_data_dir="$RUN/validation" \
  trainer.resume_mode=disable ray_init.num_cpus=8 "${MODE_ARGS[@]}" "${REWARD_ARGS[@]}" "$@"
