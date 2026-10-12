# Проверенный BF16 learner + CUDAgraph actor

Все восемь процессов завершились с кодом 0; GPU 0–7 свободны, 0 MiB. Три положительных шага Adam 51–53 и 160 проверок с Adam в памяти прошли. FP32 clean16 после обучения: 13/16 правильных, format 14/16; исходный checkpoint также 13/16. Это маленький пилот. Полный RL500 не запускался, дополнительные веса не экспортировались, исходные 32 wrapper-процесса остаются на hold.

| Шаг | Полный wall | Ответов/с | Sampled tokens/с | Generation F | Правильно | Условия |
|---|---:|---:|---:|---:|---:|---|
| 51 | 123.130 с | 0.260 | 195.13 | 17869 | 26/32 | Первый шаг с профилем; начальный capture отдельно |
| 52 | 126.445 с | 0.253 | 181.18 | 17789 | 26/32 | Обычный шаг; recapture включён |
| 53 | 703.650 с | 0.045 | 48.84 | 24665 | 16/32 | Включены resident fixtures, не steady state |

На критическом rank2 шага52: capture 12.975 с, генерация с grading 90.021 с, независимые q/FP32 fixtures 5.499 с, release .206 с, native q reference 1.412 с, BF16 teacher 5.455 с, backward 10.171 с, guard .088 с, Adam .057 с. Остальное — cleanup, serialization и gathers. Вложенные таймеры и CUDA events перекрываются; их нельзя складывать. Максимальный полный wall по всем rank — 126.445 с, включая recapture и диагностику.

Фактически проверены FP32 master Parameters, gradient storage/DDP reduction и Adam states. Teacher и actor logits — BF16, softmax/logprob — FP32. Actor сохраняет FP32 embedding, residual, RMSNorm и RoPE текущего AMP; Linear используют стабильные BF16 buffers с refresh после Adam. Teacher использует стандартный BF16 autocast, включая SDPA и lm_head. SAME-current-master native cached AMP и graph q совпали точно до и после настоящих Adam updates. Старые q неизменны. Для одного свежего update p0=BF16 teacher.detach, PPO current использует тот же BF16 teacher до optimizer.step. Detached token TIS: rho=clamp(exp(p0−q),0,2), без нормирования/KL. Batch 32×4096, mean-centered advantages, без Std. FP32 cached/full — отдельный oracle структуры, а не p0 для TIS. Пороги max .01 / mean .002 / p95 .005 сохранены; наблюдаемый max ≤6.676e-5, skips 0. Peak allocated 67.715 GB.

На шаге51 все 32 graph генерации побитово совпали с native AMP/TIS: токены, q logprobs, masks, F и reward. После Adam независимые runs могут расходиться; для следующих шагов нет утверждения об одинаковых траекториях. Новый precision/estimator runtime 126 с против прежнего FP32 baseline 267 с — описательные ~2.12×. Ускорение whole wall в 3 раза ещё не доказано. Измерен один обычный прогретый шаг52; шаг53 содержит resident fixtures.

Static KV 19.33 GB и private graph pool 8.29 GiB освобождаются перед learner; recapture включён в wall. Все FP32 resident fixtures идут без graph pools, затем BF16 graph fixtures — отдельно, с тем же Adam. Каждый build из 40 curves содержит 120 eager warm forwards и 40 Python forward calls для записи графов. Это отдельная backend работа, исключённая из generation F/R2 и учтённая во времени. Persistent capture stream в этот release не включён: его отдельно проверяет D.

История сохранена: 9068 OOM перед первым backward; 9422 — два Adam PASS, затем OOM при совмещении FP32 resident prefill и graphs; 9745 — отказ inherited config assert до модели. Attempt2 исправляет конфигурацию и разносит memory lifetimes.

Portable configs 1/2/4/8/24/32 проходят CPU proof ownership, advantages, seeds и DDP scale для фиксированных 32 ответов. Только 8 GPU проверены реально. Остальные counts не проверены по памяти/скорости; 24/32 требуют отдельного multinode launcher. Существующий launcher — только node-local8. Для 1 GPU FP32 Adam + shadows/KV могут не поместиться в 80 GB. Шаблоны не запускают production.

Proof SHA: 71d91bbdb3e39db208dd49d47a70071357b4ff70815b3f650337cad6bcb96288
Source seal: 9fbb784122c11c4b165b61a90521a14eb602498de58f584d4f8dd065a7196cb6
Train SHA: 0b315ec30d14744d28e5e294f425ac0da3d809158df573607061cd5239d6d6b0
TIS kernel: c1f7541f509bb1cda6873d1b4c14eb31da0bbf12ef06f154ba04fdf4ffd08114
