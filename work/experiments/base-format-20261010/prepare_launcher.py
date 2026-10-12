"""Instrument the isolated full-model recipe and create its single-host launcher."""
from pathlib import Path
import ast

P = Path.cwd()
B = P / 'work/experiments/base-format-20261010'
p = B / 'code/verl/trainer/fsdp_parallel_sft_trainer.py'
s = p.read_text()
assert 'base_full_proof' not in s
s = s.replace('        if self.config.model.enable_gradient_checkpointing:', '''        base_full_proof = dict(
            total_parameters=sum(p.numel() for p in self.model.parameters()),
            trainable_parameters=sum(p.numel() for p in self.model.parameters() if p.requires_grad),
            all_parameters_trainable=all(p.requires_grad for p in self.model.parameters()),
            lora_rank=self.config.model.get("lora_rank", 0),
            full_model=True, think_wrapped=False,
        )
        assert base_full_proof['all_parameters_trainable'] and base_full_proof['lora_rank'] == 0
        assert base_full_proof['total_parameters'] == base_full_proof['trainable_parameters'] > 3_000_000_000
        if self.device_mesh.get_rank() == 0:
            import json
            os.makedirs(self.config.trainer.default_local_dir, exist_ok=True)
            with open(os.path.join(self.config.trainer.default_local_dir, 'initialization-proof.json'), 'x') as f:
                json.dump(base_full_proof, f, indent=2)
        self.base_metrics_step = 0

        if self.config.model.enable_gradient_checkpointing:''', 1)
s = s.replace('        # if grad_norm is not finite, skip the update', '''        # Fail loudly rather than count skipped updates as completed training.
        assert torch.isfinite(grad_norm), f"Non-finite gradient norm: {grad_norm}"
        assert math.isfinite(step_loss), f"Non-finite loss: {step_loss}"
        transformer = next(p for name, p in self.fsdp_model.named_parameters() if 'layers.' in name and p.numel() > 0)
        before = transformer.detach().reshape(-1)[:8192].float().clone()

        # if grad_norm is not finite, skip the update''', 1)
s = s.replace('        log_gpu_memory_usage("After optimizer step", logger=logger)', '''        delta = torch.linalg.vector_norm(transformer.detach().reshape(-1)[:8192].float() - before)
        torch.distributed.all_reduce(delta, op=torch.distributed.ReduceOp.MAX)
        self.base_metrics_step += 1
        if self.device_mesh.get_rank() == 0:
            import json
            with open(os.path.join(self.config.trainer.default_local_dir, 'metrics.jsonl'), 'a') as f:
                f.write(json.dumps(dict(step=self.base_metrics_step, loss=step_loss,
                                       grad_norm=float(grad_norm), transformer_update_l2=float(delta),
                                       full_model=True)) + '\\n')
        log_gpu_memory_usage("After optimizer step", logger=logger)''', 1)
s = s.replace('                    self.save_checkpoint(step=global_step, final=True)\n                    return', '''                    self.save_checkpoint(step=global_step, final=True)
                    if rank == 0:
                        import json
                        with open(os.path.join(self.config.trainer.default_local_dir, 'result.json'), 'x') as f:
                            json.dump(dict(state='complete', steps=global_step, epochs=self.config.trainer.total_epochs,
                                           val_loss=val_loss, full_model=True, think_wrapped=False), f, indent=2)
                    return''', 1)
if 'import math\n' not in s:
    s = 'import math\n' + s
ast.parse(s)
p.write_text(s)
launcher = '''#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/jovyan/shares/SR004.nfs3/larin/tmp/r1
B="$ROOT/work/experiments/base-format-20261010"
MODE="${1:?smoke or production}"
case "$MODE" in
 smoke) TRAIN=smoke-train; VAL=smoke-val; BATCH=8; STEPS=2; EPOCHS=1; WARMUP=0.0 ;;
 production) TRAIN=train; VAL=val; BATCH=64; STEPS=126; EPOCHS=3; WARMUP=0.1 ;;
 *) exit 2 ;;
esac
RUN="$B/runs/$MODE"
test ! -e "$RUN"
mkdir -p "$RUN"
cd "$B/code"
export PYTHONPATH="$B/code" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export TMPDIR="$ROOT/t/base4bsft" WANDB_MODE=disabled
mkdir -p "$TMPDIR"
PY="${PARALLEL_R1_PYTHON:-$ROOT/.venv/bin/python}"
exec "$PY" -B -m torch.distributed.run --standalone --nnodes=1 --nproc-per-node=8 \
 -m verl.trainer.fsdp_parallel_sft_trainer --config-name=sft_qwen3_06b \
 data.train_files="$B/data/$TRAIN.parquet" data.val_files="$B/data/$VAL.parquet" \
 data.prompt_key=problem data.response_key=response data.prompt_dict_keys=null data.response_dict_keys=null \
 +data.prompt_messages_key=prompt_messages +data.defer_parallel_mask=true \
 data.max_length=8192 data.truncation=error data.trim_padding=true \
 data.train_batch_size="$BATCH" data.micro_batch_size_per_gpu=1 data.num_workers=0 \
 model.partial_pretrain="$B/model" model.strategy=fsdp model.lora_rank=0 \
 model.enable_gradient_checkpointing=true model.fsdp_config.model_dtype=fp32 \
 optim.lr=1e-5 optim.warmup_steps_ratio="$WARMUP" \
 ulysses_sequence_parallel_size=1 use_remove_padding=false \
 trainer.total_epochs="$EPOCHS" trainer.total_training_steps="$STEPS" \
 trainer.default_local_dir="$RUN" trainer.final_dir="$RUN/final" \
 trainer.experiment_name="Base-4B-no-think-$MODE" trainer.logger='[console]' \
 hydra.run.dir="$RUN/hydra"
'''
(B / 'run_train.sh').write_text(launcher)
print('Prepared isolated full-model trainer instrumentation and launcher')
